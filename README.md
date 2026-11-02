# A portable research workflow

[![Version 0.1.11](https://img.shields.io/badge/version-0.1.11-blue)](skills/research-workflow/SKILL.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python 3.11+ for bulk tools](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](#requirements)
[![zpm 1.3.1](https://img.shields.io/badge/zpm-1.3.1-blue)](skills/research-workflow/references/scripted-bulk-literature.md)
[![notebooklm-py 0.8.5](https://img.shields.io/badge/notebooklm--py-0.8.5-4285F4)](skills/research-workflow/references/scripted-bulk-literature.md)
[![rclone CLI](https://img.shields.io/badge/rclone-CLI-3F79AD)](skills/research-workflow/references/scripted-bulk-literature.md)

English | [简体中文](README.zh-CN.md)

This local candidate extends the delivery trial with [W022 synthesis and revision](changes/W022.md).
The [W023 retention regressions](changes/W023.md) test loss of earlier correct content separately from new feedback.
The [W024 format update](changes/W024.md) sets Markdown as the standard delivery format.
It is not a published release or a globally installed default.

This toolkit gives AI assistants a shared procedure for study, questions, experiments, analysis, writing, and review.
A harness is the application that runs an assistant and its tools.
Research progress stays in files so that another harness can continue the work.

The main source is [Research-Starter-Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit).
The [source map](skills/research-workflow/references/sources.md) explains its coverage and other influences, including autoresearch, AI-Scientist, Hermes, and Pi.
The workflow has detailed support for computational AI and machine learning.
It does not include an experiment scheduler or model training framework.

## Requirements

The workflow needs an assistant with file access.
The Python and tool badges apply to the optional bulk literature pipeline.

| Use | Required tools |
| --- | --- |
| Full bulk toolchain | Python 3.11+ on Linux or macOS. |
| Library export | Zotero and zpm 1.3.1. |
| Cloud transfer | rclone and a Google Drive account. |
| Literature queries | NotebookLM access and notebooklm-py 0.8.5. |

The runner itself supports Python 3.9+ and uses only the standard library.
The external tools have their own dependencies.
Install them separately with the [scripted pipeline guide](skills/research-workflow/references/scripted-bulk-literature.md#prepare-the-tools).
This repository does not need a `requirements.txt` file.
The optional [record checker](skills/research-workflow/references/collaboration.md#inspect-saved-records) uses Python 3.9+ and the standard library.
An optional [claim-evidence ledger](skills/research-workflow/references/evidence-ledger.md) binds selected claims to fixed manuscripts and structured evidence.
The checker validates references and declared context.
Support judgments remain in reviews.
Human approval follows the existing procedure.
The optional [response collector](skills/research-workflow/references/response-collection.md) keeps literal collection separate from synthesis.
It records branch gaps and fixed versions before the record checker inspects the result.

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

The researcher reviews each intermediate research output before dependent work continues.
The [human review procedure](skills/research-workflow/references/human-review.md) covers exact versions, unresolved choices, and explicit waivers with limited scope.
AI assessment and completed execution do not replace human approval.
An approved next action proceeds without repeated permission requests.

The [stage guide](skills/research-workflow/references/workflow.md#enter-a-module) defines modules that can be used separately.
Each module states its inputs, outputs, human decisions, completion evidence, and next choices.
One possible sequence is:

```text
Scope -> Study -> Question -> Design -> Run -> Analyze -> Write
```

Review can run at any stage.
Start with an existing idea in Question or Design, imported results in Analyze, or a draft in Write or Review.
Use the supplied materials without recreating unrelated earlier stages.
Missing original plans remain unknown when existing results enter the workflow.
New evidence can return the work to an earlier stage.
Failed runs and negative results stay in the project history.

After switching harnesses, use this prompt:

```text
Read the research-workflow skill and research/STATE.md.
Read the records needed for the next action.
Make sure that recorded outputs and active jobs still exist.
Restore pending human reviews and any explicit waiver before dependent work.
Continue the current task within its saved limits.
Save the result and next action in the research records.
```

Each harness supplies its own tools, credentials, and permissions.
Read the [harness guide](docs/harnesses.md) for entry files, installation, and optional skill discovery.
Read the [synthetic summation example](examples/summation-order/README.md) for a fixed plan, actual local outputs, and separate AI review.

## Choose local preferences and optional procedures

The shared skill contains no personal defaults.
You can use it without a preferences file.
For reusable choices, follow the [preferences guide](skills/research-workflow/references/preferences.md) and its [template](skills/research-workflow/templates/PREFERENCES.md).
The [Zotero and Git example](skills/research-workflow/references/zotero-git-example.md) applies only when you select it.

Researcher reports use Markdown by default, with readable evidence links and the same writing and review standards.
LaTeX sources, PDF compilation, and PDF layout inspection apply only when you explicitly request those formats.
To select a Chinese LaTeX template or return to Markdown, follow the [template guide](docs/latex-templates.md).
Its [catalog](templates/latex/README.md) lists the existing templates and dependencies.
For researcher-facing argument, synthesis, summaries, and review paths, try the separate [research-report skill](skills/research-report/SKILL.md).
It is an optional writing companion in this isolated trial, not a replacement for the workflow or a LaTeX template.

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
