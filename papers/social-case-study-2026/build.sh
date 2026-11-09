#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd -- "$HERE/../.." && pwd)"
BUILD="$ROOT/tmp/social-case-study-2026-build"
FINAL="$ROOT/output/pdf"
mkdir -p "$BUILD" "$FINAL"
cd "$HERE"
tectonic -X compile --keep-logs --keep-intermediates -r 2 -o "$BUILD" main.tex
cp "$BUILD/main.pdf" "$FINAL/social_preprint_en_2026-11-09.pdf"
tectonic -X compile --keep-logs --keep-intermediates -r 2 -o "$BUILD" main_uk.tex
cp "$BUILD/main_uk.pdf" "$FINAL/social_preprint_uk_2026-11-09.pdf"
