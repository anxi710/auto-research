"""Offline claim/evidence contract checks; every CLI run preserves its inputs."""
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


SCRIPT = Path(os.environ.get("EVIDENCE_LINTER_SCRIPT", str(
    Path(__file__).resolve().parents[1] / "skills/research-workflow/scripts/lint_records.py")))


class EvidenceLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("budget.md", "Offline synthetic inputs only.\n")
        self.write("draft.md", "On D1 test, A scored 0.8 against B at 0.7.\n")
        self.metrics = {"runs": [{"value": .8, "unit": "fraction", "dataset": "D1",
                                 "split": "test", "method": "A", "baseline": "B",
                                 "conditions": {"seed": 7, "flags": [True]}}],
                        "baselines": [{"value": .7, "unit": "fraction", "dataset": "D1",
                                       "split": "test", "method": "B",
                                       "conditions": {"seed": 7, "flags": [True]}}]}
        self.write("metrics.json", self.metrics)
        evidence = {"evidence_id": "E001", "kind": "experiment", "availability": "available",
                    "scope": "D1 test under frozen conditions.", "limitations": ["One fixture."],
                    "artifact": "metrics.json", "sha256": self.digest("metrics.json"),
                    "locator": {"type": "json_pointer", "value": "/runs/0/value"},
                    "value": .8, "unit": "fraction",
                    "context": {"dataset": "D1", "split": "test", "method": "A", "baseline": "B",
                                "conditions": {"seed": 7, "flags": [True]}},
                    "baseline_locator": "/baselines/0/value", "baseline_value": .7}
        quote = "On D1 test, A scored 0.8 against B at 0.7."
        self.ledger = {"schema_version": "1", "task_id": "T1", "attempt_id": "A1", "claims": [
            {"claim_id": "C001", "text": quote,
             "location": {"artifact": "draft.md", "sha256": self.digest("draft.md"), "exact_quote": quote},
             "evidence": [evidence], "verification_request": {"question": "Does this support the scope?", "limitations": []}}]}
        self.task = {"task_id": "T1", "revision": 1, "goal": "Check synthetic claims.", "owner": "worker",
                     "inputs": [], "dependencies": [], "write_paths": ["outputs/"], "budget_ref": "budget.md",
                     "acceptance": ["Record support and gaps."], "stop_condition": "No external calls.",
                     "evidence_ledger": "ledger.json"}
        self.result = {"task_id": "T1", "task_revision": 1, "attempt_id": "A1", "task_path": "snapshot.json",
                       "task_sha256": "0" * 64, "execution_status": "completed", "artifacts": [],
                       "unresolved": [], "resource_usage": {}, "next_action": "Review."}
        self.review = {"review_id": "R1", "task_id": "T1", "task_revision": 1, "attempt_id": "A1",
                       "result_path": "result.json", "result_sha256": "0" * 64, "reviewer": "reviewer",
                       "decision_owner": "coordinator", "decision": "accepted", "basis": ["ledger.json"],
                       "unresolved": [], "supersedes": None,
                       "claim_evidence": {"ledger": {"path": "ledger.json", "sha256": "0" * 64},
                                          "assessments": [{"claim_id": "C001", "verdict": "yes",
                                                           "scope": "Fixture scope only.", "reason": "Values and scope match.",
                                                           "gaps": [], "follow_up": []}], "unreviewed_claim_ids": []}}
        self.save()

    def write(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2) + "\n" if isinstance(data, dict) else data, encoding="utf-8")

    def digest(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def save(self, ledger=True, typed=True):
        self.write("task.json", self.task)
        self.write("snapshot.json", self.task)
        self.result["task_sha256"] = self.digest("snapshot.json")
        if ledger:
            self.write("ledger.json", self.ledger)
        self.result["artifacts"] = [{"path": "ledger.json", "sha256": self.digest("ledger.json")}]
        if typed:
            self.result["artifacts"][0]["kind"] = "claim_evidence_ledger"
        self.save_result()

    def save_result(self):
        self.write("result.json", self.result)
        self.review["result_sha256"] = self.digest("result.json")
        if "claim_evidence" in self.review:
            self.review["claim_evidence"]["ledger"]["sha256"] = self.digest("ledger.json")
        self.write_review()

    def write_review(self):
        self.write("review.md", "# Review\n\n## Task acceptance\n\n```json\n" + json.dumps(self.review) + "\n```\n")

    def save_raw_numeric(self, source_tokens=None, ledger_tokens=None):
        """Insert explicit JSON number tokens without converting them to float."""
        source_tokens = {"method_value": "0.8", "baseline_value": "0.7", "method_threshold": "0",
                         "baseline_threshold": "0", "method_nested": "0", "baseline_nested": "0",
                         **(source_tokens or {})}
        ledger_tokens = {"value": "0.8", "baseline_value": "0.7", "threshold": "0", "nested": "0",
                         **(ledger_tokens or {})}

        def render(data, tokens):
            content = json.dumps(data, indent=2) + "\n"
            for key, token in tokens.items():
                marker = json.dumps("__RAW_" + key + "__")
                self.assertEqual(content.count(marker), 1, "Raw token must replace one known field.")
                content = content.replace(marker, token)
            return content

        metrics = copy.deepcopy(self.metrics)
        for prefix, parent in (("method", metrics["runs"][0]), ("baseline", metrics["baselines"][0])):
            parent["value"] = "__RAW_" + prefix + "_value__"
            parent["conditions"] = {"threshold": "__RAW_" + prefix + "_threshold__",
                                    "nested": {"levels": ["__RAW_" + prefix + "_nested__"]}}
        self.write("metrics.json", render(metrics, source_tokens))
        ledger = copy.deepcopy(self.ledger)
        evidence = ledger["claims"][0]["evidence"][0]
        evidence["sha256"] = self.digest("metrics.json")
        evidence["value"] = "__RAW_value__"
        evidence["baseline_value"] = "__RAW_baseline_value__"
        evidence["context"]["conditions"] = {"threshold": "__RAW_threshold__",
                                               "nested": {"levels": ["__RAW_nested__"]}}
        if "locator" in ledger_tokens:
            evidence["locator"]["value"] = "__RAW_locator__"
        self.write("ledger.json", render(ledger, ledger_tokens))
        self.save(ledger=False)

    def files(self):
        result = {}
        for path in self.root.rglob("*"):
            mode = path.lstat().st_mode
            result[str(path.relative_to(self.root))] = (mode, os.readlink(path) if stat.S_ISLNK(mode)
                                                       else path.read_bytes() if stat.S_ISREG(mode) else None)
        return result

    def lint(self, code=None, args=None):
        before = self.files()
        run = subprocess.run([sys.executable, "-B", str(SCRIPT), "--root", str(self.root),
                              *(args or ["--task", "task.json", "--result", "result.json", "--review", "review.md"])],
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(before, self.files(), "Checker modified an input.")
        self.assertEqual(run.returncode, 0 if code is None else 1, run.stdout + run.stderr)
        self.assertNotIn("Traceback", run.stderr)
        diagnostics = json.loads(run.stdout)["diagnostics"]
        if code is None:
            self.assertEqual(diagnostics, [])
        else:
            self.assertIn(code, {item["code"] for item in diagnostics}, run.stdout)
        return diagnostics

    @property
    def claim(self):
        return self.ledger["claims"][0]

    @property
    def evidence(self):
        return self.claim["evidence"][0]

    def literature(self, availability="inaccessible"):
        self.claim["evidence"] = [{"evidence_id": "E001", "kind": "literature", "availability": availability,
                                   "scope": "Metadata only.", "limitations": ["No fixed source available."],
                                   "artifact": None, "sha256": None, "reason": "Fixture source cannot be retrieved.",
                                   "source": {"version": "v1", "identifier": "urn:synthetic:paper",
                                              "reading_depth": "metadata", "access_limitations": ["Full text unavailable."],
                                              "content_kind": "none"},
                                   "locator": {"type": "section", "value": "Results"}}]

    def test_valid_automatic_ledger_and_legacy(self):
        self.lint()
        del self.task["evidence_ledger"]
        del self.review["claim_evidence"]
        self.ledger["schema_version"] = "invalid but untyped legacy artifact"
        self.save(typed=False)
        self.lint()

    def test_optional_typed_ledger_still_checked(self):
        del self.task["evidence_ledger"]
        self.evidence["value"] = .1
        self.save()
        self.lint("BINDING")

    def test_required_ledger_cannot_omit_kind_or_artifact(self):
        self.save(typed=False)
        self.lint("BINDING")
        self.result["artifacts"] = [{"path": "draft.md", "sha256": self.digest("draft.md")}]
        self.save_result()
        self.lint("BINDING")

    def test_task_requirement_invalid_types_and_unsafe_path(self):
        for value in (None, False, {}, [], "", "../ledger.json", "/ledger.json"):
            with self.subTest(value=value):
                self.task["evidence_ledger"] = value
                self.save()
                self.lint("PATH" if isinstance(value, str) and value else "SCHEMA")

    def test_blocked_result_need_not_supply_required_ledger(self):
        self.result["execution_status"] = "blocked"
        self.result["artifacts"] = []
        self.review["decision"] = "blocked"
        del self.review["claim_evidence"]
        self.save_result()
        self.lint()

    def test_duplicate_typed_ledgers(self):
        self.result["artifacts"] *= 2
        self.save_result()
        self.lint("SCHEMA")

    def test_ledger_root_schema_and_authority_fields(self):
        original = copy.deepcopy(self.ledger)
        for key, value in (("schema_version", 1), ("claims", []), ("verdict", "yes"),
                           ("approval", True), ("status", "accepted"), ("task_id", "other"), ("attempt_id", "other")):
            with self.subTest(key=key):
                self.ledger = copy.deepcopy(original)
                self.ledger[key] = value
                self.save()
                self.lint("BINDING" if key in {"task_id", "attempt_id"} else "SCHEMA")

    def test_claim_and_evidence_ids_are_unique(self):
        self.ledger["claims"].append(copy.deepcopy(self.claim))
        self.save()
        self.lint("DUPLICATE_ID")
        self.ledger["claims"][1]["claim_id"] = "C002"
        self.save()
        self.lint("DUPLICATE_ID")

    def test_location_hash_text_and_unique_overlapping_occurrence(self):
        self.write("draft.md", "changed")
        self.lint("HASH")
        self.claim["text"] = self.claim["location"]["exact_quote"] = "aa"
        self.write("draft.md", "aaa")
        self.claim["location"]["sha256"] = self.digest("draft.md")
        self.save()
        self.lint("BINDING")
        self.write("draft.md", "aa")
        self.claim["location"]["sha256"] = self.digest("draft.md")
        self.claim["text"] = "different text"
        self.save()
        self.lint("BINDING")

    def test_all_reference_paths_are_safe_and_fixed(self):
        for section in (self.claim["location"], self.evidence):
            original = section["artifact"]
            for value in ("../outside", "/absolute", "C:\\source.txt", "bad\x00path"):
                with self.subTest(value=value):
                    section["artifact"] = value
                    self.save()
                    self.lint("PATH")
            section["artifact"] = original
        self.evidence["sha256"] = "0" * 64
        self.save()
        self.lint("HASH")

    def test_same_number_wrong_method_context(self):
        original = copy.deepcopy(self.metrics)
        for field, value in (("dataset", "D2"), ("split", "train"), ("method", "other"),
                             ("baseline", "other"), ("unit", "percent"), ("conditions", {"seed": 8, "flags": [True]}),
                             ("conditions", {"seed": 7, "flags": [1]})):
            with self.subTest(field=field, value=value):
                self.metrics = copy.deepcopy(original)
                self.metrics["runs"][0][field] = value
                self.write("metrics.json", self.metrics)
                self.evidence["sha256"] = self.digest("metrics.json")
                self.save()
                self.lint("BINDING")

    def test_same_number_wrong_baseline_context(self):
        original = copy.deepcopy(self.metrics)
        for field, value in (("dataset", "D2"), ("split", "train"), ("method", "A"), ("unit", "percent"),
                             ("conditions", {"seed": 7, "flags": [1]})):
            with self.subTest(field=field):
                self.metrics = copy.deepcopy(original)
                self.metrics["baselines"][0][field] = value
                self.write("metrics.json", self.metrics)
                self.evidence["sha256"] = self.digest("metrics.json")
                self.save()
                self.lint("BINDING")

    def test_pointer_requires_normalized_parent_and_strict_syntax(self):
        for pointer in ("/runs/00/value", "/runs/-/value", "/runs/-1/value", "/runs/0~2/value",
                        "/runs/0~/value", "/runs/0/value/", "runs/0/value", "/runs/0/missing", "/runs/0"):
            with self.subTest(pointer=pointer):
                self.evidence["locator"]["value"] = pointer
                self.save()
                self.lint("BINDING")
        self.evidence["locator"]["value"] = "/unbound/value"
        self.metrics["unbound"] = {"value": .8}
        self.write("metrics.json", self.metrics)
        self.evidence["sha256"] = self.digest("metrics.json")
        self.save()
        self.lint("BINDING")

    def test_valid_escaped_pointer(self):
        self.metrics["a/b~c"] = self.metrics["runs"][0]
        self.write("metrics.json", self.metrics)
        self.evidence["sha256"] = self.digest("metrics.json")
        self.evidence["locator"]["value"] = "/a~1b~0c/value"
        self.save()
        self.lint()

    def test_boolean_and_nonfinite_numbers_rejected(self):
        for field in ("value", "baseline_value"):
            old = self.evidence[field]
            self.evidence[field] = True
            self.save()
            self.lint("SCHEMA")
            self.evidence[field] = old
        self.metrics["runs"][0]["value"] = True
        self.evidence["value"] = 1
        self.write("metrics.json", self.metrics)
        self.evidence["sha256"] = self.digest("metrics.json")
        self.save()
        self.lint("BINDING")

    def test_numeric_parent_reported_false_equalities(self):
        cases = [
            ({"method_value": "1e-400"}, {"value": "0"}),
            ({"method_value": "9007199254740993.0"}, {"value": "9007199254740992"}),
            ({"method_value": "0.80000000000000004"}, {"value": "0.8"}),
            ({"method_threshold": "1e-400", "baseline_threshold": "1e-400"}, {"threshold": "0"}),
        ]
        for source, ledger in cases:
            with self.subTest(source=source, ledger=ledger):
                self.save_raw_numeric(source, ledger)
                self.lint("BINDING")

    def test_numeric_underflow_at_method_baseline_and_nested_conditions(self):
        pairs = [("method_value", "value"), ("baseline_value", "baseline_value"),
                 ("method_nested", "nested"), ("baseline_nested", "nested")]
        for source_key, ledger_key in pairs:
            for tiny in ("1e-400", "-1e-400"):
                with self.subTest(field=source_key, tiny=tiny):
                    self.save_raw_numeric({source_key: tiny}, {ledger_key: "0"})
                    self.lint("BINDING")
        self.save_raw_numeric({"method_value": "0"}, {"value": "1e-400"})
        self.lint("BINDING")

    def test_numeric_adjacent_high_precision_decimals_stay_distinct(self):
        for left, right in (("0.123456789012345678901", "0.123456789012345678902"),
                            ("0.12345678901234567890123456789012345678901",
                             "0.12345678901234567890123456789012345678902")):
            for source_key, ledger_key in (("method_value", "value"), ("baseline_value", "baseline_value")):
                with self.subTest(field=source_key, source=left, ledger=right):
                    self.save_raw_numeric({source_key: left}, {ledger_key: right})
                    self.lint("BINDING")
            with self.subTest(field="nested", source=left, ledger=right):
                self.save_raw_numeric({"method_nested": left, "baseline_nested": left}, {"nested": right})
                self.lint("BINDING")

    def test_numeric_same_tiny_values_and_equivalent_spellings(self):
        source = {"method_value": "1e-400", "baseline_value": "2e-400",
                  "method_threshold": "3e-400", "baseline_threshold": "3e-400",
                  "method_nested": "4e-400", "baseline_nested": "4e-400"}
        ledger = {"value": "1e-400", "baseline_value": "2e-400", "threshold": "3e-400", "nested": "4e-400"}
        self.save_raw_numeric(source, ledger)
        self.lint()
        for left, right in (("1", "1.0"), ("1.0", "1e0"), ("1e0", "1"),
                            ("0.123456789012345678901", "0.123456789012345678901"),
                            ("0.12345678901234567890123456789012345678901",
                             "0.123456789012345678901234567890123456789010")):
            with self.subTest(source=left, ledger=right):
                self.save_raw_numeric({key: left for key in source}, {key: right for key in ledger})
                self.lint()

    def test_numeric_exact_comparison_preserves_boolean_distinction(self):
        for source_key, ledger_key in (("method_value", "value"), ("baseline_value", "baseline_value")):
            with self.subTest(field=source_key):
                self.save_raw_numeric({source_key: "true"}, {ledger_key: "1.0"})
                self.lint("BINDING")
                self.save_raw_numeric({source_key: "1.0"}, {ledger_key: "true"})
                self.lint("SCHEMA")
        for source_token, ledger_token in (("true", "1e0"), ("1e0", "true")):
            with self.subTest(source=source_token, ledger=ledger_token):
                self.save_raw_numeric({"method_nested": source_token, "baseline_nested": source_token},
                                      {"nested": ledger_token})
                self.lint("BINDING")

    def test_numeric_overflow_and_nonfinite_tokens_remain_rejected(self):
        for token in ("1e999", "-1e999", "NaN", "Infinity", "-Infinity",
                      "1e-999999999999999999999999999999"):
            for location in ("source", "ledger"):
                with self.subTest(token=token, location=location):
                    self.save_raw_numeric({"method_value": token} if location == "source" else {},
                                          {"value": token} if location == "ledger" else {})
                    self.lint("SCHEMA")

    def test_numeric_decimal_schema_diagnostics_serialize_as_json(self):
        self.save_raw_numeric({"method_value": "1e-400"}, {"value": "1e-400", "locator": "0.125"})
        diagnostics = self.lint("SCHEMA")
        self.assertTrue(all(isinstance(item["message"], str) for item in diagnostics))

    def test_malformed_json_duplicate_keys_and_nonfinite_sources(self):
        for content in ("{", '{"a":1,"a":2}', '{"a":NaN}', '{"a":1e999}'):
            with self.subTest(content=content):
                self.write("metrics.json", content)
                self.evidence["sha256"] = self.digest("metrics.json")
                self.save()
                self.lint("SCHEMA")
        for content in ("{", '{"a":1,"a":2}', '{"a":NaN}', '{"a":1e999}'):
            with self.subTest(ledger=content):
                self.write("ledger.json", content)
                self.save(ledger=False)
                self.lint("SCHEMA")

    def test_non_utf8_manuscript_and_source(self):
        for path in ("draft.md", "metrics.json"):
            (self.root / path).write_bytes(b"\xff")
            target = self.claim["location"] if path == "draft.md" else self.evidence
            target["sha256"] = self.digest(path)
            self.save()
            self.lint("READ")

    def test_manuscript_exact_quote_preserves_crlf(self):
        (self.root / "draft.md").write_bytes(b"first\r\nsecond")
        self.claim["text"] = self.claim["location"]["exact_quote"] = "first\r\nsecond"
        self.claim["location"]["sha256"] = self.digest("draft.md")
        self.save()
        self.lint()
        self.claim["text"] = self.claim["location"]["exact_quote"] = "first\nsecond"
        self.save()
        self.lint("BINDING")

    def test_json_null_cannot_supply_numeric_measurement(self):
        self.write("metrics.json", "null")
        self.evidence["sha256"] = self.digest("metrics.json")
        self.save()
        self.lint("BINDING")

    def test_symlink_cannot_leave_research_root(self):
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "metrics.json"
            target.write_text(json.dumps(self.metrics), encoding="utf-8")
            (self.root / "escaped.json").symlink_to(target)
            self.evidence["artifact"] = "escaped.json"
            self.evidence["sha256"] = self.digest("escaped.json")
            self.save()
            self.lint("PATH")

    def test_cli_import_does_not_write_bytecode_without_b_flag(self):
        scripts = self.root / "scripts"
        scripts.mkdir()
        for name in ("lint_records.py", "evidence_ledger.py"):
            source = SCRIPT.parent / name
            if source.exists():
                (scripts / name).write_bytes(source.read_bytes())
        before = self.files()
        run = subprocess.run([sys.executable, str(scripts / "lint_records.py"), "--root", str(self.root),
                              "--task", "task.json", "--result", "result.json", "--review", "review.md"],
                             capture_output=True, text=True, timeout=10)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(before, self.files(), "CLI import created bytecode inside the research root.")

    def test_missing_and_unknown_nested_schema_fields(self):
        original = copy.deepcopy(self.ledger)
        selectors = [lambda: self.claim, lambda: self.claim["location"], lambda: self.claim["verification_request"],
                     lambda: self.evidence, lambda: self.evidence["context"], lambda: self.evidence["locator"]]
        for select in selectors:
            self.ledger = copy.deepcopy(original)
            for key in list(select()):
                with self.subTest(key=key):
                    self.ledger = copy.deepcopy(original)
                    del select()[key]
                    self.save()
                    self.lint("SCHEMA")
            self.ledger = copy.deepcopy(original)
            select()["approval"] = True
            self.save()
            self.lint("SCHEMA")

    def test_literature_unavailable_and_version_uncertain(self):
        for status in ("missing", "inaccessible", "version_uncertain"):
            with self.subTest(status=status):
                self.literature(status)
                self.review["claim_evidence"]["assessments"][0]["verdict"] = "unable_to_assess"
                self.save()
                self.lint()
        self.evidence.pop("reason")
        self.save()
        self.lint("SCHEMA")

    def test_literature_absent_hash_and_limitations_consistency(self):
        self.literature()
        original = copy.deepcopy(self.evidence)
        for field, value in (("sha256", "0" * 64), ("artifact", "missing.txt"), ("limitations", [])):
            with self.subTest(field=field):
                self.claim["evidence"][0] = copy.deepcopy(original)
                self.evidence[field] = value
                self.save()
                self.lint("SCHEMA")
        self.claim["evidence"][0] = copy.deepcopy(original)
        self.evidence["source"]["content_kind"] = "full_text"
        self.save()
        self.lint("SCHEMA")

    def test_literature_local_quote_hash_and_depth(self):
        self.literature("available")
        self.write("paper.txt", "The frozen source reports a limited effect.")
        self.evidence.update(artifact="paper.txt", sha256=self.digest("paper.txt"),
                             locator={"type": "quote", "value": "limited effect"})
        self.evidence["source"].update(content_kind="excerpt", reading_depth="excerpt")
        self.save()
        self.lint()
        self.evidence["locator"]["value"] = "universal effect"
        self.save()
        self.lint("BINDING")
        self.evidence["locator"]["value"] = "limited effect"
        self.evidence["source"]["reading_depth"] = "full_text"
        self.save()
        self.lint()
        self.evidence["source"]["access_limitations"] = []
        self.save()
        self.lint("SCHEMA")

    def test_partial_no_and_explicit_unreviewed_can_be_accepted(self):
        for verdict in ("partial", "no", "unable_to_assess"):
            self.review["claim_evidence"]["assessments"][0]["verdict"] = verdict
            self.save()
            self.lint()
        self.review["claim_evidence"].update(assessments=[], unreviewed_claim_ids=["C001"])
        self.save()
        self.lint()

    def test_review_partition_unknown_duplicate_missing_and_authority(self):
        block = copy.deepcopy(self.review["claim_evidence"])
        cases = [dict(assessments=[]), dict(unreviewed_claim_ids=["C001"]),
                 dict(unreviewed_claim_ids=["unknown"]), dict(unreviewed_claim_ids=["C001", "C001"]),
                 dict(approval=True)]
        for change in cases:
            with self.subTest(change=change):
                self.review["claim_evidence"] = {**copy.deepcopy(block), **change}
                self.save()
                self.lint("SCHEMA" if "approval" in change else "BINDING")
        self.review["claim_evidence"] = copy.deepcopy(block)
        self.review["claim_evidence"]["assessments"] *= 2
        self.save()
        self.lint("BINDING")

    def test_review_missing_block_or_wrong_ledger_binding(self):
        block = self.review.pop("claim_evidence")
        self.save()
        self.lint("BINDING")
        self.review["claim_evidence"] = block
        self.save()
        self.review["claim_evidence"]["ledger"]["sha256"] = "0" * 64
        self.write_review()
        self.lint("HASH")
        self.write("other.json", self.ledger)
        self.review["claim_evidence"]["ledger"] = {"path": "other.json", "sha256": self.digest("other.json")}
        self.write_review()
        self.lint("BINDING")

    def test_invalid_ledger_propagates_through_review_and_dependency(self):
        self.evidence["context"]["split"] = "wrong"
        self.save()
        dependent = {**copy.deepcopy(self.task), "task_id": "T2", "dependencies": [
            {"task_path": "task.json", "task_revision": 1, "result_path": "result.json",
             "result_sha256": self.digest("result.json"), "review_path": "review.md",
             "review_sha256": self.digest("review.md")} ]}
        del dependent["evidence_ledger"]
        self.write("dependent.json", dependent)
        diagnostics = self.lint("DEPENDENCY", ["--task", "dependent.json"])
        self.assertTrue(any(item["path"] == "review.md" and item["code"] == "BINDING" for item in diagnostics))


if __name__ == "__main__":
    unittest.main()
