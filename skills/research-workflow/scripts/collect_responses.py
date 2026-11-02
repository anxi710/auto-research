#!/usr/bin/env python3
"""Save literal worker responses with fixed versions and explicit collection gaps."""

import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from collection_artifacts import collect
from lint_records import Linter, valid_id


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--task", required=True, help="Current collection contract, relative to root.")
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--output", required=True, help="New aggregate file, relative to root.")
    args = parser.parse_args()
    try:
        root = Path(args.root).resolve()
        if not root.is_dir() or not valid_id(args.attempt_id):
            parser.error("Use an existing root and a valid attempt ID.")
    except (OSError, RuntimeError, ValueError):
        parser.error("Cannot access --root.")
    lint = Linter(root)
    output = lint.path(args.output, ".", required=False)
    if output is None:
        print(json.dumps(lint.output(), indent=2))
        return 1
    aggregate, diagnostics = collect(root, args.task, args.attempt_id)
    if diagnostics:
        print(json.dumps({"diagnostics": diagnostics}, indent=2))
        return 1
    lint.reference(aggregate["contract"]["path"], ".", kind="task", current=True)
    lint.load()
    task = lint.records["task"][aggregate["contract"]["path"]]
    allowed = [lint.path(value, ".", required=False) for value in task["write_paths"]]
    if not any(value is not None and Path(output).is_relative_to(Path(value)) for value in allowed):
        lint.issue("PATH", ".", "Aggregate output is outside the collection task's write_paths.")
        print(json.dumps(lint.output(), indent=2))
        return 1
    try:
        # Exclusive creation preserves submitted attempts and existing evidence.
        with (root / output).open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n")
    except OSError as error:
        print(json.dumps({"diagnostics": [{"code": "WRITE", "path": output,
                                           "message": f"Cannot create new aggregate ({type(error).__name__})."}]}))
        return 1
    print(json.dumps({"artifact": output, "coverage": aggregate["coverage"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
