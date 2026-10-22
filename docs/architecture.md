# Repository structure

This toolkit separates shared instructions, personal choices, research records, and development evidence.
Copy the complete `skills/research-workflow/` directory to reuse the skill.
Keep detailed procedures separate from its task entry point.

| Location | Purpose |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Load the skill from different harnesses. |
| `skills/research-workflow/SKILL.md` | Select the procedure for the task. |
| `skills/research-workflow/references/` | Hold procedures and optional examples. |
| `skills/research-workflow/templates/` | Supply starting records and example configuration. |
| `skills/research-workflow/scripts/` | Hold commands that travel with the skill. |
| `docs/` | Explain installation and repository structure. |
| `tests/` | Hold behavior cases, script tests, and results. |
| `changes/` | Record proposals, evidence, decisions, and recovery paths. |
| `RESEARCH.local.md` | Store optional preferences outside Git. |
| The selected research directory | Hold research records and outputs. |

The assistant handles research questions and evidence judgments.
Scripts handle repeatable file operations and tool calls.
A successful command does not establish that a research claim is correct.

The [preferences guide](../skills/research-workflow/references/preferences.md) defines how users select local choices and optional examples.
Keep credentials, library exports, and private research outside the distributed package.
Use placeholders or publishable material in public examples.

[PPT Master](https://github.com/hugohe3/ppt-master) informed this organization.
Its [skill entry](https://github.com/hugohe3/ppt-master/blob/main/skills/ppt-master/SKILL.md) loads task-specific instructions.
Its [documentation index](https://github.com/hugohe3/ppt-master/blob/main/docs/README.md) separates user guides from skill instructions.
This toolkit uses those ideas without copying its implementation or presentation assets.

Read the [source map](../skills/research-workflow/references/sources.md) for research influences.
Follow the [contribution guide](../CONTRIBUTING.md) for changes and tests.
The root [MIT license](../LICENSE) also travels with the [skill package](../skills/research-workflow/LICENSE).
External tools and sources retain their own licenses and terms.
