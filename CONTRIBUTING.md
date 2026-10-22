# Contribute to the research workflow

Keep each change focused on a user need.
Read [AGENTS.md](AGENTS.md) and the [repository structure](docs/architecture.md) before editing.
For behavior changes, follow the [evolution procedure](skills/research-workflow/references/evolution.md).
Keep lessons from sibling repositories as proposals until the user validates their intended scope.
Preserve existing research records and history.

Write toolkit documentation in plain English.
Use one instruction per sentence.
Keep each active rule in one location.

## Test the change

Use temporary directories and synthetic or explicitly publishable fixtures.
Run the affected cases.
Record actual results and limits in [tests/RESULTS.md](tests/RESULTS.md).
Proposed tests are not passing results.

| Change | Relevant cases |
| --- | --- |
| Research stages or saved state | [Research scenarios](tests/scenarios.md) |
| Workflow improvement | [Evolution scenarios](tests/evolution.md) |
| User preferences | [Preference scenarios](tests/preferences.md) |
| Batch literature analysis | [Bulk literature scenarios](tests/bulk-literature.md) |
| Scripts | Changed behavior and failure handling, without live accounts when possible. |
| Documentation | Existing paths, accurate examples, and local links. |

Run the offline script tests from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Record any live integration that you did not test.
Review the complete diff before submission.

## Submit the change

Use Conventional Commits, such as `feat: add a corpus inventory` or `fix: preserve source identifiers`.
Describe the problem, resulting behavior, and test evidence in the pull request.
Keep private papers, local preferences, credentials, and browser sessions out of commits.

This toolkit uses the MIT license.
Keep the root and skill package copies of [LICENSE](LICENSE) identical.
Keep required third-party notices.
State their source and license in the affected documentation.
