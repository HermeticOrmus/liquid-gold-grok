# Pantry queue: Liquid Gold for Grok Build

## How this fills

1. Read the latest competitor map, X mine and people mine, and the newest candidate mine and drift report.
2. Propose 5 to 8 Goal atoms that answer their themes. The Menu needs at least 3.
3. Each atom needs a Done predicate someone else can check on this repo, a surface, the evidence rows it answers, and a confidence (high, medium or low).
4. Save as `YYYY-MM-DD-pantry-queue.md`; the Menu reads the newest one.
5. Retire an atom only with a bullet under "Explicitly not stocked" of the form `<Title>: shipped, PR #N` or `<Title>: parked, <reason>`.

## Atoms

Sources: carried over from [2026-10-01 queue](2026-10-01-pantry-queue.md); new atoms from the [2026-10-01 candidate mine](2026-10-01-candidate-mine.md). Written by the gold-menu loop (deterministic: open atoms carried verbatim, merged ones retired below, the top new candidates added in the mine's order).

| # | Title | Done predicate | Surface | Evidence | Confidence |
|---|-------|----------------|---------|----------|------------|
| 1 | Assay `unity` from the official catalog | `entries/unity.md` exists for Unity-Technologies/unity-agent-plugin, pinned to a full SHA, and its ledger records what the license file at the pin says (GitHub reports NOASSERTION); it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh unity` prints PASS | repo | Candidate mine row 1 (xAI catalog, 376 stars, license NOASSERTION) | high |
| 2 | Re-assay `chrome-devtools` at its moved upstream | `entries/chrome-devtools.md` is pinned to a newer upstream commit after `scripts/repin.sh chrome-devtools` was read with the five stages; new cracks have new IDs; K-01 reads sealed if the MCP server now ships in a file Grok reads; `scripts/verify.sh chrome-devtools` prints PASS | repo | Drift report row chrome-devtools: 15 commits since the pin, 40 executable files changed; card K-01 and its [seal draft](../seals/chrome-devtools/K-01.md) | medium |
| 3 | Assay `browser-use` from the official catalog | `entries/browser-use.md` exists for browser-use/plugins at the plugin path xAI's catalog pins, with what it can execute and the ledger, and its ledger records whether a license file is present at the pin (GitHub finds none); it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh browser-use` prints PASS | repo | Candidate mine row 9 (xAI catalog, a `grok` plugin path, license none found) | medium |
| 4 | Assay the community `daisyui` plugin | `entries/daisyui.md` exists for saadeghi/daisyui at the folder its `.grok-plugin` manifest names, pinned to a full SHA, with the assay table and ledger; it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh daisyui` prints PASS | repo | Candidate mine row 24 (code search, 42,520 stars, MIT): the most-starred design library in the mine | medium |
| 5 | Seal the `libre-geo` privacy promise and admit it | The LibreGEO README no longer says no data leaves your machine without naming the brand-mention searches (a merged pull request in HermeticOrmus/LibreGEO-Claude-Code); `entries/libre-geo.md` is pinned to a commit that contains it, K-05 reads `sealed #N`, and the level is gold or assayed; `python3 scripts/check_catalog.py` exits 0 and `scripts/verify.sh libre-geo` prints PASS | repo | Card [libre-geo](../entries/libre-geo.md) K-05 and its [seal draft](../seals/libre-geo/K-05.md); drift report row libre-geo (14 commits since the pin) | medium |
| 6 | Teach `libre-secops-hooks` Grok's hook input | The LibreSecOps hook scripts accept Grok's tool names (`search_replace`, `write`, `hashline_edit`, `run_terminal_command`; see `claude_alias.rs` in xai-org/grok-build) as well as Claude's; a test in that repository feeds a Grok-shaped PreToolUse payload for a secret file and gets an ask or a deny; `entries/libre-secops-hooks.md` is re-pinned to that commit with its breaks sealed or regraded, and `python3 scripts/check_catalog.py` exits 0 | repo | Card [libre-secops-hooks](../entries/libre-secops-hooks.md) and its seal drafts; the same Bash-name crack in [railway](../entries/railway.md) K-02 | medium |
| 7 | Assay `base44` from the official catalog | `entries/base44.md` exists for base44/skills, pinned to a full SHA, with what it can execute, the assay table and the ledger, and its ledger records what the license file at the pin says (GitHub reports MIT); it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh base44` prints PASS | repo | Candidate mine row 2 (xAI catalog, 91 stars, license MIT) in [2026-10-01 candidate mine](2026-10-01-candidate-mine.md) | medium |
| 8 | Assay `wix` from the official catalog | `entries/wix.md` exists for wix/skills, pinned to a full SHA, with what it can execute, the assay table and the ledger, and its ledger records what the license file at the pin says (GitHub reports MIT); it is linked from `CATALOG.md`; `python3 scripts/check_catalog.py` exits 0; if admitted, `scripts/verify.sh wix` prints PASS | repo | Candidate mine row 3 (xAI catalog, 33 stars, license MIT) in [2026-10-01 candidate mine](2026-10-01-candidate-mine.md) | medium |

## Explicitly not stocked (and why)

- Assay `sentry` from the official catalog: shipped, PR #5
- Assay `supabase` from the official catalog: shipped, PR #5
- Assay the Grok-native `sprites` plugin: shipped, PR #5
- Report drift for every pin (`repin-all`): shipped, PR #5
- Running the hands (a real Grok session) for every hooks entry: it would settle the open hook-runtime cracks, but it spends model time, so it stays with the maintainer's own assays rather than the public Menu.
- A web page for the catalog: the Markdown catalog renders on GitHub and the marketplace file is the product; no voice has asked for more yet.
- Check the catalog counts against the cards (`catalog-counts`): shipped, PR #11
