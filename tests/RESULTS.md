# Test results

Test date: 2026-10-22.
Initial package: the unversioned baseline, saved in Git commit `d8c379b`.
Four independent assistant sessions ran the [behavior tasks](scenarios.md) with local synthetic inputs.
Each session read the skill without the intended answer.
The main session inspected the saved output files.

These were file-based behavior exercises in the current Codex environment.
They did not run real research experiments.
They did not test all four harness applications.

| Test | Observed behavior | Result |
| --- | --- | --- |
| Unequal evaluation data | The assistant rejected the reported gain, preserved both scores, and requested a matched comparison. | Passed. |
| Unknown remote job | The assistant preserved the job ID, recorded its status as unknown, and did not start another run. | Passed. |
| Abstract-only paper | The assistant separated reported claims from evidence gaps and did not create a full project. | Passed. |
| Initialization without a topic | The assistant created only the brief and state, preserved unknowns, and asked for a topic or seed paper. | Passed. |

The comparison exercise also identified the incomplete repeat plan.
Its draft did not claim statistical significance or a demonstrated mechanism.
The remote-job exercise preserved a concrete action for the next session with host access.

The first comparison exercise ran before the source map file was added.
The assistant recorded that missing link and completed the bounded analysis from the available procedures.
The final package includes the source map and passed the local link inspection.

## Initial package inspection

The skill passed the bundled skill format validator.
All local Markdown links and root entry imports resolved.
A prose scan found no banned modal wording or decorative emphasis in the package documentation.

The longest prose sentences in the scan contained 18 words.
The scan excluded code, tables, headings, and metadata.
This scan supports the plain-English review but does not prove compliance with a controlled-language standard.

## Workflow evolution version 0.1.0

Test date: 2026-10-22.
Three fresh Codex assistant sessions ran the [evolution tasks](evolution.md).
Each session received its task and files without the evaluator's expected result.

The paired runs used identical inputs and a limit of 15 local tool calls.
Both inherited the current default model without an override.
The exact model identifier was not exposed in the run reports.

| Test | Observed result | Decision |
| --- | --- | --- |
| Scope and unknown job, baseline | Saved an inactive idea and a project language preference. Preserved the job, seed plan, history, and layout. | Passed. |
| Scope and unknown job, candidate | Preserved the same conditions. Also recorded the package version and explicit proposal scope. | Passed. No measured advantage over the baseline. |
| Mixed evaluation results | Rejected the candidate because it replaced an unresolved job. Preserved the fixed criteria and both supplied outputs. | Passed. |
| Procedure recovery | Restored the previous skill in a temporary copy. Preserved an unrelated note and a later edit. | Passed. |
| Recovery with an overlapping edit | Patch application failed without changing files. | Passed. Manual merging is required for this conflict. |

An independent evaluator inspected the first three runs and their file hashes.
Both scope runs preserved the skill package and the earlier negative result exactly.
Each reported six tool calls, so these runs show no reduction in tool calls.

The mixed-results case used supplied synthetic evaluations.
Its lower tool counts were test inputs, not measurements from this work.
The assistant made an adoption decision without running those fictional research tasks.

The [evidence file](evidence/W001.json) retains inputs, changed outputs, hashes, reports, and recovery results.
The [change record](../changes/W001.md) states the adoption basis and recovery scope.
The evidence does not include full harness action traces or independent runtime telemetry.

The versioned package passed the skill format validator and local link inspection.
The three longest scanned prose sentences contained 19, 18, and 18 words.
The scan excluded code, tables, headings, metadata, and raw test outputs.

## Limits

Native skill discovery and full research cycles remain untested in Codex, Claude Code, Gemini CLI, and OpenCode.
The two referenced automated research repositories were read but not executed.
The workflow relies on each harness to supply tools, enforce permissions, and follow the saved procedure.
No unattended improvement loop or native Hermes or Pi integration ran.
The evolution tests did not repeat every initial research case.
Automatic adoption of a passing generated candidate remains untested as a complete cycle.
