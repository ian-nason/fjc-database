#!/usr/bin/env bash
# FJC Integrated Database bulk text files (tab-delimited zips).
# https://www.fjc.gov/research/idb  -- file names verified 2026-09-15
set -uo pipefail
cd "$(dirname "$0")"
BASE="https://www.fjc.gov/sites/default/files/idb/textfiles"
for f in cv88on.zip cr96on.zip cr70to95.zip ap08on_0.zip ${EXTRA_FILES:-}; do
  d="data/raw/$f"; [[ -s "$d" ]] && { echo "have $f"; continue; }
  curl -L --retry 5 --retry-delay 15 -sS -A "Mozilla/5.0 (datapond-maintenance)" -o "$d.part" "$BASE/$f" && mv "$d.part" "$d" && echo "ok $f $(stat -c %s "$d")" || { rm -f "$d.part"; echo "FAIL $f"; }
done
echo "FJC DOWNLOADS DONE"
