import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/research-workflow/scripts/lint_records.py"
CODES = {
    "SCHEMA", "PATH", "READ", "HASH", "BINDING", "DUPLICATE_ID",
    "CURRENT", "STALE", "REVIEW_HISTORY", "DEPENDENCY",
}


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("limits.md", "Use the approved total budget.\n")
        self.write("source.txt", "A negative result is evidence.\n")
        self.base = self.record("reader-a")

    def write(self, path, value):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, dict):
            value = json.dumps(value, indent=2) + "\n"
        target.write_text(value, encoding="utf-8")

    def digest(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def record(self, name, dependencies=None):
        paths = {
            "current": f"contracts/{name}.json",
            "snapshot": f"saved/{name}/contract-copy.json",
            "result": f"submissions/{name}.json",
            "review": f"decisions/{name}.md",
            "artifact": f"historical-evidence/{name}.txt",
        }
        self.write(paths["artifact"], "The result is negative.\n")
        task = {
            "task_id": name, "revision": 1, "goal": "Analyze the source.",
            "owner": "worker-a", "inputs": [{"path": "source.txt", "sha256": self.digest("source.txt")}],
            "dependencies": dependencies or [], "write_paths": [f"future/{name}/attempt/"],
            "budget_ref": "limits.md", "acceptance": ["Report the observed evidence."],
            "stop_condition": "Stop at the budget limit.",
        }
        self.write(paths["current"], task)
        self.write(paths["snapshot"], task)
        result = {
            "task_id": name, "task_revision": 1, "attempt_id": "try_01",
            "task_path": paths["snapshot"], "task_sha256": self.digest(paths["snapshot"]),
            "execution_status": "completed",
            "artifacts": [{"path": paths["artifact"], "sha256": self.digest(paths["artifact"])}],
            "unresolved": [], "resource_usage": {"tokens": None}, "next_action": "Review the evidence.",
        }
        self.write(paths["result"], result)
        review = {
            "review_id": f"review-{name}", "task_id": name, "task_revision": 1,
            "attempt_id": "try_01", "result_path": paths["result"],
            "result_sha256": self.digest(paths["result"]), "reviewer": "reviewer-a",
            "decision_owner": "coordinator", "decision": "accepted",
            "basis": [paths["artifact"]], "unresolved": [], "supersedes": None,
        }
        self.review(paths["review"], review)
        return {**paths, "task_data": task, "result_data": result, "review_data": review}

    def review(self, path, data):
        self.write(path, "# Review\n\n## Task acceptance (optional)\n\n```json\n" + json.dumps(data, indent=2) + "\n```\n")

    def dependency(self, record):
        return {
            "task_path": record["current"], "task_revision": 1,
            "result_path": record["result"], "result_sha256": self.digest(record["result"]),
            "review_path": record["review"], "review_sha256": self.digest(record["review"]),
        }

    def flags(self, record=None, review=True):
        record = record or self.base
        args = ["--task", record["current"], "--result", record["result"]]
        if review:
            args += ["--review", record["review"]]
        return args

    def snapshot(self):
        saved = {}
        for path in sorted(self.root.rglob("*")):
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                value = os.readlink(path)
            elif stat.S_ISREG(mode):
                value = path.read_bytes()
            else:
                value = None
            saved[path.relative_to(self.root).as_posix()] = (mode, value)
        return saved

    def run_cli(self, args):
        before = self.snapshot()
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(before, self.snapshot(), "The checker changed input files.")
        self.assertNotIn("Traceback", result.stderr)
        return result

    def lint(self, args=None, code=None):
        result = self.run_cli(self.flags() if args is None else args)
        self.assertEqual(result.returncode, 0 if code is None else 1, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(set(output), {"diagnostics"})
        diagnostics = output["diagnostics"]
        self.assertIsInstance(diagnostics, list)
        for item in diagnostics:
            self.assertEqual(set(item), {"code", "path", "message"})
            self.assertIn(item["code"], CODES)
            self.assertTrue(all(isinstance(value, str) and value for value in item.values()))
            self.assertFalse(Path(item["path"]).is_absolute())
            self.assertNotIn("..", Path(item["path"]).parts)
        keys = [(item["path"], item["code"], item["message"]) for item in diagnostics]
        self.assertEqual(keys, sorted(set(keys)))
        if code is None:
            self.assertEqual(diagnostics, [])
        else:
            self.assertIn(code, {item["code"] for item in diagnostics}, result.stdout)
        return result.stdout

    def test_custom_layout_reused_artifact_unknown_measurement_and_extra_fields(self):
        data = copy.deepcopy(self.base["task_data"])
        data["project_note"] = "Keep this convention."
        self.write(self.base["current"], data)
        self.write(self.base["snapshot"], data)
        result = copy.deepcopy(self.base["result_data"])
        result["task_sha256"] = self.digest(self.base["snapshot"]).upper()
        result["artifacts"][0]["sha256"] = result["artifacts"][0]["sha256"].upper()
        self.write(self.base["result"], result)
        review = copy.deepcopy(self.base["review_data"])
        review["result_sha256"] = self.digest(self.base["result"]).upper()
        self.review(self.base["review"], review)
        self.lint()

    def test_ordinary_review_and_unselected_legacy_files(self):
        self.write("old/STATE.md", "A legacy record has no JSON fields.\n")
        self.write("old/broken.json", "{unrelated")
        self.write("discussion.md", '# Review\n\n## Outcome\n\nKeep investigating.\n\n```json\n{"ordinary": true}\n```\n')
        self.lint(["--review", "discussion.md"])

    def test_usage_requires_a_record_and_rejects_unknown_flags(self):
        for args in ([], ["--unknown"], ["--task"]):
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(args).returncode, 2)

    def test_each_required_task_field(self):
        for field in self.base["task_data"]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.base["task_data"])
                del data[field]
                self.write(self.base["current"], data)
                self.lint(["--task", self.base["current"]], "SCHEMA")

    def test_task_types_ids_revisions_and_empty_text(self):
        cases = [
            ("task_id", "a.b"), ("task_id", "../reader"), ("revision", True),
            ("revision", 0), ("revision", 1.5), ("goal", " "), ("owner", None),
            ("inputs", {}), ("inputs", [{"path": "source.txt"}]),
            ("dependencies", [None]), ("write_paths", []), ("write_paths", [1]),
            ("budget_ref", ""), ("acceptance", []), ("acceptance", [False]),
            ("stop_condition", []),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.base["task_data"])
                data[field] = value
                self.write(self.base["current"], data)
                self.lint(["--task", self.base["current"]], "SCHEMA")

    def test_each_required_result_field(self):
        for field in self.base["result_data"]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.base["result_data"])
                del data[field]
                self.write(self.base["result"], data)
                self.lint(self.flags(review=False), "SCHEMA")

    def test_result_types_status_and_empty_completed_result(self):
        cases = [
            ("task_id", "bad id"), ("task_revision", False), ("attempt_id", "bad/id"),
            ("execution_status", "accepted"), ("artifacts", []),
            ("artifacts", [{"path": self.base["artifact"]}]),
            ("unresolved", "none"), ("unresolved", [1]),
            ("resource_usage", []), ("next_action", ""),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.base["result_data"])
                data[field] = value
                self.write(self.base["result"], data)
                self.lint(self.flags(review=False), "SCHEMA")

    def test_each_required_review_field(self):
        for field in self.base["review_data"]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.base["review_data"])
                del data[field]
                self.review(self.base["review"], data)
                self.lint(code="SCHEMA")

    def test_review_types_and_decisions(self):
        cases = [
            ("review_id", "bad id"), ("task_revision", True), ("reviewer", " "),
            ("decision_owner", None), ("decision", "completed"), ("basis", []),
            ("basis", [1]), ("unresolved", None), ("supersedes", {}),
        ]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.base["review_data"])
                data[field] = value
                self.review(self.base["review"], data)
                self.lint(code="SCHEMA")

    def test_broken_json_duplicate_keys_and_nonfinite_numbers(self):
        valid = json.dumps(self.base["task_data"])
        for raw in ("{", "[]", valid[:-1] + ', "revision": 1}', valid[:-1] + ', "extra": NaN}', valid[:-1] + ', "extra": Infinity}'):
            with self.subTest(raw=raw):
                self.write(self.base["current"], raw)
                self.lint(["--task", self.base["current"]], "SCHEMA")

    def test_large_json_exponents_do_not_create_nonfinite_measurements(self):
        data = copy.deepcopy(self.base["result_data"])
        data["resource_usage"] = {"tokens": "unbounded"}
        for number in ("1e999", "-1e999"):
            with self.subTest(number=number):
                raw = json.dumps(data).replace('"unbounded"', number)
                self.write(self.base["result"], raw)
                self.lint(self.flags(review=False), "SCHEMA")

    def test_acceptance_section_requires_exactly_one_json_object(self):
        block = "```json\n" + json.dumps(self.base["review_data"]) + "\n```\n"
        for body in ("No structured decision.\n", "```json\n{\n```\n", "```json\n[]\n```\n", block + block):
            with self.subTest(body=body):
                self.write(self.base["review"], "# Review\n\n## Task acceptance (optional)\n\n" + body)
                self.lint(code="SCHEMA")

    def test_unrelated_json_outside_acceptance_section_is_ignored(self):
        prefix = "# Review\n\n```json\n{broken unrelated text\n```\n\n"
        content = (self.root / self.base["review"]).read_text()
        self.write(self.base["review"], prefix + content)
        self.lint()

    def test_commented_review_cannot_satisfy_repinned_dependency(self):
        content = (self.root / self.base["review"]).read_text()
        for prefix, suffix in (("<!--\n", "-->\n"), ("<!--", "-->"), ("<!--\n", "")):
            with self.subTest(prefix=prefix, suffix=suffix):
                self.write(self.base["review"], prefix + content + suffix)
                dependent = self.record("dependent", [self.dependency(self.base)])
                output = json.loads(self.lint(self.flags(dependent), "DEPENDENCY"))
                self.assertNotIn("HASH", {item["code"] for item in output["diagnostics"]})

    def test_active_acceptance_ignores_commented_examples(self):
        active = (self.root / self.base["review"]).read_text()
        example = "<!--\n## Task acceptance\n```json\n{example only}\n```\n-->\n"
        for content in (example + active, active + example):
            with self.subTest(content=content):
                self.write(self.base["review"], content)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent))

    def test_multiline_comments_ignore_headings_and_fences(self):
        content = (self.root / self.base["review"]).read_text()
        comment = "<!-- Example only.\n## Other section\n```json\n{not active JSON}\n-->\n"
        self.write(self.base["review"], content.replace("```json\n", comment + "```json\n", 1))
        dependent = self.record("dependent", [self.dependency(self.base)])
        self.lint(self.flags(dependent))

    def test_inline_comments_preserve_active_heading_and_fence(self):
        content = (self.root / self.base["review"]).read_text()
        content = content.replace("## Task acceptance (optional)", "## Task acceptance (optional) <!-- note -->")
        content = content.replace("```json\n", "<!-- note -->```json\n", 1)
        self.write(self.base["review"], content)
        dependent = self.record("dependent", [self.dependency(self.base)])
        self.lint(self.flags(dependent))

    def test_comment_markers_in_json_strings_are_literal(self):
        for marker in ("<!-- paired -->", "<!-- opening only", "closing only -->"):
            with self.subTest(marker=marker):
                review = copy.deepcopy(self.base["review_data"])
                review["reviewer"] = marker
                review["basis"] = [marker]
                self.review(self.base["review"], review)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent))

    def test_comment_markers_in_other_fences_are_literal(self):
        content = (self.root / self.base["review"]).read_text()
        for opening, closing in (("```text", "```"), ("~~~~text", "~~~~"), ("```text <!-- literal", "```")):
            with self.subTest(opening=opening):
                prefix = opening + "\n<!-- literal data\n## Task acceptance\n" + closing + "\n"
                self.write(self.base["review"], prefix + content)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent))

    def test_review_comment_changes_raw_dependency_hash(self):
        dependent = self.record("dependent", [self.dependency(self.base)])
        content = (self.root / self.base["review"]).read_text()
        self.write(self.base["review"], content + "\n<!-- Explanatory note. -->\n")
        self.lint(self.flags(dependent), "HASH")

    def test_comment_markers_in_inline_code_and_escapes_are_literal(self):
        content = (self.root / self.base["review"]).read_text()
        for marker in ("`<!--`", "`` `<!--` ``", r"\<!--", r"\\\<!--"):
            with self.subTest(marker=marker):
                self.write(self.base["review"], "A literal " + marker + " token.\n\n" + content)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent))

    def test_real_comments_after_literal_markers_still_hide_examples(self):
        content = (self.root / self.base["review"]).read_text()
        for marker in ("`` `<!--` ``", r"\<!--"):
            with self.subTest(marker=marker):
                prefix = "A literal " + marker + " followed by <!--\n" + content + "-->\n"
                self.write(self.base["review"], prefix + content)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent))

    def test_unmatched_backtick_does_not_hide_a_real_comment(self):
        content = (self.root / self.base["review"]).read_text()
        self.write(self.base["review"], "Unmatched ` before <!--\n" + content + "-->\n")
        dependent = self.record("dependent", [self.dependency(self.base)])
        self.lint(self.flags(dependent), "DEPENDENCY")

    def test_even_backslashes_do_not_escape_a_real_comment(self):
        content = (self.root / self.base["review"]).read_text()
        self.write(self.base["review"], r"Two backslashes \\<!--" + "\n" + content + "-->\n")
        dependent = self.record("dependent", [self.dependency(self.base)])
        self.lint(self.flags(dependent), "DEPENDENCY")

    def test_only_commented_acceptance_is_an_ordinary_review(self):
        self.write("discussion.md", "# Review\n<!--\n## Task acceptance\n```json\n{example only}\n```\n-->\n")
        self.lint(["--review", "discussion.md"])

    def test_missing_required_files(self):
        for path in ("source.txt", "limits.md", self.base["snapshot"], self.base["artifact"], self.base["result"], self.base["review"]):
            with self.subTest(path=path):
                target = self.root / path
                saved = target.read_bytes()
                target.unlink()
                self.lint(code="READ")
                target.write_bytes(saved)

    def test_hashes_bind_input_artifact_contract_result_and_review(self):
        dependent = self.record("dependent", [self.dependency(self.base)])
        args = self.flags(dependent)
        for path in ("source.txt", self.base["artifact"], self.base["snapshot"], self.base["result"], self.base["review"]):
            with self.subTest(path=path):
                target = self.root / path
                saved = target.read_bytes()
                target.write_bytes(saved + b"\n")
                self.lint(args, "HASH")
                target.write_bytes(saved)

    def test_hash_format(self):
        for value in ("0" * 63, "z" * 64, None, 1):
            with self.subTest(value=value):
                data = copy.deepcopy(self.base["result_data"])
                data["task_sha256"] = value
                self.write(self.base["result"], data)
                self.lint(self.flags(review=False), "SCHEMA")

    def test_unsafe_reference_paths(self):
        for value in (str(self.root / "source.txt"), "../source.txt", "safe/../source.txt", "source\x00.txt", "source\n.txt"):
            with self.subTest(value=value):
                data = copy.deepcopy(self.base["task_data"])
                data["inputs"][0]["path"] = value
                self.write(self.base["current"], data)
                self.lint(["--task", self.base["current"]], "PATH")

    def test_unsafe_cli_path_and_symlink_escape(self):
        self.lint(["--task", "../outside.json"], "PATH")
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "task.json"
            target.write_text(json.dumps(self.base["task_data"]))
            (self.root / "escape.json").symlink_to(target)
            self.lint(["--task", "escape.json"], "PATH")
            self.assertEqual(json.loads(target.read_text()), self.base["task_data"])

    def test_directory_and_fifo_are_not_read_as_records(self):
        self.lint(["--task", "contracts"], "READ")
        os.mkfifo(self.root / "pipe.json")
        self.lint(["--task", "pipe.json"], "READ")

    def test_missing_current_context(self):
        self.lint(["--result", self.base["result"]], "CURRENT")

    def test_result_must_match_snapshot(self):
        for field, value in (("task_id", "other"), ("task_revision", 2)):
            with self.subTest(field=field):
                data = copy.deepcopy(self.base["result_data"])
                data[field] = value
                self.write(self.base["result"], data)
                self.lint(self.flags(review=False), "BINDING")

    def test_snapshot_cannot_be_the_current_file(self):
        data = copy.deepcopy(self.base["result_data"])
        data["task_path"] = self.base["current"]
        self.write(self.base["result"], data)
        self.lint(self.flags(review=False), "BINDING")

    def test_new_current_contract_marks_history_stale(self):
        for revision in (1, 2):
            with self.subTest(revision=revision):
                task = copy.deepcopy(self.base["task_data"])
                task["revision"] = revision
                task["owner"] = "new-owner"
                self.write(self.base["current"], task)
                self.lint(code="STALE")

    def test_unknown_execution_is_valid_but_cannot_be_accepted(self):
        for status in ("unknown", "blocked", "failed", "cancelled"):
            with self.subTest(status=status):
                result = copy.deepcopy(self.base["result_data"])
                result["execution_status"] = status
                result["artifacts"] = []
                self.write(self.base["result"], result)
                self.lint(self.flags(review=False))
                review = copy.deepcopy(self.base["review_data"])
                review["result_sha256"] = self.digest(self.base["result"])
                self.review(self.base["review"], review)
                self.lint(code="BINDING")

    def test_accepted_review_needs_completed_result_artifacts(self):
        result = copy.deepcopy(self.base["result_data"])
        result["artifacts"] = []
        self.write(self.base["result"], result)
        review = copy.deepcopy(self.base["review_data"])
        review["result_sha256"] = self.digest(self.base["result"])
        self.review(self.base["review"], review)
        output = json.loads(self.lint(code="BINDING"))
        self.assertIn("SCHEMA", {item["code"] for item in output["diagnostics"]})

    def test_review_must_match_result_identity(self):
        for field, value in (("task_id", "other"), ("task_revision", 2), ("attempt_id", "try_02")):
            with self.subTest(field=field):
                review = copy.deepcopy(self.base["review_data"])
                review[field] = value
                self.review(self.base["review"], review)
                self.lint(code="BINDING")

    def test_duplicate_record_identities(self):
        cases = [
            ("--task", "duplicate-task.json", self.base["current"]),
            ("--result", "duplicate-result.json", self.base["result"]),
            ("--review", "duplicate-review.md", self.base["review"]),
        ]
        for flag, duplicate, source in cases:
            with self.subTest(flag=flag):
                self.write(duplicate, (self.root / source).read_text())
                if flag == "--task":
                    data = json.loads((self.root / duplicate).read_text())
                    data["owner"] = "conflicting-owner"
                    self.write(duplicate, data)
                self.lint(self.flags() + [flag, duplicate], "DUPLICATE_ID")
                (self.root / duplicate).unlink()

    def test_repeated_canonical_aliases_are_not_duplicates(self):
        (self.root / "task-alias.json").symlink_to(self.root / self.base["current"])
        (self.root / "result-alias.json").symlink_to(self.root / self.base["result"])
        (self.root / "review-alias.md").symlink_to(self.root / self.base["review"])
        self.lint(self.flags() + ["--task", "./task-alias.json", "--result", "result-alias.json", "--review", "review-alias.md"])

    def test_required_accepted_upstream_records_are_followed(self):
        dependent = self.record("dependent", [self.dependency(self.base)])
        self.lint(self.flags(dependent))

    def test_each_required_dependency_field(self):
        reference = self.dependency(self.base)
        for field in reference:
            with self.subTest(field=field):
                dependency = dict(reference)
                del dependency[field]
                dependent = self.record("dependent", [dependency])
                self.lint(self.flags(dependent), "SCHEMA")

    def test_dependency_versions_and_identity_must_match(self):
        other = self.record("other")
        for changes in (
            {"task_revision": 2},
            {"task_path": other["current"]},
            {"review_path": other["review"], "review_sha256": self.digest(other["review"])},
        ):
            with self.subTest(changes=changes):
                dependent = self.record("dependent", [{**self.dependency(self.base), **changes}])
                self.lint(self.flags(dependent), "DEPENDENCY")

    def test_unaccepted_and_stale_dependencies(self):
        for decision in ("rework", "blocked"):
            with self.subTest(decision=decision):
                review = copy.deepcopy(self.base["review_data"])
                review["decision"] = decision
                self.review(self.base["review"], review)
                dependent = self.record("dependent", [self.dependency(self.base)])
                self.lint(self.flags(dependent), "DEPENDENCY")
        self.review(self.base["review"], self.base["review_data"])
        dependent = self.record("dependent", [self.dependency(self.base)])
        task = copy.deepcopy(self.base["task_data"])
        task["revision"] = 2
        self.write(self.base["current"], task)
        self.lint(self.flags(dependent), "DEPENDENCY")

    def test_withdrawal_invalidates_pinned_acceptance_without_artifact_changes(self):
        dependent = self.record("dependent", [self.dependency(self.base)])
        newer = copy.deepcopy(self.base["review_data"])
        newer.update(review_id="withdrawal", decision="rework", supersedes={"path": self.base["review"], "sha256": self.digest(self.base["review"])})
        self.review("decisions/withdrawal.md", newer)
        self.lint(self.flags() + ["--review", "decisions/withdrawal.md"])
        self.lint(self.flags(dependent) + ["--review", "decisions/withdrawal.md"], "DEPENDENCY")

    def test_supersedes_must_bind_same_exact_result(self):
        other = self.record("other")
        review = copy.deepcopy(self.base["review_data"])
        review.update(review_id="replacement", supersedes={"path": other["review"], "sha256": self.digest(other["review"])})
        self.review("decisions/replacement.md", review)
        self.lint(self.flags() + self.flags(other) + ["--review", "decisions/replacement.md"], "REVIEW_HISTORY")
        review["supersedes"] = {"path": self.base["review"], "sha256": "0" * 64}
        self.review("decisions/replacement.md", review)
        self.lint(self.flags() + ["--review", "decisions/replacement.md"], "HASH")

    def test_conflicting_and_branched_reviews(self):
        review = copy.deepcopy(self.base["review_data"])
        review.update(review_id="conflict", decision="rework")
        self.review("decisions/conflict.md", review)
        self.lint(self.flags() + ["--review", "decisions/conflict.md"], "REVIEW_HISTORY")
        review["supersedes"] = {"path": self.base["review"], "sha256": self.digest(self.base["review"])}
        self.review("decisions/conflict.md", review)
        review["review_id"] = "branch"
        self.review("decisions/branch.md", review)
        self.lint(self.flags() + ["--review", "decisions/conflict.md", "--review", "decisions/branch.md"], "REVIEW_HISTORY")

    def test_review_cycles_do_not_recurse_forever(self):
        one = copy.deepcopy(self.base["review_data"])
        two = copy.deepcopy(one)
        one["supersedes"] = {"path": "decisions/two.md", "sha256": "0" * 64}
        two.update(review_id="two", supersedes={"path": self.base["review"], "sha256": "0" * 64})
        self.review(self.base["review"], one)
        self.review("decisions/two.md", two)
        self.lint(code="REVIEW_HISTORY")

    def test_dependency_cycles_and_invalid_upstream_propagation(self):
        second = self.record("second", [self.dependency(self.base)])
        task = copy.deepcopy(self.base["task_data"])
        task["dependencies"] = [self.dependency(second)]
        self.write(self.base["current"], task)
        self.lint(self.flags(second), "DEPENDENCY")
        task["dependencies"] = []
        self.write(self.base["current"], task)
        third = self.record("third", [self.dependency(second)])
        self.write(self.base["artifact"], "Changed upstream evidence.\n")
        output = json.loads(self.lint(self.flags(third), "DEPENDENCY"))
        affected = {item["path"] for item in output["diagnostics"] if item["code"] == "DEPENDENCY"}
        self.assertIn(second["current"], affected)
        self.assertIn(third["current"], affected)

    def test_repeat_output_is_deterministic(self):
        self.write("source.txt", "Changed source.\n")
        self.write(self.base["artifact"], "Changed artifact.\n")
        first = self.lint(code="HASH")
        pairs = list(zip(self.flags()[::2], self.flags()[1::2]))
        reversed_flags = [part for pair in reversed(pairs) for part in pair]
        second = self.lint(reversed_flags, "HASH")
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
