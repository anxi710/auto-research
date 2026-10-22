# A portable research workflow

This repository gives AI assistants a shared research procedure.
A harness is the application that runs an assistant and its tools.
The workflow keeps research progress in files so that another harness can continue the work.

The main source is [Research-Starter-Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit).
The package turns its advice into tasks, records, completion conditions, and return paths.
It also uses selected patterns from `karpathy/autoresearch` and `SakanaAI/AI-Scientist`.

The current scope is personal research, with detailed support for computational AI and machine learning.
The workflow covers study, questions, tests, writing, and discussion.
It does not include an experiment scheduler or model training framework.

## Start a research task

Open this repository in Codex, Claude Code, Gemini CLI, or OpenCode.
Use the prompt below and replace the values in angle brackets.
The target repository holds the research work, not the workflow package.

```text
Read skills/research-workflow/SKILL.md and use it for this task.
The target research repository is <path>.
My topic or seed paper is <topic or paper>.
My current task is <task>.
Use <language> for research records.
Read existing research records before creating new ones.
Start from the stage that the task needs.
```

For a new project, the assistant creates `research/STATE.md` and `research/BRIEF.md` in the target repository.
For an existing project, it reads those records and their evidence first.
For a standalone reading task, it creates only the requested output.

If the target uses another record layout, the assistant keeps that layout.
If a tool or source is unavailable, the assistant records the limit.
It must not turn an unrun experiment into a reported result.

## Choose the work

These are natural-language requests, not custom shell commands.
The skill selects the stage from your request and the saved evidence.
You can enter the workflow at any stage.

| Request | What the assistant does | Main output |
| --- | --- | --- |
| Start a project in this topic. | Define the goal, resources, limits, and next useful task. | Research brief and state. |
| Read this paper for my question. | Explain the problem, method, evidence, and open questions. | A paper record. |
| Find the closest work. | Search sources and compare assumptions and results. | A literature record. |
| Turn these observations into a question. | Compare explanations and define a testable hypothesis. | A question record. |
| Design the smallest useful test. | Fix the comparison, metrics, resources, and stop conditions. | An experiment plan. |
| Run this experiment within this budget. | Implement the test and preserve commands, code versions, and outputs. | An experiment record. |
| Analyze these results. | Assess the comparison and state what the evidence supports. | Analysis and a claims record. |
| Draft a paper from these records. | Build an argument that links each claim to evidence. | A draft, figures, and evidence gaps. |
| Prepare a meeting or response to reviewers. | Organize evidence, questions, responses, and next actions. | A review or discussion record. |
| Continue the project. | Inspect saved state, outputs, and active jobs before taking the next action. | Updated state and the requested work. |

## Follow the research loop

```text
S0 Scope -> S1 Study -> S2 Question -> S3 Design -> S4 Run -> S5 Analyze -> S6 Write
               ^           ^            ^                       |            |
               |           |            +-----------------------+------------+
               +-----------+------------------------------------+

S7 Review can run at any stage. Its decisions update the next action.
```

The loop returns to earlier stages when evidence changes the decision.
A failed run can require an implementation repair.
A negative result can support a decision to stop an approach.
Neither result disappears from the project history.

The [stage guide](skills/research-workflow/references/workflow.md) defines inputs, actions, outputs, completion conditions, and return paths.
These conditions test the evidence available for a decision.
They do not require user approval at every stage.

## Use files to continue the work

Research files are the shared record between harnesses.
The package keeps them separate from the skill's instructions.
Create each record only when its stage needs it.

```text
target-repository/
  research/
    STATE.md
    BRIEF.md
    LITERATURE.md
    CLAIMS.md
    MANUSCRIPT.md
    papers/
    questions/
    experiments/
    reviews/
```

Code, data, raw logs, and drafts can stay in their existing project directories.
The research records link to those files.
The state file records active jobs so that a new assistant does not launch duplicate work.

Use this prompt after switching harnesses:

```text
Read the research-workflow skill and research/STATE.md.
Read the records needed for the next action.
Make sure that recorded outputs and active jobs still exist.
Continue the current task within its saved limits.
Save the result and next action in the research records.
```

Browser sessions, credentials, tools, and permissions do not move with these files.
Each harness supplies its own tools.
Read the [harness guide](docs/harnesses.md) for entry files, copy instructions, and optional skill discovery.

## Read the package

The root files load one shared procedure.
The reusable skill contains all stage rules and templates.
Copy its complete directory when you use it in another repository.

| File or directory | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Shared project entry for research tasks. |
| [CLAUDE.md](CLAUDE.md) | Import of the shared entry for Claude Code. |
| [GEMINI.md](GEMINI.md) | Import of the shared entry for Gemini CLI. |
| [SKILL.md](skills/research-workflow/SKILL.md) | Task routing, records, tools, and session rules. |
| [Stage guide](skills/research-workflow/references/workflow.md) | Procedures for S0 through S7. |
| [Templates](skills/research-workflow/templates/) | Starting files for real research records. |
| [Source map](skills/research-workflow/references/sources.md) | Guide coverage, repository references, and design choices. |
| [Behavior tests](tests/scenarios.md) | Small tasks for testing another harness. |
| [Test results](tests/RESULTS.md) | Observed behavior and the limits of the current tests. |

The package uses plain English for portable instructions.
The assistant uses your requested language for research records and conversation.
The source map distinguishes source advice from this package's added procedures.
