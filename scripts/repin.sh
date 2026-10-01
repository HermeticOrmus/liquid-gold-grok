#!/usr/bin/env bash
# Show what changed upstream since an entry's pinned SHA, so a re-assay can
# decide whether to move the pin.
#
# Usage: scripts/repin.sh <entry>
#        scripts/repin.sh --all
#
# Reads the pin from .grok-plugin/marketplace.json, or from the entry card for
# a watch entry. Prints the upstream default-branch head, the commits since the
# pin that touch the plugin folder, the files that changed, and a flag for any
# change to what the plugin can execute (hooks, MCP config, scripts, manifest).
# --all prints one drift row per card in entries/ instead, and exits 1 when any
# upstream cannot be read or no longer contains its pin.
# Nothing is installed and nothing is changed in this repository.
set -euo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
entry="${1:-}"
[[ -n "$entry" ]] || { echo "usage: scripts/repin.sh <entry> | --all" >&2; exit 2; }
EXEC_FILES='(^|/)(hooks/|\.mcp\.json$|mcp\.json$|plugin\.json$|scripts/)|\.(sh|py|js|mjs|cjs|ts)$'

# Prints "<url>\t<sha>\t<path>" for an entry, or exits 1.
pin_of() {
python3 - "$ROOT" "$1" <<'PY'
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
}

if [[ "$entry" == "--all" ]]; then
  work="$(mktemp -d)"
  trap 'rm -rf "${work:?}"' EXIT
  printf '| %s | %s | %s | %s | %s | %s |\n' entry pinned upstream "commits since pin" "executable files changed" note
  printf '|%s|%s|%s|%s|%s|%s|\n' --- --- --- --- --- ---
  bad=0
  for card in "$ROOT"/entries/*.md; do
    name="$(basename "$card" .md)"
    if ! pin="$(pin_of "$name")"; then
      printf '| %s | ? | ? | ? | ? | no pin found in the card |\n' "$name"; bad=1; continue
    fi
    IFS=$'\t' read -r url sha path <<<"$pin"
    dir="$work/$(printf '%s' "$url" | tr -c 'A-Za-z0-9' '_')"
    if [[ ! -d "$dir" ]] && ! git clone -q --filter=blob:none --no-checkout "$url" "$dir" 2>/dev/null; then
      printf '| %s | `%s` | ? | ? | ? | upstream not reachable |\n' "$name" "${sha:0:7}"; bad=1; continue
    fi
    head="$(git -C "$dir" rev-parse origin/HEAD)"
    if ! git -C "$dir" merge-base --is-ancestor "$sha" "$head" 2>/dev/null; then
      printf '| %s | `%s` | `%s` | ? | ? | pin not in the default branch: re-assay from scratch |\n' "$name" "${sha:0:7}" "${head:0:7}"; bad=1; continue
    fi
    n="$(git -C "$dir" rev-list --count "$sha..$head" -- "${path:-.}")"
    changed="$(git -C "$dir" diff --name-only "$sha" "$head" -- "${path:-.}" | grep -cE "$EXEC_FILES" || true)"
    note="no change"
    (( n == 0 )) || note="read with scripts/repin.sh $name"
    printf '| %s | `%s` | `%s` | %s | %s | %s |\n' "$name" "${sha:0:7}" "${head:0:7}" "$n" "$changed" "$note"
  done
  exit "$bad"
fi

pin="$(pin_of "$entry")" || { echo "no entry named '$entry' in the marketplace or entries/" >&2; exit 2; }

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
exec_changes="$(git diff --name-only "$sha" "$head" -- "${scope[@]}" | grep -E "$EXEC_FILES" || true)"
if [[ -n "$exec_changes" ]]; then
  echo "Changes to what the plugin can execute (read these first in the re-assay):"
  echo "$exec_changes" | sed 's/^/  /'
else
  echo "No changes to hooks, MCP config, manifests or scripts."
fi
echo
echo "To re-assay: read the diff with the five stages in RUBRIC.md, add new cracks with new IDs,"
echo "then move the SHA in .grok-plugin/marketplace.json and in entries/$entry.md in one pull request."
