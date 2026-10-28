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

## Offline CI and package checks

Test date: 2026-10-23.
Package version: `0.1.6`, unchanged.
This change adds repository checks and CI without changing the portable skill.
uv 0.13.5 created temporary environments for Python 3.9.25 and 3.14.8 on Linux.
Both environments had no installed third-party packages.
The Python 3.9 runtime download occurred before the offline tests.

Each environment ran this command on the baseline and candidate copies:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

The baseline passed its 61 tests on both Python versions.
The candidate passed 69 tests on both versions, including eight package tests.
The new tests cover local links, heading anchors, root entries, simple metadata, version badges, and matching license files.
Temporary examples cover invalid inputs, valid syntax, scope exclusions, and unchanged inspected bytes.

Two fixed faults exposed gaps in the baseline suite.
A missing local target and a changed badge image passed the baseline and failed the candidate.
The candidate reported the expected package errors and preserved file contents and inventories.
An independent reviewer fixed five additional cases before inspecting the implementation.
All ten baseline and candidate runs matched the expected outcomes.
The candidate accepted valid composed Markdown and detected four faults that the baseline missed.
Those runs preserved file hashes, modes, and directory membership.
All 61 existing behavior tests passed in every independent run.

Local YAML inspection and independent review found no remaining issue within the declared scope.
The workflow uses Ubuntu 24.04 with Python 3.9 and 3.14, read-only repository permissions, and fixed action commits.
Its test step runs the same command without dependency installation or research services.
Runner setup can download GitHub Actions and Python.
No hosted workflow run occurred, so Ubuntu runner behavior remains unverified.

[W011](../changes/W011.md) records adoption, official action sources, and the recovery path.
The [evidence record](evidence/W011.json) preserves environment details, test outputs, fault comparisons, independent review, hashes, and the exact patch.
The package checks support the repository's current Markdown and frontmatter forms.
They do not establish full parser conformance, native skill loading, or external link availability.
No real research, remote job recovery, or additional operating system was tested.

## Hosted CI follow-up

Test date: 2026-10-23.
The user authorized a push after the local N5 round.
The [first hosted run](https://github.com/anxi710/auto-research/actions/runs/39963595136) passed for commit `57a9dd309bb8e8d914c439cffb12998f6fd731d1`.
Python 3.9.25 passed 69 tests in 8.016 seconds.
Python 3.14.8 passed 69 tests in 10.557 seconds.
Both jobs used Ubuntu 24.04 and completed every workflow step successfully.
Runner setup downloaded Python 3.9 and upgraded pip before the offline test command.
The [hosted evidence](evidence/W011-hosted-ci.json) preserves job identities, results, and log excerpts.
This run tested the push event, not the pull request event.
It did not test real research services or other operating systems.

## Harness capability map

Inspection date: 2026-10-23.
Package version: `0.1.6`, unchanged.
The user approved N6 after the hosted CI follow-up.
The candidate maps DSH Agent Teams and the Codex Desktop tools exposed in this session.
DSH evidence comes from installed version `0.2.1-rc.2` and pinned official source.
Codex evidence separates declared tools from observed reviewer creation, reports, and follow-up work.
The [change record](../changes/W012.md) states the scope and adoption decision.
The [evidence record](evidence/W012.json) preserves source identities and actual inspection results.
Python 3.14.8 passed all eight package tests with the command below.

```bash
python3 -B -m unittest discover -s tests -p 'test_package.py' -v
```

Five fixed independent documentation cases passed.
Seven upstream source digests and fourteen installed file digests matched.
A draft README source-match flag was corrected after an exact byte comparison.
No review finding remains open.
The portable skill and prior evidence files remained unchanged.
No DSH team, interruption, restart, cross-harness recovery, or real research service was tested.
The earlier hosted CI runs predate N6 and do not validate this documentation change.

## Complete synthetic example

Test date: 2026-10-23.
Package version: `0.1.6`, unchanged.
The user approved P1 after N6.
The [example](../examples/summation-order/README.md) contains a fixed plan, actual local outputs, claims, and separate AI acceptance.
One measured run used CPython 3.14.8 and the standard library on Linux.
It produced 12 ordering rows and 24 method outputs across two synthetic datasets.
The methods tied in eight orderings.
The other four orderings had errors 1 and 0 for the plain loop and `math.fsum` respectively.
The report retains those ties and the opposed strict-improvement claim.

An independent AI reviewer fixed six criteria before inspecting the new code and output.
Separate rational calculations checked all 24 outputs and exact errors.
One clean replay reproduced all 7,798 output bytes.
All 12 protected example files remained unchanged.
The existing record checker returned exit code `0` with no diagnostics.
The [review](../examples/summation-order/reviews/R001.md) accepted the exact submitted result.
No repair run occurred.

The baseline passed 69 tests on Python 3.14.8.
The candidate passed 72 tests on Python 3.9.25 and 3.14.8 with the existing offline command:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

Three new tests cover decimal binary references, rejected input, and unchanged saved evidence with valid acceptance.
They use separate inputs or inspect saved output instead of repeating the measured experiment.
A supplemental probe found a missing example link that the baseline ignored and the candidate reported.
An integration review found a possible bytecode write inside the sealed attempt when tests omit `-B`.
The corrected source loader avoids that write, and the evidence test checks module loading without `-B`.
Both full suites include that regression check.

[W013](../changes/W013.md) records adoption and the recovery path.
The [evidence record](evidence/W013.json) preserves scope, actual checks, review references, hashes, and the integration patch.
The portable skill, CI configuration, and local N6 changes remained unchanged.
No new hosted CI run, DSH team, interruption, or cross-harness recovery test ran.
This synthetic AI review does not establish human endorsement, research novelty, general superiority, or a multi-agent benefit.
Assistant token and cost use remain unknown.

## Human review, version 0.1.7

Test date: 2026-10-23.
The active repository package remained `0.1.6` during the isolated trial.
The user approved the reviewed `0.1.7` candidate after the trial.
The [W014 record](../changes/W014.md) states the adopted scope and actual approval.
The [evidence record](evidence/W014.json) preserves actual artifacts, fixed criteria, independent assessments, logs, and the candidate patch.

The ten fixed worked cases produced five passes, three partial results, and two failures on the baseline.
The first candidate produced nine passes and one partial result.
Both versions passed all ten criteria in the separate H01 case.
H01 supports preservation of existing behavior, not a measured candidate advantage.
Each version used one fresh context for its worked cases and another fresh context for H01.

The partial candidate result waited for human review but created unnecessary project records.
A routing clarification kept standalone outputs and decision fields in the requested location.
Three focused replays passed the unchanged idea, existing-approval, and standalone-reading criteria.
Twenty input and artifact integrity assertions passed independent review.
The other seven cases and H01 were not rerun after the clarification.
Original outputs and the partial result remain preserved.

The baseline passed all 72 offline tests on Python 3.14.8.
The candidate passed all 72 on Python 3.9.25 and 3.14.8 before the wording clarification.
Final package checks cover the completed documentation and links.
The scripts, task and result schemas, CI configuration, and sealed P1 records remain unchanged.
All researcher messages in the behavior cases are synthetic fixtures.
No real approval capture, mandatory execution gate, long-context trial, hosted CI run, or complete research cycle ran.
The adopted procedure specifies cooperative behavior and does not technically prevent an assistant from bypassing review.
After user approval, the adopted package passed all eight package checks on Python 3.14.8.
The adoption checks also matched every runtime instruction and behavior case to its reviewed candidate digest.
They preserved unrelated local work and earlier evidence.

## Stage module adoption

Test date: 2026-10-24.
Baseline package: `0.1.7`.
Adopted repository package: `0.1.8`.
The user authorized the next stage-interface round after reviewing the remaining work.
The [W016 record](../changes/W016.md) states its scope and the later human adoption decision.
The [evidence](evidence/W016.json) preserves inputs, actor outputs, independent assessments, source hashes, and the candidate patch.

The eight fixed main cases passed on both the baseline and candidate.
Each version used one fresh actor context for its eight separate case directories.
This comparison does not show a success-rate improvement.
Independent static review found all eight module interfaces complete and the prior completion conditions preserved.
The candidate removes implicit requirements for earlier records and retains imported materials with their missing history.

Both first H01 runs passed their behavior criteria but used a flattened input path and lower limits than the frozen plan.
Both versions received those delivery errors.
The original outcomes remain preserved as limited evidence.
A recorded correction restores the original paths and limits for a fresh paired H01 replay.
The corrected result remains separate from those first runs.

Both corrected H01 runs passed all five original criteria under independent review.
Each version passed eight main cases and one correctly delivered independent case.
The corrected paths, source bytes, and artifact digests matched.
Both actual runs stayed within the original limits.
The candidate RUN records actual use but omits limit fields, which remain in the correction record and actor instruction.

The baseline and candidate each passed eight package checks on Python 3.14.8.
Final package checks cover the completed documentation and evidence links.
The scripts, their tests, task and result JSON, human review procedure, and collaboration procedure remain unchanged.
The full offline suite was not repeated during this documentation round.

All research materials and researcher decisions in these cases are synthetic fixtures.
No native skill-loading test, full paper cycle, long-context trial, hosted CI run, or cross-harness recovery ran.
The candidate does not implement execution gates or new agent assignment modes.

The user approved adoption after reviewing the candidate summary and evidence.
The adoption preserved unrelated local work and earlier evidence.

## Phase 0 / 1 isolated candidate

Test date: 2026-10-25.
Baseline: `512f6d4c4b737d57677c47a562d0a6aef7e3d38e`, version `0.1.8`.
Reviewed candidate: `0.1.9`; later adopted as recorded below.
The [W017 record](../changes/W017.md) states the scope and decision boundary.
The [evidence record](evidence/W017.json) records actual commands, counts, code hashes, corrections, and remaining limits.

Run the full offline suite from the repository root:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

| Checked tree | Python | Tests | Result | Seconds |
| --- | --- | --- | --- | --- |
| Original baseline | 3.12.14 | 72 | Passed | 5.320 |
| Phase 0 / 1 candidate | 3.12.14 | 116 | Passed | 12.814 |
| Phase 0 / 1 candidate | 3.13.5 | 116 | Passed | 12.597 |

The Python 3.13 run used `/usr/bin/python3` with the same arguments.
The candidate suite contains 23 bulk, 50 record, 29 ledger, eight package, three summation, and three ledger-example tests.
These counts come from this run, not earlier CI results.

Independent review passed 21 Phase 0 probes and 93 Phase 1 CLI cases on Python 3.12.14.
The Phase 1 review used a separate forecast fixture and preserved all input bytes and modes.
The initial Phase 0 candidate mishandled inline-code and escaped comment markers.
The corrected parser passed the unchanged independent cases.
The delivery evidence retains the initial failures and the later correction.

The Phase 1 baseline comparison used 24 frozen tests.
It recorded 74 test/subtest failures because the old checker lacked the new feature.
The candidate passed the same 24 tests and five additional boundary tests.
Two independent probe expectations changed only their diagnostic labels after inspection.
The input fixtures and required acceptance or rejection outcomes stayed fixed.

The checker covers references, file hashes, unique quotes, declared measurement context, and explicit review scope.
It does not prove scientific support, source authenticity, reading depth, human approval, or complete review history.
The small review parser is not a complete Markdown implementation.
Python 3.9 syntax passed an AST grammar check for eight files.
Python 3.9 and 3.14 runtime tests, hosted CI, and real research integration did not run.
No external research service, model trial, or paid experiment ran.
No real research data was uploaded.
All 49 historical change, test-evidence, and sealed summation files remain unchanged.

## Decimal correction after parent review

The parent reviewer found precision loss in the first delivered Phase 1 candidate.
The checker accepted four distinct numeric bindings after both files were pinned with correct hashes.
The earlier 116-test result remains valid for its recorded cases but did not establish exact numeric comparison.
The correction uses exact decimal parsing and preserves the earlier input-range rejection rule.
The [format guide](../skills/research-workflow/references/evidence-ledger.md#bind-an-experiment-to-structured-measurements) states that rule and its limits.

Seven added test methods preserve raw JSON number tokens without converting them through Python floats.
The pre-fix focused run reproduced 16 assertion failures.
After correction, all 36 ledger tests passed on Python 3.12.14.
The same full-suite command then produced these results:

| Corrected candidate | Python | Tests | Result | Seconds |
| --- | --- | --- | --- | --- |
| Exact decimal parser | 3.12.14 | 123 | Passed | 14.829 |
| Exact decimal parser | 3.13.5 | 123 | Passed | 15.137 |

These two runs executed concurrently and do not measure performance gains.
The new total retains all other test counts and increases ledger tests from 29 to 36.
Independent review passed 44 frozen numeric CLI cases and all 93 earlier structural cases on the corrected implementation.
The numeric cases cover underflow, adjacent decimals, large integer equality, nested conditions, booleans, range limits, and JSON diagnostics.
All fixtures remained unchanged.
The original false acceptance outputs remain in the updated review packet beside the corrected outputs.
During candidate correction, no original repository file or sealed example changed.

## W017 adoption verification

The user approved the final Phase 0 / 1 candidate for the original cloud worktree.
The approved source is Library file `libfile_742990423cf48191bf128045570867aa`, version `2`.
The [W017 decision](../changes/W017.md#adoption-and-recovery) records the exact approval source and limits.
Package `0.1.9` is now applied in `/workspace/auto-research` without a commit.
The original HEAD and clean worktree were checked before application.
All 25 candidate files matched the approved hashes before adoption records were updated.

The full offline command above ran again in the adopted worktree.
The Python 3.13 run again used `/usr/bin/python3`.

| Adopted worktree | Python | Tests | Result | Seconds |
| --- | --- | --- | --- | --- |
| Phase 0 / 1 | 3.12.14 | 123 | Passed | 14.842 |
| Phase 0 / 1 | 3.13.5 | 123 | Passed | 15.093 |

The two runs executed concurrently in separate temporary fixtures.
The durations do not establish a performance change.
The independent reviewer reran the same 44 frozen numeric CLI cases; all passed.
Their inputs and scoring stayed unchanged, and all outputs remained valid JSON without stderr or traceback.
The implementation and test code match the approved candidate byte for byte.
Only W017, its evidence record, and this summary gained adoption updates.
All 49 historical files and all 10 approved example files retain their hashes.
All nine Python files in the three-script and six-test scan passed the Python 3.9 grammar check.
Python 3.9 and 3.14 runtime tests remain unrun.
No commit, push, pull request, merge, publication, or external research run occurred.

## Additional source documentation

Test date: 2026-10-26.
Baseline: remote `main` at `512f6d4c4b737d57677c47a562d0a6aef7e3d38e`, package `0.1.8`.
The source map adds four reviewed candidates with fixed references and license notes.
All 17 added external links returned HTTP 200.
The full offline suite passed all 72 tests on Python 3.12.14.
Final package checks passed all eight tests after this results entry was added.
The diff passed `git diff --check` and manual scope inspection.
Only the source map and this required test record changed.
No third-party project execution, behavior trial, or native harness integration ran.
Hosted CI results are reported separately on the pull request.

## Version 0.1.9 draft PR integration

Test date: 2026-10-26.
[W018](../changes/W018.md) records the later authorization to integrate the adopted package into draft PR 1.
The source is Library version 3, not a new implementation of the earlier proposal.
Its complete patch reconstructed all 25 adopted files with matching manifest hashes in a temporary baseline tree.
The integrated tree preserves 24 files byte for byte; this file combines both histories and adds this entry.
All 93 baseline files outside the adopted patch and source map remain unchanged.
The source map now links implemented ideas to their local procedures and checker while retaining deferred candidates.

The full offline command ran on the integrated tree with separate temporary fixtures:

| Python | Tests | Result | Seconds |
| --- | --- | --- | --- |
| 3.12.14 | 123 | Passed | 10.606 |
| 3.13.5 | 123 | Passed | 10.753 |

These concurrent runs do not measure a performance gain.
The suite includes the HTML-comment, exact Decimal binding, review scope, legacy compatibility, and sealed-example checks.
Final package checks passed all eight tests after this entry was added.
All 21 newly introduced external URLs returned HTTP 200.
The complete diff passed whitespace and scope inspection.
Historical W017 approval limits and all earlier test records remain intact.
No new independent behavior trial, external research service, or native harness integration ran.
The earlier 44-case numeric replay remains historical evidence and was not rerun in this integration.
Hosted CI results are reported on the updated draft PR after push.

## W019 isolated dual-delivery trial

Test date: 2026-10-27.
Baseline: `06e6c0fb82037ffa95be3d22480c6fe182761324`, package `0.1.9`.
Candidate: `0.1.10-dual-delivery.1` in the isolated trial clone.
The [change record](../changes/W019.md) fixes five behavior cases and the allowed scope before candidate edits.

Both versions ran the existing offline command on Python 3.12.14:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

| Version | Tests | Result | Test runner seconds |
| --- | --- | --- | --- |
| Baseline | 123 | Passed | 20.540 |
| Candidate | 123 | Passed | 21.280 |

These results check package links, metadata, record formats, ledger behavior, and sealed examples.
They do not compare model behavior or measure a research improvement.
No new checker, record schema, or mirrored instruction-string test was added.
The human-review and stage rules retain their baseline bytes.
An independent read-only context inspected the delivery instructions and template.
It identified an ambiguity about sealed result artifacts, which the candidate now explicitly preserves.
Final package and patch checks were recorded in a local implementation packet that retains command output and exact file hashes.
That private packet is not included in the public repository.
The five matched model cases remain unrun.
Native harness loading, PDF generation, remote CI, and global installation were not exercised here.
Status remains trial; adoption is not authorized by these checks.

## W021 report-writing companion trial

Test date: 2026-10-27.
The [change record](../changes/W021.md) fixes one synthetic writing case before the candidate edit.
The prior W019/W020 working snapshot is the baseline.
The optional companion is `research-report` version `0.1.0-trial.1`.
The workflow entry and matching README badges use candidate `0.1.10-dual-delivery.2`.

The baseline snapshot had passed 126 offline tests in W020.
The candidate passed 129 offline tests on Python 3.12.14 in 17.333 test-runner seconds.
The three new tests cover companion metadata/UI consistency, self-contained copy links, and the included license.
Skill Creator's `quick_validate.py` accepted the candidate.
These checks do not assess argument quality, comprehension, scientific support, or human permission.
The existing human-review, stage, delivery, and collaboration procedures retain their baseline bytes.
All vendored template files retain their W020 bytes.
The bounded writing comparison and its limits are recorded in W021 separately from these mechanical checks.
Draft pull request integration repeated all 129 tests on Python 3.12.14 in 19.125 test-runner seconds.
That integration did not repeat the writing comparison.
Native automatic discovery, personal skill installation, and remote publication remain unrun.

## General limits

Native skill discovery and full research cycles remain untested in Codex, Claude Code, Gemini CLI, and OpenCode.
The two referenced automated research repositories were read but not executed.
The workflow relies on each harness to supply tools, enforce permissions, and follow the saved procedure.
No unattended improvement loop or native Hermes or Pi integration ran.
The evolution tests did not repeat every initial research case.
Automatic adoption of a passing generated candidate remains untested as a complete cycle.

## W022 collection, synthesis, and revision trial

Test date: 2026-10-28.
The [change record](../changes/W022.md) defines the local candidate scope.
The baseline `b0306c6` passed 130 tests on Python 3.12.14 in 15.134 seconds.
The isolated collection stage passed 147 tests in 19.663 seconds.
Its seventeen new tests run collection through the existing record consumer.
They cover missing branches, truncated JSON, unfinished execution, duplicate submissions, stale sources, and existing review history.
The candidate preserves partial coverage instead of inferring acceptance for missing branches.
The [run evidence](evidence/W022.json) records observed results and limits.

The isolated synthesis stage passed 157 tests in 18.377 seconds.
Its fixed bundle covers five evidence problems and includes literal and wording-only controls.
The [content review](evidence/W022-synthesis-review.json) distinguishes correct retained facts from missing joint reasoning.
The [mechanical comparison](evidence/W022-synthesis.json) measures declared finding matches, not scientific quality.
The controls' missing findings are not zero factual accuracy.
The original reviewed snapshot remains in the fixture history after technical binding corrections.

The isolated revision stage passed 169 tests in 18.793 seconds.
Four actual CLI replays compare full and local-only corrections for two frozen cases.
Both full corrections passed, while both local-only controls reported stale downstream content.
The initial preservation-criteria gap and the corrected comparison remain in the development history.
A fresh native actor also revised both initial cases without the authored candidates or rubric.
Both native results passed the record checker after copying into the repository.
An independent reader found substantive corrections and preserved useful content in both cases.
The [native evidence](../evaluations/native-revision/README.md) retains drafts, dependency plans, failures, unknown resource use, and the content review.
One native invocation across two cases does not establish general revision reliability.

The isolated architecture stage passed 171 tests in 19.143 seconds.
The [native comparison](../evaluations/native-architecture/REPORT.md) completed fourteen model calls over two repeats of one heldout synthetic case.
Strong single-agent and synthesis outputs tied across the four content dimensions in both repeats.
Literal collection retained correct evidence but lacked some explicit joint reasoning.
The report preserves variation, evaluator uncertainty, a resolved capacity denial, and resource measurement limits.
Sequential scheduling ran. Parallel scheduling, equal-token comparison, and complete efficiency measurement did not run.
