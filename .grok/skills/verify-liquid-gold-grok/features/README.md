# Liquid Gold for Grok Build verification map

This directory is the maintained source for verifying what a user of this library touches:
the marketplace in the Grok Build CLI, the cards and catalog they read before installing,
and the drift report that tells a maintainer a pin has moved upstream. Read the index, then
use the matching feature file as the recipe.

## Baseline preconditions

- The Grok Build CLI is on `PATH` (`grok --version` prints a version). No login is needed.
- Python 3, git and network access to GitHub.
- The head under review is checked out in a scratch clone by `bin/prove --pr N --expect <sha>`,
  or you are in a clean checkout whose `git rev-parse HEAD` is that SHA.
- Every install runs in a temporary `GROK_HOME` and `HOME`. Never install into the Grok home
  of the person running the check.

## Driving conventions

- Run commands from the repo root of the head under review.
- Treat every command and entry name as literal. Entry names are the `name` fields in
  `.grok-plugin/marketplace.json` and the file names in `entries/`.
- A local marketplace registers under its folder name; the published one registers as
  `liquid-gold-grok`. Install with `<entry>@<that name>`.
- Nothing here changes the repo. A recipe that would edit a card or the marketplace file is
  a contribution, not a verification.

## Proof and skip reporting

- CLI proof is the command, its output and its exit code, kept in the run's evidence
  directory (`bin/prove` does this).
- Name the head SHA and the entries checked with every artifact.
- An entry that could not be installed because GitHub or the upstream was unreachable is
  INCONCLUSIVE, not FAIL; say which upstream and paste the error.
- Do not report an entry as verified because a different entry passed.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible
behavior, then exactly four H2 sections in this order: `Sub-features`,
`How to get to it (user POV)`, `Driving it with <harness>` (starting with `Preconditions:`),
and `Gotchas`.

## Features

- [Install an entry at its pin](./install-entry.md) covers adding the marketplace, installing
  one entry or all of them, the pinned commit, and what Grok loads against the card.
- [Cards, catalog and marketplace agree](./catalog.md) covers the level counts, links, pins,
  ledger rows and totals a reader sees in CATALOG.md, README.md and each card.
- [Read the drift on a pin](./drift.md) covers the per-entry drift report and the all-cards
  drift table a re-assay starts from.
