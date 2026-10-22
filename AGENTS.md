# Research workflow

This repository contains a research workflow for AI assistants.
A harness is the application that runs the assistant.
The workflow stores progress in files so that another harness can continue the work.

For research tasks, read [the research skill](skills/research-workflow/SKILL.md).
Follow its routing rules for the requested task.
Use the research directory that the user selects.

For changes to this toolkit, work on the toolkit itself.
For workflow ideas or behavior changes, read [the evolution procedure](skills/research-workflow/references/evolution.md).
New lessons from sibling repositories remain proposals until the user validates them for the intended scope.
Do not start a research project to test a documentation change.
Use temporary directories for behavior tests.
Use Conventional Commits for commit messages, such as `feat: add workflow evaluation`.

Write toolkit documentation in plain English.
Keep instructions short and use one instruction per sentence.
Use the user's language for research notes and conversation unless the user requests another language.
