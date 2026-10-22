# Use the workflow with different harnesses

A harness runs an assistant and supplies its tools.
The portable package is `skills/research-workflow/`.
The plain `skills/` directory does not register it automatically.
Project entry files tell the assistant to read its `SKILL.md`.

This guide follows official documentation reviewed on 2026-10-22.
Native discovery, permission prompts, and full research cycles remain untested across all four harnesses.
Use the [start prompt](../README.md#start-or-resume-research) with a selected research repository.

## Load the shared rules

| Harness | Entry file | Loading rule and documentation |
| --- | --- | --- |
| Codex | `AGENTS.md` | Project rules request an explicit skill read. A same-directory `AGENTS.override.md` takes priority. [Project rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md). |
| Claude Code | `CLAUDE.md` | `@AGENTS.md` imports the shared rules. [Project instructions](https://code.claude.com/docs/en/memory). |
| Gemini CLI | `GEMINI.md` | `@./AGENTS.md` imports the shared rules. [Project instructions](https://geminicli.com/docs/cli/gemini-md/). |
| OpenCode | `AGENTS.md` | Rules request an explicit skill read. Ordinary file references do not load content. [Project rules](https://docs.opencode.ai/docs/rules/). |

The start directory, parent rules, and harness configuration can affect loading.
If local file access is unavailable, attach `SKILL.md` and the files needed for the task.
If the harness cannot write files, save its returned records yourself.
The assistant must identify unsaved records.

## Copy the package into a research repository

Copy the workflow with these steps:

1. Copy the complete `skills/research-workflow/` directory to the same path in the target repository.
2. Merge the research entry rules from [AGENTS.md](../AGENTS.md) into the target `AGENTS.md`.
3. If you use Claude Code, add `@AGENTS.md` to the target `CLAUDE.md`.
4. If you use Gemini CLI, add `@./AGENTS.md` to the target `GEMINI.md`.
5. Start a new session at the target repository root.
6. Send the start prompt from the README.

If an entry file is absent, create it.
If an import exists, keep one copy.
Preserve existing project rules and local changes.
Keep the package's references, templates, scripts, and license together.
If you move the package, update its path in the project rules.

Research records stay in the target repository.
Use the README's resume prompt after switching harnesses.
Browser logins, tool connections, permissions, and chat history do not transfer with these files.

Each package copy evolves independently.
Before updating a copy, compare its local changes.
Follow the [evolution procedure](../skills/research-workflow/references/evolution.md) for updates.
Personal preferences stay separate from the package.
Read the [preferences guide](../skills/research-workflow/references/preferences.md) before reusing them across workspaces.
Other repositories need their own ignore rule for private preferences.

## Optional automatic discovery

Use discovery only when you want a native skill menu or automatic selection.
Place the complete `research-workflow/` directory inside one of these project directories.
The final path must end with `research-workflow/SKILL.md`.

| Harness | Project skill directory | Documentation |
| --- | --- | --- |
| Codex | `.agents/skills/` | [Skills](https://learn.chatgpt.com/docs/build-skills) |
| Claude Code | `.claude/skills/` | [Skills](https://code.claude.com/docs/en/skills). Cloud project sessions use different loading rules. |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | [Tutorial](https://geminicli.com/docs/cli/tutorials/skills-getting-started/) and [management](https://geminicli.com/docs/cli/using-agent-skills/). Workspace skills require trust and activation consent. |
| OpenCode | `.opencode/skills/`, `.agents/skills/`, or `.claude/skills/` | [Skills](https://docs.opencode.ai/docs/skills/). A same-name slash command needs separate support. |

Keep one maintained copy.
If you move it into a discovery directory, update the project entry path.
Use an explicit file read when discovery is unavailable.
This toolkit does not install global files or native Hermes or Pi hooks.

## Test the first session

The harness needs file access plus the tools required by the task.
Paper searches need search and source access.
Experiments need a shell, dependencies, data, and computing resources.
The assistant records missing access or execution as a limit, never as a completed result.

Use a small task for the first session:

1. Make sure that the assistant can read `SKILL.md` and one template.
2. Make sure that it can read existing research state, if present.
3. Make sure that it can save a record in the target repository.

If file access fails, resolve the path, permission, or tool problem first.
Use the skill's initialization rules when research state is absent.
