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

## Unreleased personal-default candidate

Test date: 2026-10-23.
Four fresh Codex assistant sessions ran the [reading tasks](reading.md) with local synthetic inputs.
The paired task used identical inputs, tools, and a 15-call limit.
These tests cover W003's rejected candidate, not the replacement generic preferences procedure.
The user corrected the shared scope after these runs.

| Case | Observed result | Decision |
| --- | --- | --- |
| Existing-note reuse, baseline | Linked the existing identity and note. Preserved the reading limit and historical result. | Shared protections passed. |
| Existing-note reuse, candidate | Preserved the same behavior. Also recorded Zotero and the resolved selected-note location in the brief. | Approved default and shared protections passed. |
| Explicit project convention | Preserved the BibTeX library, wiki note, brief, and P020 identity. | Passed. No switch to the personal default. |
| Standalone abstract task | Added only the requested answer. Kept methods and results unread. | Passed. No library setup or project scaffold. |

Both paired sessions reported five local tool calls.
These results show the requested behavior in the supplied cases, without establishing a research performance gain.
No source snapshot, selected note, or package file changed during the exercises.

The [evidence file](evidence/W003.json) preserves inputs, changed outputs, hashes, and run reports.
The [change record](../changes/W003.md) preserves the passing results and the later scope rejection.
The candidate package passed the format validator, local link inspection, and plain-English scan.

The user's personal reading choices remain approved.
[W004](../changes/W004.md) moves them into local preferences and keeps a shared optional example.

The tests used explicit skill reads in the current Codex environment.
They did not exercise live Zotero tools, library writes, or native discovery in another harness.
Action counts came from the assistants' reports rather than separate runtime telemetry.

## Optional preferences and bulk literature, version 0.1.1

Test date: 2026-10-23.
Five fresh sessions exercised the generic package with synthetic local files.
The bulk baseline and candidate received identical inputs and a 15-call limit.
The three preference cases used the same limit.

| Case | Observed result | Decision |
| --- | --- | --- |
| Local preferences | Selected Library Alpha and resolved the relative note path. Preserved abstract-only depth, P007, and the old result. | Passed. |
| Project precedence | Selected Library Beta and the project's wiki over local Library Alpha. Preserved the brief and P020. | Passed. |
| No preferences | Added only the requested answer. Kept the abstract claim unresolved without library setup. | Passed. |
| Bulk baseline | Preserved duplicates, failed import, missing evidence, stale source, and the contradictory source excerpt. | Passed. |
| Bulk candidate | Preserved the same conditions and saved a corpus record with separate coverage counts and notebook handoffs. | Passed. |

Preference sessions reported six, four, and four local calls.
Both bulk sessions reported five local calls.
The tests show no measured gain in research quality or tool use.
All protected source files, historical results, and supplied skill copies retained their original hashes.

An independent review inspected the outputs against the fixed conditions.
It identified a routing sentence that omitted explicit project conventions.
The final sentence includes that choice, with a focused inspection after the edit.
Current-request precedence over a project convention and project-only bulk routing were not run as separate behavior cases.

[W004 evidence](evidence/W004.json) and [W005 evidence](evidence/W005.json) preserve the fixtures, outputs, hashes, and reports.
The final package passed metadata validation, local link inspection, and the plain-English scan.
Git ignores the actual local preferences file and does not track it.
No real corpus was exported, uploaded, imported, or analyzed through NotebookLM.

## Scripted bulk literature, version 0.1.2

Test date: 2026-10-23.
Sixteen [unit tests](test_bulk_literature.py) passed with temporary files and fake command responses.
No account login, export from a real library, or cloud operation ran.
The tests exercise the pipeline through its process boundary without installing the NotebookLM client.

The cases cover planning without effects, complete execution, source deduplication, saved citations, and repeated execution without duplicate writes.
They also cover unknown write outcomes, malformed JSON, source timeouts, degraded Drive access, query limits, and source changes.
Path traversal, symbolic links, changed configuration, unsupported client versions, and invalid saved state fail before unsafe continuation.

An independent code review found two recovery gaps that the implementation corrected.
Regression tests cover response files saved before checkpoints and changed remote content under an existing Drive ID.
The final tests also cover saved answers before checkpoints and budget rejection before remote writes.

A separate subprocess smoke test ran the default CLI with a temporary configuration.
It returned a plan and created no run directory or additional file.
The final skill passed metadata validation, local link inspection, and whitespace inspection.

[W006 evidence](evidence/W006.json) records the tested files and commands.
The source review used NotebookLM client `0.8.5` and zpm `1.3.1` contracts.
Live Google responses, account quotas, real PDF extraction, macOS, and Windows execution were not tested.
The script supports Linux and macOS locking and explicitly rejects Windows execution.

## Audit and reduction, version 0.1.3

Test date: 2026-10-23.
All 18 offline unit tests passed with temporary files and fake command responses.
The two new tests failed before the fixes and passed afterward.

Completed-run cases delete or corrupt saved indexed text and answers.
Resuming stops without repeating external writes or questions.
Coverage counts only intact outputs, and the report preserves the failure without parsing damaged answers.
The blank-answer case stops after one query and preserves its pending state on resume.
Meaningful answers without citations remain accepted as generated output.

Independent agents inspected the code diff and compared the shortened instructions with the baseline.
The wording review restored the requirement to record both passed and open stage conditions.
The package passed metadata validation, local link inspection, whitespace inspection, and the plain-English scan.
[W007](../changes/W007.md) records the documentation reduction and recovery scope.

No new assistant research exercise or live account integration ran in this round.
These results establish the tested file behavior, not improved research quality or current service compatibility.
Earlier version results remain historical evidence for their tested packages.

## README badges and Chinese translation

Test date: 2026-10-23.
The two README files, contribution guide, and scripted guide passed inspection of 57 local links and anchors.
Both README files use the same six badge images.
The version and license badges match the skill metadata and license file.
The pinned CLI packages' metadata supplied their Python requirements.
The English prose scan and whitespace inspection passed.
Shields.io returned HTTP 403 in this environment, so live badge rendering remains unverified.
No script code changed, and runtime tests were not repeated.

## Atomic JSON publication, version 0.1.4

Test date: 2026-10-23.
The baseline and candidate used Python 3.14.8 on Linux with the same 23 offline tests.
The candidate passed all 23 tests in 0.061 seconds.
The baseline produced six failing subcases.
Two exposed a partial final JSON file and missing recovery guidance.
Four covered the new publication procedure and do not establish additional defects in the old pipeline.

The new cases cover partial writes, existing outputs, remaining temporary files, publication failures, and damaged legacy answers.
Two resume attempts after a failed answer save kept the query count at one.
The pending request and original response files remained unchanged.
Existing tests still cover complete responses saved before state updates.
An independent review found and confirmed the fix for a temporary hard link left after publication.
The final review found no further required changes.
The changed documents passed inspection of 68 local links and anchors.
Skill metadata, version badges, license copies, and the changed English prose passed inspection.

[W008](../changes/W008.md) records the scope and recovery path.
The [evidence record](evidence/W008.json) contains the comparison, file hashes, and implementation patch.
No live account, macOS, power-loss, or cross-harness test ran.
These results describe local file behavior, not research quality or current service compatibility.

## Optional collaboration records, version 0.1.5

Test date: 2026-10-23.
Three synthetic tasks ran once with baseline 0.1.4 and once with candidate 0.1.5 in fresh Codex subagent contexts.
They covered two reading assignments, review after interruption, and standalone abstract reading.
A separate candidate case covered a withdrawn upstream acceptance with unchanged artifact bytes.
Each task allowed ten local tool calls and five minutes.

An independent evaluator inspected the saved files against fixed criteria.
The result was 40 pass, zero fail, and 11 uncertain across seven executions.
All 40 protected-file comparisons passed.
All supplied skill files remained unchanged during the exercises.
Both versions met the requirements that file evidence can establish.
The separate case correctly withheld downstream acceptance and kept the earlier artifacts and reviews.

The uncertain criteria prohibit actions that file snapshots cannot rule out.
Execution reports stated three or four local tool calls and no external actions per case.
Those reports lack an independent action trace and do not establish hard permission or timing limits.
Token use and cost remain unknown.
The assignment case produced three output files with the baseline and seven with the candidate.
The review case produced three with the baseline and four with the candidate.
Both standalone runs created only answer.md.
No general quality, speed, or cost improvement follows from these cases.

The new JSON templates and optional review block parsed successfully.
Inspection covered 72 local links and anchors, skill metadata, and matching version badges.
The stage guide, claim states, evolution procedure, N7 script, and its tests remained unchanged.
[W009](../changes/W009.md) records adoption of the requested optional format and its limits.
The [evidence record](evidence/W009.json) preserves task inputs, outputs, review decisions, file hashes, and the implementation patch.
No real account, second harness, runtime adapter, or operating-system isolation test ran.
The N7 unit tests were not repeated because their script and test bytes did not change.

## Read-only collaboration checks, version 0.1.6

Test date: 2026-10-23.
The baseline 0.1.5 and candidate 0.1.6 used Python 3.14.8 on Linux.
Both used this offline command from their repository roots:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

The baseline passed its 23 tests in 0.063 seconds.
The candidate passed all 61 tests in 6.562 seconds, including 38 checker tests.
Each checker test invocation compared input file bytes, inventories, and modes.
Coverage includes custom layouts, required fields, missing files, hashes, versions, dependencies, review replacement, unsafe paths, cycles, and deterministic diagnostics.
Ordinary discussion reviews and unselected legacy records remained valid.

Two fixed command cases covered a valid custom layout and a withdrawn upstream acceptance.
Both candidate outcomes matched their declared conditions without changing research files.
The baseline lacked the checker, so these commands reported a missing script.
This comparison establishes a new local checking capability, not better scientific judgments.

The independent case passed three states for a replacement that accepted the same upstream result.
The old dependency pin failed after replacement.
A new downstream revision with the new pin passed while reusing the unchanged artifact.
All record bytes and inventories remained unchanged.

Review caught JSON exponent overflow and unsafe diagnostic paths for rejected CLI selections.
The final implementation and regression checks cover both findings.
Focused probes also covered a hardlink alias, invalid UTF-8, and an escaping symbolic link in a future output path.
The new scripts passed Python 3.9 grammar inspection.
That inspection did not execute Python 3.9.
Local links, metadata, version badges, license copies, and changed English prose passed inspection.

[W010](../changes/W010.md) records adoption and the recovery path.
The [evidence record](evidence/W010.json) preserves the comparison, independent review, fixtures, outputs, file hashes, and implementation patch.
No live account, CI service, other operating system, or real research project was tested.
The command cannot prove complete review history, scientific truth, actual authority, or live job state.
Concurrent writers remain outside the tested read-only snapshot.

## Limits

Native skill discovery and full research cycles remain untested in Codex, Claude Code, Gemini CLI, and OpenCode.
The two referenced automated research repositories were read but not executed.
The workflow relies on each harness to supply tools, enforce permissions, and follow the saved procedure.
No unattended improvement loop or native Hermes or Pi integration ran.
The evolution tests did not repeat every initial research case.
Automatic adoption of a passing generated candidate remains untested as a complete cycle.
