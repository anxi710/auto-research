# Use the workflow with different harnesses

A harness runs an AI agent and its tools. A skill is a reusable set of task instructions. A repository holds the files for a versioned project.

This guide uses official documentation reviewed on 2026-10-22. The file layout follows the documented loading rules. We did not run a full research task in each harness.

The reusable package is `skills/research-workflow/`. Its `SKILL.md` file defines the workflow. Its `references/` directory contains detailed instructions. Its `templates/` directory contains files that start new research records.

The plain `skills/` directory does not register the skill with a harness. The project entry files tell the agent to read it. This approach needs no installer or change to global configuration.

## Use this repository

Open this repository in your harness. Use this prompt:

```text
Read skills/research-workflow/SKILL.md and follow its workflow.
Use this target research repository: <path to the research repository>.
First read research/STATE.md in that directory, if it exists.
Then continue the current task.
Separate assumptions from decisions that need my input.
My task is: <research task>.
```

This repository contains the workflow package. Editing the package does not start a research project. Give the agent a target research directory when you start research.

The root entry files share one set of project rules:

| Harness | Entry file | How this package loads |
| --- | --- | --- |
| Codex | `AGENTS.md` | The project rules tell the agent to read `skills/research-workflow/SKILL.md` for research tasks. |
| Claude Code | `CLAUDE.md` | `@AGENTS.md` imports the shared project rules. |
| Gemini CLI | `GEMINI.md` | `@./AGENTS.md` imports the shared project rules. |
| OpenCode | `AGENTS.md` | The project rules tell the agent to read the skill. File paths alone do not load their content. |

Codex reads project `AGENTS.md` files. An `AGENTS.override.md` file takes priority in the same directory. The start directory and parent rules also affect loading. See the [Codex project rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

Claude Code supports `@` imports in `CLAUDE.md`. Some current versions also read `AGENTS.md` directly. The import supports sessions where direct loading is unavailable. See the [Claude Code project instructions](https://code.claude.com/docs/en/memory).

Gemini CLI loads `GEMINI.md` and supports relative `@` imports. Its configuration and workspace trust affect the available context. See the [Gemini CLI project instructions](https://geminicli.com/docs/cli/gemini-md/).

OpenCode uses `AGENTS.md` before the fallback `CLAUDE.md`. It does not expand ordinary file references in `AGENTS.md`. The shared rules explicitly tell the agent to read the skill. See the [OpenCode rules](https://docs.opencode.ai/docs/rules/).

If the harness cannot read local files, attach `SKILL.md` and the files needed for the current task. If it cannot write files, save its research records yourself. The agent must state which records it did not save.

## Copy the workflow to a research repository

Keep the package files together. Paths inside the skill use the directory that contains `SKILL.md` as their starting point. Research outputs use the target research repository as their starting point.

Copy the package with these steps:

1. Copy the complete `skills/research-workflow/` directory to the same path in the target repository.
2. Merge the research entry rules from this repository into the target `AGENTS.md`.
3. If you use Claude Code, add `@AGENTS.md` to the target `CLAUDE.md`.
4. If you use Gemini CLI, add `@./AGENTS.md` to the target `GEMINI.md`.
5. Start a new session at the root of the target repository.
6. Send the research prompt from the previous section.

If an entry file does not exist, create it. If an import already exists, keep one copy. Do not replace existing project rules or local changes.

Keep `references/` and `templates/` with `SKILL.md`. If you move the package, update the skill path in the project rules. Keep the template files unchanged when you create research records.

Research records belong in `research/` in the target repository. The file `research/STATE.md` stores progress for the next session. It lets another harness resume the work without the previous chat history.

You can give the copy task to a harness that can read and write files:

```text
Copy <workflow repository>/skills/research-workflow into skills/ in the current research repository.
If that skill already exists, compare the files before merging changes.
Keep existing research records and local changes.
Merge the research entry rules into AGENTS.md.
Add the short entry file for my harness.
Keep global configuration unchanged.
Make sure that every local file referenced by SKILL.md exists.
```

To resume the work, open the same research repository in another harness. Send this prompt:

```text
Read skills/research-workflow/SKILL.md and research/STATE.md.
Restore the research state from the saved records.
Review completed work, evidence paths, open questions, and the next action.
Then continue the current task.
Do not treat a missing experiment log as evidence that an experiment ran.
```

The package transfers the workflow. Saved records transfer research progress. Browser logins, tool connections, permissions, and chat history do not transfer with the files.

## Optional automatic skill discovery

Skill discovery lets a harness find available skills. The default method above uses explicit file reads. Use a discovery directory only if you want the native skill menu or automatic selection.

Each path below starts at the target repository. Place the complete `research-workflow/` directory inside it. The final path must end with `research-workflow/SKILL.md`.

| Harness | Project skill directory | Behavior |
| --- | --- | --- |
| Codex | `.agents/skills/` | It searches from the current directory to the repository root. See the [skill documentation](https://learn.chatgpt.com/docs/build-skills). |
| Claude Code | `.claude/skills/` | Local project sessions support automatic selection and `/research-workflow`. Cloud project sessions use different loading rules. See the [skill documentation](https://code.claude.com/docs/en/skills). |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | Workspace skills require trust. `/skills list` shows available skills. `/skills reload` reloads them. Activation requires consent. See the [tutorial](https://geminicli.com/docs/cli/tutorials/skills-getting-started/) and [management guide](https://geminicli.com/docs/cli/using-agent-skills/). |
| OpenCode | `.opencode/skills/`, `.agents/skills/`, or `.claude/skills/` | Its `skill` tool loads permitted skills. A same-name slash command needs separate support. See the [skill documentation](https://docs.opencode.ai/docs/skills/). |

Keep one maintained copy of the skill. If you move it into a discovery directory, update the path in the project rules. Duplicate skill names can produce different results across harnesses.

The `.agents/skills/` directory serves Codex, Gemini CLI, and OpenCode under the documented rules. Do not assume that Claude Code searches it. Use the explicit entry file or its documented `.claude/skills/` directory.

This delivery does not write to the restricted project `.agents/` or `.codex/` directories. It does not install global files or change harness configuration. The discovery paths are optional locations for a target repository where you have write permission.

## Required tools and first-use test

The workflow defines tasks, outputs, and decision rules. The files do not open a browser, search papers, or run experiments. The harness provides those tools.

MCP connects an agent to external tools. Each harness needs its own tool connections and permissions. The workflow does not assume that all harnesses provide the same capabilities.

| Task | Required capability | If the capability is absent |
| --- | --- | --- |
| Find and read papers | Search and access to full text, or supplied paper files | Use accessible material and record the search limits. |
| Read a page that requires login | An authorized browser session | Ask the user to log in or supply an export. |
| Save research progress | Read and write access to the research repository | Return the records and state that they remain unsaved. |
| Run an experiment | A shell, dependencies, data, and required computing resources | Prepare the design and implementation. Mark the experiment as not run. |
| Divide work among agents | Support for additional agents | Complete the same tasks in sequence. |

Use a small task for the first session. Make sure that the agent can read the skill and one template. Make sure that it can read existing research state and save a record in the target repository.

If `research/STATE.md` does not exist, follow the initialization rules in the skill. Do not infer that a research project already exists. If file access fails, resolve the path, permission, or tool problem first.

This package received documentation review and static file adaptation. We did not test native discovery, permission prompts, or a full research cycle in all four harnesses. A copied skill is not proof that these operations work in your environment.
