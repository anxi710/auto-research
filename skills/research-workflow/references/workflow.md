# Stage guide

Use only the stages that the current task needs.
Treat a completed stage as a supported decision, not a permanent result.
If new evidence changes that decision, propose a return to the relevant stage.

Apply [human review](human-review.md) to every research output, including AI review reports.
A stage's completion conditions describe evidence readiness, not permission for dependent work.
Present the output version and proposed next actions before crossing that review point.
Use an existing approval or explicit waiver only within its recorded scope.
A standalone output can end the requested task without an unrelated next action.

## S0: Define the scope

Input: The user's goal, existing project, or seed paper.
Output: `BRIEF.md` and `STATE.md`.
Use the matching [templates](../templates/).

1. Separate the broad topic from the question that the project can answer.
2. Record the intended outcome and the user's current starting point.
3. Record available data, code, tools, compute, time, and spending limits.
4. Record known restrictions and existing authorization.
5. Identify the smallest useful next task.

Present unresolved research choices and ask for the researcher's decision.
Ask for missing context or evidence that the requested task needs.
Keep unknown facts explicit after the decision.
Do not turn a publication goal into a promise of acceptance.

For literature work, record the chosen primary library and selected-note location in `BRIEF.md`.
Use local preferences only when the current request and project do not specify the choice.
Keep access status separate from the chosen library.

Complete this stage when the next task and its limits are clear.
If the question is unknown, propose S1 to gather evidence for one.
If the topic is unknown, ask for a topic or seed paper.

## S1: Find and understand the literature

Input: A topic, question, or seed paper.
Output: `LITERATURE.md`, existing note links, or task-specific paper records.
A baseline is a reference method for comparison.
A benchmark is a shared task and evaluation procedure.

Inspect available library entries and existing notes before creating another record.
If access is unavailable, use supplied evidence and record the lookup limit.
Do not require library setup for a narrow reading task.

If the task selects NotebookLM for a large collection, use [the bulk literature procedure](bulk-literature.md).
Keep its corpus record linked from the project's literature record when one exists.

1. Start from sources that directly address the topic.
2. Expand through references, later citations, related methods, and benchmark results.
3. Record search terms, search date, inclusion reasons, and access limits.
4. Make sure that each paper's title, authors, and source link are real.
5. Group papers by the problem or mechanism that they address.
6. Select close readings that can change the current research decision.

Do not use venue rank or citation count as the sole inclusion rule.
Do not invent a fixed paper quota.
Stop the search when the decision has enough relevant coverage within the task budget.
Record what the search did not cover.

Reuse stable library identities and links to existing notes.
Add only the analysis that the current task needs.
Use a local paper record when no existing note fits or the task needs separate analysis.
Keep a selection reason with each selected note.
Store comparisons and research judgments across papers in a topic summary.
An existing `LITERATURE.md` comparison can serve as that summary.

Keep metadata maintenance in the chosen primary library.
Use links or a dated export for metadata in project records.
Record actual reading depth and source locations independently of library tags.

For each close reading, follow these steps:

1. Read the abstract and inspect the figures to identify the work's scope.
2. State the research question in plain language.
3. Describe previous solutions and the claimed remaining problem.
4. Record an independent possible solution before studying the method in detail.
5. Explain the proposed method from input to output.
6. Examine the data, baseline choices, metrics, and experimental conditions.
7. Record questions, failure cases, and links to related work.

If the user already knows the method, label the independent solution as retrospective.
For a central paper, inspect its implementation when available.
If reproduction can change a decision, create an experiment record in S3.
Reproduction is a new run that attempts to recover a reported result.

Complete this stage when the requested paper is understood or the research question has a usable evidence map.
Record source locations for important claims.
If only an abstract is available, retain the limited reading status.
If papers disagree, record their differing assumptions and propose a test in S2.

## S2: Choose a question and hypothesis

Input: Literature records, observations, failed runs, or a practical need.
Output: A question record linked to its sources.
Use [QUESTION.md](../templates/QUESTION.md).

1. State the observed limitation without assuming its cause.
2. Explain who needs an answer and what the answer can change.
3. Compare the question with the closest existing work.
4. State a hypothesis and at least one plausible alternative explanation.
5. Define evidence that can support or oppose the hypothesis.
6. Choose the smallest test that can distinguish the explanations.

Look for failures, unexplained successes, conflicting findings, or unmet practical needs.
Use an existing method only when it fits the question.
Do not treat a combination of methods as a contribution by itself.
Keep the problem narrow enough for the available resources.

Complete this stage when the question is specific, useful, testable, and feasible.
Label any unresolved claim of novelty.
If existing work already answers the question, revise it or treat the task as reproduction.
If the question lacks observable consequences, revise it before implementing a method.

## S3: Design the test

Input: A question record and known resources.
Output: The plan section of an experiment record.
Use [EXPERIMENT.md](../templates/EXPERIMENT.md).

1. State the decision that the test will inform.
2. Link the hypothesis and the alternative explanation.
3. Specify data, comparison methods, metrics, and relevant controls.
4. Define the evaluation conditions before viewing the test results.
5. Define a minimum run that can reveal implementation errors.
6. Record the run budget, stop conditions, and analysis plan.
7. Record the expected files, commands, and environment information.

A protocol is the fixed set of evaluation rules.
Give the protocol a version in the experiment record.
If those rules change, start a new comparison series.
Keep earlier results linked to their original protocol.

A control holds another possible cause fixed.
Keep data splits, evaluation code, and resource conditions comparable across methods.
If conditions differ, record the difference before interpreting the result.
Do not tune on data reserved for final evaluation.

Select extra experiments from the claims that need support.
An ablation removes or replaces one part to study its effect.
Use ablations, failure cases, sensitivity tests, or cost measurements when they answer a specific question.
Do not require every experiment type for every project.

For theoretical work, use a derivation or counterexample as the test.
Record assumptions, proof steps, and the result instead of training metrics.
Mark fields that do not apply and give the reason.

For stochastic results, record the repeat plan and the uncertainty that the resources can support.
If a plan changes after viewing results, label the change as exploratory.
Exploratory analysis develops ideas from observed results.
Do not present that analysis as a test specified in advance.

Complete this stage when the planned comparison can answer the question within known limits.
If the baseline is untrusted, plan reproduction before interpreting improvements.
If important data or compute is unavailable, report the missing resource and a bounded alternative.

## S4: Implement and run

Input: An experiment plan and the required execution access.
Output: Code changes, run records, logs, and result files.
Use the execution section of the same experiment record.

1. Inspect the project's implementation and all affected callers.
2. Make the smallest change that implements the test.
3. Run a small test for the changed behavior.
4. Make sure that inputs, outputs, metrics, and data splits match the plan.
5. Run the planned experiment within the recorded limits.
6. Record the command, environment, code version, configuration, and seed when relevant.
7. Save raw outputs and record the actual exit status.

If the code contains uncommitted changes, save the diff with the run record.
Do not reset the user's work to recover an experiment.
Preserve the failed run before changing the implementation.
If a metric is missing or non-finite, mark the attempt as invalid.

If a run continues after the session, record its host, job ID, and status command.
Record the exact cancellation command when the execution system provides one.
If a session restarts, inspect that job before launching another run.
If the job cannot be inspected, mark its state as unknown.
Do not treat an unknown job as stopped.

Complete this stage when the planned run ends with traceable outputs or a recorded failure.
Completion of execution does not prove the hypothesis.
If the run fails, classify the cause before choosing a retry.
Use a bounded retry only when it can resolve that cause.
For an experiment batch, follow its limit on runs and repair attempts.
Do not change fixed evaluation files to improve the measured score.

## S5: Analyze and decide

Input: Actual result files and the experiment plan.
Output: Analysis in the experiment record and updates to `CLAIMS.md`.
Use [CLAIMS.md](../templates/CLAIMS.md) when the project first forms conclusions.

1. Make sure that the recorded run used the planned evaluation conditions.
2. Compare the method with the baseline under those conditions.
3. Calculate the metric and uncertainty that the data supports.
4. Separate observed differences from explanations of those differences.
5. Examine failures, contradictory results, and resource costs.
6. State what the evidence supports, opposes, or leaves unresolved.
7. Propose the next action and record its reason for human review.

Do not infer causation from a performance difference alone.
Do not claim statistical significance without the required analysis.
If a single run cannot establish stability, state that limit.
If the test did not address the hypothesis, return to S3.

A negative result can complete the test.
Revise the hypothesis, retain the negative finding, or stop the line of work.
Do not change the metric after the result solely to create an apparent gain.
Keep exploratory results separate from the original test.

Complete this stage when the decision cites actual outputs and states its limits.
If a contribution lacks evidence, keep it unproven in `CLAIMS.md`.
If the baseline or comparison is invalid, correct that problem before judging the idea.

## S6: Write the paper or report

Input: The question, method, literature records, claims, and result files.
Output: `MANUSCRIPT.md`, a draft, figure sources, and references.
Use [MANUSCRIPT.md](../templates/MANUSCRIPT.md).
Apply the shared review rule to the outline, draft sections, figures, and complete manuscript.

1. Identify the audience, target format, and intended contribution.
2. Build an outline from the supported claims.
3. Map each claim to an experiment, analysis, or source location.
4. Explain the problem, previous work, remaining gap, and contribution.
5. Describe the actual method from input to output.
6. Explain the experiments and their limits.
7. Make sure that the draft, figures, equations, and implementation agree.
8. Make sure that each citation exists and supports the nearby statement.

Use each section for its own purpose:

| Section | Required content | Reason to return to an earlier stage |
| --- | --- | --- |
| Abstract | Problem, main idea, measured result, and relevant conditions. | The result does not answer the stated problem. |
| Introduction | Why the problem matters, the specific gap, and supported contributions. | The gap or contribution lacks evidence. |
| Related work | Groups of approaches and the relation to the closest work. | The closest work is unread or the difference is unclear. |
| Method | Formulation, inputs, outputs, operations, and reasons for the design. | The explanation disagrees with the implementation. |
| Experiments | Setup, fair comparisons, claim-specific tests, and limits. | A comparison cannot support the claim. |
| Discussion and conclusion | Supported findings, limits, and open questions. | The text expands beyond the tested conditions. |

Define each symbol when it first appears.
Distinguish training from inference when the method uses both.
Explain why each module exists and where its effect is tested.
Use the target venue's reference style instead of a universal formatting rule.

Generate result figures from saved data.
Keep the plotting source and the path to its input data.
Label illustrations separately from measurements.
Make sure that labels, units, scales, and comparisons preserve the result.
Start each figure with the one message that its caption must explain.
Make sure that the figure remains readable at its final display size.

Record author contributions and publication decisions from the researchers.
Do not invent authorship, affiliation, or permission to submit.
If the user requests an early draft, mark unsupported claims and missing results as unresolved.
Do not fill those gaps with plausible numbers or citations.

Complete this stage when the requested draft has traceable claims and explicit evidence gaps.
A submission-ready draft cannot contain unresolved central evidence gaps.
If the argument needs a new experiment, return to S3 with a specific question.

## S7: Review, discuss, and respond

Input: Research records, a draft, a meeting request, or reviewer comments.
Output: A review record and updates to the affected research files.
Use [REVIEW.md](../templates/REVIEW.md).

For a review, follow these steps:

1. State whether the reviewer is an AI simulation or an actual person.
2. Examine the question, closest work, method, comparison, and evidence limits.
3. Record each concern with its affected claim and evidence location.
4. Assign a concrete response, analysis, or experiment to each material concern.
5. Make sure that each resolved concern links to an actual change.

Do not present simulated review as peer review or publication approval.
If an unresolved concern changes the conclusion, revise that conclusion.
Route missing evidence to S3 or S5 before polishing the wording.

For a meeting or talk, follow these steps:

1. Identify the audience, time available, and decisions needed.
2. Review the previous actions and explain their outcomes.
3. Explain the problem and the latest evidence in a short outline.
4. Show the method's input, output, and role of each main part.
5. Record unknowns, failed attempts, and alternatives before the discussion.
6. Record actual decisions, owners, and next actions after the discussion.

If the discussion did not occur, leave its decisions pending.
Make sure that diagrams reflect the method's logic.
Match the level of detail to the audience.
Treat font sizes and presentation ratios as examples, not research completion conditions.
Use a meeting to discuss uncertainty even when there is no positive result.
Choose a meeting schedule with the researcher instead of imposing a fixed interval.

For a response to reviewers, map every material comment to a direct answer.
Separate existing evidence from new analysis and planned experiments.
Do not claim that a proposed experiment is complete.
Use the venue's actual response rules when available.
Admit factual errors and link their corrections.
Keep responses factual and respectful.
Do not replace missing evidence with claims about a reviewer's motives.

Complete this stage when the requested review, discussion record, or response is traceable.
Keep unresolved disagreements visible.
Update `STATE.md` with the next action and its owner.
