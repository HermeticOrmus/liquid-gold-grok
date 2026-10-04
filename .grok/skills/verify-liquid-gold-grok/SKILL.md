---
name: verify-liquid-gold-grok
description: Prove a head of the Liquid Gold for Grok Build library (a Grok Build plugin marketplace with kintsugi cards) on its user surface, the Grok Build CLI. Checks one exact commit in a scratch clone, installs every marketplace entry at its pin in a fresh Grok home, compares what Grok loads with each card, and keeps the log. Use when proving a pull request's Done-when, reproducing an install failure, or showing that main is green.
---

# Verify Liquid Gold for Grok Build

This repo has no server. What a user touches is the marketplace: they add it to the Grok
Build CLI and install an entry by name. So the proof is an install, done the way a user
does it, in a Grok home nobody else uses, at the exact commit under review.

The one check command is `scripts/check.sh`: the marketplace file parses, the cards, the
catalog and the marketplace agree (`scripts/check_catalog.py`), and every entry installs
at its pin with what Grok loads matching its card (`scripts/verify.sh`). CI runs the same
command (`.github/workflows/check.yml`).

Helper (executable, bash): `.grok/skills/verify-liquid-gold-grok/bin/prove`

```bash
P=.grok/skills/verify-liquid-gold-grok/bin/prove
$P --help
$P --pr 17 --expect <head sha>          # the head under review, every entry
$P --pr 17 --expect <head sha> -- sentry supabase   # only the entries the PR touched
$P --ref main                           # what main holds now
$P                                      # this checkout at HEAD (reports dirty: true if edited)
```

One JSON line on stdout (`head`, `source`, `dirty`, `exit`, `evidence`), the check's own
output on stderr. Exit is the check's exit code, 3 when the head is not the expected one.

## Launch

- **Needs:** Python 3, git, network access to GitHub, and the Grok Build CLI on `PATH`
  (`curl -fsSL https://x.ai/cli/install.sh | bash`, then `$HOME/.grok/bin`). Plugin
  commands need no login.
- **Head.** `--pr N` clones the public repo into a scratch directory and checks out
  `pull/N/head`; `--ref REF` does the same for a branch or tag. `--expect SHA` refuses any
  other head, so pass the head SHA the review names.
- **Isolation.** `scripts/verify.sh` gives every entry its own temporary `GROK_HOME` and
  `HOME`, so two runs can go side by side and the user's own Grok home is never read or
  written.
- **Ready.** There is nothing to wait for. A run is ready to judge when the JSON line
  prints.
- **Teardown.** `prove` removes its scratch clone on exit; `verify.sh` removes its
  temporary homes. Nothing else is started.

## Doctor

```bash
grok --version                                 # a Grok Build CLI is on PATH
git rev-parse HEAD                             # the head you think you are on
python3 -m json.tool .grok-plugin/marketplace.json > /dev/null && echo json ok
```

Run these first when anything looks off. A `grok not found` from `verify.sh` (exit 2)
means the CLI is missing, not that an entry failed.

## Drive

The feature map in [features/README.md](features/README.md) has one recipe per feature.
For a pull request:

1. Read which files changed. A card or the marketplace file changed: name those entries
   after `--`. Scripts, the rubric or CI changed: run every entry.
2. Run `prove --pr N --expect <head sha>` with those entries.
3. Read the table. Every row must end in `PASS`. A `diff` in `commit` means the install did
   not land on the pin; a `diff` in `card` means the card's "Components at the pin" row and
   what Grok loaded disagree; `files more` means the plugin folder holds a component Grok
   skipped, which the card's ledger must explain (RUBRIC.md).
4. For a Done-when that names something the check does not cover (a seal merged upstream,
   a pin moved), drive that feature's recipe too and keep its output.

## Evidence

- Each run writes `<evidence>/head.txt` (the head and its subject, the source, dirty or
  not, the entries, the Grok version), `<evidence>/check.log` (the full check output with
  the per-entry table) and `<evidence>/result.json`.
- Evidence lives under `$VERIFY_LIQUID_GOLD_GROK_HOME`, default
  `${XDG_STATE_HOME:-$HOME/.local/state}/verify-liquid-gold-grok/evidence/<head12>-<stamp>/`.
- A verdict cites the head SHA and pastes the table rows from `check.log`. A green CI run
  alone is not proof of a Done-when; the rows for the entries the PR touched are.
- `dirty: true` means the run judged a checkout with local edits. Never post a verdict
  from a dirty run; use `--pr`.

## Cleanup

`prove` and `verify.sh` remove what they created. The evidence directory stays. To clear
old evidence, delete directories under `.../verify-liquid-gold-grok/evidence/` by name;
never delete the Grok home in `$HOME/.grok`.

## Maintain

When a feature changes or a new script lands, update its file under `features/` in the
same pull request. A recipe that no longer matches the repo is a crack in this skill: fix
the recipe, not the check.
