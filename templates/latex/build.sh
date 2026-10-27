#!/usr/bin/env bash
# Copyright 2026 auto-research contributors. MIT; see repository LICENSE.
set -euo pipefail
catalog=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
style=${1:-}
case "$style" in
  paper|note|book) ;;
  *) echo "Usage: $0 {paper|note|book} [absolute-output-directory]" >&2; exit 2 ;;
esac
out=${2:-"$catalog/build/$style"}
case "$out" in /*) ;; *) echo "Output directory must be absolute." >&2; exit 2 ;; esac
for tool in xelatex bibtex kpsewhich; do
  command -v "$tool" >/dev/null || { echo "Missing executable: $tool" >&2; exit 1; }
done
for package in ctex.sty xeCJK.sty biblatex.sty texgyretermes-regular.otf texgyreheros-regular.otf; do
  kpsewhich "$package" >/dev/null || { echo "Missing TeX dependency: $package. See templates/latex/README.md." >&2; exit 1; }
done
if [ "$style" = book ]; then
  kpsewhich TeXGyreTermesX-Regular.otf >/dev/null || { echo "Missing TeXGyreTermesX-Regular.otf (newtx)." >&2; exit 1; }
fi
mkdir -p -- "$out"
class="elegant$style"
export TEXINPUTS="$out:$catalog/vendor/$class:$catalog/examples/shared:$catalog/adapters:${TEXINPUTS:-}:"
export BIBINPUTS="$catalog/examples/shared:${BIBINPUTS:-}:"
printf 'auto-research curated runtime subset: %s; upstream class unchanged.\n' "$class"
printf 'See %s/vendor/%s/auto-research-NOTICE.md for packaging changes and full upstream sources.\n' "$catalog" "$class"
cd -- "$catalog/examples/$style"
if [ "$style" = book ]; then
  for cover_pass in 1 2; do
    xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory="$out" cover-geometric.tex > "$out/cover-pass-$cover_pass.log"
  done
fi
xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory="$out" report.tex > "$out/pass-1.log"
(cd -- "$out" && bibtex report) > "$out/bibtex.log"
xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory="$out" report.tex > "$out/pass-2.log"
xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory="$out" report.tex > "$out/pass-3.log"
printf 'Built %s/report.pdf\n' "$out"
