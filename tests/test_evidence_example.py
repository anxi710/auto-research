"""Replay the synthetic fixture without changing submitted records or judgments."""

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/claim-evidence"
ATTEMPT = "tasks/T001/attempts/A001"
ARTIFACTS = ATTEMPT + "/artifacts"
SEALED_HASHES = {
    "BRIEF.md": "e2e5f6659f111933aacbcd732236b0c9f23c904eb3ce3031b3decd1cafd97e87",
    "reviews/R001.md": "c668b8e648131f791f43d96e36a9f71497c4af3241c9eba95e7a78aa90289d5e",
    ARTIFACTS + "/draft.md": "73565f53227681fac88d79fdf4be381d86f49e06bdfaee92986780874ec17ce8",
    ARTIFACTS + "/evidence-ledger.json": "5f72d26f69d8bc4b52b1178560b21fd3fedae53b6ca696c074ac7be04b508993",
    ARTIFACTS + "/metrics.json": "46f590091043e904a5dcf6e185ba61016fcea3ff89101ef6d2deaeb9331442d1",
    ATTEMPT + "/result.json": "91c1043f0722d7404539dc53102a265ab38f0b2330030cc8d3aa1dcb6d12c40d",
    ATTEMPT + "/task.json": "d8c3b8f3309e16a30257edce337d6b58397ad122c37bccce233f539079f4956b",
}


def snapshot(root):
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*") if path.is_file()}


def read_json(path):
    return json.loads((EXAMPLE / path).read_text(encoding="utf-8"), parse_float=Decimal)


def review_record():
    content = (EXAMPLE / "reviews/R001.md").read_text(encoding="utf-8")
    return json.loads(content.split("## Task acceptance\n\n```json\n", 1)[1].split("\n```", 1)[0])


class EvidenceExampleTests(unittest.TestCase):
    def test_submitted_versions_and_current_contract_stay_fixed(self):
        actual = snapshot(EXAMPLE)
        for path, expected in SEALED_HASHES.items():
            with self.subTest(path=path):
                self.assertEqual(actual[path], expected)
        self.assertEqual((EXAMPLE / "tasks/T001/task.json").read_bytes(),
                         (EXAMPLE / ATTEMPT / "task.json").read_bytes())
        result = read_json(ATTEMPT + "/result.json")
        ledger_path = ARTIFACTS + "/evidence-ledger.json"
        self.assertEqual(read_json("tasks/T001/task.json")["evidence_ledger"], ledger_path)
        self.assertEqual([item["path"] for item in result["artifacts"]
                          if item.get("kind") == "claim_evidence_ledger"], [ledger_path])

    def test_clean_temporary_replay_is_read_only(self):
        original = snapshot(EXAMPLE)
        with tempfile.TemporaryDirectory() as temporary:
            copied = Path(temporary) / "example copy"
            shutil.copytree(EXAMPLE, copied)
            before = snapshot(copied)
            replay = subprocess.run(
                [sys.executable, "-B", str(ROOT / "skills/research-workflow/scripts/lint_records.py"),
                 "--root", str(copied), "--task", "tasks/T001/task.json",
                 "--result", ATTEMPT + "/result.json", "--review", "reviews/R001.md"],
                cwd=temporary, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(replay.returncode, 0, replay.stdout + replay.stderr)
            self.assertEqual(json.loads(replay.stdout), {"diagnostics": []})
            self.assertEqual(replay.stderr, "")
            self.assertEqual(snapshot(copied), before)
        self.assertEqual(snapshot(EXAMPLE), original)

    def test_limited_support_and_inaccessible_content_are_preserved(self):
        metrics = read_json(ARTIFACTS + "/metrics.json")
        method, baseline = metrics["runs"][0], metrics["baselines"][0]
        self.assertEqual((method["dataset"], method["split"]), ("synthetic-D1", "test-v1"))
        self.assertEqual((method["method"], method["baseline"], baseline["method"]), ("A", "B", "B"))
        for key in ("dataset", "split", "unit", "conditions"):
            self.assertEqual(method[key], baseline[key])
        self.assertEqual(method["value"], Decimal("0.62"))
        self.assertEqual(baseline["value"], Decimal("0.60"))
        self.assertEqual(method["value"] - baseline["value"], Decimal("0.02"))
        self.assertLess(method["value"] - baseline["value"], Decimal("0.05"))
        self.assertEqual((len(metrics["runs"]), len(metrics["baselines"])), (1, 1))

        ledger = read_json(ARTIFACTS + "/evidence-ledger.json")
        claims = {claim["claim_id"]: claim for claim in ledger["claims"]}
        manuscript = (EXAMPLE / ARTIFACTS / "draft.md").read_text(encoding="utf-8")
        for claim in claims.values():
            self.assertEqual(manuscript.count(claim["text"]), 1)
            self.assertEqual(claim["location"]["exact_quote"], claim["text"])
            self.assertNotIn("verdict", claim)
        literature = claims["C004"]["evidence"][0]
        self.assertEqual(literature["availability"], "inaccessible")
        self.assertIsNone(literature["artifact"])
        self.assertIsNone(literature["sha256"])
        self.assertEqual(literature["source"]["content_kind"], "none")
        self.assertEqual(literature["source"]["reading_depth"], "metadata")
        self.assertTrue(literature["source"]["access_limitations"])

        review = review_record()
        assessments = review["claim_evidence"]["assessments"]
        self.assertEqual({entry["claim_id"]: entry["verdict"] for entry in assessments},
                         {"C001": "yes", "C002": "partial", "C003": "no", "C004": "unable_to_assess"})
        self.assertEqual(review["claim_evidence"]["unreviewed_claim_ids"], [])
        self.assertEqual(len(assessments), len(claims))
        self.assertEqual(review["decision"], "accepted")
        self.assertEqual(review["reviewer"], read_json("tasks/T001/task.json")["owner"])
        prose = (EXAMPLE / "reviews/R001.md").read_text(encoding="utf-8")
        self.assertIn("Decision status: Pending.", prose)
        self.assertIn("Researcher and decision source: Not recorded.", prose)
        self.assertIn("Approved next actions and limits: None.", prose)
        self.assertIn("Review waiver: Not granted.", prose)


if __name__ == "__main__":
    unittest.main()
