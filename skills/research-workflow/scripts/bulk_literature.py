#!/usr/bin/env python3
"""Export, import, and query a dated literature selection. Plan by default."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


class Stop(RuntimeError):
    """Stop without guessing whether a remote write succeeded."""


def require(condition, message):
    if not condition:
        raise Stop(message)


def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def matches_hash(path, expected):
    return bool(expected) and path.is_file() and digest(path) == expected


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise Stop(f"Cannot read JSON: {path.name}.") from exc


def save_json(path, value, exclusive=False):
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("x" if exclusive else "w", encoding="utf-8") as stream:
        stream.write(encoded(value))
    if exclusive:
        # A hard link publishes the complete file without replacing existing evidence.
        os.link(temporary, path)
        temporary.unlink()
    else:
        temporary.replace(path)


def load_config(path):
    path = Path(path).resolve()
    data = read_json(path)
    required = {"collection_key", "question", "remote", "run_dir", "source_limit", "batch_size", "max_queries"}
    optional = {"recursive", "command_timeout", "wait_timeout"}
    require(isinstance(data, dict), "Settings must be a JSON object.")
    require(required <= data.keys() and not data.keys() - required - optional,
            "Settings have missing or unknown fields.")
    for name in ("collection_key", "question", "remote", "run_dir"):
        require(isinstance(data[name], str) and data[name].strip(), f"Set {name} to nonempty text.")
    require(re.fullmatch(r"[A-Za-z0-9]+", data["collection_key"]), "Invalid collection key.")
    require(re.fullmatch(r"[\w.-]+:[^\r\n\x00]*", data["remote"]), "Use a named rclone remote and path.")
    require(".." not in PurePosixPath(data["remote"].split(":", 1)[1]).parts, "Remote path contains '..'.")
    data.setdefault("recursive", True)
    data.setdefault("command_timeout", 300)
    data.setdefault("wait_timeout", 600)
    require(type(data["recursive"]) is bool, "recursive must be true or false.")
    for name in ("source_limit", "batch_size", "max_queries", "command_timeout", "wait_timeout"):
        require(type(data[name]) is int and 1 <= data[name] <= 10000, f"{name} must be between 1 and 10000.")
    require(data["batch_size"] <= data["source_limit"], "batch_size exceeds source_limit.")
    run_dir = (path.parent / data["run_dir"]).resolve()
    package = Path(__file__).resolve().parents[1]
    require(not run_dir.is_relative_to(package), "Keep run_dir outside the skill package.")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", run_dir.name), "Use a short run directory name with letters, numbers, dots, dashes, or underscores.")
    data["run_dir"] = str(run_dir)
    data["remote"] = data["remote"].rstrip("/")
    return data


@contextmanager
def run_lock(path):
    try:
        import fcntl
    except ImportError as exc:
        raise Stop("This runner needs Linux or macOS file locking.") from exc
    with path.open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise Stop("Another process holds this run. Wait for it to stop.") from exc
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def safe_file(root, relative):
    require(isinstance(relative, str) and relative and relative == relative.strip() and not any(c in relative for c in "\r\n\x00\\"), "Invalid export path.")
    posix = PurePosixPath(relative)
    require(not posix.is_absolute() and ".." not in posix.parts and not relative.startswith(("#", ";")), "Export path leaves the snapshot or conflicts with the upload list.")
    candidate = root / relative
    require(candidate.resolve().is_relative_to(root.resolve()), "Export path leaves the snapshot.")
    require(not any(parent.is_symlink() for parent in [candidate, *candidate.parents] if parent != root.parent), "Export paths cannot use symbolic links.")
    require(candidate.is_file(), "An active exported file is missing.")
    require(candidate.suffix.lower() == ".pdf", "An active export is not a PDF.")
    with candidate.open("rb") as stream:
        require(stream.read(5) == b"%PDF-", "An active export has no PDF header.")
    return candidate


def inventory(export_root, collection_key):
    metadata_paths = sorted(export_root.glob("*/.zpm/metadata.json"))
    require(len(metadata_paths) == 1, "Expected one zpm workspace with .zpm/metadata.json.")
    metadata_path = metadata_paths[0]
    require(not metadata_path.is_symlink(), "Metadata cannot be a symbolic link.")
    metadata = read_json(metadata_path)
    require(isinstance(metadata, dict) and metadata.get("generated_by") == "zpm" and metadata.get("schema_version") == 1,
            "Unsupported zpm metadata schema.")
    require(metadata.get("collection_key") == collection_key and isinstance(metadata.get("items"), list), "Metadata does not match the selected collection.")
    workspace = metadata_path.parent.parent
    files, excluded, paths, attachment_hashes = {}, [], set(), {}
    for entry in metadata["items"]:
        require(isinstance(entry, dict), "Invalid zpm metadata entry.")
        for name in ("item_key", "attachment_key", "collection_key", "state", "destination_path"):
            require(isinstance(entry.get(name), str) and entry[name], f"Metadata entry lacks {name}.")
        member = {name: entry[name] for name in ("item_key", "attachment_key", "collection_key", "destination_path")}
        if entry["state"] != "active":
            require(entry["state"] in {"missing", "removed"}, "Unknown zpm entry state.")
            excluded.append({**member, "reason": entry["state"]})
            continue
        file_path = safe_file(workspace, entry["destination_path"])
        require(entry["destination_path"] not in paths, "Duplicate export path in metadata.")
        paths.add(entry["destination_path"])
        sha = entry.get("sha256")
        require(isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{64}", sha) and digest(file_path) == sha, "Export hash does not match metadata.")
        previous = attachment_hashes.setdefault(entry["attachment_key"], sha)
        require(previous == sha, "An attachment has conflicting versions in one snapshot.")
        if sha not in files:
            files[sha] = {"path": entry["destination_path"], "sha256": sha,
                          "title": str(entry.get("title") or file_path.stem), "members": []}
        files[sha]["members"].append(member)
    require(files, "No active PDFs are available for this selection.")
    selected = list(files.values())
    for index, item in enumerate(selected, 1):
        item["file_id"] = f"F{index:04d}"
    return {"workspace": str(workspace.relative_to(export_root.parent)),
            "metadata_path": str(metadata_path.relative_to(export_root.parent)),
            "metadata_sha256": digest(metadata_path), "files": selected, "excluded": excluded,
            "library_items_without_attachments": "unknown; zpm metadata lists attachments only"}


class Pipeline:
    def __init__(self, settings, runner=subprocess.run):
        self.settings = settings
        self.runner = runner
        self.root = Path(settings["run_dir"])
        self.config_hash = hashlib.sha256(encoded(settings).encode()).hexdigest()
        self.run_id = f"{self.root.name}-{self.config_hash[:12]}"
        self.remote = f"{settings['remote']}/{self.run_id}"
        self.state = None
        self.manifest = None

    def plan(self):
        return {"mode": "plan", "run_dir": str(self.root), "destination": self.remote,
                "collection_key": self.settings["collection_key"], "question": self.settings["question"],
                "recursive": self.settings["recursive"], "source_limit": self.settings["source_limit"],
                "batch_size": self.settings["batch_size"],
                "max_queries": self.settings["max_queries"], "versions": {"zpm": "1.3.1", "notebooklm-py": "0.8.5"},
                "steps": ["Test tool versions and existing NotebookLM authentication", "Export a fresh zpm selection", "Freeze validated PDF identities and hashes", "Copy immutable files to Drive and compare content", "Create notebooks and import explicit Drive file IDs", "Wait for sources and save indexed text", "Ask once per batch and save unverified answers with citations"],
                "effects": "No commands or files changed. Add --execute to run."}

    def call(self, args, json_output=False, timeout=None):
        try:
            result = self.runner(args, capture_output=True, text=True, timeout=timeout or self.settings["command_timeout"], check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise Stop(f"{args[0]} did not finish. Resume only after reviewing the saved operation.") from exc
        require(result.returncode == 0, f"{args[0]} exited with code {result.returncode}. Raw diagnostics were not saved.")
        if not json_output:
            return result.stdout
        try:
            value = json.loads(result.stdout)
        except (ValueError, TypeError) as exc:
            raise Stop(f"{args[0]} returned invalid JSON. The saved operation remains pending.") from exc
        require(isinstance(value, (dict, list)), f"{args[0]} returned an unknown JSON shape.")
        require(not isinstance(value, dict) or not value.get("error"), f"{args[0]} returned an error.")
        return value

    def checkpoint(self):
        save_json(self.root / "state.json", self.state)

    def preflight(self):
        for tool, version in (("notebooklm", "0.8.5"), ("zpm", "1.3.1")):
            text = self.call([tool, "--version"])
            require(re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.a-zA-Z+-])", text), f"Use {tool} version {version} for this runner.")
        self.call(["rclone", "version"])
        auth = self.call(["notebooklm", "auth", "check", "--test", "--passive", "--json"], True)
        require(isinstance(auth, dict) and auth.get("status") == "ok" and isinstance(auth.get("checks"), dict) and auth["checks"].get("token_fetch") is True, "NotebookLM authentication is not ready.")

    def run(self):
        self.preflight()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        with run_lock(self.root / ".lock"):
            state_path = self.root / "state.json"
            if state_path.exists():
                self.state = read_json(state_path)
                require(isinstance(self.state, dict) and self.state.get("schema_version") == 1 and isinstance(self.state.get("batches"), list), "Unsupported saved state.")
                require(type(self.state.get("queries_attempted")) is int and self.state["queries_attempted"] >= 0, "Invalid saved query count.")
                require(all(isinstance(batch, dict) and isinstance(batch.get("file_ids"), list) and isinstance(batch.get("sources"), dict) and all(isinstance(source, dict) for source in batch["sources"].values()) for batch in self.state["batches"]), "Invalid saved batches.")
                require(self.state.get("config_hash") == self.config_hash, "Settings changed. Use a new run directory.")
            else:
                require(not any(p.name != ".lock" for p in self.root.iterdir()), "Use an empty run directory.")
                self.state = {"schema_version": 1, "config_hash": self.config_hash, "created_at": datetime.now(timezone.utc).isoformat(),
                              "run_id": self.run_id, "status": "running", "queries_attempted": 0, "batches": []}
                self.checkpoint()
            try:
                self.export()
                require(len(self.state["batches"]) <= self.settings["max_queries"], "The selection needs more queries than max_queries. Use a new run with a sufficient budget or smaller selection.")
                self.transfer()
                self.analyze()
                self.state["status"] = "complete"
                self.state.pop("stop_reason", None)
                self.checkpoint()
                self.report()
                return {"status": "complete", "report": str(self.root / "REPORT.md")}
            except Stop as exc:
                self.state["status"] = "stopped"
                self.state["stop_reason"] = str(exc)
                self.checkpoint()
                if self.manifest is not None:
                    self.report()
                raise

    def export(self):
        manifest_path = self.root / "manifest.json"
        if self.state.get("manifest_sha256"):
            require(matches_hash(manifest_path, self.state["manifest_sha256"]), "Frozen manifest changed. Use a new run.")
            self.manifest = read_json(manifest_path)
            require(isinstance(self.manifest, dict), "Unsupported frozen manifest.")
            current = inventory(self.root / "export", self.settings["collection_key"])
            require(current == self.manifest, "The frozen export changed. Use a new run.")
            expected = [self.manifest["files"][start:start + self.settings["batch_size"]] for start in range(0, len(self.manifest["files"]), self.settings["batch_size"])]
            require(len(expected) == len(self.state["batches"]), "Saved batches do not match the frozen selection.")
            for index, (files, batch) in enumerate(zip(expected, self.state["batches"]), 1):
                require(batch.get("title") == f"literature-{self.run_id}-batch-{index:03d}" and batch["file_ids"] == [f["file_id"] for f in files] and set(batch["sources"]) <= set(batch["file_ids"]), "Saved batch identity changed.")
            return
        require(not self.state.get("export_started"), "The export was interrupted. Preserve it and use a new run directory.")
        self.state["export_started"] = True
        self.checkpoint()
        self.call(["zpm", "export", self.settings["collection_key"], "--output", str(self.root / "export"),
                   "--recursive" if self.settings["recursive"] else "--no-recursive", "--pdf-only", "--metadata"])
        self.manifest = inventory(self.root / "export", self.settings["collection_key"])
        batches = (len(self.manifest["files"]) + self.settings["batch_size"] - 1) // self.settings["batch_size"]
        save_json(manifest_path, self.manifest, exclusive=True)
        self.state["manifest_sha256"] = digest(manifest_path)
        for index in range(batches):
            files = self.manifest["files"][index * self.settings["batch_size"]:(index + 1) * self.settings["batch_size"]]
            self.state["batches"].append({"title": f"literature-{self.run_id}-batch-{index + 1:03d}", "file_ids": [f["file_id"] for f in files], "sources": {}})
        self.checkpoint()

    def transfer(self):
        files = self.manifest["files"]
        listing = self.root / "upload-files.txt"
        expected_list = "\n".join(f["path"] for f in files) + "\n"
        if listing.exists():
            require(listing.read_text(encoding="utf-8") == expected_list, "The upload list changed.")
        else:
            listing.write_text(expected_list, encoding="utf-8")
        args = [str(self.root / self.manifest["workspace"]), self.remote, "--files-from", str(listing)]
        if not self.state.get("transfer_complete"):
            self.call(["rclone", "copy", *args, "--immutable", "--drive-skip-shortcuts"])
        self.call(["rclone", "check", *args, "--one-way", "--download", "--drive-skip-shortcuts"])
        rows = self.call(["rclone", "lsjson", self.remote, "--recursive", "--files-only", "--drive-skip-shortcuts"], True)
        require(isinstance(rows, list), "Unexpected Drive inventory JSON.")
        found = {}
        for row in rows:
            require(isinstance(row, dict) and isinstance(row.get("Path"), str) and valid_id(row.get("ID")), "Drive inventory lacks a path or file ID.")
            require(row["Path"] not in found, "Drive has duplicate file paths. Resolve them before resuming.")
            found[row["Path"]] = row["ID"]
        require(set(found) == {f["path"] for f in files}, "Drive inventory does not match the frozen selection.")
        require(len(set(found.values())) == len(found), "Drive inventory repeats a file ID.")
        if self.state.get("drive_ids"):
            require(self.state["drive_ids"] == found, "Drive file identities changed. Use a new run.")
        self.state["drive_ids"] = found
        self.state["transfer_complete"] = True
        self.checkpoint()

    def notebooks(self):
        result = self.call(["notebooklm", "list", "--json"], True)
        require(isinstance(result, dict) and isinstance(result.get("notebooks"), list), "Unknown notebook list shape.")
        require(all(isinstance(row, dict) and valid_id(row.get("id")) and isinstance(row.get("title"), str) for row in result["notebooks"]), "Invalid notebook list entry.")
        return result["notebooks"]

    def source_rows(self, notebook_id):
        result = self.call(["notebooklm", "source", "list", "-n", notebook_id, "--json"], True)
        require(isinstance(result, dict) and isinstance(result.get("sources"), list), "Unknown source list shape.")
        rows = result["sources"]
        require(all(isinstance(row, dict) and valid_id(row.get("id")) and {"drive_document_id", "status", "drive_status", "is_drive_degraded"} <= row.keys() for row in rows), "Invalid source identity or status schema.")
        return rows

    def notebook(self, batch):
        if batch.get("notebook_id"):
            require(valid_id(batch["notebook_id"]), "Invalid saved notebook ID.")
            return batch["notebook_id"]
        matches = [row for row in self.notebooks() if row["title"] == batch["title"]]
        require(len(matches) <= 1, "Several notebooks match the run title. Resolve the conflict before resuming.")
        if matches:
            require(batch.get("create_pending"), "A notebook already uses this run title. Use a new run directory.")
            result = matches[0]
        else:
            require(not batch.get("create_pending"), "A notebook creation is unconfirmed. No matching notebook is visible. Wait and resume; do not repeat the write.")
            batch["create_pending"] = True
            self.checkpoint()
            payload = self.call(["notebooklm", "create", batch["title"], "--json"], True)
            result = payload.get("notebook") if isinstance(payload, dict) else None
        require(isinstance(result, dict) and valid_id(result.get("id")) and result.get("title") == batch["title"], "Unknown notebook creation result.")
        batch["notebook_id"] = result["id"]
        batch.pop("create_pending", None)
        self.checkpoint()
        return result["id"]

    def source(self, batch, file):
        notebook_id = batch["notebook_id"]
        drive_id = self.state["drive_ids"][file["path"]]
        state = batch["sources"].setdefault(file["file_id"], {})
        rows = self.source_rows(notebook_id)
        require(len(rows) <= self.settings["source_limit"], "Notebook source count exceeds the recorded account limit.")
        matches = [row for row in rows if row.get("drive_document_id") == drive_id]
        require(len(matches) <= 1, "The notebook has duplicate sources for one Drive file.")
        if state.get("source_id"):
            require(len(matches) == 1 and matches[0]["id"] == state["source_id"], "Saved source identity no longer matches Drive.")
        elif matches:
            require(state.get("add_pending"), "An unexpected source already uses this Drive file. Inspect the notebook.")
            state["source_id"] = matches[0]["id"]
            state.pop("add_pending", None)
            self.checkpoint()
        else:
            require(not state.get("add_pending"), "A source import is unconfirmed. No matching Drive source is visible. Wait and resume; do not repeat the write.")
            require(len(rows) < self.settings["source_limit"], "The notebook reached its source limit.")
            state["add_pending"] = True
            self.checkpoint()
            payload = self.call(["notebooklm", "source", "add-drive", drive_id, f"{file['file_id']} {file['title']}", "--mime-type", "pdf", "-n", notebook_id, "--json"], True)
            result = payload.get("source") if isinstance(payload, dict) else None
            require(isinstance(result, dict) and valid_id(result.get("id")) and result.get("drive_file_id") == drive_id, "Unknown Drive import result.")
            state["source_id"] = result["id"]
            state.pop("add_pending", None)
            self.checkpoint()
        source_id = state["source_id"]
        ready = self.call(["notebooklm", "source", "wait", source_id, "-n", notebook_id, "--timeout", str(self.settings["wait_timeout"]), "--json"], True, self.settings["wait_timeout"] + 30)
        require(isinstance(ready, dict) and ready.get("status") == "ready" and ready.get("source_id") == source_id, "The source is not ready.")
        current = [row for row in self.source_rows(notebook_id) if row["id"] == source_id]
        require(len(current) == 1 and current[0].get("drive_document_id") == drive_id and current[0].get("status") == "ready" and current[0].get("is_drive_degraded") is False and current[0].get("drive_status") == "active", "Drive source access is not confirmed active.")
        state["drive_status"] = current[0]["drive_status"]
        text_path = self.root / "outputs" / f"{file['file_id']}.text.json"
        if not state.get("text_sha256"):
            # A crash can leave the complete response before its state update.
            text = read_json(text_path) if text_path.exists() else self.call(["notebooklm", "source", "fulltext", source_id, "-n", notebook_id, "--json"], True)
            require(isinstance(text, dict) and text.get("source_id") == source_id and isinstance(text.get("content"), str) and text["content"].strip(), "Indexed source text is missing or unreadable.")
            if not text_path.exists():
                save_json(text_path, text, exclusive=True)
            state["text_sha256"] = digest(text_path)
        else:
            require(matches_hash(text_path, state["text_sha256"]), "Saved indexed text changed.")
        self.checkpoint()
        return source_id

    def analyze(self):
        output = self.root / "outputs"
        output.mkdir(exist_ok=True)
        files = {f["file_id"]: f for f in self.manifest["files"]}
        for number, batch in enumerate(self.state["batches"], 1):
            answer_path = output / f"batch-{number:03d}.answer.json"
            if batch.get("answer_sha256"):
                require(matches_hash(answer_path, batch["answer_sha256"]), "Saved answer changed.")
                for file_id in batch["file_ids"]:
                    expected = batch["sources"].get(file_id, {}).get("text_sha256")
                    require(matches_hash(output / f"{file_id}.text.json", expected), "Saved indexed text changed.")
                continue
            self.notebook(batch)
            ids = [self.source(batch, files[file_id]) for file_id in batch["file_ids"]]
            recovery = (f"Inspect notebook {batch['notebook_id']} history and {answer_path.name}. "
                        "Preserve this run. Do not clear ask_pending or reduce queries_attempted. "
                        "This run will not repeat the request.")
            if batch.get("ask_pending") and answer_path.exists():
                try:
                    answer = read_json(answer_path)
                    self.validate_answer(answer, ids)
                except Stop as exc:
                    raise Stop(f"{exc} {recovery}") from exc
                batch["answer_sha256"] = digest(answer_path)
                batch.pop("ask_pending")
                self.checkpoint()
                continue
            require(not batch.get("ask_pending"), f"An answer request is unconfirmed. {recovery}")
            require(self.state["queries_attempted"] < self.settings["max_queries"], "The query budget is exhausted.")
            prompt_path = output / f"batch-{number:03d}.prompt.txt"
            prompt = (f"Question: {self.settings['question']}\n\nUse only the selected sources.\n"
                      "Return one row per file ID below. Extract relevant methods, data, findings, limits, and contradictions.\n"
                      "Attach source citations and passage locations to each finding. Separate author claims from evidence.\n"
                      "Mark missing evidence unresolved. Retrieval silence does not show absence. Do not claim full reading.\n\n"
                      + "\n".join(f"{fid}: source {sid}; Zotero items " + ", ".join(sorted({m['item_key'] for m in files[fid]['members']})) for fid, sid in zip(batch["file_ids"], ids)) + "\n")
            prompt_path.write_text(prompt, encoding="utf-8")
            batch["ask_pending"] = True
            self.state["queries_attempted"] += 1
            self.checkpoint()
            args = ["notebooklm", "ask", "--prompt-file", str(prompt_path), "-n", batch["notebook_id"], "--json"]
            for source_id in ids:
                args.extend(["-s", source_id])
            answer = self.call(args, True)
            self.validate_answer(answer, ids)
            try:
                save_json(answer_path, answer, exclusive=True)
            except OSError as exc:
                raise Stop(f"Cannot save {answer_path.name}: {exc}. {recovery}") from exc
            batch["answer_sha256"] = digest(answer_path)
            batch.pop("ask_pending", None)
            self.checkpoint()

    @staticmethod
    def validate_answer(answer, source_ids):
        require(isinstance(answer, dict) and isinstance(answer.get("answer"), str) and answer["answer"].strip() and isinstance(answer.get("references"), list), "Unknown or empty answer.")
        require(all(isinstance(ref, dict) and ref.get("source_id") in source_ids for ref in answer["references"]), "An answer cites a source outside the selected batch.")

    def report(self):
        files = self.manifest["files"]
        batches = self.state["batches"]
        sources = [s for b in batches for s in b["sources"].values()]
        output = self.root / "outputs"
        saved_texts = sum(matches_hash(output / f"{fid}.text.json", source.get("text_sha256"))
                          for batch in batches for fid, source in batch["sources"].items())
        saved_answers = [matches_hash(output / f"batch-{number:03d}.answer.json", batch.get("answer_sha256"))
                         for number, batch in enumerate(batches, 1)]
        coverage = {"selected_item_records": len({m["item_key"] for f in files for m in f["members"]}),
                    "active_export_records": sum(len(f["members"]) for f in files), "unique_files": len(files),
                    "excluded_attachment_records": len(self.manifest["excluded"]),
                    "transferred_files": len(self.state.get("drive_ids", {})),
                    "imported_sources": sum("source_id" in s for s in sources),
                    "indexed_sources_saved": saved_texts,
                    "batch_answers_saved": sum(saved_answers),
                    "queries_attempted": self.state["queries_attempted"],
                    "papers_fully_read": 0, "claims_inspected_in_originals": 0,
                    "extracted_paper_rows": "unverified", "items_without_attachments": "unknown"}
        save_json(self.root / "coverage.json", coverage)
        lines = ["# Generated literature report", "", "Status: generated and unverified.", "", f"Run state: {self.state['status']}.", "", "Question: " + self.settings["question"], "", "## Coverage", "", "```json", encoded(coverage).rstrip(), "```", "", "Import, indexed text, and generated answers do not prove full reading.", "Items without attachments need a separate library inventory.", "Citation offsets in raw responses are not offsets into saved plain text."]
        for number, batch in enumerate(batches, 1):
            lines.extend(["", f"## Batch {number}", "", "Files: " + ", ".join(batch["file_ids"])])
            if batch.get("notebook_id"):
                lines.append(f"Notebook: https://notebooklm.google.com/notebook/{batch['notebook_id']}")
            if saved_answers[number - 1]:
                answer = read_json(self.root / "outputs" / f"batch-{number:03d}.answer.json")
                lines.extend(["", answer["answer"], "", f"Raw answer and citations: [batch-{number:03d}.answer.json](outputs/batch-{number:03d}.answer.json)"])
            else:
                lines.extend(["", "Answer: missing or changed." if batch.get("answer_sha256") else "Answer: pending."])
        lines.extend(["", "## Next actions", "", self.state.get("stop_reason", "Inspect citations in the original PDFs before using any claim."), "Reconcile generated rows with every file and item in manifest.json.", "Keep unresolved rows and extraction failures visible.", "Compare batches with compatible data and methods in the research harness.", "Global scientific synthesis and original-source review remain unfinished.", ""])
        (self.root / "REPORT.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", type=Path, help="JSON settings file")
    parser.add_argument("--execute", action="store_true", help="Run uploads, imports, and bounded questions")
    args = parser.parse_args(argv)
    try:
        pipeline = Pipeline(load_config(args.settings))
        result = pipeline.run() if args.execute else pipeline.plan()
        print(encoded(result), end="")
        return 0
    except (Stop, OSError) as exc:
        print(encoded({"status": "stopped", "reason": str(exc)}), end="", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
