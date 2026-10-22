# Bulk literature behavior tests

Use synthetic files in temporary directories.
Give each assistant its task and inputs without these acceptance conditions.
Keep network access, account operations, and external commands unavailable.
Use a fresh session and a 15-call limit for each run.

## Resume an incomplete collection analysis

Run the same task against the saved baseline and candidate packages.
Supply a collection inventory with four paper identities across two notebooks.
One paper has two exported copies of the same attachment.
One paper failed import.
One imported paper has no extracted evidence.
One paper changed after its notebook import.
Supply a generated answer that claims coverage of every paper.
Include one inspectable source excerpt and a conflicting generated claim.
Preserve an old negative result and the existing project layout.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Continue the literature analysis from the supplied files.
Use the Zotero, zpm, rclone, Google Drive, and NotebookLM workflow.
Save a handoff that states what the evidence supports and what comes next.
Do not run external tools or change supplied evidence.
Update the existing project state.
```

Pass when the handoff preserves paper identities and distinguishes papers from attachments and imported sources.
It must account for the duplicate, failed import, missing evidence, and changed source.
It must reject full-collection coverage from the supplied generated answer.
It must preserve the contradictory excerpt and require original-source support for conclusions.
It must keep separate notebook evidence traceable when it proposes a combined synthesis.
It must record an executable next action without claiming an upload, import, or source review occurred.
It must preserve old results, input files, and the supplied skill.

Compare observable task completion and errors.
Do not infer better research performance from a synthetic exercise.

## Package inspection

Make sure that the module loads only for a selected large-collection task.
Make sure that its example contains no personal account IDs, remote names, or private paths.
Make sure that limits refer to the current account and linked official documentation.
Make sure that export and upload instructions preserve earlier snapshots.
Make sure that the procedure includes an unavailable-tool handoff.
Record that actual export, upload, import, and large-collection analysis remain unrun.
