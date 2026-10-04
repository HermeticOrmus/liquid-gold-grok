#!/usr/bin/env bash
# The one check for this library. CI runs it on every pull request and on every
# push to main (.github/workflows/check.yml). Run it before you open a pull request.
#
#   1. The marketplace file is valid JSON.
#   2. Cards, catalog and marketplace agree (scripts/check_catalog.py).
#   3. Every marketplace entry installs clean at its pin in a fresh Grok home
#      (scripts/verify.sh).
#
# Usage:
#   scripts/check.sh                  check the whole library
#   scripts/check.sh <entry> ...      steps 1 and 2 for the whole library, step 3
#                                     only for these entries
#
# Needs Python 3, git and the Grok Build CLI. Exits non-zero on the first step
# that fails.
set -euo pipefail
IFS=$'\n\t'
cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "== marketplace JSON"
python3 -m json.tool .grok-plugin/marketplace.json > /dev/null
echo "ok"
echo "== cards, catalog and marketplace"
python3 scripts/check_catalog.py
echo "== installs at the pin"
scripts/verify.sh "$@"
