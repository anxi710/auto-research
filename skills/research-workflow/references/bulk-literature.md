# Analyze a large literature collection

A corpus is the selected set of papers for one analysis.
Use this optional procedure when the task selects NotebookLM for a large corpus.
It extends S1 and keeps the user's chosen library and project layout.
It does not require this tool chain for ordinary reading.

For command-line execution, use [the scripted procedure](scripted-bulk-literature.md).
Keep this guide's coverage and evidence conditions when the script performs the transfer and query steps.

This example uses Zotero, zpm, rclone, Google Drive, and NotebookLM.
Zotero owns the library records.
Exports and cloud copies support analysis of a dated selection.
NotebookLM retrieves evidence within each notebook.
The assistant tracks coverage, compares results across notebooks, and inspects claims in original papers.

```text
Zotero selection -> zpm export -> rclone copy -> Google Drive -> NotebookLM
       |                |             |              |              |
       +----------------+-------------+--------------+--------------+
                         Corpus record and source links
                                      |
                         Checked evidence -> synthesis
```

## Define the question and selection

Record the question, inclusion rules, exclusions, and expected output.
Identify the chosen Zotero library and collection.
Record whether the selection includes child collections.
Use [CORPUS.md](../templates/CORPUS.md) for the selection, file inventory, batches, and next action.
Reuse existing equivalent records when present.

Record the export location, Drive destination, notebook links, and time or usage budget.
Keep account-specific values in project records or [local preferences](preferences.md).
Use existing authorization for the selected data and destination.
If a required destination or access decision is missing, finish local preparation before asking for it.

Read the account's current [source and usage limits](https://support.google.com/notebooklm/answer/16213268?hl=en) before planning batches.
Record the observed limits and date.
Do not assume one paper equals one imported source.
One paper can have several attachments, versions, and copies across collections.

## Export a dated selection

The commands below match Zotero Project Manager 1.3.1.
Inspect the installed `zpm --version` and `zpm export --help` before using them.
Keep the exporter replaceable when another user selects a different tool.

Use a new export directory for each collection snapshot.
A snapshot is the saved content at a recorded time.
Zpm can replace changed files in an earlier managed export.
Keep earlier snapshots when their evidence supports an existing result.

Replace the example values before running these commands.
Run them on the host with the selected Zotero library and zpm configuration.

```bash
zpm export COLLECTION_KEY --output /path/to/new-export --recursive --pdf-only --metadata --dry-run
zpm export COLLECTION_KEY --output /path/to/new-export --recursive --pdf-only --metadata
```

Use `--no-recursive` when the selection excludes child collections.
Inspect the dry-run selection before the real export.
Record the exact command, tool version, selection, output path, and export errors.
Do not add `--overwrite` to resolve an unexplained conflict.

The output path is a parent directory.
Zpm creates a workspace beneath it using the collection name.
Find the actual workspace from the export result.
Read its `.zpm/metadata.json` for attachment identities, relative `destination_path` values, states, and SHA-256 hashes.
Make sure that selected files exist and match their recorded hashes.
Do not upload missing or inactive records as current attachments.
The metadata lists attachments rather than every library item.
Reconcile it with the selected library items to retain papers without PDFs.

Map each paper ID to its Zotero item key, attachment key, exported path, and content hash.
Use the library identity with the item key when the selection spans libraries.
Use DOI or another stable source link to reconcile alternate records.
Retain missing PDFs and excluded items with their reasons.

Zpm can export the same attachment through several collections.
Upload one selected copy of each duplicate file.
Preserve all collection memberships in the inventory.
Keep distinct paper versions separate unless the task selects one version.
Treat hash matches as duplicate content, not proof that two bibliographic records mean the same work.

## Transfer the selected files

Create `upload-files.txt` with one selected PDF path per line, relative to the export workspace.
Preserve paths that distinguish attachments with the same filename.
Keep the metadata inventory local unless the task needs it in Drive.
Zpm metadata can contain local source paths.
This avoids importing metadata or annotations as extra paper sources.

Use an existing rclone remote for the selected Google Drive account.
Replace the paths below with the export workspace, upload list, and a new run-specific destination.
`rclone copy` copies directory contents and can update different files at the destination.
It preserves destination-only files.

```bash
rclone copy /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --dry-run
rclone copy /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --log-file /path/to/transfer.log
rclone check /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --one-way
```

Inspect the dry run before the transfer.
Do not use `rclone sync` for this snapshot transfer.
It can delete files at the destination.
Make sure that the transfer comparison succeeds before recording files as transferred.
Record any missing hash comparison or unresolved mismatch.
Save Drive file IDs or links for import and later reconciliation.
A successful upload does not establish a successful NotebookLM import.

## Import and reconcile each batch

Group papers by the analysis question within the account's current limits.
Record every batch's paper IDs, notebook link, and selected source IDs.
If a paper appears in several batches, count it once in corpus coverage.
Each notebook has its own sources.
Do not assume that one notebook can query another notebook.

Use the available NotebookLM interface to import the selected Drive files.
Wait for each source to finish processing.
Match imported sources to the inventory by identity and file version.
Record failures, duplicates, unreadable files, and pending imports separately.
Inspect representative text, tables, equations, and scans before relying on their extracted content.
Keep extraction problems visible even when import succeeds.

Drive source updates depend on the available interface and source type.
After any update, make sure that the notebook contains the intended version.
Use the available sync control when needed.
If updated content remains unavailable, record the issue before replacing or reimporting the source.
Preserve earlier response evidence and its source version.
Do not assume that an upload or a sync refreshes saved answers.

## Extract evidence with explicit coverage

Start with a small representative batch before extending the analysis.
Select the intended sources for each prompt.
Save the question, selected source IDs, response, and citation links.
Use stable paper IDs in prompts and output rows.

Adapt this prompt to the research question:

```text
Use only the selected sources for paper IDs <IDs>.
For each paper, extract its problem, method, data, evaluation, findings, and limits relevant to <question>.
Return one row per paper ID.
Attach a source citation and passage location to each substantive finding.
Mark unavailable evidence as unresolved.
Keep author claims separate from results supported by the cited passage.
List contradictions and missing source access.
Do not infer that a method is absent because retrieval did not find it.
```

Reconcile returned rows against the planned paper IDs.
Retry missing rows with smaller source selections or inspect their original papers.
Keep unresolved rows when the task budget ends.
NotebookLM retrieves relevant passages for a question.
A broad answer does not prove that every imported paper contributed evidence.

Keep import status, extraction coverage, and actual reading depth separate.
Do not mark a paper fully read from a generated answer.
For each finding used in the final argument, open its citation and inspect the original supporting passage.
Record the paper version, page or section, and the support or contradiction found.
Treat unchecked generated findings as leads for further reading.

## Compare batches and save the result

Export or save each batch's evidence table with its source links.
Keep the raw response separate from the assistant's synthesis.
Join batches by paper identity and preserve disagreements between versions or sources.
Use comparable data and evaluation conditions before comparing reported results.
Do not rank methods from incompatible benchmarks.

Build a topic summary from the inspected evidence.
Link it from `LITERATURE.md` or the user's existing note index.
State the covered selection and unresolved papers beside any corpus-wide claim.
Do not treat a failed import or missing retrieval as evidence of a research gap.
Use original-paper citations for research claims, not only a notebook or generated summary link.

Save separate counts for selected papers, exported attachments, transferred files, imported sources, extracted papers, and inspected claims.
Record unresolved evidence and the next useful close reading or S2 question.
Complete the task when the requested output matches the declared coverage and limits.
If coverage remains incomplete, return a bounded synthesis and its gaps.

## Resume or hand off

Read the corpus record and existing batch outputs before repeating an operation.
Reconcile unknown transfer and import states against their destinations before retrying.
Continue from missing or changed items rather than exporting the whole library again.

If a tool is unavailable, save the prepared inputs and exact remaining action.
For a manual import, name the Drive files, target notebook, and expected source count.
Ask the user to perform only the blocked interface step.
Record it as pending until its result is observed or reported with that limitation.
Never invent a completed transfer, import, citation inspection, or full-text reading.

Read [the source map](sources.md#bulk-literature-tools) for observed versions and official service behavior.
