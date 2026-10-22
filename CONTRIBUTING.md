# Contribute to the research workflow

Contributions can improve research procedures, tool support, examples, or documentation.
Keep each change focused on a specific user need.
Read [AGENTS.md](AGENTS.md) and the [repository structure](docs/architecture.md) before editing.

## Prepare a change

For a procedure change, follow the [evolution procedure](skills/research-workflow/references/evolution.md).
Record the intended scope and acceptance conditions before changing behavior.
Keep personal preferences in local configuration.

Explain which task fails or needs improvement.
Preserve existing record layouts, identifiers, and research history.
Keep external lessons as proposals until the user validates their intended scope.

Write toolkit documentation in plain English.
Use one instruction per sentence.
Keep each active rule in one location.

## Test the affected behavior

Use temporary directories for behavior tests.
Run the cases affected by your change.
Save the actual result and its limits in [tests/RESULTS.md](tests/RESULTS.md).

| Change | Relevant evidence |
| --- | --- |
| Research stage or saved state | [Research scenarios](tests/scenarios.md) |
| Workflow improvement | [Evolution scenarios](tests/evolution.md) |
| User preferences | [Preference scenarios](tests/preferences.md) |
| Batch literature analysis | [Bulk literature scenarios](tests/bulk-literature.md) |
| A command or script | A focused test of its changed behavior and failure handling. |
| Documentation only | Existing paths, accurate examples, and working local links. |

If you change a script, test its affected behavior without live accounts when possible.
Record any live integration that you did not test.
Do not report a proposed test as a passing result.

## Submit the change

Use Conventional Commits, such as `feat: add a corpus inventory` or `fix: preserve source identifiers`.
Describe the problem, resulting behavior, and evidence in the pull request.
Review the complete diff before submitting it.

Keep private papers, local preferences, credentials, and browser sessions out of commits.
Use synthetic or explicitly publishable data in test fixtures and examples.
Keep the root and skill package copies of [LICENSE](LICENSE) identical.

This toolkit uses the MIT license.
Keep required notices when you reuse third-party material.
State its source and license in the affected documentation.
