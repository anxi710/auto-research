# Improve the workflow

RSI means repeated changes to the procedure that performs work.
Here, each round uses outcomes from earlier rounds to improve workflow instructions.
It does not train model weights or guarantee better research.

Use this procedure when the user offers a workflow idea, corrects a repeated behavior, or requests a workflow improvement.
Keep ordinary research work in its current stage.
This file travels with the complete skill package.

## Select the scope

Use the user's stated intent to choose where the change belongs.
An idea is a proposal until it becomes an active rule.
Do not infer a permanent rule from a one-time workaround.

| User intent | Destination | What becomes active |
| --- | --- | --- |
| Do this for the current task. | Current task in `STATE.md`, when state exists. | Only this task. |
| Use this convention in this project. | Project conventions in `BRIEF.md`. | Only this project. |
| Remember an idea for later. | A change record with status `captured`. | Nothing. |
| Try this workflow change. | A scoped trial and its change record. | Only the named trial. |
| Make this a reusable default. | The authorized skill copy and affected references or templates. | The updated package copy. |
| Improve the workflow from recent evidence. | A bounded improvement round. | Changes that meet its declared adoption conditions. |

If the scope is unclear, record a proposal and ask which scope the user intends.
Continue unrelated authorized work.
Do not ask again when the user already specified the scope and authorized the change.

A simple project preference needs a brief entry, not a full change study.
For example, store a project-specific note language directly in `BRIEF.md`.
Keep its scope and source beside the convention.

## Capture useful feedback

Capture evidence that can change a repeatable decision or action.
Useful triggers include user corrections, repeated friction, and a successful resolution of a recurring failure.
An external article can suggest a candidate but cannot authorize a change.

1. Record the user's intent or the observed failure in plain language.
2. Link the smallest relevant evidence without copying entire conversations or logs.
3. Search existing change records for the same problem.
4. If a matching record exists, add the new evidence to it.
5. Otherwise, create a record from [CHANGE.md](../templates/CHANGE.md).

Use `changes/W001.md`, then the next unused ID.
For toolkit changes, place `changes/` in the toolkit repository.
For project changes, place it in the selected research directory.
Keep unadopted proposals out of startup instructions.

Save lessons that explain when a procedure works and when it fails.
Do not treat the volume of saved lessons as a measure of improvement.
If no useful lesson exists, record no change.

## Prepare one bounded round

A candidate is a proposed version of the procedure.
A baseline is the saved version used for comparison.
A regression is behavior that a change makes worse.

1. Define the behavior to improve and the evidence that can show a benefit.
2. Record the allowed files, resource limits, and authority to adopt a passing change.
3. Save the baseline with a commit, a patch, or file snapshots.
4. Define a representative task and the expected observable behavior before editing the candidate.
5. Select existing cases that protect the affected research behavior.
6. Make the smallest candidate change in an isolated copy.

Use one candidate per round unless the user supplies another limit.
For several rounds, record maximum rounds and a time or spending limit before starting.
Stop when the requested improvement is complete or a limit is reached.
Do not turn an evaluation task into a new self-improvement run.

Protect evidence accuracy, reading depth, job state, user scope, and existing research records.
Keep evaluation tasks and expected outcomes fixed during a candidate trial.
If evaluation rules need a correction, record a separate change and repeat the baseline comparison.
Do not change the success criteria to make the candidate pass.

For a wording correction or an explicit simple preference, use a direct edit and a focused inspection.
Do not claim a measured performance improvement from that inspection.
For a behavioral change, run the comparison below before adopting an AI-proposed default.

## Compare behavior

Use the same task, files, tools, and budget for the baseline and candidate.
Use a fresh session for each run when the harness supports it.
Record model and harness differences that prevent a direct comparison.

1. Run the baseline on the chosen task in a temporary directory.
2. Run the candidate on the same task in another temporary directory.
3. Save both outputs and the actual evaluation result.
4. Run the relevant regression cases on the candidate.
5. Compare task success, factual errors, unnecessary actions, and resource use when measured.

Use an independent evaluator when available.
Give it the task and output files rather than the author's preferred conclusion.
Keep at least one separate case outside the candidate author's worked example when the budget permits.

If an independent evaluator is unavailable, label a same-session review as limited evidence.
If execution is unavailable, mark the comparison as unrun.
Do not convert a proposed test or a plausible answer into a passing result.

Choose an outcome from the evidence:

| Outcome | Condition | Next action |
| --- | --- | --- |
| Adopt | The requested behavior works, relevant protections pass, and adoption is authorized. | Apply the candidate to its declared scope. |
| Trial | Evidence or adoption scope remains incomplete. | Keep the candidate isolated or activate only the authorized local trial. |
| Reject | The candidate fails a required condition or has no useful benefit. | Preserve the result and stop this candidate. |
| No change | The current behavior already meets the need. | Record that result only when a change record already exists. |

A passing example does not prove general improvement.
State which cases support the decision and which remain untested.
For competing benefits, let the user's stated priorities determine the tradeoff.

## Adopt and observe

Keep each active rule in one maintained location.
A change record explains the decision but does not duplicate the runtime procedure.
Apply only the hunks needed for the accepted behavior.

1. Update the affected instructions, templates, examples, and tests together.
2. Make sure that local links and skill metadata remain valid.
3. Advance `metadata.version` in `SKILL.md` when package behavior changes.
4. Record the new version, evidence, and changed files in the change record.
5. Remove the active trial from `STATE.md` when the trial ends.
6. Review the result during the next relevant real task.

Start an unversioned package at `0.1.0`.
Use the next patch version for compatible behavior changes.
If record formats or entry paths break, document the change before choosing a new minor version.
Project-only conventions do not change the shared package version.

Use the next real task to seek failures outside the original example.
Append that evidence to the same change record.
If it changes the decision, open another bounded round or revert the change.

Do not silently upgrade other repositories or global skill installations.
When updating a copied package, compare it with the new version before merging.
Keep project conventions, old record layouts, IDs, and experimental history intact.
Missing new template fields do not require a full migration.

## Revert without losing research

A workflow rollback restores procedure text, not past research results.
A conversation branch does not restore changed files.
Use the saved baseline and the exact change diff.

1. Identify the change and the behavior that now fails.
2. Compare the current files with the saved post-change version.
3. Reverse only the affected change while preserving later edits.
4. Run the case that exposed the failure and relevant regression cases.
5. Mark the record as `reverted` and link the replacement decision, if one exists.

Do not use a blanket repository reset.
If later edits overlap, merge the rollback instead of overwriting them.
Retain earlier experiments, measurements, notes, and the rejected candidate's evidence.

Use `captured`, `trial`, `adopted`, `rejected`, or `reverted` for change status.
Record a tested no-change decision as `rejected` with the reason `already satisfied`.
After a rollback changes package behavior, assign a new version and record the version it restores behavior from.
