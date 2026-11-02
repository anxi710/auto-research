"""Development regressions for retained meaning across two fixed revision rounds."""

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/revision-retention"
SCRIPTS = ROOT / "skills/research-workflow/scripts"
sys.path.insert(0, str(SCRIPTS))
import revision_loop


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


def bind_second_round(root, first_report):
    """Bind the frozen graph to the actual first result, including its revision."""
    case = read(root / "round2/case-template.json")
    result = read(root / first_report["result"]["path"])
    current_task = str(Path(first_report["result"]["path"]).parent / "current-task.json")
    case["initial_task"] = revision_loop.file_ref(root, current_task)
    case["initial_result"] = first_report["result"]
    artifacts = {Path(item["path"]).stem: {key: item[key] for key in ("path", "sha256")}
                 for item in result["artifacts"]}
    for node in case["nodes"]:
        actual = artifacts[node["id"]]
        if node["artifact"] is not None and node["artifact"] != actual:
            raise ValueError("An unchanged node differs from the frozen second-round source.")
        node["artifact"] = actual
    path = "round2-bound-case.json"
    revision_loop.write_json(root / path, case)
    return path


class RevisionRetentionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "retention"
        shutil.copytree(FIXTURE, self.root)

    def first_round(self):
        report = revision_loop.run_revision(self.root, "round1/case.json",
                                            "round1/full.json", "runs/R1")
        return report, bind_second_round(self.root, report)

    def second_round(self, case, candidate, output=None):
        return revision_loop.run_revision(self.root, case, "round2/" + candidate + ".json",
                                          output or "runs/" + candidate)

    def status(self, report):
        return read(self.root / report["result"]["path"])["execution_status"]

    def prose_probe(self, name, appended_text):
        candidate = read(self.root / "round2/full.json")
        directory = self.root / name
        directory.mkdir()
        report_path = name + "/report.md"
        original_report = self.root / candidate["replacements"]["report"]["path"]
        (self.root / report_path).write_text(original_report.read_text() + "\n" + appended_text + "\n")
        ledger = read(self.root / candidate["replacements"]["ledger"]["path"])
        for claim in ledger["claims"]:
            claim["location"].update(artifact=report_path,
                                     sha256=revision_loop.file_ref(self.root, report_path)["sha256"])
        ledger_path = name + "/ledger.json"
        revision_loop.write_json(self.root / ledger_path, ledger)
        candidate["replacements"]["report"] = revision_loop.file_ref(self.root, report_path)
        candidate["replacements"]["ledger"] = revision_loop.file_ref(self.root, ledger_path)
        candidate_path = name + "/candidate.json"
        revision_loop.write_json(self.root / candidate_path, candidate)
        return candidate_path

    def test_new_development_material_is_frozen(self):
        expected = read(FIXTURE / "frozen-sha256.json")
        actual = snapshot(FIXTURE)
        actual.pop("frozen-sha256.json")
        self.assertEqual(actual, expected)
        self.assertEqual((FIXTURE / "evidence/source.json").read_bytes(),
                         (ROOT / "tests/revision/synthetic/initial/source.json").read_bytes())

    def test_two_rounds_pin_actual_prior_result_and_allow_equivalent_retained_text(self):
        before = snapshot(self.root)
        first, case_path = self.first_round()
        first_before_second = snapshot(self.root / "runs/R1")
        second = self.second_round(case_path, "full")
        first_result = read(self.root / first["result"]["path"])
        second_result = read(self.root / second["result"]["path"])
        self.assertEqual((first_result["task_revision"], second_result["task_revision"]), (2, 3))
        self.assertEqual(read(self.root / case_path)["initial_result"], first["result"])
        self.assertEqual(self.status(first), "completed")
        self.assertEqual(self.status(second), "completed")
        self.assertTrue(all(item["preserved"] for item in second["prior_content_preservation"]))
        self.assertTrue(any(item["matched_text"] != item["text"]
                            for item in second["prior_content_preservation"]))
        self.assertTrue(all(item["withdrawn"] for item in first["withdrawn_conclusions"]))
        self.assertTrue(first["history_preserved"] and second["history_preserved"])
        self.assertEqual(snapshot(self.root / "runs/R1"), first_before_second)
        for path, digest in before.items():
            self.assertEqual(snapshot(self.root)[path], digest)
        plan = read(self.root / second["revision_plan"]["path"])
        self.assertEqual(plan["affected_nodes"], ["A", "B", "ledger", "report"])
        self.assertTrue(plan["preserved_statements"])
        self.assertTrue(all(item["present_before"] for item in plan["preserved_statements"]))
        self.assertTrue(all(item["reason"] and item["evidence"] for item in plan["withdrawn_statements"]))

    def test_latest_request_does_not_hide_reintroduced_withdrawn_conclusion(self):
        _, case = self.first_round()
        report = self.second_round(case, "reintroduced-ranking")
        self.assertTrue(all(item["matches_frozen_finding"] and item["evidence_ids_match"]
                            for item in report["feedback_implementation"]))
        self.assertTrue(all(item["preserved"] for item in report["prior_content_preservation"]))
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        self.assertFalse(all(item["withdrawn"] for item in report["withdrawn_conclusions"]))
        self.assertEqual(self.status(report), "blocked")

    def test_deleted_counterevidence_and_qualifier_fail_separate_retention_check(self):
        _, case = self.first_round()
        for candidate in ("deleted-counterevidence", "deleted-qualifier"):
            with self.subTest(candidate=candidate):
                report = self.second_round(case, candidate)
                self.assertTrue(all(item["matches_frozen_finding"] for item in report["feedback_implementation"]))
                self.assertFalse(all(item["preserved"] for item in report["prior_content_preservation"]))
                self.assertEqual(self.status(report), "blocked")

    def test_broken_evidence_and_local_only_change_remain_blocked(self):
        _, case = self.first_round()
        for candidate in ("broken-numeric", "broken-citation"):
            with self.subTest(candidate=candidate):
                broken = self.second_round(case, candidate)
                self.assertTrue(broken["citation_support"]["record_diagnostics"])
                self.assertEqual(self.status(broken), "blocked")
        local = self.second_round(case, "local-only")
        self.assertEqual(local["stale_nodes"], ["B", "ledger", "report"])
        self.assertEqual(self.status(local), "blocked")
        self.assertTrue(local["history_preserved"])

    def test_all_controls_use_the_same_frozen_second_round_rubric(self):
        _, case = self.first_round()
        expected = read(self.root / "round2/case-template.json")["rubric"]
        self.assertEqual(read(self.root / case)["rubric"], expected)
        for candidate in ("full", "reintroduced-ranking", "deleted-counterevidence", "deleted-qualifier",
                          "broken-numeric", "broken-citation", "local-only"):
            report = self.second_round(case, candidate)
            plan = read(self.root / report["revision_plan"]["path"])
            self.assertEqual(plan["rubric"], expected)
            self.assertEqual(report["independent_content_assessment"], "required_not_run")
            self.assertNotIn("scientific_approval", report)

    def test_unknown_paraphrase_still_needs_independent_content_review(self):
        _, case = self.first_round()
        candidate = self.prose_probe("paraphrase-probe", "P produces superior plans with every possible executor.")
        report = revision_loop.run_revision(self.root, case, candidate, "runs/paraphrase-probe")
        self.assertEqual(self.status(report), "completed")
        self.assertTrue(all(item["withdrawn"] for item in report["withdrawn_conclusions"]))
        self.assertEqual(report["independent_content_assessment"], "required_not_run")
        self.assertNotIn("scientific_approval", report)

    def test_historical_quote_exposes_the_exact_text_guard_false_positive(self):
        _, case = self.first_round()
        candidate = self.prose_probe("quotation-probe", 'The earlier draft incorrectly stated: '
                                    '"P has better plan quality than Q for every executor." That claim is withdrawn.')
        report = revision_loop.run_revision(self.root, case, candidate, "runs/quotation-probe")
        self.assertEqual(self.status(report), "blocked")
        self.assertFalse(all(item["withdrawn"] for item in report["withdrawn_conclusions"]))
        self.assertIn("historical quotation", report["retention_scope"])
        self.assertEqual(report["independent_content_assessment"], "required_not_run")


if __name__ == "__main__":
    unittest.main()
