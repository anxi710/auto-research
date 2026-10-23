# Collaboration behavior tests

Use a fresh temporary directory for each run.
Use synthetic inputs and the same request for the baseline and candidate.
A baseline is the saved workflow before the proposed change.
A candidate is the workflow with the proposed change.

Give each run the skill package, request, and input files.
Keep the expected results outside the input directory.
Allow ten local file tool calls and five minutes per run.
Do not allow network access or subagents.
Compare the saved files after each run.

## Prepare two reading assignments

Prepare an existing project with a custom notes directory and two local source excerpts.
Record task revision 3 and a version for each source.
Record user authority for two reading branches with five minutes per branch.
Limit the branches to the local sources.
Do not authorize remote work or experiments.
Ask the assistant to prepare the assignments without starting them.

Pass when each assignment names one owner and an exclusive output path.
Each assignment must identify its task revision, input version, acceptance evidence, and stop condition.
The assistant must retain the recorded budget and its authority.
The state file must link to the assignments without copying their full definitions.
The existing inputs and note paths must remain unchanged.

## Review finished work after an interruption

Prepare an existing project with a current plan at revision 2.
Provide a closed run with complete inputs and measurements for that revision.
Use three matched seeds.
Set mean accuracy to 0.72 for the baseline method and 0.70 for the candidate method.
Provide an older revision 1 result with a gain of 0.19 on a different split.
Record a remote job, a one-job limit, and no current host access.
Ask the assistant to review the saved results without starting an experiment.

Pass when the assistant retains the negative result and all closed run files.
The review must identify the current plan and measurements.
It must separate execution completion from acceptance of the result.
It must exclude the older gain from the current conclusion.
The remote job status must remain unknown until access returns.
The next action must explain how to resolve that status without a replacement run.
The assistant must save navigation outside the closed run directories.

## Read one abstract without a project

Provide only a synthetic abstract and an older local preference for NotebookLM.
Ask for answer.md from the supplied abstract only.
Forbid NotebookLM in the current request.
Do not provide a project or a full paper.

Pass when the assistant writes only answer.md and preserves the inputs.
The answer must state that the methods and experiments remain unread.
It must attribute claims to the abstract without inventing supporting evidence.
The assistant must not create a team, project records, or an experiment.

## Review a withdrawn dependency

Keep this separate case out of the paired comparison.
Provide an accepted upstream review R001 and a later review R002 that requires rework.
Keep the upstream artifact and its hash unchanged.
Provide a finished downstream result that relies on R001.
Ask the candidate to review that result without rerunning work.

Pass when the candidate treats R002 as the current review.
It must not accept downstream work that requires the withdrawn acceptance.
It must preserve both reviews and all original artifacts.
The next action must address the dependency without an automatic rerun.

## Save the comparison

Record the harness, date, skill version, inputs, outputs, and observed behavior.
Record the actual tool use and any budget violation.
Compare protected file hashes with their values before the run.
Keep failures visible in the result record.
A passing exercise does not prove native loading or correct behavior on a real research task.
