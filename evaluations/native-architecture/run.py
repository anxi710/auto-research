#!/usr/bin/env python3
"""Record native calls. This script never generates model answers."""

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def frozen_files(root):
    return {str(p.relative_to(root)): digest(p)
            for p in sorted((root / "frozen").rglob("*")) if p.is_file()}


def freeze(root):
    path = root / "freeze.json"
    if path.exists():
        raise ValueError("The study is already frozen.")
    save(path, {"frozen_at": now(), "files": frozen_files(root)})


def verify(root):
    frozen = json.loads((root / "freeze.json").read_text())
    if frozen["files"] != frozen_files(root):
        raise ValueError("Frozen inputs changed. Do not use this run as heldout evidence.")
    return frozen


def start(root, call_id):
    verify(root)
    plan = json.loads((root / "frozen/plan.json").read_text())
    spec = next((c for c in plan["calls"] if c["id"] == call_id), None)
    if spec is None:
        raise ValueError("The call is absent from the frozen plan.")
    records = list((root / "runs").glob("*/call.json"))
    if len(records) >= plan["call_limit"]:
        raise ValueError("The native call limit is reached.")
    path = root / "runs" / call_id
    path.mkdir(parents=True, exist_ok=False)
    save(path / "call.json", {
        **spec, "status": "started", "started_at": now(),
        "model_requested": "gpt-6-astra", "reasoning_requested": "ultra",
        "model_actual": None, "fast_tier_actual": None,
        "runtime_reason": "The native tool confirms requested model and reasoning, but supplies no actual model or Fast-tier receipt.",
        "tokens": None, "cost": None,
        "usage_reason": "Native collaboration tools do not expose token or billing counters.",
        "prompt_sha256": digest(root / spec["prompt"]),
    })


def finish(root, call_id, agent_id, status="completed"):
    verify(root)
    folder = root / "runs" / call_id
    path = folder / "call.json"
    record = json.loads(path.read_text())
    if record["status"] != "started":
        raise ValueError("The call already has a terminal record.")
    output = folder / "output.md"
    if status == "completed" and not output.is_file():
        raise ValueError("A completed call needs a native output file.")
    record.update({"status": status, "agent_id": agent_id, "finished_at": now()})
    record["elapsed_seconds"] = (datetime.fromisoformat(record["finished_at"])
                                 - datetime.fromisoformat(record["started_at"])).total_seconds()
    record["timing_scope"] = "Before native dispatch through parent-observed completion. Includes orchestration and observation delay."
    if output.is_file():
        record["output_sha256"] = digest(output)
        record["output_bytes"] = output.stat().st_size
    save(path, record)


def dispatched(root, call_id, agent_id):
    path = root / "runs" / call_id / "call.json"
    record = json.loads(path.read_text())
    if record["status"] != "started" or "agent_id" in record:
        raise ValueError("The call already has a dispatch receipt or terminal record.")
    record.update({"agent_id": agent_id, "successful_dispatch_observed_at": now()})
    save(path, record)


def package(root, repeat):
    verify(root)
    plan = json.loads((root / "frozen/plan.json").read_text())
    prefix = f"r{repeat}"
    paths = {name: root / "runs" / f"{prefix}-{name}" / "output.md"
             for name in ("single", "quality", "operations", "revision")}
    for path in paths.values():
        record = json.loads((path.parent / "call.json").read_text())
        if record["status"] != "completed" or digest(path) != record["output_sha256"]:
            raise ValueError("Packaging needs unchanged, completed native outputs.")
    merged = root / "runs" / f"{prefix}-merge.md"
    with merged.open("xb") as stream:
        stream.write(b"# Quality worker\n\n" + paths["quality"].read_bytes())
        stream.write(b"\n\n# Operations worker\n\n" + paths["operations"].read_bytes())
    paths["merge"] = merged
    manifest = {"method": "Literal byte concatenation. No model inference.",
                "shared_workers": [str(paths[name].relative_to(root)) for name in ("quality", "operations")],
                "candidates": {}}
    for label, role in plan["candidate_map"][prefix].items():
        destination = root / "runs" / f"{prefix}-candidate-{label.lower()}.md"
        with destination.open("xb") as stream:
            stream.write(paths[role].read_bytes())
        manifest["candidates"][label] = {"role": role, "path": str(destination.relative_to(root)),
                                             "sha256": digest(destination), "source": str(paths[role].relative_to(root))}
    save(root / "runs" / f"{prefix}-package.json", manifest)


def summarize(root):
    frozen = verify(root)
    plan = json.loads((root / "frozen/plan.json").read_text())
    calls = [json.loads(p.read_text()) for p in sorted((root / "runs").glob("*/call.json"))]
    for record in calls:
        output = root / "runs" / record["id"] / "output.md"
        if record["status"] == "completed" and digest(output) != record["output_sha256"]:
            raise ValueError("A native output changed after completion.")
    arms = {}
    for arm in ("single", "merge", "synthesis_revision"):
        selected = [c for c in calls if arm in c["charged_to"]]
        expected_ids = {c["id"] for c in plan["calls"] if arm in c["charged_to"]}
        arms[arm] = {
            "native_calls": sum("agent_id" in c for c in selected),
            "call_ids": [c["id"] for c in selected],
            "measured_call_seconds": sum(c.get("elapsed_seconds", 0) for c in selected),
            "all_calls_completed": {c["id"] for c in selected} == expected_ids and all(c["status"] == "completed" for c in selected),
            "tokens": None, "cost": None,
            "usage_reason": "No native token or billing counters. Shared workers and evaluators are charged in full to each consuming arm.",
        }
    finished = [c["finished_at"] for c in calls if "finished_at" in c]
    observed_end = max(finished) if finished else None
    study_seconds = ((datetime.fromisoformat(observed_end) - datetime.fromisoformat(frozen["frozen_at"])).total_seconds()
                     if observed_end else None)
    failures = [item for p in (root / "runs").glob("*/dispatch-failures.json")
                for item in json.loads(p.read_text())]
    return {"unique_native_calls": sum("agent_id" in c for c in calls), "planned_native_calls": len(plan["calls"]),
            "denied_dispatches": len(failures),
            "native_calls_by_role": dict(Counter(c["role"] for c in calls if "agent_id" in c)),
            "failed_or_open_calls": [c["id"] for c in calls if c["status"] != "completed"],
            "arms": arms, "tokens": None, "cost": None,
            "study_started_at": frozen["frozen_at"], "study_finished_at": observed_end,
            "study_wall_seconds": study_seconds,
            "study_wall_scope": "Frozen inputs through final observed actor completion. Includes lead orchestration, local processing, and capacity waits after freeze. Excludes preparation before freeze.",
            "unique_actor_seconds": sum(c.get("elapsed_seconds", 0) for c in calls),
            "preexisting_coordinator_contexts": 2,
            "coordinator_model_receipts": None,
            "coordinator_preparation_seconds": None,
            "lead_tokens": None, "lead_cost": None,
            "lead_usage_reason": "The study lead and outer toolkit coordinator also use native contexts. Their token and billing counters are unavailable.",
            "timing_limit": "Arm seconds exclude unallocated lead preparation and local processing. See study wall time separately. This is not end-to-end latency.",
            "all_planned_calls_completed": len(calls) == len(plan["calls"]) and all(c["status"] == "completed" for c in calls)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("freeze", "verify", "start", "dispatched", "finish", "package", "summary"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--call")
    parser.add_argument("--agent-id")
    parser.add_argument("--repeat", type=int, choices=(1, 2))
    parser.add_argument("--status", choices=("completed", "failed", "blocked", "cancelled", "unknown"), default="completed")
    args = parser.parse_args()
    try:
        if args.command == "freeze":
            freeze(args.root)
        elif args.command == "verify":
            verify(args.root)
        elif args.command == "start":
            if not args.call:
                parser.error("start needs --call")
            start(args.root, args.call)
        elif args.command in ("dispatched", "finish"):
            if not args.call or not args.agent_id:
                parser.error(f"{args.command} needs --call and --agent-id")
            if args.command == "dispatched":
                dispatched(args.root, args.call, args.agent_id)
            else:
                finish(args.root, args.call, args.agent_id, args.status)
        elif args.command == "package":
            if not args.repeat:
                parser.error("package needs --repeat")
            package(args.root, args.repeat)
        else:
            print(json.dumps(summarize(args.root), indent=2))
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
