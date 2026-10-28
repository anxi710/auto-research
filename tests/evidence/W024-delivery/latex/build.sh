#!/usr/bin/env bash
set -euo pipefail
report_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
catalog=/workspace/auto-research-markdown-delivery/templates/latex
for tool in xelatex kpsewhich; do
  command -v "$tool" >/dev/null || { echo "Missing executable: $tool" >&2; exit 1; }
done
missing=0
for package in biblatex.sty logreq.sty texgyretermes-regular.otf texgyreheros-regular.otf; do
  if ! kpsewhich "$package" >/dev/null; then
    echo "Missing TeX dependency: $package" >&2
    missing=1
  fi
done
if [ "$missing" -ne 0 ]; then
  echo "Build stopped before compilation. No dependencies were installed." >&2
  exit 1
fi
export TEXINPUTS="$report_dir:$catalog/vendor/elegantpaper:$catalog/adapters:${TEXINPUTS:-}:"
cd -- "$report_dir"
for pass in 1 2; do
  xelatex -no-shell-escape -halt-on-error -interaction=nonstopmode -output-directory="$report_dir" "$report_dir/report.tex" > "$report_dir/pass-$pass.log"
done
printf 'Built %s/report.pdf\n' "$report_dir"
