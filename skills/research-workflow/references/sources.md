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

## Adaptations and limits

The guide includes local habits and tool-specific tips.
We retain their purpose without requiring one schedule, writing formula, tool, or harness command.
The workflow does not impose paper counts, fixed meeting intervals, or a universal experiment duration.

We retain negative and anomalous results without minimizing their effect through wording.
We use respectful, evidence-based responses instead of adversarial reviewer tactics.
We preserve valid citation metadata and apply the target venue's style at output time.

Persistent state, evidence labels, job recovery rules, budgets, and portable entry files are implementation choices in this package.
They make the guide usable across sessions and harnesses.
They do not establish that every assistant will follow the instructions or produce correct research.
