# Review or discussion record

Use this file for review, meeting preparation, a talk, or a response to reviewers.
Keep plans separate from events that occurred.
Record AI review as simulation.
Use only the sections that the requested task needs.
By default, propose changes without editing the reviewed files.
Present proposed changes for human review before dependent work uses them.
For standalone work, put needed human decision fields in the requested output or response.
Follow [human review](../references/human-review.md) for the decision and waiver records below.
Replace template links with project links before saving this record.

## Purpose

ID and date: Unknown.
Type: Unknown.
Actual reviewer or AI simulation: Unknown.
Audience and time available: Unknown.
Files and versions under review: Unknown.
Requested review scope: Unknown.
Decision needed: Unknown.
Relevant venue rules: Not assessed.

## Preparation

Previous actions, outcomes, and reasons for unfinished work: None recorded.
Work summary: Unknown.
Latest evidence and its limits: Unknown.
Main question: Unknown.
Options and tradeoffs: Unknown.
Previous attempts and their outcomes: None recorded.
Unresolved problems: Unknown.
Talk outline or draft response: Not prepared.

## Concerns and responses

| Concern or question | Affected claim | Evidence location | Response or action | Owner | Status |
| --- | --- | --- | --- | --- | --- |

Distinguish existing evidence, new analysis, and planned experiments.
Use `open`, `resolved`, or `disputed` for concern status.
Link a resolved concern to its actual change or answer.

## Outcome

Did the meeting or review occur?: Not recorded.
Actual decisions: None recorded.
Remaining disagreements: None recorded.
Actions, owners, and agreed dates: None recorded.
Changes to research state: None yet.
Next action: Unknown.

## Human decision

Decision ID and date: Not recorded.
Presented output paths and exact revisions or SHA256 digests: Not recorded.
Evidence, uncertainties, and alternatives: Not recorded.
Requested next actions: Not recorded.
Decision status: Pending.
Researcher and decision source: Not recorded.
Approved next actions and limits: None.
Reasons or requested revisions: None recorded.
Superseded decision record: None.

Use `pending`, `approved`, or `rejected` for the decision status.
Record the actual researcher message or its stable reference as the source.
Preserve earlier output versions and decisions when a revision needs another review.
An AI recommendation or successful test does not fill in human approval.

## Review waiver (optional)

Waiver ID and date: Not recorded.
Researcher and instruction source: Not recorded.
Covered outputs, stages, and next actions: Not recorded.
Limits: Not recorded.
End condition: Not recorded.
Waiver status: Not granted.
End or revocation source: None recorded.

Use this section only for an explicit waiver under the shared human review rule.
Use `active`, `ended`, or `revoked` after the researcher grants the waiver.
Retain the original scope and source after the waiver ends.
Link this record from project navigation instead of copying its fields.

## Task acceptance (optional)

Use this block only for a task under the [collaboration procedure](../references/collaboration.md).
Replace template links with project links before saving this record.
Remove this section from ordinary discussions.
Fill every required field from the inspected files and actual decision.
Keep these fields in this block only.

```json
{
  "review_id": "R001",
  "task_id": "T001",
  "task_revision": 1,
  "attempt_id": "A001",
  "result_path": "tasks/T001/attempts/A001/result.json",
  "result_sha256": null,
  "reviewer": null,
  "decision_owner": null,
  "decision": null,
  "basis": [],
  "unresolved": [],
  "supersedes": null
}
```

Use `basis` for evidence paths, source locations, and observed checks.
Use `supersedes` with `path` and `sha256` only when this decision replaces a review of the same result.
The procedure defines valid decisions and the effect of later changes.
This technical task decision remains separate from human permission above.
The record checker does not establish human approval.
