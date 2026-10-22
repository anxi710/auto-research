# Reading record behavior tests

These are the original conditions for the rejected [W003 candidate](../changes/W003.md).
The candidate passed these cases before the user corrected its shared scope.
They do not test the replacement [preferences procedure](preferences.md).

Use synthetic files in temporary directories.
Copy only the complete skill into each fixture.
Give the testing assistant its request and input files without these acceptance conditions.

## Reuse a library item and selected note

Run the same task with the baseline and candidate packages.
Use fresh sessions with the same local tools and a 15-call limit.
Keep networking, experiments, and library operations unavailable.

Supply an existing project with an old brief and state.
The brief does not specify a literature library.
Supply a Zotero item snapshot with a stable source link and a `read` tag.
Supply an existing selected note in `paper-I-love/notes/` that cites only an abstract.
The full paper is unavailable.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Continue the project using its existing notes directory.
Use the supplied library snapshot and selected note to assess the evidence gap for our question.
Save only task-specific analysis and update the project records.
Keep the source snapshot and selected note unchanged.
Use Chinese for research records.
```

Pass when the result links the existing library identity and selected note.
It must preserve abstract-only reading depth despite the library tag.
It must add only relevant analysis without copying the selected note or creating another library.
It must preserve existing IDs, layout, source files, and recorded results.
The candidate must record the approved default and the resolved selected-note location in the project brief.
It must distinguish saved local records from unavailable live library operations.

Record the added default fields separately from shared behavior outcomes.
They are a requested capability, not proof of a research performance gain.
Record both results even when both preserve the existing research behavior.

## Honor a project convention

Supply an existing project brief that selects a local BibTeX file as its primary library.
Its selected notes live in `wiki/`, with existing record IDs.
Supply one abstract and an existing note in that layout.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Use the existing project's conventions to explain the evidence limits in the supplied abstract.
Save the requested explanation in notes/answer.md and update the existing state.
Preserve the library, selected note, and old record IDs.
```

Pass when the result honors the explicit project library and note location.
It must not switch the project to Zotero or `paper-I-love`.
It must preserve the input files and avoid account setup or migration requests.

## Finish a standalone abstract task

Supply only an abstract and a source link.
Provide no project state, library connection, or selected-note repository.
Keep browsing unavailable.

User request:

```text
Read toolkit/skills/research-workflow/SKILL.md.
Explain the supplied abstract and whether the available evidence establishes its claimed result.
Save answer.md only.
```

Pass when the answer separates reported claims from unread methods and results.
It must finish without library setup, a new project, or invented findings.
Only the requested answer can be added outside the supplied skill.
