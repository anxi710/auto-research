# Test results

Test date: 2026-10-22.
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

## Package inspection

The skill passed the bundled skill format validator.
All local Markdown links and root entry imports resolved.
A prose scan found no banned modal wording or decorative emphasis in the package documentation.

The longest prose sentences in the scan contained 18 words.
The scan excluded code, tables, headings, and metadata.
This scan supports the plain-English review but does not prove compliance with a controlled-language standard.

## Limits

Native skill discovery and full research cycles remain untested in Codex, Claude Code, Gemini CLI, and OpenCode.
The two referenced automated research repositories were read but not executed.
The workflow relies on each harness to supply tools, enforce permissions, and follow the saved procedure.
