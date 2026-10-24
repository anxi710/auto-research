"""Compare two summation methods for three distinct binary float inputs."""

import argparse
from fractions import Fraction
from itertools import permutations
import json
import math
from pathlib import Path
import sys


def rational(value):
    return {"numerator": value.numerator, "denominator": value.denominator}


def evaluate(data):
    """Return exact errors for every input order without writing files."""
    if not isinstance(data, dict) or set(data) != {"protocol_version", "cases"}:
        raise ValueError("Input must contain only protocol_version and cases.")
    if data["protocol_version"] != "1":
        raise ValueError('Set protocol_version to the string "1".')
    if not isinstance(data["cases"], list) or not data["cases"]:
        raise ValueError("Provide a nonempty list of cases.")

    cases = []
    ids = set()
    for case in data["cases"]:
        if not isinstance(case, dict) or set(case) != {"id", "values"}:
            raise ValueError("Each case must contain only id and values.")
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip() or case_id in ids:
            raise ValueError("Give each case a unique, nonempty string id.")
        ids.add(case_id)
        values = case["values"]
        if not isinstance(values, list) or len(values) != 3:
            raise ValueError(f"Case {case_id!r} must contain three values.")
        if any(type(value) not in (int, float) for value in values):
            raise ValueError(f"Case {case_id!r} must contain numbers without booleans.")
        try:
            values = [float(value) for value in values]
        except OverflowError as error:
            raise ValueError(f"Case {case_id!r} contains a number outside the float range.") from error
        if not all(math.isfinite(value) for value in values):
            raise ValueError(f"Case {case_id!r} must contain finite numbers.")
        if len(set(values)) != 3:
            raise ValueError(f"Case {case_id!r} must contain three distinct float values.")
        cases.append((case_id, values))

    rows = []
    for case_id, values in cases:
        reference = sum((Fraction.from_float(value) for value in values), Fraction())
        for order_index, order in enumerate(permutations(values), 1):
            naive = 0.0
            for value in order:
                naive += value
            try:
                accurate = math.fsum(order)
            except OverflowError as error:
                raise ValueError(f"Case {case_id!r} overflowed during summation. Use smaller values.") from error
            methods = {}
            for name, value in (("naive", naive), ("fsum", accurate)):
                if not math.isfinite(value):
                    raise ValueError(f"Case {case_id!r} produced a nonfinite sum. Use smaller values.")
                methods[name] = {
                    "value_hex": value.hex(),
                    "absolute_error": rational(abs(Fraction.from_float(value) - reference)),
                }
            rows.append({
                "case_id": case_id,
                "order_index": order_index,
                "input_hex": [value.hex() for value in order],
                "reference": rational(reference),
                "methods": methods,
            })
    return {"protocol_version": "1", "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs_json", type=Path)
    args = parser.parse_args()
    try:
        with args.inputs_json.open(encoding="utf-8") as source:
            data = json.load(source)
        result = evaluate(data)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Cannot evaluate inputs: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
