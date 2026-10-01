# Contributing

Pick a crack. Seal it with gold.

This library admits a Grok Build plugin only after an assay: one pinned commit, a clean install, a reading of everything it can execute, and a ledger of what broke and how it was sealed. You can help at any of those steps. The rules for every step are in [RUBRIC.md](RUBRIC.md).

## Ways to contribute

- **Take a Menu item.** The pantry names the next useful work, with a check anyone can run: [pantry/MENU.md](pantry/MENU.md). Open items are also issues labeled `menu` ([the menu filter](https://github.com/HermeticOrmus/liquid-gold-grok/issues?q=is%3Aopen+label%3Amenu)), and smaller ones are under [good first issues](https://github.com/HermeticOrmus/liquid-gold-grok/contribute). Comment on the issue to claim it, then open a pull request that says `Closes #N`.
- **Nominate a plugin** with the [nomination form](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=nominate.yml).
- **Report a crack** in an entry with the [crack form](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=crack.yml).
- **Seal a crack** in an entry card, or upstream in the plugin's own project.
- **Re-assay a pinned entry** when its upstream moves.
- **Share what you built** with an entry in [Discussions](https://github.com/HermeticOrmus/liquid-gold-grok/discussions).

## Nominate a plugin

Use the [nomination form](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=nominate.yml): the repository (and subfolder), what it does, why it might be gold, and any cracks you already know. You can also run the assay yourself and open a pull request:

1. Copy [templates/entry-card.md](templates/entry-card.md) to `entries/<plugin name>.md`. The file name is the name Grok resolves for the plugin (the `name:` line of `grok plugin validate`).
2. Run the five stages in [RUBRIC.md](RUBRIC.md) and fill the card: the assay table, the ledger, what it can execute, and the level.
3. For a gold or assayed entry, add it to `.grok-plugin/marketplace.json` as a remote entry:

   ```json
   {
     "name": "<plugin name>",
     "description": "<one line>",
     "category": "<category>",
     "source": {
       "source": "url",
       "url": "https://github.com/<owner>/<repo>.git",
       "sha": "<40-character commit sha>",
       "path": "<subfolder, only when the plugin is not at the repository root>"
     }
   }
   ```

   A plugin at the repository root has no `path`. The key is `path`; Grok ignores `subdir`.
4. Add a row to [CATALOG.md](CATALOG.md). A watch entry gets a card and a catalog row but stays out of the marketplace file.
5. Credit the author and link their license at the pinned commit.

## Report a crack

Use the [crack form](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=crack.yml). Say what is wrong in one or two sentences and show the evidence: a command and its output with your `grok --version`, or a file and line at the pinned SHA. Give your best guess at the grade (hairline, fracture, break); the assay confirms it.

## Seal a crack

A seal is always visible. Pick the form that fits:

- **In the entry card.** Add or update the ledger row, and when there is a workaround, write the exact steps in the card's Workarounds section. Say whether you ran the workaround at the pinned SHA; only a workaround that was run counts as sealed.
- **In the upstream project.** Fix it there, in their style and under their rules, then link the pull request from the ledger row. If you would rather hand it off, add the draft text to `seals/<entry>/K-NN.md` for the maintainer to send.

Never reuse a crack ID. A crack you withdraw keeps its row with the reason.

## Re-assay a pinned entry

1. `scripts/repin.sh --all` prints one drift row per card: the pinned SHA, the upstream head, the commits since the pin that touch the plugin folder, and how many of the changed files are hooks, MCP config, manifests or scripts. Pick a row that moved, then `scripts/repin.sh <entry>` shows its commits and files, and flags the changes to what it can execute.
2. Read that diff with the five stages. New cracks get new IDs.
3. Move the SHA in `.grok-plugin/marketplace.json` and in the card's Pinned SHA and Source rows in one pull request, and update the date of the assay.

### Test your change locally

You need the Grok Build CLI (`curl -fsSL https://x.ai/cli/install.sh | bash`), Python 3 and git. Plugin commands do not need a login.

```bash
# The cards, the catalog and the marketplace file agree
python3 scripts/check_catalog.py

# Every entry installs clean at its pin, in a fresh Grok home per entry
scripts/verify.sh

# Or only the entries you touched
scripts/verify.sh <entry> <entry>

# Validate one plugin folder at its pin
grok plugin validate <path to the plugin folder>
```

To try the marketplace the way a user will, keep your own Grok home out of it:

```bash
export GROK_HOME="$(mktemp -d)" HOME="$(mktemp -d)"
grok plugin marketplace add "$PWD"
grok plugin install <entry>@"$(basename "$PWD")" --trust
grok plugin details <entry>
```

A local marketplace registers under its folder name; the published one registers as `liquid-gold-grok`.

CI runs the same checks on every pull request (`.github/workflows/verify.yml`). A first-time contributor's CI run waits for a maintainer to approve it.

## Style

Plain sentences, the reader's words, no marketing words, no emojis. The gold is proven, never claimed: say what broke and show the seal. Commits follow `type(scope): summary`.
