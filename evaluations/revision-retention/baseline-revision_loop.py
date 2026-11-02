#!/usr/bin/env python3
"""Replay a frozen revision candidate in a new attempt without changing its inputs."""

import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from evidence_ledger import finite_decimal
from lint_records import Linter, cycle_members, finite_number, unique_object, valid_id


def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=finite_number, parse_float=finite_decimal)


def affected_closure(nodes, changed_ids):
    """Return changed nodes and every node that depends on them."""
    edges = {node["id"]: set(node["depends_on"]) for node in nodes}
    if len(edges) != len(nodes) or any(not valid_id(key) for key in edges):
        raise ValueError("Node IDs must be unique identifiers.")
    if any(not targets <= edges.keys() for targets in edges.values()):
        raise ValueError("A dependency names an unknown node.")
    if cycle_members(edges):
        raise ValueError("Artifact dependencies contain a cycle.")
    affected = set(changed_ids)
    if not affected or not affected <= edges.keys():
        raise ValueError("Feedback must name existing changed nodes.")
    while True:
        extended = affected | {key for key, targets in edges.items() if targets & affected}
        if extended == affected:
            return sorted(affected)
        affected = extended


def reference(root, value):
    lint = Linter(root)
    path = lint.reference(value["path"], ".", value["sha256"])
    if lint.diagnostics:
        raise ValueError(json.dumps(lint.output()))
    return (root / path).read_bytes()


def file_ref(root, path):
    return {"path": path, "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest()}


def write_json(path, value):
    def encode(item):
        if isinstance(item, Decimal):
            return str(item)
        if isinstance(item, dict):
            return "{" + ",\n".join(json.dumps(key) + ": " + encode(val) for key, val in item.items()) + "}"
        if isinstance(item, list):
            return "[" + ", ".join(encode(val) for val in item) + "]"
        return json.dumps(item, ensure_ascii=False, allow_nan=False)
    path.write_text(encode(value) + "\n", encoding="utf-8")


def inspect_records(root, task_path, result_path):
    lint = Linter(root)
    lint.reference(task_path, ".", kind="task", current=True)
    lint.reference(result_path, ".", kind="result")
    lint.load()
    lint.check()
    return lint.output()["diagnostics"]


def run_revision(root, case_path, candidate_path, output_dir):
    """Copy supplied revisions, repin their ledger, and report separate checks.

    The case is a finite evaluation fixture, not a research approval record.
    The caller supplies substantive replacement text. This function runs no AI.
    """
    root = Path(root).resolve()
    lint = Linter(root)
    selected = [lint.path(path, ".") for path in (case_path, candidate_path)]
    output = lint.path(output_dir, ".", required=False)
    if lint.diagnostics:
        raise ValueError(json.dumps(lint.output()))
    if (root / output).exists():
        raise ValueError("The output directory already exists. Select a new attempt.")
    case, candidate = [read_json((root / path).read_bytes()) for path in selected]
    frozen = [case["initial_task"], case["initial_result"], case["feedback"], case["rubric"]]
    frozen += [node["artifact"] for node in case["nodes"]]
    originals = {entry["path"]: reference(root, entry) for entry in frozen}
    feedback = read_json(originals[case["feedback"]["path"]])
    rubric = read_json(originals[case["rubric"]["path"]])
    affected = affected_closure(case["nodes"], feedback["changed_nodes"])
    nodes = {node["id"]: node for node in case["nodes"]}
    replacements = candidate["replacements"]
    if not isinstance(replacements, dict) or not replacements.keys() <= set(affected):
        raise ValueError("Replacements must name affected nodes only.")
    if not valid_id(candidate["attempt_id"]):
        raise ValueError("The candidate must name a new attempt ID.")
    initial_result = read_json(originals[case["initial_result"]["path"]])
    if candidate["attempt_id"] == initial_result["attempt_id"]:
        raise ValueError("The candidate must use a new attempt ID.")
    content = {key: reference(root, value) for key, value in replacements.items()}
    initial_issues = inspect_records(root, case["initial_task"]["path"], case["initial_result"]["path"])
    if initial_issues:
        raise ValueError(json.dumps({"initial_record_diagnostics": initial_issues}))

    # Compute the full affected set before writing any revised artifact.
    stale = [key for key in affected if key not in content
             or content[key] == originals[nodes[key]["artifact"]["path"]]]
    (root / output / "artifacts").mkdir(parents=True)
    current = {key: dict(node["artifact"]) for key, node in nodes.items()}
    for key, raw in content.items():
        suffix = Path(replacements[key]["path"]).suffix
        path = output + "/artifacts/" + key + suffix
        (root / path).write_bytes(raw)
        current[key] = file_ref(root, path)
    ledger_id = case["ledger_node"]
    if ledger_id in content:
        ledger = read_json(content[ledger_id])
        ledger["attempt_id"] = candidate["attempt_id"]
        for claim in ledger["claims"]:
            location = claim["location"]
            matches = [key for key, ref in replacements.items()
                       if location["artifact"] == ref["path"] and location["sha256"] == ref["sha256"]]
            if matches:
                location.update(artifact=current[matches[0]]["path"], sha256=current[matches[0]]["sha256"])
        write_json(root / current[ledger_id]["path"], ledger)
        current[ledger_id] = file_ref(root, current[ledger_id]["path"])

    task = read_json(originals[case["initial_task"]["path"]])
    task["revision"] += 1
    task["write_paths"] = [output + "/"]
    task["inputs"] = list({entry["path"]: entry for entry in frozen}.values())
    task["evidence_ledger"] = (current[ledger_id]["path"] if ledger_id in content
                               else output + "/artifacts/" + ledger_id + ".json")
    task_path, result_path = output + "/task.json", output + "/result.json"
    current_task_path = output + "/current-task.json"
    write_json(root / task_path, task)
    write_json(root / current_task_path, task)
    result = {
        "task_id": task["task_id"], "task_revision": task["revision"],
        "attempt_id": candidate["attempt_id"], "task_path": task_path,
        "task_sha256": file_ref(root, task_path)["sha256"],
        "execution_status": "blocked" if stale else "completed",
        "artifacts": [dict(ref, **({"kind": "claim_evidence_ledger"}
                                   if key == ledger_id and key in content else {}))
                      for key, ref in current.items()],
        "unresolved": ["Stale affected node: " + key for key in stale],
        "resource_usage": {"tokens": None, "measurement": "unavailable"},
        "next_action": "Read the revision checks and assess scientific support independently.",
    }
    write_json(root / result_path, result)
    diagnostics = inspect_records(root, current_task_path, result_path)
    ledger = read_json((root / current[ledger_id]["path"]).read_bytes())
    claims = {claim["claim_id"]: claim for claim in ledger["claims"]}
    checks = []
    for expected in rubric["expected_claims"]:
        actual = claims.get(expected["claim_id"], {})
        checks.append({"claim_id": expected["claim_id"],
                       "matches_frozen_finding": actual.get("text") == expected["text"],
                       "evidence_ids_match": sorted(item["evidence_id"] for item in actual.get("evidence", []))
                       == sorted(expected["evidence_ids"])})
    failures = [item["claim_id"] for item in checks
                if not item["matches_frozen_finding"] or not item["evidence_ids_match"]]
    preservation = [{"node_id": item["node_id"], "text": item["text"],
                     "preserved": item["text"] in (root / current[item["node_id"]]["path"]).read_text(encoding="utf-8")}
                    for item in rubric["preserved_statements"]]
    result["unresolved"] += ["Feedback finding differs: " + key for key in failures]
    result["unresolved"] += ["Prior content is missing: " + item["node_id"]
                             for item in preservation if not item["preserved"]]
    if diagnostics:
        result["unresolved"].append("Record or evidence bindings need correction.")
    if result["unresolved"]:
        result["execution_status"] = "blocked"
    write_json(root / result_path, result)
    history = all((root / path).read_bytes() == raw for path, raw in originals.items())
    report = {
        "case_id": case["case_id"], "run_kind": "deterministic_fixture_replay",
        "affected_nodes": affected, "revised_nodes": sorted(content), "stale_nodes": stale,
        "feedback_implementation": checks,
        "prior_content_preservation": preservation,
        "unaffected_content": [{"node_id": key, "artifact": current[key], "reused_original": True}
                               for key in sorted(set(nodes) - set(affected))],
        "citation_support": {"record_diagnostics": diagnostics,
                             "ledger_current": ledger_id in content and ledger_id not in stale,
                             "scope": "Declared locations, evidence values, and file versions only."},
        "history_preserved": history, "new_experiment_run": False,
        "independent_content_assessment": "required_not_run",
        "assessment_limit": "Structured findings do not prove that the prose is sound or that agent performance improved.",
        "result": file_ref(root, result_path),
    }
    write_json(root / output / "revision-checks.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("root", "case", "candidate", "output"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args()
    try:
        report = run_revision(args.root, args.case, args.candidate, args.output)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["stale_nodes"] or report["citation_support"]["record_diagnostics"] or any(
        not item["preserved"] for item in report["prior_content_preservation"]) or any(
        not item["matches_frozen_finding"] or not item["evidence_ids_match"]
        for item in report["feedback_implementation"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
