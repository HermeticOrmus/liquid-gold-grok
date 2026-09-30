#!/usr/bin/env bash
# Prove every entry in .grok-plugin/marketplace.json installs clean at its pin.
#
# For each entry: a fresh GROK_HOME and HOME, add this marketplace, install the
# entry by name, then check that
#   - the installed commit is the pinned SHA and the plugin carries the entry's name,
#   - `grok plugin validate` and `grok plugin details` pass,
#   - what Grok loaded (`grok inspect --json`: skills, agents, commands, hook
#     events, MCP servers) matches the card's "Components at the pin" row.
# The "files" column says whether the plugin folder holds more than Grok loaded
# (a component Grok skipped); the card's ledger explains any difference.
# Prints one table row per entry and exits 1 on any failure.
#
# Usage:
#   scripts/verify.sh                 verify every entry
#   scripts/verify.sh <name> ...      verify only these entries
#   MARKETPLACE=HermeticOrmus/liquid-gold-grok scripts/verify.sh
#                                     verify the published marketplace instead
#                                     of this checkout
set -euo pipefail
IFS=$'\n\t'

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="$ROOT/.grok-plugin/marketplace.json"
GROK="${GROK:-$(command -v grok || true)}"
[[ -n "$GROK" ]] || GROK="$HOME/.grok/bin/grok"
[[ -x "$GROK" ]] || { echo "grok not found; install it with: curl -fsSL https://x.ai/cli/install.sh | bash" >&2; exit 2; }

MARKETPLACE="${MARKETPLACE:-$ROOT}"
if [[ -d "$MARKETPLACE" ]]; then
  MK_NAME="$(basename "$MARKETPLACE")"   # a local marketplace registers under its folder name
else
  MK_NAME="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["name"])' "$MANIFEST")"
fi

WORK="$(mktemp -d)"
trap 'rm -rf "${WORK:?}"' EXIT

entries="$(python3 - "$MANIFEST" "$@" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
want = set(sys.argv[2:])
for p in m["plugins"]:
    if want and p["name"] not in want:
        continue
    s = p["source"]
    print("\t".join([p["name"], s["url"], s["sha"], s.get("path", "")]))
PY
)"
[[ -n "$entries" ]] || { echo "no matching entries" >&2; exit 2; }

row() { printf '| %-24s | %-7s | %-7s | %-6s | %-8s | %-7s | %-44s | %-7s | %-5s | %-6s |\n' "$@"; }
echo "grok: $("$GROK" --version)"
echo "marketplace: $MARKETPLACE (as $MK_NAME)"
echo
row entry sha install commit validate details "loaded by grok" files card result
printf '|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|\n' "$(printf -- '-%.0s' {1..26})" "---------" "---------" "--------" "----------" "---------" "$(printf -- '-%.0s' {1..46})" "---------" "-------" "--------"

failed=0
total=0
while IFS=$'\t' read -r name url sha path; do
  total=$((total + 1))
  base="$WORK/$name"; gh="$base/grok-home"; hm="$base/home"; cwd="$base/cwd"; log="$base/log"
  mkdir -p "$gh" "$hm" "$cwd"
  run() { GROK_HOME="$gh" HOME="$hm" "$GROK" "$@" >>"$log" 2>&1; }

  install=fail commit=- validate=- details=- loaded=- files=- card=- result=FAIL
  if run plugin marketplace add "$MARKETPLACE" && run plugin install "$name@$MK_NAME" --trust; then
    install=ok
    info="$(python3 - "$gh/installed-plugins/registry.json" "$name" <<'PY'
import json, sys
reg = json.load(open(sys.argv[1]))
for repo in reg.get("repos", {}).values():
    if sys.argv[2] in repo.get("plugins", {}):
        sub = repo["plugins"][sys.argv[2]].get("subdir") or repo["kind"].get("subdir") or ""
        print(repo["kind"].get("commit", "") + "\t" + repo["path"] + ("/" + sub if sub else ""))
        break
PY
)"
    got_commit="${info%%$'\t'*}"; dir="${info#*$'\t'}"
    if [[ -z "$info" ]]; then
      commit=name
      echo "installed, but no plugin named $name (the entry name must match the plugin's manifest name)" >>"$log"
    elif [[ "$got_commit" == "$sha" ]]; then
      commit=ok
      run plugin validate "$dir" && validate=ok || validate=fail
      run plugin details "$name" && details=ok || details=fail
      if (cd "$cwd" && GROK_HOME="$gh" HOME="$hm" "$GROK" inspect --json >"$base/inspect.json" 2>>"$log"); then
        loaded="$(python3 "$ROOT/scripts/loaded_components.py" "$base/inspect.json" "$name" "$dir")"
      fi
      on_disk="$(python3 "$ROOT/scripts/count_components.py" "$dir")"
      if [[ "$on_disk" == "$loaded" ]]; then files=same; else files=more; echo "files on disk: $on_disk" >>"$log"; fi
      card_counts="$(python3 - "$ROOT/entries/$name.md" <<'PY'
import re, sys
try:
    text = open(sys.argv[1], encoding="utf-8").read()
except OSError:
    sys.exit(0)
m = re.search(r"^\| Components at the pin \| (.+?) \|$", text, re.M)
if m:
    nums = dict(re.findall(r"(skills|agents|commands|hook events|MCP servers) (\d+)", m.group(1)))
    keys = [("skills", "skills"), ("agents", "agents"), ("commands", "commands"), ("hooks", "hook events"), ("mcp", "MCP servers")]
    print(" ".join(f"{k}={nums.get(c, '?')}" for k, c in keys))
PY
)"
      if [[ -z "$card_counts" ]]; then card=none
      elif [[ "$card_counts" == "$loaded" ]]; then card=ok
      else card=diff; echo "card says: $card_counts" >>"$log"; echo "grok loaded: $loaded" >>"$log"; fi
    else
      commit=diff
    fi
  fi
  if [[ $install == ok && $commit == ok && $validate == ok && $details == ok && $card == ok ]]; then
    result=PASS
  else
    failed=$((failed + 1))
  fi
  row "$name" "${sha:0:7}" "$install" "$commit" "$validate" "$details" "$loaded" "$files" "$card" "$result"
  if [[ $result == FAIL ]]; then
    sed 's/^/    /' "$log" >&2
  fi
done <<<"$entries"

echo
echo "$((total - failed)) of $total entries passed"
[[ $failed -eq 0 ]]
