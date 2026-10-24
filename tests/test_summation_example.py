"""Check the synthetic example without replacing its saved experiment outputs."""

import copy
from fractions import Fraction
import hashlib
from itertools import permutations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/summation-order"
ARTIFACTS = EXAMPLE / "tasks/T001/attempts/A001/artifacts"
EXPERIMENT = types.ModuleType("summation_example")
SCRIPT = ARTIFACTS / "run.py"
# Keep bytecode caches out of the sealed attempt, including under other test runners.
exec(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec"), EXPERIMENT.__dict__)


class SummationExampleTests(unittest.TestCase):
    def test_binary_reference_and_all_input_orders(self):
        values = [0.1, 0.2, 0.3]
        data = {"protocol_version": "1", "cases": [{"id": "decimal-control", "values": values}]}
        before = copy.deepcopy(data)
        rows = EXPERIMENT.evaluate(data)["rows"]
        self.assertEqual(data, before)
        self.assertEqual(len(rows), 6)
        self.assertEqual({tuple(row["input_hex"]) for row in rows},
                         {tuple(value.hex() for value in order) for order in permutations(values)})
        reference = Fraction(0.1) + Fraction(0.2) + Fraction(0.3)
        self.assertNotEqual(reference, Fraction(3, 5), "The reference must use actual binary inputs.")
        for row in rows:
            self.assertEqual(Fraction(**row["reference"]), reference)
            self.assertEqual(set(row["methods"]), {"naive", "fsum"})
            for output in row["methods"].values():
                exact_output = Fraction(float.fromhex(output["value_hex"]))
                self.assertEqual(Fraction(**output["absolute_error"]), abs(exact_output - reference))

    def test_invalid_input_fails_before_output(self):
        valid = {"protocol_version": "1", "cases": [{"id": "small", "values": [0.25, 0.5, 0.75]}]}
        invalid = [None, {**valid, "protocol_version": "2"}, {**valid, "cases": []}]
        for values in ([True, 0.5, 0.75], [float("nan"), 0.5, 0.75], [float("inf"), 0.5, 0.75],
                       [0.25, 0.25, 0.75], [0.25, 0.5], ["0.25", 0.5, 0.75]):
            invalid.append({**valid, "cases": [{"id": "small", "values": values}]})
        invalid.append({**valid, "cases": valid["cases"] * 2})
        for data in invalid:
            with self.subTest(data=data), self.assertRaises(ValueError):
                EXPERIMENT.evaluate(data)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.json"
            path.write_text('{"protocol_version":"1","cases":[]}', encoding="utf-8")
            result = subprocess.run([sys.executable, "-B", str(ARTIFACTS / "run.py"), str(path)],
                                    capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("nonempty list", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_saved_result_and_review_remain_bound(self):
        before = {str(p.relative_to(EXAMPLE)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in EXAMPLE.rglob("*") if p.is_file()}
        loaded = subprocess.run(
            [sys.executable, "-c", "import runpy, sys\nrunpy.run_path(sys.argv[1], run_name='loader_probe')", __file__],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(loaded.returncode, 0, loaded.stdout + loaded.stderr)
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "skills/research-workflow/scripts/lint_records.py"),
             "--root", str(EXAMPLE), "--task", "tasks/T001/task.json",
             "--result", "tasks/T001/attempts/A001/result.json", "--review", "reviews/R001.md"],
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {"diagnostics": []})
        after = {str(p.relative_to(EXAMPLE)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in EXAMPLE.rglob("*") if p.is_file()}
        self.assertEqual(after, before)
        rows = json.loads((ARTIFACTS / "results.json").read_text())["rows"]
        self.assertEqual(len(rows), 12)
        self.assertEqual({(row["case_id"], row["order_index"]) for row in rows},
                         {(case, index) for case in ("control", "cancellation") for index in range(1, 7)})
        ties = 0
        for row in rows:
            self.assertEqual(set(row["methods"]), {"naive", "fsum"})
            errors = [Fraction(**entry["absolute_error"]) for entry in row["methods"].values()]
            ties += errors[0] == errors[1]
        self.assertEqual(ties, 8, "Keep the stored ties as part of the reported result.")


if __name__ == "__main__":
    unittest.main()
