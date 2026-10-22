# Sources and design choices

Source review date: 2026-10-22.
The workflow paraphrases the sources below.
It does not copy their manuals or source code.

The main guide targets researchers who are starting work in AI.
This package turns its advice into procedures for an AI assistant.
Stage IDs, record names, completion conditions, and return paths are this package's design.

## Research-Starter-Kit

The [repository README](https://github.com/LAMDA-NeSy/Research-Starter-Kit) links to the guide's Feishu documents.
We read the core text through an authorized browser session.
We used document text, not the site's generated summaries, for the rules below.

| Source | Distilled rule | Workflow location |
| --- | --- | --- |
| [How to do research](https://dy8q0bnq8y.feishu.cn/wiki/LfR9woW57iWpQWkRKJhcoFF7ndb) | Move from a topic to a problem, an idea, and concrete evidence. | S0 to S5. |
| [Find papers](https://dy8q0bnq8y.feishu.cn/wiki/Co5awLsRiiuYAlkqHhCcwGBanub) | Expand from seed papers through citations, groups, methods, and benchmarks. | S1 and `LITERATURE.md`. |
| [Read papers](https://dy8q0bnq8y.feishu.cn/wiki/Ow8fw2HtEiixDgkWlkbckdvHnef) | Find the problem, consider a solution, inspect the method, and question the evidence. | S1 and `PAPER.md`. |
| [Find ideas](https://dy8q0bnq8y.feishu.cn/wiki/MxYVwN0lEiv5HUkLEJccRJI3nTd) | Study failures, mechanisms, contradictions, and practical needs. | S2 and `QUESTION.md`. |
| [Academic presentations](https://dy8q0bnq8y.feishu.cn/wiki/Wr0lwNhUdiMpt1kK6UmcgnWEnJI) | Explain the problem, method, evidence, limits, and relevance to the audience. | S7 and `REVIEW.md`. |
| [Meetings](https://dy8q0bnq8y.feishu.cn/wiki/B8FBwaHe6ivi2skemtFc3lWbnmh) | Review previous actions, discuss evidence and uncertainty, and record the next actions. | S7, `STATE.md`, and `REVIEW.md`. |
| [Research habits](https://dy8q0bnq8y.feishu.cn/wiki/Bp2AwrSnAiGaH2khJaqczVXznwc) | Save reading questions, experiment details, failures, and the next small test. | S1 to S5 and persistent records. |
| [Paper writing](https://dy8q0bnq8y.feishu.cn/wiki/NsK3wnWeiivKNukNJOqcd985nTY) | Connect the problem, prior work, contribution, evidence, and limits. | S6 and `MANUSCRIPT.md`. |
| [Figures](https://dy8q0bnq8y.feishu.cn/wiki/OGpcw6zaRiQ6OwkNxfYcl7IKnBh) | Define a figure's message and keep its data or method source traceable. | S6 and the figure table. |
| [Abstract](https://dy8q0bnq8y.feishu.cn/wiki/Tz2pwvxTyiBK0zkCVszcZmJ3nwd) | Connect the stated problem to the method and the actual result. | S6 section requirements. |
| [Introduction](https://dy8q0bnq8y.feishu.cn/wiki/ULATwBu2MiLqqRkXxV6c2S7AnPd) | State a specific gap and contributions that the evidence can support. | S6 section requirements. |
| [Related work](https://dy8q0bnq8y.feishu.cn/wiki/CLSAwWm6qifjwQkTd82czgMNnYf) | Group approaches and explain the relation to the closest work. | S1 and S6. |
| [Methods](https://dy8q0bnq8y.feishu.cn/wiki/CtiAwh1eOiqOfCkPKVLc0WsxnZg) | Explain inputs, outputs, operations, symbols, and reasons for each part. | S6 method requirements. |
| [Experiments](https://dy8q0bnq8y.feishu.cn/wiki/KHgSw2MkrikxlskGe5qclkdbn2c) | Use fair comparisons and claim-specific tests with reproducible conditions. | S3 to S5 and `EXPERIMENT.md`. |
| [References](https://dy8q0bnq8y.feishu.cn/wiki/A4q2wSnmRi91rykHke1cQIhnnAh) | Inspect citation metadata and keep the reference format consistent. | S6 citation requirements. |
| [Rebuttal](https://dy8q0bnq8y.feishu.cn/wiki/M9d1wv5Efi2aG4kH4IDc5zqVnQh) | Answer each material concern with evidence or a clear limitation. | S7 and the response table. |
| [AI research tips](https://lamda3-nju.feishu.cn/wiki/Uf9fwnQFxiJS1akJZkPc87gFniq) | Set concrete goals, preserve context, and inspect actual code and results. | Session rules and persistent records. |

We read these sections' text.
We did not inspect every example image or follow every linked tool, video, or paper.
Conference attendance and scholarship advice are outside this version's research execution scope.

## Existing automated research projects

The following links use fixed commits from the source review.
We read the listed instructions and implementation files.
We did not install or run these projects.

### karpathy/autoresearch

Read the [README](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/README.md) and [program.md](https://github.com/karpathy/autoresearch/blob/228791fb499afffb54b46200aca536f79142f117/program.md).
The project separates human-maintained experiment rules from editable training code.
It uses a fixed evaluation, a starting baseline, and a compact record for each experiment.

This workflow uses those mechanisms in S3, S4, and `EXPERIMENT.md`.
It records fixed files, protocol versions, code versions, outputs, and decisions.
Its completion conditions depend on the research question instead of one universal score.

We do not copy the default endless loop or automatic branch resets.
We also do not assign zero as a result for a crashed run.
A failed run has an execution status and no valid measurement.

### SakanaAI/AI-Scientist

Read the [README](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/README.md), [launcher](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/launch_scientist.py), and stage implementations.
The implementation stores experiment code and results, writes from research notes, and saves a separate AI review.
It also defines experiment and repair limits.

The relevant stage files cover [experiments](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/ai_scientist/perform_experiments.py), [ideas](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/ai_scientist/generate_ideas.py), [writing](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/ai_scientist/perform_writeup.py), and [review](https://github.com/SakanaAI/AI-Scientist/blob/1de1dbc1f4ee2c5f61e9c94348d55eb51d7fa2eb/ai_scientist/perform_review.py).
This workflow adopts bounded runs, saved evidence, and a separate review record.
It adds a claims table and explicit inspection of active jobs before resuming.

The project's saved idea files do not establish recovery from every interrupted run.
Its AI review is not an audit of all raw experimental evidence.
This workflow does not treat an AI score as scientific confirmation.

## Hermes and Pi

We read the official documentation and selected implementation files at the commits linked below.
We did not install or run either harness.
These mechanisms inform [the evolution procedure](evolution.md).

### Hermes

Hermes can turn user input into skills through [`/learn`](https://github.com/NousResearch/hermes-agent/blob/dc0fe3e476a06cfa9c0cb289f3604b0f80bc2734/website/docs/user-guide/features/skills.md).
Its [background review](https://github.com/NousResearch/hermes-agent/blob/dc0fe3e476a06cfa9c0cb289f3604b0f80bc2734/agent/background_review.py#L390-L516) favors reusable lessons and updates to existing skills.
Its [memory guide](https://github.com/NousResearch/hermes-agent/blob/dc0fe3e476a06cfa9c0cb289f3604b0f80bc2734/website/docs/user-guide/features/memory.md) separates short facts and preferences from procedures that load when needed.
Its [skill ledger](https://github.com/NousResearch/hermes-agent/blob/dc0fe3e476a06cfa9c0cb289f3604b0f80bc2734/tools/skill_ledger.py#L569-L633) records changes and supports recovery.
Its [curator](https://github.com/NousResearch/hermes-agent/blob/dc0fe3e476a06cfa9c0cb289f3604b0f80bc2734/website/docs/user-guide/features/curator.md#L125-L178) also supports recovery from a saved group of changes.

We adopt scoped lessons, small updates, and recoverable change records.
We permit a review to leave the workflow unchanged.
The inspected learning path does not require fixed behavioral comparisons before each skill update.
Our baseline comparison and adoption conditions are additions to that design.

### Pi

The former `badlogic/pi-mono` repository redirects to `earendil-works/pi`.
Pi's [core design](https://github.com/earendil-works/pi/blob/74f46864025c68504cd10c89eeb626b7e3d64cea/README.md) keeps the harness small and supports extensions.
Its [skills](https://github.com/earendil-works/pi/blob/74f46864025c68504cd10c89eeb626b7e3d64cea/packages/coding-agent/docs/skills.md) load full instructions when needed.
Its [extension events](https://github.com/earendil-works/pi/blob/74f46864025c68504cd10c89eeb626b7e3d64cea/packages/coding-agent/docs/extensions.md) expose user input, tool results, and completed turns.
Its [sessions](https://github.com/earendil-works/pi/blob/74f46864025c68504cd10c89eeb626b7e3d64cea/packages/coding-agent/docs/sessions.md) preserve conversation branches.
Its [agent loop](https://github.com/earendil-works/pi/blob/74f46864025c68504cd10c89eeb626b7e3d64cea/packages/agent/README.md) supports an explicit decision to continue or finish a turn.

We adopt a small core, optional procedure loading, feedback capture, and bounded trials.
Conversation branches do not replace file snapshots or patches.
Fixed evaluation cases, comparisons, and adoption rules belong to this toolkit's design.
These source mechanisms do not establish reliable self-improvement or better research outcomes.

## Bulk literature tools

Source review date: 2026-10-23.
The user supplied the Zotero, zpm, rclone, Google Drive, and NotebookLM pattern as an optional example.
We inspected installed command help and selected source files without running exports or cloud operations.
The source code confirmed zpm 1.3.1 and the local command reported rclone 1.75.2.

[Zotero Project Manager](https://github.com/sbilmis/zotero-project-manager) exports ordinary collection workspaces.
Its installed `cli.py`, `exporter.py`, `metadata.py`, and package documentation define the flags and metadata used here.
Exports include attachment identities, collection memberships, destination paths, states, and hashes.
Repeated exports can update files, and collection membership can produce duplicate attachments.
The workflow therefore records dated exports and an explicit upload selection.
This is a procedure design, not evidence of a completed large-library run.

The [rclone copy guide](https://rclone.org/commands/rclone_copy/) states that copies preserve destination-only files.
The [sync guide](https://rclone.org/commands/rclone_sync/) documents destination deletion.
The [check guide](https://rclone.org/commands/rclone_check/) describes file comparison and `--one-way`.
We use selected copies and comparisons for each new transfer destination.

NotebookLM's [limits](https://support.google.com/notebooklm/answer/16213268?hl=en) vary by plan.
Its [FAQ](https://support.google.com/notebooklm/answer/16269187?hl=en) describes source limits and retrieval from large source sets.
The [source guide](https://support.google.com/notebooklm/answer/16215270?hl=en) describes bulk Drive import and current source update controls.
Google's current help redirects to Gemini Notebook pages and describes automatic Drive updates with manual sync controls.
The procedure requires inspecting the actual imported version because account behavior and supported source types can differ.

The [chat guide](https://support.google.com/notebooklm/answer/16179559?hl=en) explains source selection and clickable citations.
The [notebook guide](https://support.google.com/notebooklm/answer/16206563?hl=en) describes separate notebooks and exported reports or tables.
One notebook cannot jointly query another notebook's sources.
The workflow combines saved evidence across notebooks and inspects original passages before using findings in research claims.
These source capabilities do not guarantee exhaustive coverage or accurate extraction of every scan, equation, or table.

### NotebookLM command-line adapter

The scripted procedure uses [notebooklm-py v0.8.5](https://github.com/teng-lin/notebooklm-py/releases/tag/v0.8.5).
It is a third-party client built on undocumented interfaces.
The inspected source commit is `50493ddf9f9eb9230de998d3dff8565243383078`.
We did not identify an official consumer CLI in the reviewed documentation.

The [command reference](https://github.com/teng-lin/notebooklm-py/blob/v0.8.5/docs/cli-reference.md) defines notebook creation, Drive imports, source waits, and JSON answers.
The [exit-code contract](https://github.com/teng-lin/notebooklm-py/blob/v0.8.5/docs/cli-exit-codes.md) distinguishes source wait timeouts from failed or uncertain writes.
We inspected the corresponding command renderers, source serializers, error handlers, and chat types.
The script retains source IDs and returned citation text instead of treating citation offsets as plain-text positions.

Google's [Enterprise notebook API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) requires separate Enterprise configuration.
It is not a drop-in API for the selected personal-account workflow.
The adapter's local tests use fake command results and do not establish live service compatibility.

## Adaptations and limits

The user approved the literature division from the local `paper-I-love/WORKFLOW.md` as their personal default on 2026-10-23.
The source defines Zotero as the primary library and Git as the home for selected notes and summaries.
The [optional example](zotero-git-example.md) shares that convention without activating it for every user.
[Local preferences](preferences.md) keep each user's choices separate from shared instructions.
This is a user-approved convention, without a measured claim of better research outcomes.

The guide includes local habits and tool-specific tips.
We retain their purpose without requiring one schedule, writing formula, tool, or harness command.
The workflow does not impose paper counts, fixed meeting intervals, or a universal experiment duration.

We retain negative and anomalous results without minimizing their effect through wording.
We use respectful, evidence-based responses instead of adversarial reviewer tactics.
We preserve valid citation metadata and apply the target venue's style at output time.

Persistent state, evidence labels, job recovery rules, budgets, and portable entry files are implementation choices in this package.
They make the guide usable across sessions and harnesses.
They do not establish that every assistant will follow the instructions or produce correct research.
