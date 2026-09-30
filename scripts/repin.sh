#!/usr/bin/env bash
# Show what changed upstream since an entry's pinned SHA, so a re-assay can
# decide whether to move the pin.
#
# Usage: scripts/repin.sh <entry>
#
# Reads the pin from .grok-plugin/marketplace.json, or from the entry card for
# a watch entry. Prints the upstream default-branch head, the commits since the
# pin that touch the plugin folder, the files that changed, and a flag for any
# change to what the plugin can execute (hooks, MCP config, scripts, manifest).
# Nothing is installed and nothing is changed in this repository.
set -euo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
entry="${1:-}"
[[ -n "$entry" ]] || { echo "usage: scripts/repin.sh <entry>" >&2; exit 2; }

pin="$(python3 - "$ROOT" "$entry" <<'PY'
import json, re, sys
root, name = sys.argv[1], sys.argv[2]
m = json.load(open(f"{root}/.grok-plugin/marketplace.json"))
for p in m["plugins"]:
    if p["name"] == name:
        s = p["source"]
        print("\t".join([s["url"], s["sha"], s.get("path", "")]))
        sys.exit(0)
try:
    card = open(f"{root}/entries/{name}.md", encoding="utf-8").read()
except OSError:
    sys.exit(1)
src = re.search(r"^\| Source \| \[[^\]]+\]\(https://github\.com/([^/]+/[^/]+)/tree/([0-9a-f]{40})/?([^)]*)\)", card, re.M)
if not src:
    sys.exit(1)
print("\t".join([f"https://github.com/{src.group(1)}.git", src.group(2), src.group(3).strip("/")]))
PY
)" || { echo "no entry named '$entry' in the marketplace or entries/" >&2; exit 2; }

IFS=$'\t' read -r url sha path <<<"$pin"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
git clone -q --filter=blob:none --no-checkout "$url" "$work/repo"
cd "$work/repo"
head="$(git rev-parse origin/HEAD)"
branch="$(git rev-parse --abbrev-ref origin/HEAD)"
scope=("${path:-.}")

echo "entry:    $entry"
echo "source:   $url${path:+ (path $path)}"
echo "pinned:   $sha ($(git log -1 --format=%cs "$sha"))"
echo "upstream: $head ($(git log -1 --format=%cs "$head"), $branch)"
echo

if ! git merge-base --is-ancestor "$sha" "$head"; then
  echo "The pinned commit is not an ancestor of $branch (history was rewritten or the pin is on another branch)."
  echo "Re-assay from scratch."
  exit 1
fi
if [[ "$sha" == "$head" ]]; then
  echo "No upstream change since the pin."
  exit 0
fi

n="$(git rev-list --count "$sha..$head" -- "${scope[@]}")"
echo "Commits since the pin that touch ${path:-the repository}: $n"
git log --format='  %h %cs %s' "$sha..$head" -- "${scope[@]}"
echo
echo "Files changed:"
git diff --stat=100 "$sha" "$head" -- "${scope[@]}" | sed 's/^/  /'
echo
exec_changes="$(git diff --name-only "$sha" "$head" -- "${scope[@]}" \
  | grep -E '(^|/)(hooks/|\.mcp\.json$|mcp\.json$|plugin\.json$|scripts/)|\.(sh|py|js|mjs|cjs|ts)$' || true)"
if [[ -n "$exec_changes" ]]; then
  echo "Changes to what the plugin can execute (read these first in the re-assay):"
  echo "$exec_changes" | sed 's/^/  /'
else
  echo "No changes to hooks, MCP config, manifests or scripts."
fi
echo
echo "To re-assay: read the diff with the five stages in RUBRIC.md, add new cracks with new IDs,"
echo "then move the SHA in .grok-plugin/marketplace.json and in entries/$entry.md in one pull request."
