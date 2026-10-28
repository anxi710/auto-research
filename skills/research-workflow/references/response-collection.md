# Collect responses and preserve gaps

A branch is one assigned worker task.
A literal aggregate stores worker text without rewriting it.
A synthesis connects evidence into an argument.
These are separate artifact types.

Use the existing [collaboration records](collaboration.md) for execution and technical acceptance.
Use the existing [human review procedure](human-review.md) for permission.
Use the existing [claim-evidence ledger](evidence-ledger.md) for selected claims and their evidence.
The collector does not create another decision record.

## Fix the collection scope

Add `response_branches` to the current collection task before dispatch.
Each entry names one expected branch and its fixed worker contract:

```json
{
  "branch_id": "B1",
  "task_path": "tasks/T1/task.json",
  "task_revision": 1,
  "task_sha256": "<actual SHA256 of the worker task>",
  "result_path": "tasks/T1/attempts/A1/result.json",
  "response_path": "tasks/T1/attempts/A1/artifacts/response.json"
}
```

Use unique branch IDs.
Use paths relative to the research root.
Keep the current collection contract and its attempt copy identical.
Keep its `write_paths` within the new collection attempt.

`response_branches` names expected submissions, including missing or unfinished submissions.
It does not declare accepted dependencies.
If an action requires an accepted upstream result, use the existing `dependencies` field and its exact review references.
Keep human decision or waiver references in the existing contract acceptance conditions and review records.
Do not copy their decisions into response artifacts.

## Save a worker response

Save each response as UTF-8 JSON.
Use these exact fields:

```json
{
  "schema_version": "1",
  "artifact_type": "worker_response",
  "task_id": "T1",
  "task_revision": 1,
  "attempt_id": "A1",
  "branch_id": "B1",
  "content": "The worker's literal response."
}
```

List the response in its result with `kind: "worker_response"` and the actual file SHA256.
Keep execution status in that result.
Finish the response before submitting the result.
The response must match its result identity and the expected branch.

## Run the collector

Create the new attempt directory before collection.
Run this command with the current collection contract:

```sh
python /path/to/research-workflow/scripts/collect_responses.py \
  --root /path/to/research \
  --task tasks/T2/task.json \
  --attempt-id A1 \
  --output tasks/T2/attempts/A1/artifacts/aggregate.json
```

The collector creates one new file within the contract `write_paths`.
It refuses to overwrite an existing file.
It does not change worker files or call external services.

The aggregate uses `schema_version: "1"` and `artifact_type: "literal_aggregate"`.
Its task and attempt fields follow the worker format.
Its other fields are:

| Field | Content |
| --- | --- |
| `contract` | The collection task `path` and exact `sha256`. |
| `branches` | One entry for every expected branch, in contract order. |
| `coverage.expected` | Every expected branch ID. |
| `coverage.collected` | Branch IDs with complete, valid submitted responses. |
| `coverage.gaps` | Each other branch ID and its collection gap reason. |

Each branch entry contains `branch_id`, `state`, `result`, `response`, `content`, and `diagnostics`.
The result and response references contain `path` and `sha256`, or `null` when unavailable.
The content preserves the decoded response text, including its line endings.
Malformed sources retain their file references without invented text.
Each diagnostic uses the existing `code`, `path`, and `message` fields.

The state is `collected`, `missing`, `unfinished`, `malformed`, `duplicate`, `stale`, or `invalid`.
The gap reason equals the branch state.
Duplicate physical submissions cannot count as two collected branches.
Incomplete responses can retain text while remaining gaps.

A zero exit code means that the collector saved an accurate aggregate.
It does not mean that every branch completed or passed review.
Read `coverage.gaps` before presenting the output.
An accepted review of accurate partial collection does not accept the missing branches.

List the aggregate in its result with `kind: "literal_aggregate"` and its actual SHA256.
A completed task with `response_branches` requires this typed artifact.
The aggregate must use the exact contract stored with its result.
Changing the scope requires a new contract revision and attempt.

## Connect a synthesis to evidence

Use a separate manuscript for the argument.
Follow the [synthesis guide](synthesis-revision.md) for reasoning across branches.
Save its selected claims in the existing ledger.
Add the exact aggregate reference to the synthesis task `inputs`.
Set the task `synthesis` field to its planned synthesis artifact path.

The synthesis artifact contains these exact fields:

```json
{
  "schema_version": "1",
  "artifact_type": "synthesis",
  "task_id": "T3",
  "task_revision": 1,
  "attempt_id": "A1",
  "aggregate": {"path": "<aggregate path>", "sha256": "<actual SHA256>"},
  "coverage": {"expected": ["B1"], "collected": ["B1"], "gaps": []},
  "manuscript": {"path": "<manuscript path>", "sha256": "<actual SHA256>"},
  "evidence_ledger": {"path": "<ledger path>", "sha256": "<actual SHA256>"}
}
```

Copy the exact aggregate coverage, including every gap.
List the synthesis, manuscript, and ledger in the same result.
Use `kind: "synthesis"` and the existing ledger kind `claim_evidence_ledger`.
Each ledger claim must locate the fixed synthesis manuscript.
Keep scientific assessments in the existing review.
Do not add acceptance or approval fields to these artifact types.

## Inspect before consumption

Run the existing `lint_records.py` command with the selected tasks, results, and relevant review history.
The checker finds these artifact kinds through result artifacts.
It requires no extra command flag.
Legacy records without these fields need no migration.

The checker reads the fixed contract and current worker records again.
It compares source versions, literal text, branch coverage, manuscript references, and ledger references.
Changed sources or newly available branches invalidate the saved aggregate for current consumption.
Preserve that aggregate as history and collect into a new attempt.

Collection and inspection require finished writes.
The tools do not lock files or provide a transaction across records.
The checker cannot establish scientific quality, authentic consent, or omitted review history.
Use the existing review and human decision procedures before dependent research.
