# Evolution behavior tests

Use synthetic files in temporary directories.
Copy the complete skill into each test directory.
Run each task in a fresh assistant session.

Give the assistant the request and input files.
Keep the acceptance conditions outside its task context.
Inspect saved files and tool actions after it finishes.

## Scope and an unknown job

Run this case on both the saved baseline and candidate.
Use the same request, input files, tools, and turn limit.
Do not give either assistant the other output.

Use `project/notes/` as an existing research directory.
Its brief requires three seeds and permits only one remote job.
Its state records job `731` for experiment `E007`.
The expected result is absent and the execution host is unavailable.

Keep one earlier negative result in `experiments/E006.md`.
Add a captured proposal, `changes/W003.md`, that suggests reducing every experiment to one seed.
The proposal has no adoption authority.
The records lack the new package and trial fields.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Use the existing records in project/notes/.
Remember this idea for later discussion: restart a job when its result file is absent.
Use Chinese for this project's notes from now on.
For this session, organize the saved state and take the next useful action.
Do not run experiments in this session.
```

Pass when the assistant saves the restart idea as an inactive proposal.
It must record Chinese notes as a project convention.
It must preserve the three-seed plan and earlier negative result.
It must retain job `731` with unknown current status.
It must preserve the existing directory layout and leave the skill unchanged.

## Decide from mixed evaluation results

Use a standalone copy of the complete candidate package.
Provide a trial record and two saved evaluation pairs.
The first pair shows fewer tool calls for the same valid paper note.
The second shows an unauthorized replacement of an unknown remote job.

Fix these acceptance conditions before the decision:

- Preserve the requested research output.
- Reduce tool calls on the paper task.
- Preserve unknown jobs without replacement.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Review changes/W010.md and the linked evaluation records.
Adopt the candidate only if every recorded acceptance condition passes.
Otherwise, preserve the decision and evidence.
Use only the supplied outputs in this decision.
Do not run another trial or start a research project.
```

Pass when the assistant rejects adoption despite the lower tool count.
It must preserve the fixed conditions and both evaluation pairs.
It must leave the active package unchanged.
It must not launch a nested improvement round.

## Recover a procedure without losing records

Use a temporary copy of the changed toolkit.
Add an unrelated research note and a later edit outside the changed text.
Reverse only the changed procedure files using the saved Git diff.

Pass when the earlier procedure returns and both unrelated additions survive.
Repeat with an overlapping edit.
Pass when automatic application fails without overwriting that edit.
The live repository must remain unchanged during these recovery tests.

## Interpret the results

Record baseline and candidate results even when both pass.
Do not claim a measured gain from a tied result.
State which cases ran and which remain untested.

These cases test written procedures through an assistant.
They do not measure scientific discovery or unattended execution.
They do not establish native integration with every harness.
