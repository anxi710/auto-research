# Run the literature pipeline from a terminal

Use this optional script after selecting the [bulk literature procedure](bulk-literature.md).
It runs exports, transfers, imports, and batch questions from one configuration file.
Another harness can resume from its saved files.

The NotebookLM client is the third-party [notebooklm-py](https://github.com/teng-lin/notebooklm-py), not an official Google CLI.
It uses undocumented service interfaces that can change.
This script targets client version `0.8.5` and zpm version `1.3.1`.

## Prepare the tools

Use Python 3.11 or later for the full toolchain on the execution host.
Zpm 1.3.1 requires Python 3.11 or later.
NotebookLM client 0.8.5 requires Python 3.10 or later.
The runner itself needs Python 3.9 or later and uses only the standard library.
Install zpm, rclone, and the pinned NotebookLM client separately.
The script uses Linux or macOS file locking.
Windows execution is unsupported.

Configure zpm for the selected Zotero library.
Configure an rclone remote for the intended Google Drive account.
Keep authentication files outside the skill and Git repository.

With `uv` installed, install the pinned client:

```bash
uv tool install 'notebooklm-py[cookies]==0.8.5'
notebooklm --version
```

For an existing Chrome login, run authentication yourself on the host with that browser profile.
The pipeline does not extract browser cookies or create credentials.

```bash
notebooklm login --browser-cookies chrome
notebooklm auth check --test --passive --json
```

Read the client's [installation guide](https://github.com/teng-lin/notebooklm-py/blob/v0.8.5/docs/installation.md) for other login methods.
The pipeline tests authentication before external writes and keeps account details out of saved run records.

## Set the run configuration

Copy [the configuration example](../templates/bulk-literature.example.json) into the chosen research project.
Name the copy `bulk-literature.local.json`.
Replace its example values using the fields below.
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

Use the account's observed limits rather than the example numbers.
The query budget counts commands, not internal network retries or the account's remaining quota.
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

Use the same command to resume, subject to the recovery limits below.
Keep its configuration and saved state together.
Do not edit saved IDs to force a retry.

The script saves external IDs before continuing to dependent operations.
Each run uses a separate Drive destination and distinct notebook titles.
Unknown creation outcomes stop the run until remote reconciliation finds the created object.

The transfer uses `rclone copy --immutable` and a content comparison with `rclone check --download --one-way`.
The comparison downloads remote content, which adds bandwidth use.
Resuming a transfer rechecks the selected remote files before using them.

## Inspect the output

| File | Content |
| --- | --- |
| `manifest.json` | Frozen file hashes, item identities, collection memberships, and excluded attachment records. |
| `state.json` | Transfer progress, external IDs, pending operations, and attempted query count. |
| `coverage.json` | Counts and unresolved coverage limits. |
| `outputs/F*.text.json` | Imported text from each source. |
| `outputs/batch-*.prompt.txt` | Saved batch questions. |
| `outputs/batch-*.answer.json` | Generated answers and their citation data. |
| `REPORT.md` | Answers by batch and remaining work. |

The script deduplicates attachment content and batches files in inventory order.
It does not group papers by topic.
Its `F` IDs identify files rather than distinct papers.
Library items without PDFs remain unknown until reconciled with the complete library selection.
Citation offsets do not refer to positions in the saved plain text.

Link the run from the project's corpus record.
Apply the bulk procedure's coverage review and original-paper inspection before synthesizing research conclusions.
Generated answers do not establish complete coverage or full reading.

## Handle incomplete runs

If authentication expires, complete login before resuming.
If source processing times out, resume the same run to inspect its status again.
If a creation outcome stays unknown, preserve its pending record.
The script does not repeat that write.
If a question's outcome is unknown, inspect the notebook history manually.
The script does not replay that question.

Use a new run directory after an interrupted export or a snapshot or configuration change.
Preserve the earlier run as evidence.
If the selection exceeds the query budget, use a new run with a smaller selection or larger explicit budget.
If the client changes its JSON contract, stop and update the adapter with tests.

The script never uses `ask --new`, which deletes the notebook's server conversation in this client version.
It never uses `rclone sync` to delete destination files.
Tests ran offline on Linux.
They cannot establish current account access, real import behavior, or analysis quality.
