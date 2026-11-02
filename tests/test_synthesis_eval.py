"""Keep finite relation checks separate from an independent prose assessment."""

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/synthesis"
SCRIPTS = ROOT / "skills/research-workflow/scripts"
sys.path.insert(0, str(SCRIPTS))
from synthesis_eval import evaluate, facts, read_json


class SynthesisEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "case"
        shutil.copytree(FIXTURE, self.root)

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding="utf-8"))

    def reference(self, name):
        return {"path": name, "sha256": hashlib.sha256((self.root / name).read_bytes()).hexdigest()}

    def refresh(self):
        artifact = self.read("synthesis-artifact.json")
        artifact.update(aggregate=self.reference("literal-aggregate.json"),
                        manuscript=self.reference("synthesis.md"),
                        evidence_ledger=self.reference("synthesis-ledger.json"))
        self.write("synthesis-artifact.json", artifact)
        task = self.read("T_SYNTH/task.json")
        task["inputs"] = [self.reference("literal-aggregate.json")]
        self.write("T_SYNTH/task.json", task)
        self.write("T_SYNTH/snapshot.json", task)
        result = self.read("T_SYNTH/result.json")
        result["task_sha256"] = self.reference("T_SYNTH/snapshot.json")["sha256"]
        for item in result["artifacts"]:
            item["sha256"] = self.reference(item["path"])["sha256"]
        self.write("T_SYNTH/result.json", result)
        candidate = self.read("synthesis.json")
        candidate.update(artifact=self.reference("synthesis-artifact.json"),
                         task=self.reference("T_SYNTH/task.json"), result=self.reference("T_SYNTH/result.json"))
        self.write("synthesis.json", candidate)

    def test_frozen_inputs_and_outputs(self):
        frozen = self.read("frozen.json")["sha256"]
        for name, expected in frozen.items():
            with self.subTest(name=name):
                self.assertEqual(self.reference(name)["sha256"], expected)

    def test_reviewed_snapshot_and_binding_correction_keep_scientific_material_fixed(self):
        original = self.read("history/reviewed-v1/frozen.json")["sha256"]
        correction = self.read("history/technical-binding-correction.json")
        self.assertFalse(correction["criteria_changed"])
        self.assertFalse(correction["scientific_material_changed"])
        for name, expected in original.items():
            self.assertEqual(self.reference("history/reviewed-v1/" + name)["sha256"], expected)
        for name, expected in correction["unchanged"].items():
            self.assertEqual(self.reference(name)["sha256"], expected)
        before = self.read("history/reviewed-v1/literal-aggregate.json")
        after = self.read("literal-aggregate.json")
        self.assertEqual([row["content"] for row in before["branches"]],
                         [row["content"] for row in after["branches"]])

    def test_actual_consumer_runs_before_four_separate_relation_reports(self):
        for candidate in ("literal", "polished", "synthesis"):
            with self.subTest(candidate=candidate):
                run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "synthesis_eval.py"),
                                      "--root", str(self.root), "--case", "case.json",
                                      "--candidate", candidate + ".json"], capture_output=True,
                                     text=True, timeout=10)
                self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
                report = json.loads(run.stdout)
                self.assertEqual(set(report["dimensions"]), {
                    "source_quality", "claim_support", "cross_branch_inference", "question_coverage"})
                checks = [item for rows in report["dimensions"].values() for item in rows]
                self.assertEqual(sum(item["matched"] for item in checks), 13 if candidate == "synthesis" else 0)
                self.assertNotIn("score", report)
                self.assertNotIn("accepted", report)
                self.assertEqual(report["annotation_scope"], "declared_findings_only")
                self.assertEqual(report["independent_content_assessment"], "required_not_run_by_this_script")

    def test_wrong_arithmetic_and_boolean_numeric_substitution_fail(self):
        for incorrect in (1, False):
            with self.subTest(incorrect=incorrect):
                candidate = self.read("synthesis.json")
                finding = next(row for row in candidate["findings"] if row["finding_id"] == "utility")
                finding["facts"]["delta"] = incorrect
                self.write("synthesis.json", candidate)
                report = evaluate(self.root, "case.json", "synthesis.json")
                self.assertFalse(report["dimensions"]["cross_branch_inference"][0]["matched"])

    def test_changed_conditions_do_not_become_a_dispute(self):
        sources = read_json(self.root / "sources.json")
        with self.assertRaisesRegex(ValueError, "matching conditions"):
            facts({"kind": "dispute", "source_ids": ["A1", "A2"]}, sources)
        sources["B1"]["conditions"]["budget"] = True
        with self.assertRaisesRegex(ValueError, "matching conditions"):
            facts({"kind": "weighted_difference", "source_ids": ["A1", "B1"], "cost_weight": 0}, sources)

    def test_changed_source_bytes_invalidate_the_run(self):
        with (self.root / "sources.json").open("a") as stream:
            stream.write("\n")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            evaluate(self.root, "case.json", "synthesis.json")

    def test_hidden_aggregate_coverage_fails_actual_consumer(self):
        aggregate = self.read("literal-aggregate.json")
        aggregate["coverage"] = {"expected": ["A"], "collected": ["A"], "gaps": []}
        self.write("literal-aggregate.json", aggregate)
        self.refresh()
        with self.assertRaisesRegex(ValueError, "coverage"):
            evaluate(self.root, "case.json", "synthesis.json")

    def test_wrong_citation_location_is_not_supported_by_matching_source_ids(self):
        ledger = self.read("synthesis-ledger.json")
        ledger["claims"][0]["evidence"][0]["locator"]["value"] = "A1"
        self.write("synthesis-ledger.json", ledger)
        self.refresh()
        with self.assertRaisesRegex(ValueError, "citation differs"):
            evaluate(self.root, "case.json", "synthesis.json")

    def test_matching_findings_do_not_prove_the_prose_is_true(self):
        # This adversarial control records the need for an independent reader.
        ledger = self.read("synthesis-ledger.json")
        claim = ledger["claims"][8]
        old = claim["text"]
        claim["text"] = "M is always better than N for all users. [A1, B1]"
        manuscript = (self.root / "synthesis.md").read_text().replace(old, claim["text"])
        (self.root / "synthesis.md").write_text(manuscript)
        for item in ledger["claims"]:
            item["location"]["sha256"] = self.reference("synthesis.md")["sha256"]
            item["location"]["exact_quote"] = item["text"]
        self.write("synthesis-ledger.json", ledger)
        self.refresh()
        report = evaluate(self.root, "case.json", "synthesis.json")
        self.assertTrue(all(row["matched"] for rows in report["dimensions"].values() for row in rows))
        self.assertEqual(report["independent_content_assessment"], "required_not_run_by_this_script")
        self.assertNotIn("scientific_verdict", report)

    def test_unlisted_candidate_and_duplicate_findings_are_rejected(self):
        candidate = self.read("synthesis.json")
        candidate["artifact"] = self.reference("polished-artifact.json")
        self.write("synthesis.json", candidate)
        with self.assertRaisesRegex(ValueError, "absent from its fixed result"):
            evaluate(self.root, "case.json", "synthesis.json")
        candidate["artifact"] = self.reference("synthesis-artifact.json")
        candidate["findings"].append(copy.deepcopy(candidate["findings"][0]))
        self.write("synthesis.json", candidate)
        with self.assertRaisesRegex(ValueError, "repeats a finding"):
            evaluate(self.root, "case.json", "synthesis.json")


if __name__ == "__main__":
    unittest.main()
