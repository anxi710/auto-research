# Optional Chinese LaTeX templates

The [template catalog](../templates/latex/README.md) provides three official ElegantLaTeX templates as optional starting points.
Markdown is the standard report format, and these templates are inactive by default.
Only an explicit user request selects LaTeX or PDF delivery.
Within that choice, the recommended starting point is the Paper example with the separate local researcher adapter.
The build helper still requires an explicit choice.

| Choice | Template version | Starting document |
| --- | --- | --- |
| `paper` | ElegantPaper 0.12 | [Paper example](../templates/latex/examples/paper/report.tex) |
| `note` | ElegantNote 2.70 | [Note example](../templates/latex/examples/note/report.tex) |
| `book` | ElegantBook 4.7 | [Book example](../templates/latex/examples/book/report.tex) |

The note example uses `device=normal` for a portrait page.
The examples contain local adaptations.
The `vendor/` directories retain the supplied upstream source files.
The [manifest](../templates/latex/manifest.json) records versions, sources, and file digests.
Read the catalog for dependencies, upstream notices, and asset limits.

## Select and build

To select LaTeX for one report, request it explicitly:

```text
Deliver this report as LaTeX and PDF using the Paper example.
Preserve the evidence links, scientific version, and current human-review status.
Report missing dependencies before installing anything.
```

Read the catalog's dependency list before building.
If a dependency is missing, report the missing tool or package and the unbuilt output.
Install dependencies only with explicit user authorization.
Do not mark a build or PDF inspection as complete when it did not run.

Run the build helper from the repository root with one explicit choice:

```bash
./templates/latex/build.sh paper
./templates/latex/build.sh note
./templates/latex/build.sh book
```

Each command builds the named example.
Running the helper without a choice does not select a template.
Use the example for the chosen layout as the starting point for a document.
Keep local content changes outside `vendor/`.
Follow the catalog for build requirements and output locations.
For a compiled PDF, inspect its pages, citations, and evidence links.
Deliver the report's editable sources and build instructions with the requested PDF.

A one-report LaTeX request leaves later reports on the Markdown default.
To change the current report back, explicitly request Markdown.
If you saved a LaTeX choice in existing local preferences, change that preference to Markdown.
No new configuration file is required.
The Markdown path does not run the build helper or require a PDF.

## Scope and evidence

These templates supply document formatting.
They do not change the research procedure or the [W019 delivery trial](../changes/W019.md).
Selecting a layout does not approve scientific claims or satisfy a pending human review.
Keep the existing research records and review decisions when preparing a formatted view.
A layout choice alone does not require new literature searches or research runs.

The [W020 integration record](../changes/W020.md) records the integration checks and their limits.
A successful PDF build checks that the selected example can render in the tested environment.
It does not establish scientific correctness or improved assistant behavior.
