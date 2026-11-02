#!/usr/bin/env python3
"""Compare frozen synthesis findings without assigning a scientific verdict."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from lint_records import Linter, unique_object, finite_number
from evidence_ledger import strict_equal, finite_decimal


DIMENSIONS = ("source_quality", "claim_support", "cross_branch_inference", "question_coverage")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), parse_float=finite_decimal,
                      parse_constant=finite_number, object_pairs_hook=unique_object)


def pinned(root, reference):
    """Reuse the record checker's path and digest rules."""
    checker = Linter(root)
    path = checker.reference(reference["path"], ".", expected=reference["sha256"])
    if checker.diagnostics:
        raise ValueError("; ".join(item[2] for item in sorted(checker.diagnostics)))
    return root / path


def facts(rule, sources):
    """Compute the small set of relations declared by this frozen trial."""
    selected = [sources[source_id] for source_id in rule["source_ids"]]
    kind = rule["kind"]
    result = {"relation": kind, "source_ids": rule["source_ids"]}
    if kind == "source_status":
        source = selected[0]
        result.update({key: source[key] for key in ("availability", "reading_depth")})
        result["freshness"] = "superseded" if source.get("superseded_by") else "current"
    elif kind == "difference":
        source = selected[0]
        result.update(delta=source["method_value"] - source["baseline_value"],
                      unit=source["unit"], conditions=source["conditions"])
    elif kind == "weighted_difference":
        outcome, cost = selected
        if not strict_equal(outcome["conditions"], cost["conditions"]):
            raise ValueError("The utility comparison needs matching conditions.")
        if outcome["branch_id"] == cost["branch_id"]:
            raise ValueError("The utility comparison needs both branches.")
        weight = rule["cost_weight"]
        value = (outcome["method_value"] - outcome["baseline_value"]
                 - weight * (cost["method_value"] - cost["baseline_value"]))
        result.update(cost_weight=weight, delta=value, conditions=outcome["conditions"],
                      preference="method" if value > 0 else "baseline" if value < 0 else "tie")
    elif kind == "condition_difference":
        left, right = selected
        result["different_fields"] = sorted(key for key in left["conditions"].keys() | right["conditions"].keys()
                                            if not strict_equal(left["conditions"].get(key), right["conditions"].get(key)))
        if not result["different_fields"]:
            raise ValueError("The condition case needs different conditions.")
    elif kind == "dispute":
        left, right = selected
        if not strict_equal(left["conditions"], right["conditions"]) or left["unit"] != right["unit"]:
            raise ValueError("The dispute case needs matching conditions and units.")
        deltas = [source["method_value"] - source["baseline_value"] for source in selected]
        result.update(opposing_signs=deltas[0] * deltas[1] < 0, conditions=left["conditions"])
    elif kind == "evidence_gap":
        result.update(availability=selected[0]["availability"], judgment="unresolved")
        if result["availability"] == "available":
            raise ValueError("The gap case needs unavailable evidence.")
    elif kind == "answer":
        # These are fixed task judgments, not inferred scientific truth.
        result.update(rule["expected"])
    else:
        raise ValueError("Unknown frozen relation: " + str(kind))
    return result


def evaluate(root, case_path, candidate_path):
    root = Path(root).resolve()
    checker = Linter(root)
    case_path = checker.path(case_path, ".")
    candidate_path = checker.path(candidate_path, ".")
    if checker.diagnostics:
        raise ValueError("; ".join(item[2] for item in sorted(checker.diagnostics)))
    case = read_json(root / case_path)
    candidate = read_json(root / candidate_path)
    checker.reference(candidate["task"]["path"], ".", candidate["task"]["sha256"], kind="task", current=True)
    result_path = checker.reference(candidate["result"]["path"], ".", candidate["result"]["sha256"], kind="result")
    checker.load()
    checker.check()
    if checker.diagnostics:
        raise ValueError("; ".join(item[2] for item in sorted(checker.diagnostics)))
    result = checker.records["result"][result_path]
    if not any(entry["path"] == candidate["artifact"]["path"]
               and entry["sha256"] == candidate["artifact"]["sha256"]
               and entry.get("kind") in {"literal_aggregate", "synthesis"} for entry in result["artifacts"]):
        raise ValueError("The candidate artifact is absent from its fixed result.")
    sources = read_json(pinned(root, case["sources"]))
    source_ids = {source["identifier"]: source_id for source_id, source in sources.items()}
    rubric = read_json(pinned(root, case["rubric"]))
    artifact_path = pinned(root, candidate["artifact"])
    artifact = read_json(artifact_path)
    if artifact["artifact_type"] == "literal_aggregate":
        manuscript = "\n\n".join(branch["content"] for branch in artifact["branches"]
                                  if branch["state"] == "collected")
        claims = {}
    elif artifact["artifact_type"] == "synthesis":
        pinned(root, artifact["aggregate"])
        manuscript_path = pinned(root, artifact["manuscript"])
        manuscript = manuscript_path.read_text(encoding="utf-8")
        ledger = read_json(pinned(root, artifact["evidence_ledger"]))
        claims = {claim["claim_id"]: claim for claim in ledger["claims"]}
        if len(claims) != len(ledger["claims"]):
            raise ValueError("The ledger repeats a claim ID.")
        for claim in claims.values():
            location = claim["location"]
            if (location["artifact"] != artifact["manuscript"]["path"]
                    or location["sha256"] != artifact["manuscript"]["sha256"]
                    or location["exact_quote"] != claim["text"]
                    or manuscript.count(claim["text"]) != 1):
                raise ValueError("A claim does not match its fixed manuscript location.")
            for evidence in claim["evidence"]:
                source_id = source_ids.get(evidence["source"]["identifier"])
                if source_id is None:
                    raise ValueError("A claim cites a source outside the frozen case.")
                source = sources[source_id]
                if (evidence["artifact"] != case["sources"]["path"]
                        or evidence["sha256"] != case["sources"]["sha256"]
                        or evidence["availability"] != source["availability"]
                        or evidence["source"]["version"] != source["version"]
                        or evidence["source"]["reading_depth"] != source["reading_depth"]
                        or evidence["locator"] != {"type": "section", "value": source_id}):
                    raise ValueError("A citation differs from its frozen source record.")
    else:
        raise ValueError("The candidate needs a literal aggregate or synthesis artifact.")
    findings = {finding["finding_id"]: finding for finding in candidate["findings"]}
    if len(findings) != len(candidate["findings"]):
        raise ValueError("The candidate repeats a finding ID.")
    expected_ids = {rule["finding_id"] for rule in rubric["checks"]}
    if set(findings) - expected_ids:
        raise ValueError("The candidate contains findings outside the fixed rubric.")
    dimensions = {name: [] for name in DIMENSIONS}
    for rule in rubric["checks"]:
        expected = facts(rule, sources)
        finding = findings.get(rule["finding_id"])
        reasons = []
        if finding is None:
            reasons.append("The structured finding is absent.")
        else:
            if not strict_equal(finding["facts"], expected):
                reasons.append("The finding differs from the fixed evidence relation.")
            claim = claims.get(finding["claim_id"])
            if claim is None:
                reasons.append("The finding has no claim in the fixed ledger.")
            elif sorted(source_ids[item["source"]["identifier"]] for item in claim["evidence"]) != sorted(rule["source_ids"]):
                reasons.append("The claim cites a different set of sources.")
        dimensions[rule["dimension"]].append({
            "finding_id": rule["finding_id"], "matched": not reasons, "reasons": reasons,
        })
    return {
        "case_id": case["case_id"], "synthetic": case["synthetic"],
        "case_sha256": hashlib.sha256((root / case_path).read_bytes()).hexdigest(),
        "candidate_sha256": hashlib.sha256((root / candidate_path).read_bytes()).hexdigest(),
        "dimensions": dimensions,
        "annotation_scope": "declared_findings_only",
        "independent_content_assessment": "required_not_run_by_this_script",
        "limits": [
            "The checks compare fixed structured findings and exact source references.",
            "An independent reader must assess whether the prose follows from those sources.",
            "Absent findings in a control do not show that its source summaries are false.",
            "These results do not measure agent improvement or grant human approval.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--case", required=True)
    parser.add_argument("--candidate", required=True)
    args = parser.parse_args(argv)
    try:
        report = evaluate(args.root, args.case, args.candidate)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}))
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
