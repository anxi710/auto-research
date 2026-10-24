# Use the workflow with different harnesses

A harness runs an assistant and supplies its tools.
The portable package is `skills/research-workflow/`.
The plain `skills/` directory does not register it automatically.
Project entry files tell the assistant to read its `SKILL.md`.

The loading instructions below follow official documentation reviewed on 2026-10-22.
Native discovery, permission prompts, and full research cycles remain untested across the four harnesses in the loading tables.
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

## Map collaboration capabilities

This section was reviewed on 2026-10-23.
It maps DSH Agent Teams and the Codex Desktop tools available in this session.
A tool declaration describes an interface, not a completed runtime test.
Use the [collaboration procedure](../skills/research-workflow/references/collaboration.md) for ownership, records, acceptance, and recovery.

The DSH column uses installed package version `0.2.1-rc.2` and official source commit `687f282e8625c6b8d11ff58211a90524be2e4317`.
The [Team tools](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/experimental/tool-agent-team/src/index.ts) define the calls and result fields.
The [Team runtime](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/experimental/agent-team/README.md) describes persistence, errors, and shared files.
The [Team bundle](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/experimental/agent-team-profile/README.md) is experimental and disabled by default.
Package presence does not establish that a running DSH session enables it.
No DSH team ran during this inspection.

The Codex column uses the current session's tool declarations.
This session spawned separate reviewers, received their reports, and used `collaboration.followup_task` to continue a reviewer.
Cancellation, restart recovery, and isolated worktrees were not tested.
These observations do not establish the interface of another Codex session or release.
The installed CLI reports `0.163.0`, which does not identify the Desktop collaboration service version.

| Capability | DSH Agent Teams | Codex Desktop in this session |
| --- | --- | --- |
| Create a worker | Lead-only `spawn_teammate` accepts a unique name, description, prompt, and optional `fresh` or `fork` context. The default is `fresh`. | `collaboration.spawn_agent` creates a child. `fork_turns` selects inherited history or no history. Creation and report delivery were observed. |
| Send a message | `send_message` steers a running member or starts an inactive member. `{sent:true}` confirms inbox acceptance only. | `collaboration.send_message` queues a message without starting an idle agent. `collaboration.followup_task` can start an idle agent. |
| Wait or join | `wait_agent` waits for new activity. It returns `timedOut` or immediate `noProgress` when no peer can progress. It is not a completion join. | `collaboration.wait_agent` reports mailbox activity, timeout, or user interruption. `collaboration.list_agents` lists live agent status. Neither establishes research acceptance. |
| Cancel | Lead-only `interrupt_agent` interrupts a turn. Configuration can disable it. It retains the inbox and task owner. | `collaboration.interrupt_agent` interrupts the current turn and returns the previous status. The agent remains available. This call was not tested here. |
| Persist and resume | Team membership and task records use the Lead session store. Stored teammates can resume. Accepted but unlogged messages can be lost after a crash. | The exposed collaboration interface gives no cross-restart recovery guarantee for child handles. Cross-harness recovery was not tested. |
| Isolate writes | Members share a directory and filesystem. Write scopes are advisory. Team tools create no worktrees, file locks, or automatic merges. | Child agents share the working directory and filesystem. Separate conversation contexts do not isolate file writes. |
| Measure use | Team result schemas expose no complete token or cost ledger. Member, task, and message capacity limits do not enforce research budgets. | Collaboration results expose no complete token or cost ledger. No per-agent usage measurement was recorded. |
| Read every page | `team_task_list` returns `nextCursor`. Its default limit is 50 and maximum is 100. `list_agents` returns the roster without paging. | The child-agent tools expose no paged history reader. Separate app task readers use cursors, as described below. |
| Detect truncation | The Team adapter renders complete JSON at its own layer. Truncation elsewhere in the harness was not tested. | Shell output can report truncation under `max_output_tokens`. A truncated read occurred here, followed by narrower reads. |

DSH `fork` copies completed Lead turns through its [fork provider](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/subagent/subagent-fork-in-process/README.md).
It does not create a separate filesystem.
The [subagent service](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/subagent/subagent/README.md) describes stored child recovery and process-local execution ownership.
One Team cannot use concurrent writers in separate processes as a supported recovery strategy.
Neither backend's worker interruption establishes that an external experiment stopped or that all later writes are impossible.

Use the tools actually exposed in the active session.
If worker tools are absent, follow the procedure's [sequential fallback](../skills/research-workflow/references/collaboration.md#choose-responsibilities).
Follow its [recovery rules](../skills/research-workflow/references/collaboration.md#resume-within-the-existing-limits) before replacing work with an unknown outcome.
The same rules define unknown usage and the total budget across workers.

## Handle partial results and tool errors

A cursor identifies where a paged read continues.
For DSH task lists, follow each returned `nextCursor` until no cursor remains.
The pages are not a frozen snapshot, so read the current task revision before an update.
The task board remains a runtime view, not the authority for research acceptance.

Codex app tasks and child agents use different tools.
`codex_app.read_thread` exposes `cursor`, `turnLimit`, `includeOutputs`, and `maxOutputCharsPerItem` for app task history.
`codex_app.wait_threads` exposes `afterCursor` for progress notifications.
Those declarations do not provide a child-agent history reader.
Their paging behavior was not tested in N6.
For truncated file output, request the missing range or read the saved file in smaller parts.
If required content remains unavailable, state the gap before relying on it.

These responses apply the existing collaboration limits to tool failures.
They are guidance from inspected interfaces, not results of injected runtime failures.
Do not translate every backend failure into one generic retry.

| Observation | Next action |
| --- | --- |
| Invalid arguments or unsupported fields | Read the active tool schema and correct the arguments. DSH Team creation does not accept per-call model, directory, or token-budget fields. |
| DSH `TEAM_TASK_STALE_REVISION` | Read the current task and reconcile the change before an update. A runtime revision is separate from the research contract revision. |
| DSH `TEAM_MESSAGE_TOO_LARGE` or capacity limits | Shorten the message or reduce new assignments. Repeating the same call does not remove the limit. |
| Missing pages or truncated content | Read the supported remaining pages or ranges. Keep unresolved gaps explicit. |
| Temporary read failure | Retry within the approved limits when the failure is temporary. A wait timeout does not prove that a worker failed. |
| Permission refusal or DSH `TEAM_LEAD_REQUIRED` | Stop dependent work and resolve the required authority. Do not use another tool to bypass the refusal. |
| Unknown send, write, or execution outcome | Inspect the saved records and target state before another request. Follow the procedure's recovery rules for external jobs. |

DSH Team errors can carry stable codes, but storage and child-service failures can also produce other errors.
The Codex collaboration declarations provide no common failure-code catalog.
Preserve the actual error and the known scope of its effects.
The [N6 evidence](../tests/evidence/W012.json) records source versions, observations, and inspection limits.
No runtime adapter, restart guarantee, or measured research improvement follows from this map.
