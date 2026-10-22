# Run the literature pipeline from a terminal

Use this optional script after selecting the [bulk literature procedure](bulk-literature.md).
It runs exports, transfers, imports, and batch questions from one configuration file.
It saves progress so that another harness can continue the same run.

The NotebookLM client is the third-party [notebooklm-py](https://github.com/teng-lin/notebooklm-py), not an official Google CLI.
It uses undocumented service interfaces that can change.
This script targets client version `0.8.5` and zpm version `1.3.1`.
Authentication can expire and require another login.

## Prepare the tools

Use Python 3.9 or later, zpm, rclone, and the pinned NotebookLM client on the execution host.
The script uses only Python's standard library.
Its run lock supports Linux and macOS.
The local tests ran on Linux without live accounts.
Windows execution is unsupported in this version.

Configure zpm for the selected Zotero library.
Configure an rclone remote for the intended Google Drive account.
Keep authentication files outside the skill and Git repository.

With `uv` installed, install the pinned client:

```bash
uv tool install 'notebooklm-py[cookies]==0.8.5'
notebooklm --version
```

The client can use an existing Chrome login through its documented cookie login command.
Run authentication yourself on the host with that browser profile.
The pipeline does not extract browser cookies or create credentials.

```bash
notebooklm login --browser-cookies chrome
notebooklm auth check --test --passive --json
```

Read the client's [installation guide](https://github.com/teng-lin/notebooklm-py/blob/v0.8.5/docs/installation.md) for other login methods.
The pipeline requires a successful network authentication check before external mutations.
It keeps returned account details out of saved run records.

## Set the run configuration

Copy [the configuration example](../templates/bulk-literature.example.json) into the chosen research project.
Name the copy `bulk-literature.local.json`.
Replace its example values with the selected collection, destination, question, and limits.
Do not execute the template against its fictional collection key.

| Field | Meaning |
| --- | --- |
| `collection_key` | The selected Zotero collection key. |
| `question` | The research question used for batch evidence extraction. |
| `remote` | The configured Google Drive remote and parent folder, such as `gdrive:research-literature`. |
| `run_dir` | A new private run directory, resolved from the configuration file. |
| `source_limit` | The source limit observed for the current NotebookLM account. |
| `batch_size` | Sources per notebook, within that limit. |
| `max_queries` | Maximum batch question commands permitted for this run. |
| `recursive` | Whether zpm includes child collections. |
| `command_timeout` | Maximum seconds for an ordinary command. |
| `wait_timeout` | Maximum seconds for a source-processing wait. |

The example numbers illustrate configuration, not service limits or recommended paper quotas.
The query budget does not measure the client's internal network retries or the account's remaining quota.
Keep the run directory outside the portable skill package.
Keep the configuration and run data out of Git.
This repository ignores its root `bulk-literature.local.json` and `runs/` directory.
Other project repositories need their own ignore rules.

## Plan, execute, and resume

Replace the configuration path below with the project copy.
Run the command from this toolkit's root, or use an absolute script path.
Without `--execute`, the command prints a plan without running tools or creating run files.

```bash
python3 skills/research-workflow/scripts/bulk_literature.py /path/to/project/bulk-literature.local.json
```

Inspect the collection, destination, limits, and output paths in that plan.
Use `--execute` when the selected data and destination are authorized for this run.
This command writes to Google Drive and NotebookLM.

```bash
python3 skills/research-workflow/scripts/bulk_literature.py /path/to/project/bulk-literature.local.json --execute
```

Use the same command to resume an interrupted run.
Keep its configuration and saved state together.
Use a new run directory for changed source content or configuration.
Do not edit saved IDs to force a retry.

The script saves external IDs before continuing to dependent operations.
It uses a separate Drive destination and distinct notebook titles for each run.
It reconciles unknown creation outcomes before sending another write.
If the outcome stays unknown, it stops with pending work.

The transfer uses `rclone copy --immutable` and a content comparison with `rclone check --download --one-way`.
The comparison downloads remote content, which adds bandwidth use.
Resuming a transfer rechecks the selected remote files before using them.

## Inspect the output

The run retains `manifest.json`, `state.json`, `coverage.json`, and `REPORT.md`.
It also saves transfer progress, notebook IDs, source IDs, prompts, and raw answers.
It saves imported text and citation data separately from generated answers.
Its combined report preserves batch boundaries and unresolved work.

The manifest deduplicates selected attachment content across collections.
It retains the original item identities and collection memberships.
Attachment metadata alone cannot establish the number of library items without PDFs.
Record that coverage limit until the complete collection selection is available.

An answered batch is not proof that every paper contributed relevant evidence.
The report contains generated findings that require original-paper inspection.
Use the coverage procedure before turning those findings into research conclusions.
The script does not label imported or summarized papers as fully read.

Link the run and its evidence from the project's corpus record.
Use the assistant to inspect coverage and synthesize findings across batches.
The script does not perform an independently checked scientific review.

## Handle incomplete runs

If authentication expires, complete login before resuming.
If source processing times out, resume the same run to inspect its status again.
If a write outcome is unknown, keep its pending record until remote reconciliation resolves it.

If a local export is interrupted, preserve its files and use a new run directory.
The script does not replay a question with an unknown outcome.
Inspect that notebook's server answer manually before deciding whether another query is needed.

If the selection exceeds the query budget, reduce the selection or use a new run with a larger explicit budget.
If a query result is unknown, inspect its saved pending state before any further question.
If a snapshot or configuration changes, start a new run rather than mixing evidence versions.
If the client changes its JSON contract, stop and update the adapter with tests.

The script never uses `ask --new`, which deletes the notebook's server conversation in this client version.
It never uses `rclone sync` to delete destination files.
Local tests cannot establish current account access, real import behavior, or the quality of generated analysis.
