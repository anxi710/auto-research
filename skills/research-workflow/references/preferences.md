# Optional research preferences

Preferences store choices that a user wants to reuse.
The shared skill contains no personal defaults.
A preferences file is optional.

## Find and apply preferences

The workspace root is the directory opened in the harness.
The target research repository can be elsewhere.
Read `RESEARCH.local.md` from the workspace root when it exists.
If the user names another preferences file, read that file instead.

For each configurable choice, use the first applicable source:

1. The current user request.
2. An explicit project convention in `BRIEF.md` or the project's existing records.
3. The selected local preferences file.

Resolve paths in preferences from the directory that contains that file.
Record relevant choices and their source when the project first uses them.
Do not replace an existing project convention with a local default.
Preferences do not grant new account access or permission for external actions.
Apply [human review](human-review.md) independently of reusable preferences.
A review waiver needs an explicit user source, scope, limits, and end condition.
Link its authoritative record instead of inferring a waiver from a general autonomy preference.
Restore review when that waiver ends or the researcher revokes it.

If no preferences file exists, continue with the request, project conventions, and supplied evidence.
Do not require preference setup for a reading task.
If a choice blocks the task, ask only for that choice.
Keep unchosen libraries and note locations explicit rather than inventing defaults.

## Save and reuse choices

Use [PREFERENCES.md](../templates/PREFERENCES.md) as a starting point.
Keep only choices that the user selects.
Save personal choices outside the shared skill package.

This toolkit ignores its root `RESEARCH.local.md` in Git.
Other repositories need their own ignore rule before saving private preferences.
To reuse a file in another workspace, name its path in the request or copy it there.
Update relative paths when moving that file.
Do not put credentials in a preferences file.

The [Zotero and Git example](zotero-git-example.md) describes one optional reading setup.
Use it only when the user selects it through a request, project convention, or preferences file.
Copying the skill does not select the example or copy personal preferences.
