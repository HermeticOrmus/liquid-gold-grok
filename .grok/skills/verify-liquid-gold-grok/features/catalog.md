# Cards, catalog and marketplace agree

A reader picks an entry from CATALOG.md or README.md, opens its card, and trusts that the
level, the pin, the crack counts and the links there are the same facts the marketplace file
installs. This feature is the agreement between those files.

## Sub-features

- `catalog-parse` every JSON file parses, and every YAML file under `.github/` parses.
- `catalog-pins` every marketplace entry is remote and pinned to a full 40-character SHA.
- `catalog-links` every card is linked from CATALOG.md and every catalog link has a card.
- `catalog-levels` every marketplace entry has a gold or assayed card with the same SHA; no
  watch card is in the marketplace.
- `catalog-ledger` every ledger row has seven cells and a grade, and each card's level obeys
  the rubric.
- `catalog-counts` the level counts, entry total and crack and sealed totals in CATALOG.md and
  README.md match the cards.

## How to get to it (user POV)

- Read README.md and CATALOG.md on GitHub, then open a card under `entries/`.

## Driving it with scripts/check_catalog.py

Preconditions:

- The baseline in [README.md](./README.md) holds. No Grok CLI or network is needed for this one.

- **Run the check.** Run `python3 scripts/check_catalog.py`. Exit code `0` and one line
  `ok: <M> marketplace entries, <C> cards, all linked from CATALOG.md`.
- **Read a failure.** On exit `1` it prints one line per problem naming the file. Each line is
  a FAIL with rung `check`.
- **Confirm by reading.** For each card the change touched, open it and compare its Level and
  Pinned SHA rows with its row in `.grok-plugin/marketplace.json` and in CATALOG.md.
- **Proof.** The command, its output and exit code, with the head SHA. `bin/prove` keeps this in
  `check.log` under the "cards, catalog and marketplace" heading.

## Gotchas

- The check counts a crack as sealed only when its State starts with `sealed` or
  `hallmarked`; a `withdrawn` row stays in the found total.
- YAML under `.github/` is parsed only when PyYAML is installed. CI has it; a bare local Python
  may skip that part silently.
- A green check does not mean a card's prose is right. It means the counted facts agree.
