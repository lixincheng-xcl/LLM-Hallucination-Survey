#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error -outdir=build_author author_version.tex
python3 scripts/validate_submission.py
python3 scripts/package_release.py
