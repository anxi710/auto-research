# A portable research workflow

This toolkit gives AI assistants a shared procedure for study, questions, experiments, analysis, writing, and review.
A harness is the application that runs an assistant and its tools.
Research progress stays in files so that another harness can continue the work.

The main source is [Research-Starter-Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit).
The [source map](skills/research-workflow/references/sources.md) explains its coverage and other influences, including autoresearch, AI-Scientist, Hermes, and Pi.
The workflow has detailed support for computational AI and machine learning.
It does not include an experiment scheduler or model training framework.

## Start or resume research

Open this repository in your harness.
Replace the values below with your task and target research repository:

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
For an existing project, it keeps the record layout and reads the saved evidence first.
For a standalone task, it creates only the requested output.

The [stage guide](skills/research-workflow/references/workflow.md) defines the research loop:

```text
Scope -> Study -> Question -> Design -> Run -> Analyze -> Write
```

Review can run at any stage.
New evidence can return the work to an earlier stage.
Failed runs and negative results stay in the project history.

After switching harnesses, use this prompt:

```text
Read the research-workflow skill and research/STATE.md.
Read the records needed for the next action.
Make sure that recorded outputs and active jobs still exist.
Continue the current task within its saved limits.
Save the result and next action in the research records.
```

Each harness supplies its own tools, credentials, and permissions.
Read the [harness guide](docs/harnesses.md) for entry files, installation, and optional skill discovery.

## Choose local preferences and optional procedures

The shared skill contains no personal defaults.
You can use it without a preferences file.
For reusable choices, follow the [preferences guide](skills/research-workflow/references/preferences.md) and its [template](skills/research-workflow/templates/PREFERENCES.md).
The [Zotero and Git example](skills/research-workflow/references/zotero-git-example.md) applies only when you select it.

For dozens or hundreds of papers, use the [bulk literature procedure](skills/research-workflow/references/bulk-literature.md).
It describes an optional Zotero, zpm, rclone, Google Drive, and NotebookLM setup.
The [scripted pipeline guide](skills/research-workflow/references/scripted-bulk-literature.md) covers installation, execution, recovery, and output inspection.
Its NotebookLM client, `notebooklm-py`, is third-party software that uses undocumented interfaces.
Generated answers require original-paper inspection and do not establish complete evidence coverage.

For workflow ideas or improvements, follow the [evolution procedure](skills/research-workflow/references/evolution.md).
It separates proposals, local choices, project conventions, and shared rules.
Behavior changes use a bounded comparison with saved evidence and a recovery path.
The package supplies no background worker or native Hermes or Pi extension.

## Develop and share

Read the [repository structure](docs/architecture.md) and [contribution guide](CONTRIBUTING.md) before editing.
The [test results](tests/RESULTS.md) distinguish observed behavior from untested claims.
Toolkit instructions use plain English.
Research records use your requested language.

This toolkit uses the [MIT license](LICENSE).
The complete skill package includes its own [license copy](skills/research-workflow/LICENSE).
External tools and research sources retain their own licenses and terms.
