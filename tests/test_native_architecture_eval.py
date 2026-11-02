"""These tests use dummy bytes. They are not model evaluation results."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "evaluations/native-architecture/run.py"
SPEC = importlib.util.spec_from_file_location("native_eval", SCRIPT)
RUN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUN)


class NativeRecordTests(unittest.TestCase):
    def test_frozen_inputs_and_unknown_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "frozen").mkdir()
            (root / "runs").mkdir()
            prompt = root / "frozen/prompt.md"
            prompt.write_text("dummy test prompt")
            RUN.save(root / "frozen/plan.json", {"call_limit": 1, "calls": [
                {"id": "test", "role": "unit-test-only", "prompt": "frozen/prompt.md", "charged_to": ["merge", "synthesis_revision"]}
            ]})
            RUN.freeze(root)
            self.assertFalse(RUN.summarize(root)["arms"]["merge"]["all_calls_completed"])
            RUN.start(root, "test")
            self.assertEqual(RUN.summarize(root)["unique_native_calls"], 0)
            RUN.dispatched(root, "test", "unit-test-only")
            self.assertEqual(RUN.summarize(root)["unique_native_calls"], 1)
            with self.assertRaises(ValueError):
                RUN.start(root, "test")
            (root / "runs/test/output.md").write_text("dummy unit test bytes")
            RUN.finish(root, "test", "unit-test-only")
            result = RUN.summarize(root)
            self.assertIsNone(result["tokens"])
            self.assertEqual(result["arms"]["merge"]["native_calls"], 1)
            self.assertEqual(result["arms"]["synthesis_revision"]["native_calls"], 1)
            prompt.write_text("changed")
            with self.assertRaises(ValueError):
                RUN.verify(root)

    def test_literal_package_keeps_worker_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "frozen").mkdir()
            (root / "runs").mkdir()
            (root / "frozen/prompt.md").write_text("dummy unit test prompt")
            names = ("single", "quality", "operations", "revision")
            RUN.save(root / "frozen/plan.json", {"call_limit": 4, "calls": [
                {"id": f"r1-{name}", "role": "unit-test-only", "prompt": "frozen/prompt.md", "charged_to": []}
                for name in names
            ], "candidate_map": {"r1": {"A": "revision", "B": "single", "C": "merge"}}})
            RUN.freeze(root)
            for name in names:
                RUN.start(root, f"r1-{name}")
                (root / "runs" / f"r1-{name}" / "output.md").write_bytes(f"dummy {name}\n".encode())
                RUN.finish(root, f"r1-{name}", "unit-test-only")
            RUN.package(root, 1)
            merged = (root / "runs/r1-merge.md").read_bytes()
            self.assertEqual(merged, b"# Quality worker\n\ndummy quality\n\n\n# Operations worker\n\ndummy operations\n")
            self.assertEqual((root / "runs/r1-candidate-c.md").read_bytes(), merged)
            with self.assertRaises(FileExistsError):
                RUN.package(root, 1)


if __name__ == "__main__":
    unittest.main()
