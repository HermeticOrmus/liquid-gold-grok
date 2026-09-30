# Menu: liquid-gold-grok

Queue: 2026-09-30-pantry-queue.md
Counts: open 7, in flight 0, shipped 0, parked 0, dropped 0, needs fixing 0

## Steer

- none

## Up next

**repin-all**: Report drift for every pin (`repin-all`) (queue #4, high, repo, since 2026-09-30)

- Done when: `scripts/repin.sh --all` prints one row per card in `entries/` with the pinned SHA, the upstream head, the number of commits since the pin that touch the plugin folder, and whether hooks, MCP config, manifests or scripts changed; it exits 0 when every upstream is reachable; CONTRIBUTING.md's re-assay section names the command
- Verify on: repo
- Evidence: Matrix row "Shows upstream changes before a pin moves" (xAI and Anthropic open SHA-bump pull requests; ours works one entry at a time)
- Issue: none yet (promote after merge)
- Order: repin-all, sentry, supabase, libre-geo, libre-secops-hooks, sprites, chrome-devtools
- Tie: repin-all over sentry, supabase, by key order (jev off)

## Atoms

| Key | Title | State | Confidence | Class | Since | Queue # | Issue | Because |
|-----|-------|-------|------------|-------|-------|---------|-------|---------|
| chrome-devtools | Raise `chrome-devtools` from assayed to gold | open | low | repo | 2026-09-30 | 7 | - | - |
| libre-geo | Seal the `libre-geo` privacy promise and admit it | open | medium | repo | 2026-09-30 | 5 | - | - |
| libre-secops-hooks | Teach `libre-secops-hooks` Grok's hook input | open | medium | repo | 2026-09-30 | 6 | - | - |
| repin-all | Report drift for every pin (`repin-all`) | open | high | repo | 2026-09-30 | 4 | - | - |
| sentry | Assay `sentry` from the official catalog | open | high | repo | 2026-09-30 | 1 | - | - |
| sprites | Assay the Grok-native `sprites` plugin | open | medium | repo | 2026-09-30 | 3 | - | - |
| supabase | Assay `supabase` from the official catalog | open | high | repo | 2026-09-30 | 2 | - | - |

## Retired

| Key | Title | State | Since | Issue | Because |
|-----|-------|-------|-------|-------|---------|
| none | | | | | |

## Notes

- none
