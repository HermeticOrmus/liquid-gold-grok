# Pantry queue: Liquid Gold for Grok Build

## How this fills

1. Read the latest competitor map, X mine and people mine.
2. Propose 5 to 8 Goal atoms that answer their themes. The Menu needs at least 3.
3. Each atom needs a Done predicate someone else can check on this repo, a surface, the evidence rows it answers, and a confidence (high, medium or low).
4. Save as `YYYY-MM-DD-pantry-queue.md`; the Menu reads the newest one.
5. Retire an atom only with a bullet under "Explicitly not stocked" of the form `<Title>: shipped, PR #N` or `<Title>: parked, <reason>`.

## Atoms

Sources: [competitor map](2026-09-30-competitor-map.md), [X mine](2026-09-30-x-mine.md) (no hits), [people mine](2026-09-30-people-mine.md) (no outside voices yet), and the first stock of entry cards in [`entries/`](../entries/).

| # | Title | Done predicate | Surface | Evidence | Confidence |
|---|-------|----------------|---------|----------|------------|
| 1 | Assay `sentry` from the official catalog | `entries/sentry.md` exists for getsentry/plugin-grok, pinned to a full SHA, with the assay table, the ledger and a level; it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if the level is gold or assayed, the entry is in `.grok-plugin/marketplace.json` and `scripts/verify.sh sentry` prints PASS | repo | Map row xai-org/plugin-marketplace (lists `sentry`; xAI does not publish per-entry findings); matrix row "Publishes per-entry findings with evidence" | high |
| 2 | Assay `supabase` from the official catalog | `entries/supabase.md` exists for supabase-community/supabase-plugin, pinned to a full SHA, and its ledger records whether a license file is present at the pin (the manifest states MIT); it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh supabase` prints PASS | repo | Map row xai-org/plugin-marketplace (lists `supabase`); matrix row "Checks the license" (xAI P) | high |
| 3 | Assay the Grok-native `sprites` plugin | `entries/sprites.md` exists for superfly/sprites-grok-plugin, pinned to a full SHA, with what it can execute and the ledger; it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh sprites` prints PASS | repo | Map row DominikTobureto/awesome-grok-build (lists Grok resources without installing them); matrix row "Tested under Grok Build" | medium |
| 4 | Report drift for every pin (`repin-all`) | `scripts/repin.sh --all` prints one row per card in `entries/` with the pinned SHA, the upstream head, the number of commits since the pin that touch the plugin folder, and whether hooks, MCP config, manifests or scripts changed; it exits 0 when every upstream is reachable; CONTRIBUTING.md's re-assay section names the command | repo | Matrix row "Shows upstream changes before a pin moves" (xAI and Anthropic open SHA-bump pull requests; ours works one entry at a time) | high |
| 5 | Seal the `libre-geo` privacy promise and admit it | The LibreGEO README no longer says no data leaves your machine without naming the brand-mention searches (a merged pull request in HermeticOrmus/LibreGEO-Claude-Code); `entries/libre-geo.md` is pinned to a commit that contains it, K-05 reads `sealed #N`, and the level is gold or assayed; `python3 scripts/check_catalog.py` exits 0 and `scripts/verify.sh libre-geo` prints PASS | repo | Card [libre-geo](../entries/libre-geo.md) K-05 and its [seal draft](../seals/libre-geo/K-05.md); matrix row "Reads what a plugin executes" | medium |
| 6 | Teach `libre-secops-hooks` Grok's hook input | The LibreSecOps hook scripts accept Grok's tool names (`search_replace`, `write`, `hashline_edit`, `run_terminal_command`; see `claude_alias.rs` in xai-org/grok-build) as well as Claude's; a test in that repository feeds a Grok-shaped PreToolUse payload for a secret file and gets an ask or a deny; `entries/libre-secops-hooks.md` is re-pinned to that commit with its breaks sealed or regraded, and `python3 scripts/check_catalog.py` exits 0 | repo | Card [libre-secops-hooks](../entries/libre-secops-hooks.md) and its seal drafts; matrix row "Tested under Grok Build" | medium |
| 7 | Raise `chrome-devtools` from assayed to gold | Upstream chrome-devtools-mcp ships the MCP server in a file Grok reads; at a new pin `grok plugin details chrome-devtools` shows MCP servers, the card's K-01 reads sealed with the upstream link, the level is gold, and `scripts/verify.sh chrome-devtools` prints PASS with `mcp=1` | repo | Card [chrome-devtools](../entries/chrome-devtools.md) K-01 and its [seal draft](../seals/chrome-devtools/K-01.md); map row xai-org/plugin-marketplace (lists the same plugin) | low |

## Explicitly not stocked (and why)

- Running the hands (a real Grok session) for every hooks entry: it would settle the open hook-runtime cracks, but it spends model time, so it stays with the maintainer's own assays rather than the public Menu.
- A web page for the catalog: the Markdown catalog renders on GitHub and the marketplace file is the product; no voice has asked for more yet.
