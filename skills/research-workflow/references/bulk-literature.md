# Analyze a large literature collection

A corpus is the selected set of papers for one analysis.
Use this optional procedure when the task selects NotebookLM for a large corpus.
It extends S1 and keeps the user's chosen library and project layout.
For command-line execution, use [the scripted procedure](scripted-bulk-literature.md).
Its outputs still need the coverage and evidence review below.
Apply [human review](human-review.md) before dependent research uses the selection, batch plan, evidence tables, or synthesis.
Present each output's version and the proposed next actions.
Without a matching review waiver, use this manual procedure with those review points.

This example keeps library records in Zotero.
NotebookLM retrieves passages within each notebook.
The assistant tracks coverage, compares batches, and inspects claims in original papers.

```text
Zotero selection -> zpm export -> rclone copy -> Google Drive -> NotebookLM
```

## Define the question and selection

Use [CORPUS.md](../templates/CORPUS.md) or equivalent records for the question, selection, inventory, batches, and next action.
Record the inclusion rules, exclusions, expected output, and chosen Zotero library and collection.
Record whether the selection includes child collections.
Record the export location, Drive destination, notebook links, and time or usage budget.
Keep account-specific values in project records or [local preferences](preferences.md).
Use existing authorization for the selected data and destination.
If a required destination or access decision is missing, finish local preparation before asking for it.

Read the account's current [source and usage limits](https://support.google.com/notebooklm/answer/16213268?hl=en) before planning batches.
Record the observed limits and date.
One paper can have several attachments, versions, and copies across collections.

## Export a dated selection

These commands use Zotero Project Manager 1.3.1.
Inspect the installed `zpm --version` and `zpm export --help` before using them.

A snapshot is the saved content at a recorded time.
Use a new export directory for each snapshot.
Zpm can replace changed files in an earlier managed export.
Keep earlier snapshots when their evidence supports an existing result.
On the host with the selected library and zpm configuration, replace the example values before execution.

```bash
zpm export COLLECTION_KEY --output /path/to/new-export --recursive --pdf-only --metadata --dry-run
zpm export COLLECTION_KEY --output /path/to/new-export --recursive --pdf-only --metadata
```

Use `--no-recursive` when the selection excludes child collections.
Inspect the dry-run selection before the real export.
Record the exact command, tool version, selection, output path, and export errors.
Do not add `--overwrite` to resolve an unexplained conflict.

Zpm creates a workspace beneath the output path using the collection name.
Find the actual workspace from the export result.
Read its `.zpm/metadata.json` for attachment identities, `destination_path` values, states, and SHA-256 hashes.
Make sure that selected files exist and match their recorded hashes.
Do not upload missing or inactive records as current attachments.
Reconcile this attachment inventory with the library selection to retain papers without PDFs.

Map each paper ID to its Zotero item key, attachment key, exported path, and content hash.
Use the library identity with the item key when the selection spans libraries.
Use DOI or another stable source link to reconcile alternate records.
Retain missing PDFs and excluded items with their reasons.

For duplicate exports across collections, upload one copy of each file.
Preserve all item identities and collection memberships.
Keep distinct paper versions separate unless the task selects one version.
Treat hash matches as duplicate content, not proof that two bibliographic records mean the same work.

## Transfer the selected files

Create `upload-files.txt` with one selected PDF path per line, relative to the export workspace.
Preserve paths that distinguish attachments with the same filename.
Keep the metadata inventory local unless the task needs it in Drive.
Zpm metadata can contain local source paths.
Do not import metadata or annotations as extra paper sources unless requested.

Use an existing rclone remote for the selected Google Drive account.
Replace the paths below with the export workspace, upload list, and a new run-specific destination.
`rclone copy` can update different files but preserves destination-only files.

```bash
rclone copy /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --dry-run
rclone copy /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --log-file /path/to/transfer.log
rclone check /path/to/workspace REMOTE:literature/RUN_ID --files-from /path/to/upload-files.txt --one-way
```

Inspect the dry run before the transfer.
Do not use `rclone sync` for this snapshot transfer.
It can delete files at the destination.
Make sure that the transfer comparison succeeds before recording files as transferred.
Record unresolved mismatches and unavailable hash comparisons.
Save Drive file IDs or links for import.
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
Inspect representative text, tables, equations, and scans for extraction problems, even after a successful import.

Drive source updates depend on the available interface and source type.
After an update or sync, make sure that the notebook contains the intended version.
If it does not, record the issue before replacing or reimporting the source.
Preserve earlier response evidence and its source version.
Do not assume that an upload or a sync refreshes saved answers.

## Extract evidence with explicit coverage

Start with a small representative batch before extending the analysis.
Select the intended sources for each prompt.
Save the question, selected source IDs, response, and citation links.
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

Reconcile returned rows against the stable paper IDs in the inventory.
Retry missing rows with smaller source selections or inspect their original papers.
Keep unresolved rows when the task budget ends.
A broad answer does not prove that every imported paper contributed evidence.

Keep import status, extraction coverage, and actual reading depth separate.
Do not mark a paper fully read from a generated answer.
For each finding used in the final argument, open its citation and inspect the original supporting passage.
Record the paper version, page or section, and the support or contradiction found.
Treat unchecked generated findings as leads for further reading.

## Compare batches and save the result

Save each batch's evidence table and raw response separately from the synthesis.
Keep their source links.
Join batches by paper identity and preserve disagreements between versions or sources.
Use comparable data and evaluation conditions before comparing reported results.
Do not rank methods from incompatible benchmarks.

Build a topic summary from the inspected evidence.
Link it from `LITERATURE.md` or the user's existing note index.
State the covered selection and unresolved papers beside any corpus-wide claim.
Do not treat a failed import or missing retrieval as evidence of a research gap.
Use original-paper citations for research claims, not only a notebook or generated summary link.

Save separate counts for selected papers, exported attachments, transferred files, imported sources, extracted papers, and inspected claims.
Record the next close reading or S2 question.
If coverage remains incomplete, return a bounded synthesis and its gaps.

## Resume or hand off

Read the corpus record and existing batch outputs before repeating an operation.
Restore the linked human decisions and any review waiver before resuming dependent research.
Keep a pending decision pending until an actual approval or valid waiver covers the next action.
Inspect active or unknown jobs without silently cancelling them when review becomes pending.
Reconcile unknown transfer and import states against their destinations before retrying.
Continue from missing or changed items rather than exporting the whole library again.

If a tool is unavailable, save its prepared inputs and exact remaining action.
For a blocked import, ask the user to import the named Drive files into the target notebook.
State the expected source count.
Keep the step pending until its result is observed or reported with that limitation.
Never invent a completed transfer, import, citation inspection, or full-text reading.

Read [the source map](sources.md#bulk-literature-tools) for observed versions and official service behavior.
