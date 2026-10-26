# Coordinate research tasks

Use this procedure when delegated work needs saved ownership, separate outputs, or an independent review.
Keep a small standalone task in one context when that meets the request.
Use the existing [stages](workflow.md) to decide what evidence the research needs.
This procedure adds records, not a scheduler or tool permissions.
Apply the [human review procedure](human-review.md) to every delegated output and AI assessment.
Technical task acceptance does not authorize dependent research without human approval or a matching waiver.

## Choose responsibilities

The coordinator assigns work and maintains shared research records.
A worker produces the output for one assigned task.
A reviewer inspects that output against the task requirements.
Use a separate review context for important results when one is available.
If the same assistant performs both roles, record that limit.

1. Select only tasks that need separate ownership or review.
2. Record the execution mode and its reason in `STATE.md` when state exists.
3. Assign one coordinator to shared `STATE.md`, `CLAIMS.md`, and task contracts.
4. Give each worker a separate output directory.
5. Assign one reviewer to each review record.

If workers share writable files without workspace isolation, run their tasks in sequence.
If subagents are unavailable, perform the roles in sequence.
The coordinator records technical task acceptance after inspecting the review evidence.
The coordinator can delegate that decision to one named reviewer in the task's acceptance conditions.
The decision owner alone writes the final review record.
Do not treat a worker message or a runtime task status as an acceptance decision.
Present the output and AI assessment to the researcher before dependent research proceeds.
Delegating technical acceptance does not delegate the researcher's authority.

## Select records and paths

A contract states the task's goal, inputs, limits, and acceptance conditions.
A revision identifies one saved contract version.
An attempt is one execution under a fixed contract.
SHA256 is a digest of a file's exact bytes.

Keep the project's existing research directory and record layout.
Use paths relative to that research directory in new JSON fields.
Resolve Markdown links from the file that contains them.
Preserve documented path conventions in old records.
Missing new fields do not require migration of old projects.

For a new task, use this layout unless the project defines another one:

```text
tasks/T001/task.json
tasks/T001/HANDOFF.md
tasks/T001/attempts/A001/task.json
tasks/T001/attempts/A001/result.json
tasks/T001/attempts/A001/artifacts/
reviews/R001.md
```

| Record | Authority |
| --- | --- |
| Current `task.json` | Current goal, owner, fixed inputs, output scope, limits, and required dependencies. |
| Attempt's `task.json` | Exact copy of the contract used for that attempt. |
| `result.json` | Submitted execution status and file versions, not acceptance. |
| Review's task acceptance block | Technical decision about one exact result version. |
| Human decision or review waiver | Researcher's authority for stated versions and next actions. |
| `STATE.md` | Existing project state and an index of collaboration records. |
| `HANDOFF.md` | Current navigation derived from linked records. |

Keep active job facts in the existing experiment records and `STATE.md` active runs table.
Do not place a continuously updated job record inside a submitted attempt.
Do not make a second editable copy of acceptance fields in `STATE.md` or `HANDOFF.md`.

## Prepare a contract

Start with [TASK.json](../templates/TASK.json).
Replace its empty fields before assigning work.
Template values do not establish authorization or completed work.

1. Set a stable task ID, a positive revision number, and one owner.
2. Record the goal and observable acceptance conditions.
3. List each required input file with its actual SHA256 digest.
4. Assign `write_paths` to the new attempt directory only.
5. Point `budget_ref` to the approved limits and this task's share.
6. State when the worker must stop.
7. Save the current contract and copy its exact bytes to the attempt's `task.json` before dispatch.

Include the required human review in `acceptance` and `stop_condition`, unless a matching waiver applies.
Link the actual human decision or waiver in the contract's acceptance conditions when one already permits the task.
Keep its authority and limits in the linked record rather than copying them into several contracts.

The coordinator makes the contract copy before the worker starts.
The worker must not edit either contract file.
Increase `revision` whenever any contract field changes, including owner, output scope, budget reference, or acceptance conditions.
Use a new attempt for a retry, and update the revision when its output path changes.
Keep execution notes separate from the fixed contract.
Preserve old contract copies and input versions that earlier results need.
If an input version is unavailable, record that limit.

All entries in `dependencies` are required upstream results.
Use an empty array when there are none.
Each entry contains `task_path`, `task_revision`, `result_path`, `result_sha256`, `review_path`, and `review_sha256`.
`task_path` identifies the upstream current contract, so later revisions remain visible.
The result identifies its own fixed contract copy.
The review must accept that exact result and remain valid under the rules below.
Before dependent dispatch, also establish the required human approval or matching waiver for its inputs and next action.
Keep optional background sources in `inputs` instead of treating an unfinished branch as accepted work.

## Submit an attempt

Start with [RESULT.json](../templates/RESULT.json).
Use `completed`, `blocked`, `failed`, `cancelled`, or `unknown` for `execution_status`.
`completed` means that execution ended with the required outputs, not that a hypothesis is true.

1. Match the task ID and revision to the saved contract copy.
2. Record the attempt ID and the contract copy's path and SHA256 digest.
3. List each submitted artifact with its path and actual SHA256 digest.
4. Record unresolved issues, measured resource use, and one next action.
5. Finish artifact writes before saving the result record.
6. Send the coordinator the task ID, revision, attempt ID, and result path after the record is readable.

Use `null` for an unknown measurement, not zero.
Keep failed runs, negative findings, and incomplete outputs with their limits.
An empty artifact list cannot establish completed work.
Make sure that the submission matches the current contract before accepting it.
If its revision or content changed, preserve the submission as historical work and require a new decision.

A sealed attempt is a submitted directory that stays unchanged.
Seal the contract copy, result, and listed artifacts together.
Use a new attempt for corrections instead of editing the sealed files.
These rules require cooperative writers and the harness's available controls.
They do not provide file locks or transactions across several files.

Use the optional [claim-evidence ledger](evidence-ledger.md) to bind selected claims to fixed evidence.
Declare a required ledger with the task's `evidence_ledger` path.
List a submitted ledger as a result artifact with `kind: "claim_evidence_ledger"`.
Keep its support assessments in the existing review.

## Review the exact result

Use the optional task acceptance block in [REVIEW.md](../templates/REVIEW.md).
Keep ordinary S7 discussions in that template's existing prose sections.
The acceptance block is the authority for technical task acceptance.
Record the human decision separately under the [human review procedure](human-review.md#record-the-human-decision).
HTML comments do not supply active acceptance content.
Comment markers inside fenced code remain literal data.

1. Open the current contract, fixed contract copy, result, and actual artifacts.
2. Make sure that their IDs, revisions, and SHA256 digests agree.
3. Read each required input and compare its SHA256 digest with the contract.
4. Make sure that each required dependency still has a valid acceptance decision.
5. Inspect the evidence for each acceptance condition, including limits and opposing evidence.
6. Record the reviewer, decision owner, evidence locations, and unresolved issues.
7. As the decision owner, save `accepted`, `rework`, or `blocked` in a new review record.

`accepted` means that this result meets its contract.
An AI `accepted` decision alone does not authorize the next research task.
`rework` means that the result needs correction.
`blocked` means that required evidence or access is missing.
If a required input is unavailable, record the limit and withhold acceptance.
A negative finding can be accepted when the task required an accurate analysis.
Keep the [claim states](../templates/CLAIMS.md) separate from task acceptance.
Do not modify the reviewed attempt or raw evidence during review.
Do not apply a review decision to changed files.
Inspect the new version separately.

Keep each completed review unchanged.
To replace a decision about the same result, write a new review.
Set `supersedes` to the old review's path and SHA256 digest.
Use `null` when no decision is replaced.
Inspect later review records before relying on an earlier acceptance.
If decisions conflict or the review history is incomplete, keep acceptance unresolved.

Stale means no longer valid for the current task.
If a contract, required input, artifact, or upstream acceptance changes, record which dependent result is stale and why.
Do not accept that result for current work until the affected conditions receive a new review.
For a changed contract, create a new attempt and result before seeking acceptance.
Reuse intact artifacts when they satisfy the new contract.
Record their original paths and versions, and state that no new experiment ran.
Preserve the original result and decision as history.
This is a review rule, not automatic dependency tracking.

## Resume within the existing limits

Use [HANDOFF.md](../templates/HANDOFF.md) only when a saved navigation summary helps the next session.
Keep it outside the sealed attempt directory.
List the record versions used to prepare it.
If it disagrees with those records, rebuild the summary from them.

1. Read the current task, result, review history, and relevant project state.
2. Inspect existing outputs before deciding that work needs another run.
3. Review completed but unreviewed work before starting a replacement.
4. Apply the existing [job recovery rules](workflow.md#s4-implement-and-run) to active or unknown jobs.
5. Update the shared index and one next action after the decision.

Restore human review requests, their exact output versions, and any active waiver before scheduling dependent work.
If a waiver ended or was revoked, restore the required human review.

Use task ID, revision, and attempt ID to recognize duplicate completion messages.
Message delivery does not prove that a result was saved or accepted.
Keep unknown remote outcomes unresolved until the execution system or its owner supplies evidence.
Cancelling a worker does not establish that its remote job stopped.

The coordinator accounts for all workers and reviews within the approved total budget.
Do not treat the total budget as a separate allowance for each worker.
If usage cannot be measured, record it as unknown.
Stop new assignments when the known remaining budget cannot cover them.
Preserve partial results and record any budget decision that requires the user.

## Inspect saved records

The [record checker](../scripts/lint_records.py) reads selected records and their file references.
It uses Python 3.9+ and the standard library.
It does not change research files or contact external services.

Run this command from the toolkit repository root.
Replace the research directory and record paths with your paths.
Repeat each record flag when you need more files.

```bash
python3 skills/research-workflow/scripts/lint_records.py \
  --root /path/to/research \
  --task tasks/T001/task.json \
  --result tasks/T001/attempts/A001/result.json \
  --review reviews/R001.md \
  --review reviews/R002.md
```

Use `--task` for a current contract, not an attempt's fixed copy.
Supply the current contract for each selected result.
Supply later reviews explicitly, including decisions that replace earlier acceptance.
The command follows record references but does not search the project for other reviews.
Ordinary review files without a task acceptance section remain outside the task schema.
Unselected old records need no migration.
The checker automatically inspects selected result artifacts tagged as claim-evidence ledgers.
An explicit contract requirement cannot skip a missing or untyped ledger.
See the [ledger format and limits](evidence-ledger.md) for claim locations and review scope.

All supplied paths use the selected research directory as their root.
Use plain file paths in `budget_ref` and JSON path fields, not Markdown links or section references.
Custom directory layouts remain valid.
File references must stay inside that root, including symbolic link targets.
Input files, artifacts, budgets, and linked records must exist.
Output directories in `write_paths` can be absent before execution.

The command prints JSON diagnostics with a code, record path, and message.
The path `.` marks an error in the initial file selection.
Exit code `0` means no issue was found in the supplied scope.
Exit code `1` means a record issue or missing context needs attention.
Exit code `2` means the command arguments are invalid.

| Diagnostic code | Meaning |
| --- | --- |
| `SCHEMA` | A required field, value, or JSON structure is invalid. |
| `PATH` | A path is unsafe or leaves the research directory. |
| `READ` | A required regular file is missing or unreadable. |
| `HASH` | A file differs from its recorded SHA256 digest. |
| `BINDING` | A result or review does not match its linked record. |
| `DUPLICATE_ID` | Different records claim the same identity. |
| `CURRENT` | A result lacks its current contract. |
| `STALE` | A historical result differs from the current contract. |
| `REVIEW_HISTORY` | Supplied review history has a conflict or invalid replacement. |
| `DEPENDENCY` | A required upstream result lacks valid current acceptance. |

Keep sealed files when a result is stale.
Follow the review rules above before using it for current work.
A clean report does not prove that review history is complete or a scientific claim is true.
The command cannot establish decision authority, live job status, or actual resource use.
It does not inspect human decision prose or enforce permission to start dependent research.
Run it while writers are idle because it does not lock the files.
