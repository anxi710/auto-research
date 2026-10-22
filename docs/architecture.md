# Repository structure

This toolkit separates shared instructions, personal choices, research records, and development evidence.
A harness runs the assistant and supplies its tools.
The skill defines the procedure that the assistant follows.

| Location | Purpose |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Load the shared skill from different harnesses. |
| `skills/research-workflow/SKILL.md` | Select the procedure for the current task. |
| `skills/research-workflow/references/` | Hold detailed procedures and optional examples. |
| `skills/research-workflow/templates/` | Supply starting records and example configuration. |
| `skills/research-workflow/scripts/` | Hold commands that travel with the skill package. |
| `docs/` | Explain installation, use, and repository structure. |
| `tests/` | Hold behavior cases, script tests, and saved results. |
| `changes/` | Record proposals, evidence, adoption scope, and recovery paths. |
| `RESEARCH.local.md` | Store optional preferences outside Git. |
| The selected research directory | Hold research records, source inventories, and outputs. |

## Keep the skill portable

Copy the complete `skills/research-workflow/` directory when you install the skill.
Keep its `LICENSE` file with the package.
Resolve package paths from the directory that contains `SKILL.md`.

Load detailed procedures only when the task needs them.
Keep each active rule in one maintained location.
Link to that location from other documents.

The assistant handles research questions and evidence judgments.
Scripts handle repeatable file operations and tool calls.
A successful command does not establish that a research claim is correct.

## Keep choices and data separate

The shared skill supports different libraries, tools, and research conventions.
Optional examples describe setups that a user can select.
They do not become defaults when a preferences file is absent.

The [preferences guide](../skills/research-workflow/references/preferences.md) defines how requests, project conventions, and local defaults interact.
The selected research directory owns the research records.
The toolkit owns its procedures and development evidence.

Keep credentials, browser sessions, library exports, and private research files outside the distributed package.
Use placeholders in example configuration.
Use synthetic or explicitly publishable material for public examples and tests.

## Sources and maintenance

[PPT Master](https://github.com/hugohe3/ppt-master) provides a reference for this organization.
Its [skill entry](https://github.com/hugohe3/ppt-master/blob/main/skills/ppt-master/SKILL.md) selects a procedure before loading detailed instructions.
Its [documentation index](https://github.com/hugohe3/ppt-master/blob/main/docs/README.md) separates user guides from instructions inside the skill package.
This toolkit applies those organizational ideas without copying its implementation or presentation assets.

[Research-Starter-Kit](https://github.com/LAMDA-NeSy/Research-Starter-Kit) remains the main source for the research procedure.
The [source map](../skills/research-workflow/references/sources.md) explains other influences.
The [contribution guide](../CONTRIBUTING.md) describes how to propose and test changes.

The root [LICENSE](../LICENSE) covers this toolkit.
An identical [license copy](../skills/research-workflow/LICENSE) travels with the skill package.
External tools and research sources retain their own licenses and terms.
