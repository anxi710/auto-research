"""Frozen revision replays test change propagation, not agent performance."""

import hashlib
from decimal import Decimal
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/revision"
SCRIPTS = ROOT / "skills/research-workflow/scripts"
sys.path.insert(0, str(SCRIPTS))
import revision_loop


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


class RevisionLoopTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "revision"
        shutil.copytree(FIXTURES, self.root)

    def run_case(self, name="synthetic", candidate="full", output="attempts/A002"):
        return revision_loop.run_revision(self.root, name + "/case.json",
                                          name + "/" + candidate + ".json", output)

    def test_materials_feedback_and_rubrics_are_frozen(self):
        expected = read(FIXTURES / "frozen-sha256.json")
        actual = snapshot(FIXTURES)
        actual.pop("frozen-sha256.json")
        self.assertEqual(actual, expected)
        for name in ("synthetic", "public-source"):
            self.assertEqual(revision_loop.inspect_records(
                self.root, name + "/task.json", name + "/initial/result.json"), [])

    def test_full_revision_propagates_and_keeps_original_bytes(self):
        before = snapshot(self.root)
        report = self.run_case()
        self.assertEqual(report["affected_nodes"], ["A", "B", "ledger", "report"])
        self.assertEqual(report["stale_nodes"], [])
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        self.assertTrue(all(item["matches_frozen_finding"] and item["evidence_ids_match"]
                            for item in report["feedback_implementation"]))
        self.assertTrue(report["history_preserved"])
        self.assertTrue(all(item["preserved"] for item in report["prior_content_preservation"]))
        self.assertFalse(report["new_experiment_run"])
        for path, digest in before.items():
            self.assertEqual(snapshot(self.root)[path], digest)
        reused = {item["node_id"]: item["artifact"] for item in report["unaffected_content"]}
        self.assertEqual(set(reused), {"C", "source"})
        self.assertEqual(reused["source"]["path"], "synthetic/initial/source.json")
        result = read(self.root / report["result"]["path"])
        self.assertEqual((result["task_revision"], result["attempt_id"], result["execution_status"]),
                         (2, "A002", "completed"))
        self.assertEqual(report["independent_content_assessment"], "required_not_run")

    def test_local_fix_leaves_dependent_conclusions_stale(self):
        report = self.run_case(candidate="local-only", output="attempts/A003")
        self.assertEqual(report["revised_nodes"], ["A"])
        self.assertEqual(report["stale_nodes"], ["B", "ledger", "report"])
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        self.assertFalse(report["citation_support"]["ledger_current"])
        self.assertFalse(all(item["matches_frozen_finding"] for item in report["feedback_implementation"]))
        result = read(self.root / report["result"]["path"])
        self.assertEqual(result["execution_status"], "blocked")
        self.assertIn("synthetic/initial/report.md", [item["path"] for item in result["artifacts"]])
        self.assertTrue(report["history_preserved"])

    def test_changed_source_is_rejected_before_output_creation(self):
        (self.root / "synthetic/initial/source.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "HASH"):
            self.run_case()
        self.assertFalse((self.root / "attempts").exists())

    def test_damaged_numeric_support_remains_blocked(self):
        path = self.root / "synthetic/candidate/ledger.json"
        ledger = read(path)
        ledger["claims"][0]["evidence"][0]["value"] = 73
        revision_loop.write_json(path, ledger)
        candidate = read(self.root / "synthetic/full.json")
        candidate["replacements"]["ledger"] = revision_loop.file_ref(self.root, "synthetic/candidate/ledger.json")
        revision_loop.write_json(self.root / "synthetic/full.json", candidate)
        report = self.run_case()
        self.assertTrue(report["citation_support"]["record_diagnostics"])
        self.assertEqual(read(self.root / report["result"]["path"])["execution_status"], "blocked")

    def test_repin_preserves_exact_decimal_evidence_conditions(self):
        precise = Decimal("0.80000000000000004")
        source = read(self.root / "synthetic/initial/source.json")
        for measurement in (source["planner_p"], source["planner_q"]):
            measurement["conditions"]["temperature"] = precise
        revision_loop.write_json(self.root / "synthetic/initial/source.json", source)
        source_ref = revision_loop.file_ref(self.root, "synthetic/initial/source.json")
        for location in ("initial", "candidate"):
            path = self.root / "synthetic" / location / "ledger.json"
            ledger = read(path)
            for claim in ledger["claims"]:
                evidence = claim["evidence"][0]
                evidence["sha256"] = source_ref["sha256"]
                evidence["context"]["conditions"]["temperature"] = precise
            revision_loop.write_json(path, ledger)
        for path in ("synthetic/task.json", "synthetic/initial/task.json"):
            task = read(self.root / path)
            task["inputs"] = [source_ref]
            revision_loop.write_json(self.root / path, task)
        result_path = "synthetic/initial/result.json"
        result = read(self.root / result_path)
        result["task_sha256"] = revision_loop.file_ref(self.root, result["task_path"])["sha256"]
        for artifact in result["artifacts"]:
            artifact.update(revision_loop.file_ref(self.root, artifact["path"]))
        revision_loop.write_json(self.root / result_path, result)
        case = read(self.root / "synthetic/case.json")
        for key in ("initial_task", "initial_result"):
            case[key] = revision_loop.file_ref(self.root, case[key]["path"])
        for node in case["nodes"]:
            node["artifact"] = revision_loop.file_ref(self.root, node["artifact"]["path"])
        revision_loop.write_json(self.root / "synthetic/case.json", case)
        candidate = read(self.root / "synthetic/full.json")
        candidate["replacements"]["ledger"] = revision_loop.file_ref(self.root, "synthetic/candidate/ledger.json")
        revision_loop.write_json(self.root / "synthetic/full.json", candidate)
        report = self.run_case()
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        revised = revision_loop.read_json((self.root / "attempts/A002/artifacts/ledger.json").read_bytes())
        self.assertEqual(revised["claims"][0]["evidence"][0]["context"]["conditions"]["temperature"], precise)

    def test_feedback_can_match_while_prior_report_content_breaks(self):
        statement = read(self.root / "synthetic/rubric.json")["preserved_statements"][0]["text"]
        manuscript = self.root / "synthetic/candidate/report.md"
        manuscript.write_text(manuscript.read_text().replace(statement, ""), encoding="utf-8")
        ledger_path = self.root / "synthetic/candidate/ledger.json"
        ledger = read(ledger_path)
        for claim in ledger["claims"]:
            claim["location"]["sha256"] = revision_loop.file_ref(self.root, "synthetic/candidate/report.md")["sha256"]
        revision_loop.write_json(ledger_path, ledger)
        candidate = read(self.root / "synthetic/full.json")
        for key in ("report", "ledger"):
            candidate["replacements"][key] = revision_loop.file_ref(self.root, candidate["replacements"][key]["path"])
        revision_loop.write_json(self.root / "synthetic/full.json", candidate)
        report = self.run_case()
        self.assertTrue(all(item["matches_frozen_finding"] for item in report["feedback_implementation"]))
        self.assertFalse(report["prior_content_preservation"][0]["preserved"])
        self.assertEqual(read(self.root / report["result"]["path"])["execution_status"], "blocked")

    def test_unaffected_replacement_and_existing_output_are_rejected(self):
        candidate = read(self.root / "synthetic/full.json")
        candidate["replacements"]["C"] = revision_loop.file_ref(self.root, "synthetic/initial/C.md")
        revision_loop.write_json(self.root / "synthetic/extra.json", candidate)
        with self.assertRaisesRegex(ValueError, "affected nodes only"):
            self.run_case(candidate="extra")
        self.run_case()
        before = snapshot(self.root)
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.run_case()
        self.assertEqual(snapshot(self.root), before)

    def test_graph_requires_known_nodes_and_no_cycles(self):
        nodes = [{"id": "A", "depends_on": ["B"]}, {"id": "B", "depends_on": ["A"]}]
        with self.assertRaisesRegex(ValueError, "cycle"):
            revision_loop.affected_closure(nodes, ["A"])
        with self.assertRaisesRegex(ValueError, "unknown node"):
            revision_loop.affected_closure(nodes[:1], ["A"])
        with self.assertRaisesRegex(ValueError, "existing changed nodes"):
            revision_loop.affected_closure([{"id": "A", "depends_on": []}], ["Z"])

    def test_public_source_revision_preserves_version_and_reading_limits(self):
        report = self.run_case(name="public-source")
        self.assertEqual(report["stale_nodes"], [])
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        ledger = read(self.root / "attempts/A002/artifacts/ledger.json")
        for claim in ledger["claims"]:
            source = claim["evidence"][0]["source"]
            self.assertEqual((source["version"], source["reading_depth"], source["content_kind"]),
                             ("arXiv:2601.13217v1", "excerpt", "metadata"))
        self.assertEqual(report["independent_content_assessment"], "required_not_run")

    def test_structural_matches_do_not_establish_prose_support(self):
        manuscript = self.root / "synthetic/candidate/report.md"
        manuscript.write_text(manuscript.read_text() + "P is also proven best for every executor.\n", encoding="utf-8")
        ledger_path = self.root / "synthetic/candidate/ledger.json"
        ledger = read(ledger_path)
        for claim in ledger["claims"]:
            claim["location"]["sha256"] = revision_loop.file_ref(self.root, "synthetic/candidate/report.md")["sha256"]
        revision_loop.write_json(ledger_path, ledger)
        candidate = read(self.root / "synthetic/full.json")
        for key in ("report", "ledger"):
            candidate["replacements"][key] = revision_loop.file_ref(self.root, candidate["replacements"][key]["path"])
        revision_loop.write_json(self.root / "synthetic/full.json", candidate)
        report = self.run_case()
        self.assertEqual(report["citation_support"]["record_diagnostics"], [])
        self.assertTrue(all(item["matches_frozen_finding"] for item in report["feedback_implementation"]))
        self.assertEqual(report["independent_content_assessment"], "required_not_run")
        self.assertNotIn("accepted", report)

    def test_cli_reports_partial_and_unsafe_attempts(self):
        args = [sys.executable, "-B", str(SCRIPTS / "revision_loop.py"), "--root", str(self.root),
                "--case", "synthetic/case.json", "--candidate", "synthetic/local-only.json", "--output"]
        partial = subprocess.run(args + ["attempts/A003"], capture_output=True, text=True, timeout=10)
        self.assertEqual(partial.returncode, 1, partial.stdout + partial.stderr)
        self.assertEqual(json.loads(partial.stdout)["stale_nodes"], ["B", "ledger", "report"])
        unsafe = subprocess.run(args + ["../outside"], capture_output=True, text=True, timeout=10)
        self.assertEqual(unsafe.returncode, 2)
        self.assertIn("PATH", json.loads(unsafe.stdout)["error"])


if __name__ == "__main__":
    unittest.main()
