# Contribute to the research workflow

Keep each change focused on a user need.
Read [AGENTS.md](AGENTS.md) and the [repository structure](docs/architecture.md) before editing.
For behavior changes, follow the [evolution procedure](skills/research-workflow/references/evolution.md).
Keep lessons from sibling repositories as proposals until the user validates their intended scope.
Preserve existing research records and history.

Write toolkit documentation in plain English.
Use one instruction per sentence.
Keep each active rule in one location.
Keep [README.md](README.md) and [README.zh-CN.md](README.zh-CN.md) consistent.
If the package version or requirements change, update both README files and their badges.

## Test the change

Use temporary directories and synthetic or explicitly publishable fixtures.
Run the affected cases.
Record actual results and limits in [tests/RESULTS.md](tests/RESULTS.md).
Proposed tests are not passing results.

| Change | Relevant cases |
| --- | --- |
| Research stages or saved state | [Research scenarios](tests/scenarios.md) |
| Collaboration records and handoffs | [Collaboration scenarios](tests/collaboration.md) and [record checker tests](tests/test_lint_records.py). |
| Workflow improvement | [Evolution scenarios](tests/evolution.md) |
| User preferences | [Preference scenarios](tests/preferences.md) |
| Batch literature analysis | [Bulk literature scenarios](tests/bulk-literature.md) |
| Scripts | Changed behavior and failure handling, without live accounts when possible. |
| Documentation and package metadata | [Package checks](tests/test_package.py), accurate examples, and local links. |

Run all offline tests from the repository root:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
```

The suite includes script behavior and package consistency checks.
Package checks cover local inline links, Markdown heading anchors, entry files, skill metadata, version badges, and license copies.
They support the Markdown and frontmatter forms used in this repository.
They skip code examples and do not request external URLs.
Personal files and the research report stay outside the package checks.
The package checks do not establish native skill loading in a harness.

The [CI workflow](.github/workflows/tests.yml) runs the same command for pushes and pull requests.
It uses Ubuntu with Python 3.9 and 3.14.
The test steps need no installed dependencies, research accounts, or external research tools.
Runner setup can download GitHub Actions and Python.
The workflow uses read-only repository permissions and does not retain checkout credentials.
A local pass does not establish that GitHub ran the workflow.

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
