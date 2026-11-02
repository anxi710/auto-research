#!/usr/bin/env python3
"""Check selected collaboration records and their local references without writes."""

import argparse
import hashlib
import json
import math
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
import unicodedata

# Keep direct CLI use read-only even when scripts live inside the research root.
sys.dont_write_bytecode = True
from evidence_ledger import LedgerValidator
from collection_artifacts import CollectionValidator


def text(value):
    return isinstance(value, str) and bool(value.strip())


def valid_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value))


def revision(value):
    return type(value) is int and value > 0


def sha256(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[a-fA-F0-9]{64}", value))


def texts(value):
    return isinstance(value, list) and all(text(item) for item in value)


def nonempty_texts(value):
    return texts(value) and bool(value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}.")
        result[key] = value
    return result


def finite_number(value):
    raise ValueError(f"Non-finite JSON number: {value}.")


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("Non-finite JSON number.")
    return result


def cycle_members(edges):
    """Find cycle members without using the Python call stack."""
    done, active, cycles = set(), {}, set()
    for start in sorted(edges):
        if start in done:
            continue
        stack = [(start, iter(sorted(edges.get(start, ()))))]
        active[start] = 0
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                done.add(node)
                active.pop(node)
                stack.pop()
            elif child in active:
                cycles.update(item[0] for item in stack[active[child]:])
            elif child not in done:
                active[child] = len(stack)
                stack.append((child, iter(sorted(edges.get(child, ())))))
    return cycles


class Linter:
    def __init__(self, root, artifact_stack=None):
        self.root = root
        self.diagnostics = set()
        self.bad = set()
        self.records = {"task": {}, "result": {}, "review": {}}
        self.refs = {}
        self.current = set()
        self.pending = []
        self.physical = {}
        self.hashes = {}
        self.contents = {}
        self.ledger_validator = LedgerValidator(self)
        self.artifact_stack = artifact_stack if artifact_stack is not None else set()
        self.collection_validator = CollectionValidator(self)

    def issue(self, code, path, message):
        self.diagnostics.add((path, code, message))
        self.bad.add(path)

    def path(self, value, source, required=True):
        if (not text(value) or Path(value).is_absolute() or PureWindowsPath(value).drive
                or ".." in Path(value).parts
                or any(unicodedata.category(char) == "Cc" for char in value)):
            self.issue("PATH", source, f"Unsafe research-relative path: {value!r}.")
            return None
        try:
            path = (self.root / value).resolve()
            if not path.is_relative_to(self.root):
                self.issue("PATH", source, f"Path leaves the research root: {value!r}.")
                return None
            relative = path.relative_to(self.root).as_posix()
            if not required:
                return relative
            info = path.stat()
            if not stat.S_ISREG(info.st_mode):
                self.issue("READ", source, f"Expected a regular file: {relative}.")
                return None
            identity = (info.st_dev, info.st_ino)
            return self.physical.setdefault(identity, relative)
        except (OSError, RuntimeError, ValueError):
            self.issue("READ", source, f"Cannot access file: {value!r}.")
            return None

    def digest(self, path, source):
        if path not in self.hashes:
            try:
                value = hashlib.sha256()
                with (self.root / path).open("rb") as stream:
                    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                        value.update(chunk)
                self.hashes[path] = value.hexdigest()
            except OSError:
                self.issue("READ", source, f"Cannot read file: {path}.")
                return None
        return self.hashes[path]

    def reference(self, value, source, expected=None, kind=None, current=False):
        path = self.path(value, source)
        if path is None:
            return None
        actual = self.digest(path, source)
        if actual is None:
            return None
        if expected is not None and actual != expected.lower():
            self.issue("HASH", source, f"SHA256 mismatch: {path}.")
        if kind is not None:
            if current:
                self.current.add(path)
            if path not in self.records[kind]:
                self.records[kind][path] = None
                self.pending.append((kind, path))
        return path

    def object_fields(self, value, fields, path, label):
        if not isinstance(value, dict):
            self.issue("SCHEMA", path, f"{label} must be an object.")
            return False
        valid = True
        for key, check in fields.items():
            if key not in value or not check(value[key]):
                self.issue("SCHEMA", path, f"Invalid or missing {label}.{key}.")
                valid = False
        return valid

    def schema(self, kind, value, path):
        common = {"task_id": valid_id}
        if kind == "task":
            fields = dict(common, revision=revision, goal=text, owner=text, inputs=lambda v: isinstance(v, list),
                          dependencies=lambda v: isinstance(v, list), write_paths=nonempty_texts,
                          budget_ref=text, acceptance=nonempty_texts, stop_condition=text)
        elif kind == "result":
            fields = dict(common, task_revision=revision, attempt_id=valid_id, task_path=text, task_sha256=sha256,
                          execution_status=lambda v: isinstance(v, str) and v in
                          {"completed", "blocked", "failed", "cancelled", "unknown"},
                          artifacts=lambda v: isinstance(v, list), unresolved=texts,
                          resource_usage=lambda v: isinstance(v, dict), next_action=text)
        else:
            fields = dict(common, review_id=valid_id, task_revision=revision, attempt_id=valid_id,
                          result_path=text, result_sha256=sha256, reviewer=text, decision_owner=text,
                          decision=lambda v: isinstance(v, str) and v in {"accepted", "rework", "blocked"},
                          basis=nonempty_texts, unresolved=texts, supersedes=lambda v: v is None or isinstance(v, dict))
        valid = self.object_fields(value, fields, path, kind)
        if not isinstance(value, dict):
            return False
        entries = "inputs" if kind == "task" else "artifacts"
        if kind in {"task", "result"} and isinstance(value.get(entries), list):
            for index, entry in enumerate(value[entries]):
                valid = self.object_fields(entry, {"path": text, "sha256": sha256}, path,
                                           f"{entries}[{index}]") and valid
        if kind == "task" and isinstance(value.get("dependencies"), list):
            fields = {"task_path": text, "task_revision": revision, "result_path": text,
                      "result_sha256": sha256, "review_path": text, "review_sha256": sha256}
            for index, entry in enumerate(value["dependencies"]):
                valid = self.object_fields(entry, fields, path, f"dependencies[{index}]") and valid
        if kind == "task" and "evidence_ledger" in value and not text(value["evidence_ledger"]):
            self.issue("SCHEMA", path, "task.evidence_ledger must be a research-relative path.")
            valid = False
        if kind == "task":
            valid = self.collection_validator.task_schema(value, path) and valid
        if kind == "result" and isinstance(value.get("artifacts"), list):
            ledgers = [entry for entry in value["artifacts"] if isinstance(entry, dict)
                       and entry.get("kind") == "claim_evidence_ledger"]
            if len(ledgers) > 1:
                self.issue("SCHEMA", path, "A result may reference at most one claim_evidence_ledger artifact.")
                valid = False
        if kind == "review" and isinstance(value.get("supersedes"), dict):
            valid = self.object_fields(value["supersedes"], {"path": text, "sha256": sha256},
                                       path, "supersedes") and valid
        if kind == "result" and value.get("execution_status") == "completed" and value.get("artifacts") == []:
            self.issue("SCHEMA", path, "A completed result needs at least one artifact.")
            valid = False
        return valid

    def review_json(self, content, path):
        section = False
        found = 0
        fence = None
        capture = None
        comment = False
        blocks = []
        for line in content.splitlines():
            if fence:
                if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                    if capture is not None:
                        blocks.append("\n".join(capture))
                    fence, capture = None, None
                elif capture is not None:
                    capture.append(line)
                continue
            opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if comment or not opening:
                visible = []
                offset = 0
                while offset < len(line):
                    if comment:
                        end = line.find("-->", offset)
                        if end < 0:
                            break
                        offset = end + 3
                        comment = False
                    else:
                        token = re.search(r"\\.|`+|<!--", line[offset:])
                        if token is None:
                            visible.append(line[offset:])
                            break
                        start = offset + token.start()
                        visible.append(line[offset:start])
                        marker = token.group()
                        offset = start + len(marker)
                        if marker == "<!--":
                            comment = True
                        elif marker.startswith("`"):
                            # Only a matching run closes an inline code span.
                            closing = re.search(r"(?<!`)" + re.escape(marker) + r"(?!`)", line[offset:])
                            if closing is not None:
                                offset += closing.end()
                            visible.append(line[start:offset])
                        else:
                            # Escaped characters are literal; paired backslashes
                            # leave a later comment marker unescaped.
                            visible.append(marker)
                line = "".join(visible)
                opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if opening:
                # Fenced content, including JSON strings, keeps literal comment markers.
                fence = opening.group(1)
                if section and opening.group(2).strip().lower() == "json":
                    capture = []
                continue
            heading = re.match(r"^ {0,3}(#{1,2})\s+(.+?)\s*#*\s*$", line)
            if heading:
                section = (len(heading.group(1)) == 2 and heading.group(2) in
                           {"Task acceptance", "Task acceptance (optional)"})
                if section:
                    found += 1
        if not found:
            return None
        if found != 1 or len(blocks) != 1 or capture is not None:
            self.issue("SCHEMA", path, "Use one closed JSON block in one task acceptance section.")
            return None
        return blocks[0]

    def load(self):
        index = 0
        while index < len(self.pending):
            kind, path = self.pending[index]
            index += 1
            try:
                raw = (self.root / path).read_bytes()
                self.contents[path] = raw
                self.hashes[path] = hashlib.sha256(raw).hexdigest()
                content = raw.decode("utf-8")
                if kind == "review":
                    content = self.review_json(content, path)
                    if content is None:
                        continue
                value = json.loads(content, object_pairs_hook=unique_object,
                                   parse_constant=finite_number, parse_float=finite_float)
            except (OSError, UnicodeError) as exc:
                self.issue("READ", path, f"Cannot read UTF-8 record ({type(exc).__name__}).")
                continue
            except (ValueError, RecursionError):
                self.issue("SCHEMA", path, "Record must contain valid JSON with unique keys and finite numbers.")
                continue
            if not self.schema(kind, value, path):
                continue
            self.records[kind][path] = value
            refs = self.refs[kind, path] = {}
            if kind == "task":
                self.reference(value["budget_ref"], path)
                if "evidence_ledger" in value:
                    self.path(value["evidence_ledger"], path, required=False)
                if "synthesis" in value:
                    self.path(value["synthesis"], path, required=False)
                for entry in value["inputs"]:
                    self.reference(entry["path"], path, entry["sha256"])
                for target in value["write_paths"]:
                    self.path(target, path, required=False)
                refs["dependencies"] = []
                for dep in value["dependencies"]:
                    refs["dependencies"].append({
                        "task": self.reference(dep["task_path"], path, kind="task", current=True),
                        "result": self.reference(dep["result_path"], path, dep["result_sha256"], kind="result"),
                        "review": self.reference(dep["review_path"], path, dep["review_sha256"], kind="review")})
            elif kind == "result":
                refs["task"] = self.reference(value["task_path"], path, value["task_sha256"], kind="task")
                refs["ledger_entries"] = []
                for artifact in value["artifacts"]:
                    target = self.reference(artifact["path"], path, artifact["sha256"])
                    if artifact.get("kind") == "claim_evidence_ledger":
                        refs["ledger_entries"].append(target)
            else:
                refs["result"] = self.reference(value["result_path"], path, value["result_sha256"], kind="result")
                refs["supersedes"] = None
                if value["supersedes"] is not None:
                    old = value["supersedes"]
                    refs["supersedes"] = self.reference(old["path"], path, old["sha256"], kind="review")

    def identities(self, kind, fields, paths=None):
        groups = {}
        for path, value in self.records[kind].items():
            if value is not None and (paths is None or path in paths):
                key = tuple(value[field] for field in fields)
                groups.setdefault(key, []).append(path)
        for paths in groups.values():
            if len(paths) > 1:
                for path in paths:
                    self.issue("DUPLICATE_ID", path, f"Conflicting {kind} identity in: {', '.join(sorted(paths))}.")
        return groups

    def result_ledger(self, path, result, task, refs):
        entries = refs["ledger_entries"]
        ledger_path = entries[0] if entries else None
        required = task.get("evidence_ledger") if task is not None else None
        required_now = required is not None and result["execution_status"] == "completed"
        refs["ledger_expected"] = bool(entries) or required_now
        if required_now:
            required_path = self.path(required, path)
            if len(entries) != 1 or ledger_path != required_path:
                self.issue("BINDING", path, "Completed result must include its required evidence ledger artifact with kind claim_evidence_ledger.")
            if not entries:
                ledger_path = required_path
        refs["ledger_path"] = ledger_path
        refs["ledger"] = (self.ledger_validator.validate(ledger_path, path, result)
                          if ledger_path is not None else None)

    def check(self):
        tasks, results, reviews = (self.records[kind] for kind in ("task", "result", "review"))
        current = self.identities("task", ["task_id"], self.current)
        self.identities("result", ["task_id", "task_revision", "attempt_id"])
        self.identities("review", ["review_id"])
        edges = {path: set() for records in self.records.values() for path in records}
        for path, result in results.items():
            if result is None:
                continue
            refs = self.refs["result", path]
            snapshot = refs["task"]
            if snapshot is not None:
                edges[path].add(snapshot)
            task = tasks.get(snapshot)
            self.result_ledger(path, result, task, refs)
            self.collection_validator.result(path, result, task)
            if task is not None and (result["task_id"], result["task_revision"]) != (task["task_id"], task["revision"]):
                self.issue("BINDING", path, "Result identity does not match its fixed contract.")
            matches = current.get((result["task_id"],), [])
            if len(matches) != 1:
                self.issue("CURRENT", path, "Provide exactly one current contract for this result's task.")
                continue
            current_path = matches[0]
            refs["current"] = current_path
            edges[path].add(current_path)
            if snapshot == current_path:
                self.issue("BINDING", path, "Current contract and fixed snapshot must be separate files.")
            if (result["task_revision"] != tasks[current_path]["revision"]
                    or self.hashes.get(snapshot) != self.hashes.get(current_path)):
                self.issue("STALE", path, "Result uses an earlier or different contract. Preserve it as history.")
        history = {}
        result_reviews = {}
        for path, review in reviews.items():
            if review is None:
                continue
            refs = self.refs["review", path]
            result_path = refs["result"]
            if result_path is not None:
                edges[path].add(result_path)
                result_reviews.setdefault(result_path, set()).add(path)
            result = results.get(result_path)
            if result is None and review["decision"] == "accepted":
                self.issue("BINDING", path, "An accepted review requires a valid completed result with artifacts.")
            if result is not None:
                if any(review[key] != result[key] for key in ("task_id", "task_revision", "attempt_id")):
                    self.issue("BINDING", path, "Review identity does not match its result.")
                if review["decision"] == "accepted" and result["execution_status"] != "completed":
                    self.issue("BINDING", path, "An accepted review requires completed execution with artifacts.")
                result_refs = self.refs["result", result_path]
                if result_refs.get("ledger_expected"):
                    if review["decision"] == "accepted" and "claim_evidence" not in review:
                        self.issue("BINDING", path, "An accepted review of a ledger result requires claim_evidence scope and assessments.")
                    if result_path in self.bad:
                        self.issue("BINDING", path, "Review references a result with invalid ledger evidence or bindings.")
            if "claim_evidence" in review:
                result_refs = self.refs.get(("result", result_path), {})
                self.ledger_validator.validate_review(review["claim_evidence"], path, result,
                                                      result_refs.get("ledger_path"), result_refs.get("ledger"))
            old_path = refs["supersedes"]
            history[path] = {old_path} if old_path else set()
            if old_path:
                edges[path].add(old_path)
                if reviews.get(old_path) is None:
                    self.issue("REVIEW_HISTORY", path, "Replaced review has no valid acceptance block.")
                elif (self.refs["review", old_path]["result"] != result_path
                      or reviews[old_path]["result_sha256"].lower() != review["result_sha256"].lower()):
                    self.issue("REVIEW_HISTORY", path, "A replacement must review the same exact result.")
        for path in cycle_members(history):
            self.issue("REVIEW_HISTORY", path, "Review replacement history contains a cycle.")
        replaced = {old for old_paths in history.values() for old in old_paths}
        children = {}
        for newer, old_paths in history.items():
            for old in old_paths:
                children.setdefault(old, set()).add(newer)
        for old, newer in children.items():
            if len(newer) > 1:
                for path in newer | {old}:
                    self.issue("REVIEW_HISTORY", path, "Review replacement history branches into conflicting decisions.")
        for paths in result_reviews.values():
            tips = paths - replaced
            if len(tips) > 1:
                for path in tips:
                    self.issue("REVIEW_HISTORY", path, "Multiple supplied decisions lack one replacement history.")
        task_edges = {}
        for path, task in tasks.items():
            if task is None:
                continue
            task_edges[path] = set()
            for dep, refs in zip(task["dependencies"], self.refs["task", path]["dependencies"]):
                upstream, result, review = (self.records[kind].get(refs[kind]) for kind in ("task", "result", "review"))
                edges[path].update(ref for ref in refs.values() if ref is not None)
                if refs["task"] is not None:
                    task_edges[path].add(refs["task"])
                if upstream is None or result is None or review is None:
                    self.issue("DEPENDENCY", path, "Required dependency lacks a valid task, result, or acceptance block.")
                    continue
                if (upstream["revision"] != dep["task_revision"]
                        or (result["task_id"], result["task_revision"]) != (upstream["task_id"], dep["task_revision"])):
                    self.issue("DEPENDENCY", path, "Required dependency does not match its current task revision.")
                if (self.refs["review", refs["review"]]["result"] != refs["result"]
                        or review["result_sha256"].lower() != dep["result_sha256"].lower()
                        or review["decision"] != "accepted"):
                    self.issue("DEPENDENCY", path, "Required dependency needs an accepted review of its exact result.")
                if refs["review"] in replaced:
                    self.issue("DEPENDENCY", path, "Required acceptance was replaced by a supplied later review.")
        for path in cycle_members(task_edges):
            self.issue("DEPENDENCY", path, "Required task dependencies contain a cycle.")
        invalid = set(self.bad)
        changed = True
        while changed:
            before = len(invalid)
            invalid.update(path for path, targets in edges.items() if targets & invalid)
            changed = len(invalid) != before
        for path, task in tasks.items():
            if task is not None:
                for refs in self.refs["task", path]["dependencies"]:
                    if any(target in invalid for target in refs.values()):
                        self.issue("DEPENDENCY", path, "Required upstream records are invalid, stale, or unresolved.")

    def output(self):
        return {"diagnostics": [{"code": code, "path": path, "message": message}
                                for path, code, message in sorted(self.diagnostics)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Research directory containing the selected records.")
    for kind in ("task", "result", "review"):
        parser.add_argument("--" + kind, action="append", default=[], metavar="REL")
    args = parser.parse_args()
    if not (args.task or args.result or args.review):
        parser.error("Provide at least one --task, --result, or --review.")
    try:
        root = Path(args.root).resolve()
        if not root.is_dir():
            parser.error("--root must be an existing directory.")
    except (OSError, RuntimeError, ValueError):
        parser.error("Cannot access --root.")
    lint = Linter(root)
    for kind in ("task", "result", "review"):
        for path in sorted(getattr(args, kind)):
            lint.reference(path, ".", kind=kind, current=(kind == "task"))
    lint.load()
    lint.check()
    print(json.dumps(lint.output(), ensure_ascii=False, sort_keys=True, indent=2))
    return 1 if lint.diagnostics else 0


if __name__ == "__main__":
    raise SystemExit(main())
