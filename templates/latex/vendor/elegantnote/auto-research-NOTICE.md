# auto-research curated runtime subset: ElegantNote 2.70

This directory is a curated runtime subset, not the complete upstream release.
The supplied upstream class, README, and license bytes are unchanged.
The packaging change is the omission of the files listed below.
The repository license does not replace LPPL-1.3c-or-later for these upstream files.
This integration does not claim to be an upstream release or to be maintained by ElegantLaTeX.
Integration support belongs to the auto-research integration maintainers.
Upstream authors do not promise support for this curated package.

## Sources and changes

- Official project: https://github.com/ElegantLaTeX/ElegantNote
- CTAN project: https://ctan.org/pkg/elegantnote
- Locked commit: `e45cde75e4d265f72042097cd10be03a961440c3`.
- Complete unmodified upstream source: https://github.com/ElegantLaTeX/ElegantNote/archive/e45cde75e4d265f72042097cd10be03a961440c3.zip
- CTAN release archive: https://ctan.math.illinois.edu/macros/latex/contrib/elegantnote.zip
- CTAN archive SHA256: `61609b0cb3f78c5adca105a3e677a224ab5fc25242cb1596c6fdbcfeeae85b54`.
- Included upstream files: `elegantnote.cls`, `README.md`, `License`.
- File-level provenance and digests: [manifest](../../manifest.json).
- Original copyright and maintenance statements remain in the files.
- No separate NOTICE file was found in the locked upstream tree or CTAN archive.

The CTAN release archive omits the full license text.
`License` was added verbatim from https://raw.githubusercontent.com/ElegantLaTeX/ElegantNote/e45cde75e4d265f72042097cd10be03a961440c3/License.
This supplemental file did not come from the CTAN zip.

Omitted release files:

- `elegantnote/elegantnote-en.tex`.
- `elegantnote/elegantnote-cn.tex`.
- `elegantnote/elegantnote-cn.pdf`.
- `elegantnote/elegantnote-en.pdf`.
- `elegantnote/build.lua`.
- `elegantnote/image/logo-blue.png`.
- `elegantnote/image/scatter.pdf`.
- `elegantnote/image/scatter.py`.
- `elegantnote/image/logo.png`.
- `elegantnote/image/founder.png`.

## Redistribution and adaptation

LPPL 1.3c section 2 treats partial distribution as modification.
This notice records the packaging difference and complete upstream acquisition path.
The integration treats the byte-identical runtime class as an unchanged component and the selection as a packaging change.
No upstream class is renamed, edited, or presented as a modified class.
Keep this notice, the original license, author headers, and manifest with redistributed copies.
For an actual class modification, use a distinct adapter or class identity and meet LPPL section 6 identification and change-log requirements.
Do not imply upstream support for an adaptation.
The section 6b notice requirement for every derived component remains relevant.
This directory-level notice documents the integration's scope; it is not a legal certification that a curated subset resolves every possible interpretation of the Work boundary.

No upstream demonstration image or font is redistributed here.
Optional Founder/FangZheng and mtpro2 branches in the original class do not grant font licenses.
Local examples use installed open fonts through the supported ctex/xeCJK nofont option.
