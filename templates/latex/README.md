# Chinese research report templates

Start with the Paper example for a conventional research report.
Compare Note for short thematic notes and Book for a chapter-length review.
These are optional presentation choices in an isolated trial.
No existing research document is migrated.

The user authorized aesthetic selection after the initial catalog request.
The recommended starting style is [the Paper example](examples/paper/report.tex), with [a separate local adapter](adapters/researcher-paper.sty).
The build helper still requires an explicit choice.
This recommendation does not approve research claims or adopt the separate delivery protocol trial.

## Choose a layout

| Choice | Base and visual character | Suitable document | Official Chinese demo |
| --- | --- | --- | --- |
| `paper` | ElegantPaper 0.12; restrained article body, muted blue headings, no cover or decorative boxes. | A compact report or a sustained article-style review. | [Paper demo](https://ctan.math.illinois.edu/macros/latex/contrib/elegantpaper/elegantpaper-cn.pdf) |
| `note` | ElegantNote 2.70; more prominent colored headings, simple note structure. | A short thematic note or reading memo. | [Note demo](https://ctan.math.illinois.edu/macros/latex/contrib/elegantnote/elegantnote-cn.pdf) |
| `book` | ElegantBook 4.7; cover, contents, and chapter navigation. | A long chapter-based review or reference manuscript. | [Book demo](https://ctan.math.illinois.edu/macros/latex/contrib/elegantbook/elegantbook-cn.pdf) |

The official demos are upstream manuals, not the local examples.
Their mutable CTAN URLs are not version locks.
The [manifest](manifest.json) records exact commits, release digests, and copied file digests.
Note uses `device=normal` for portrait A4 pages.
Its local example uses 10pt text, a smaller paragraph gap, and a Chinese abstract label.
Its upstream demo may use a landscape screen layout.
Book uses original vector geometry drawn in [cover-geometric.tex](examples/book/cover-geometric.tex), without upstream photos or logos.
The Book example restores chapter-opening page numbers through a local plain-page style.
The recommended Paper style has no cover.

The recommendation favors sustained Chinese reading over decoration.
It retains Paper's body rhythm, uses restrained heading color inspired by Note, and exposes a navigable heading hierarchy inspired by Book.
It loads one upstream class, not a combination of classes.
No Note or Book class code is copied into the Paper adapter.
It does not add ornamental boxes, a full-page cover, or extra blank chapter pages.
The local preview is a visual smoke test, not a user study or a measured readability improvement.

## Build an example

Use XeLaTeX, BibTeX, and a coherent TeX Live or MiKTeX installation.
The examples select the supported `chinesefont=nofont` option, then set CJK fonts through ctex/xeCJK.
They still require ctex and xeCJK.
They do not replace those packages with a custom CJK engine.

Install or provide these dependencies through your trusted TeX distribution:

- `ctex`, `xecjk`, `zhnumber`, `biblatex`, and `logreq`.
- TeX Gyre Termes and Heros fonts from `tex-gyre`.
- `newtx` for Book's upstream `TeXGyreTermesX` font.
- Standard packages used by the classes, including `titlesec`, `bookmark`, `xurl`, `booktabs`, `tikz`, `tcolorbox`, `bbding`, and `adforn`.
- System fonts named `Noto Serif CJK SC`, `Noto Sans CJK SC`, and `Noto Sans Mono CJK SC`.

The Chinese families use upright glyphs for italic contexts explicitly.
No synthetic Chinese italic font or commercial font is assumed.
No font binary is stored in this repository.
Keep TeX package versions compatible with the installed LaTeX kernel.

From the repository root:

```bash
./templates/latex/build.sh paper
./templates/latex/build.sh note
./templates/latex/build.sh book
```

Each command writes its PDF and build logs below `templates/latex/build/<choice>/`.
Pass an absolute second argument to use another output directory.
The helper runs XeLaTeX, BibTeX, and two further XeLaTeX passes.
Book's geometric cover first runs twice so TikZ page positions resolve in a fresh output directory.
It uses `-no-shell-escape` and performs no download or installation.
It stops on missing preflight dependencies or a compiler error.
Use `TEXMFHOME` to supply a private, compatible TeX tree when global installation is unavailable.
Do not mix a new ctex requiring a newer LaTeX kernel into an older installation.

The examples share [the same placeholder content](examples/shared/overview.tex), [evidence prompts](examples/shared/evidence.tex), and [references](examples/shared/references.bib).
All content is marked as a layout example.
It contains no research result or approval.
A document's real content, evidence binding, and review status need their own checks after a layout choice.

## Source, license, and maintenance

The three templates use LPPL 1.3c or later.
Original class files, README files, copyright headers, and full licenses remain in [vendor](vendor/).
The repository MIT license does not replace those licenses.
Local examples, the original geometric artwork, build helper, and Paper adapter use the repository MIT license.

Each vendor directory has a prominent `auto-research-NOTICE.md` with copied and omitted files, full-source links, and redistribution details:

- [Paper notice and license scope](vendor/elegantpaper/auto-research-NOTICE.md).
- [Note notice and separately sourced full license](vendor/elegantnote/auto-research-NOTICE.md).
- [Book notice and license scope](vendor/elegantbook/auto-research-NOTICE.md).

This is a curated subset, not a complete upstream release.
LPPL treats partial distribution as modification.
The notices record the packaging boundary and full upstream acquisition path.
They explain the remaining interpretation boundary rather than claiming legal certification.
Keep those notices and source records with a redistributed integration.
Modify local adapters instead of overwriting upstream files.
Do not imply that upstream authors support the adaptations.

The upstream README files report renewed release activity in 2026 after the earlier discontinuation.
Book identifies the current 2026 maintainer.
No assumption of permanent abandonment is made here.
Upstream demonstrations may contain historical instructions and optional font branches.
Those instructions do not grant licenses to separate fonts or images.
No upstream image, demonstration PDF, or font is vendored.
Note's broken five-byte image placeholders are also omitted.

Read [W020](../../changes/W020.md) for the integration checks and their limits.
