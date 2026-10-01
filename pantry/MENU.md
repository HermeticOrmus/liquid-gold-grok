# Menu: liquid-gold-grok

Queue: 2026-10-01-pantry-queue.md
Counts: open 7, in flight 0, shipped 4, parked 0, dropped 0, needs fixing 0

## Steer

- none

## Up next

**catalog-counts**: Check the catalog counts against the cards (`catalog-counts`) (queue #1, high, repo, since 2026-10-01)

- Done when: `python3 scripts/check_catalog.py` fails, naming the file and the number, when the level counts, the entry total, or the crack and sealed totals written in `CATALOG.md` or `README.md` differ from what the cards in `entries/` hold; the library itself still passes
- Verify on: repo
- Evidence: The second stock moved every count by hand (27 to 40 entries, 160 to 234 cracks), and a hand-kept catalog cell for pstack was cut off until this stock found it
- Issue: none yet (promote after merge)
- Order: catalog-counts, unity, chrome-devtools, libre-geo, libre-secops-hooks, browser-use, daisyui
- Tie: catalog-counts over unity, by key order (jev off)

## Atoms

| Key | Title | State | Confidence | Class | Since | Queue # | Issue | Because |
|-----|-------|-------|------------|-------|-------|---------|-------|---------|
| browser-use | Assay `browser-use` from the official catalog | open | medium | repo | 2026-10-01 | 4 | - | - |
| catalog-counts | Check the catalog counts against the cards (`catalog-counts`) | open | high | repo | 2026-10-01 | 1 | - | - |
| chrome-devtools | Re-assay `chrome-devtools` at its moved upstream | open | medium | repo | 2026-09-30 | 3 | - | - |
| daisyui | Assay the community `daisyui` plugin | open | medium | repo | 2026-10-01 | 5 | - | - |
| libre-geo | Seal the `libre-geo` privacy promise and admit it | open | medium | repo | 2026-09-30 | 6 | - | - |
| libre-secops-hooks | Teach `libre-secops-hooks` Grok's hook input | open | medium | repo | 2026-09-30 | 7 | - | - |
| unity | Assay `unity` from the official catalog | open | high | repo | 2026-10-01 | 2 | - | - |

## Retired

| Key | Title | State | Since | Issue | Because |
|-----|-------|-------|-------|-------|---------|
| repin-all | Report drift for every pin (`repin-all`) | shipped | 2026-09-30 | #3 | bullet: Report drift for every pin (`repin-all`): shipped, PR #5 |
| sentry | Assay `sentry` from the official catalog | shipped | 2026-09-30 | #6 | bullet: Assay `sentry` from the official catalog: shipped, PR #5 |
| sprites | Assay the Grok-native `sprites` plugin | shipped | 2026-09-30 | - | bullet: Assay the Grok-native `sprites` plugin: shipped, PR #5 |
| supabase | Assay `supabase` from the official catalog | shipped | 2026-09-30 | - | bullet: Assay `supabase` from the official catalog: shipped, PR #5 |

## Notes

- README latest run points at 2026-09-30-pantry-queue.md, newest file is 2026-10-01-pantry-queue.md
