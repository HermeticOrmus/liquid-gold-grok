# Install an entry at its pin

A user adds this marketplace to the Grok Build CLI and installs an entry by name. The install
lands on the commit the card pins, Grok validates the plugin and lists its details, and the
skills, agents, commands, hook events and MCP servers Grok loads match the card's
"Components at the pin" row.

## Sub-features

- `install-add` adds the marketplace, local or published.
- `install-one` installs one entry by name with `--trust`.
- `install-pin` lands on the pinned SHA, and the installed plugin carries the entry's name.
- `install-loaded` matches what `grok inspect --json` loads with the card's row.
- `install-all` repeats the above for every marketplace entry.

## How to get to it (user POV)

- Run `grok plugin marketplace add HermeticOrmus/liquid-gold-grok`, then
  `grok plugin install <entry>@liquid-gold-grok`, as each card's Install section says.
- From a checkout, add the folder instead: `grok plugin marketplace add "$PWD"`.

## Driving it with scripts/verify.sh

Preconditions:

- The baseline in [README.md](./README.md) holds.
- You know which entries the change touched (the cards and marketplace rows in the diff).

- **One entry, the head under review.** Run `bin/prove --pr N --expect <sha> -- <entry>`.
  The table row for `<entry>` reads `ok` in install, commit, validate and details, `same` or
  `more` in files, `ok` in card, and `PASS` in result. The last line reads `1 of 1 entries passed`.
- **Every entry.** Run `bin/prove --pr N --expect <sha>` with no entries. The last line reads
  `N of N entries passed`, where N is the number of plugins in `.grok-plugin/marketplace.json`.
- **The published marketplace.** Run `MARKETPLACE=HermeticOrmus/liquid-gold-grok scripts/verify.sh <entry>`.
  It installs from GitHub's copy of main instead of the checkout; use it to show what users get
  today, not to judge a pull request.
- **By hand, the way a user does.** Run
  `export GROK_HOME="$(mktemp -d)" HOME="$(mktemp -d)"`, then
  `grok plugin marketplace add "$PWD"`,
  `grok plugin install <entry>@"$(basename "$PWD")" --trust` and
  `grok plugin details <entry>`. Exit code `0` on each, and the details name the entry.
- **Proof.** `check.log` in the run's evidence directory holds the table; paste the rows for
  the touched entries with the head SHA.

## Gotchas

- `files more` is not a failure by itself: the plugin folder holds a component Grok skipped.
  It needs a ledger row on the card that names it (RUBRIC.md), or it is a crack.
- `commit name` means the install worked but no plugin carries the entry's name: the
  marketplace `name` must equal the plugin manifest's name.
- A watch card is never in the marketplace, so it has no install row; `catalog.md` covers it.
- An upstream that is down fails the install. Re-run that entry before calling it a FAIL.
