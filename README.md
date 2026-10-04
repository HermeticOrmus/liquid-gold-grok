<p align="center">
  <img src="https://ormus.solutions/mascot/pixellab_liquid_to_swan.gif" alt="Liquid Gold for Grok Build" width="128" style="image-rendering: pixelated;" />
</p>

<h1 align="center">Liquid Gold for Grok Build</h1>

<p align="center">
  <em>A living library of Grok Build plugins — each one kintsugi-verified: cracks traced with evidence, seals in plain sight, one pinned commit that survived</em>
</p>

<p align="center">
  <a href="https://github.com/HermeticOrmus/liquid-gold-grok/stargazers"><img src="https://img.shields.io/github/stars/HermeticOrmus/liquid-gold-grok?style=flat-square&color=aa8142" alt="Stars" /></a>
  <a href="https://github.com/HermeticOrmus/liquid-gold-grok/blob/main/LICENSE"><img src="https://img.shields.io/github/license/HermeticOrmus/liquid-gold-grok?style=flat-square&color=aa8142" alt="License" /></a>
  <a href="https://github.com/HermeticOrmus/liquid-gold-grok/commits"><img src="https://img.shields.io/github/last-commit/HermeticOrmus/liquid-gold-grok?style=flat-square&color=aa8142" alt="Last Commit" /></a>
  <img src="https://img.shields.io/badge/Kintsugi_verified-aa8142?style=flat-square" alt="Kintsugi verified" />
  <img src="https://img.shields.io/badge/Grok_Build-aa8142?style=flat-square&logo=x&logoColor=white" alt="Grok Build" />
</p>

---

> Liquid Gold for Grok Build: the best Grok Build plugins, each one kintsugi-verified. We find the cracks, prove them, seal them with gold, and pin what survives.

## Why kintsugi

Kintsugi mends broken pottery with gold, and the repair is the part people look at. A plugin list that only shows favorites hides the cracks. This one shows them.

Every entry here was pinned to one commit, installed into a clean Grok home, and read for everything it can execute: hooks, scripts, MCP servers, network calls, and whether its README says so. What broke is written down in the entry's ledger with the evidence. What we could seal is sealed where you can see it: a fix already in the pinned commit, a pull request, a workaround in the card, or a draft for the upstream author. An entry that breaks a promise stays out of the marketplace, and its card says why.

The cracks are where the gold goes.

## Install

Add the library as a Grok marketplace once:

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
```

Then install any entry by name:

```bash
grok plugin install design-mastery@liquid-gold-grok
grok plugin list
```

Every entry installs from its upstream repository at the pinned commit, so what you get is exactly what was assayed. `grok plugin details <name>` shows what it loaded.

## Catalog

Two stocks and one later reading hold 41 entries: 11 from the HermeticOrmus Libre packs and design-mastery, 30 by other authors. The two stocks were assayed with grok 1.0.44. The ledgers hold 238 cracks, and 66 of them are sealed.

| Level | Entries |
|-------|---------|
| gold (12) | [api-documentation](entries/api-documentation.md), [cloudflare](entries/cloudflare.md), [communication-buses](entries/communication-buses.md), [design-mastery](entries/design-mastery.md), [frontend-design](entries/frontend-design.md), [ledger-design](entries/ledger-design.md), [mattpocock-skills](entries/mattpocock-skills.md), [mongodb](entries/mongodb.md), [multiplayer-networking](entries/multiplayer-networking.md), [netlify-skills](entries/netlify-skills.md), [ponytail](entries/ponytail.md), [rag-architecture](entries/rag-architecture.md) |
| assayed (15) | [chrome-devtools](entries/chrome-devtools.md), [compound-engineering](entries/compound-engineering.md), [datadog](entries/datadog.md), [domain-driven-design](entries/domain-driven-design.md), [feature-dev](entries/feature-dev.md), [handoff](entries/handoff.md), [kubernetes-operations](entries/kubernetes-operations.md), [modern-web-guidance](entries/modern-web-guidance.md), [pr-review-toolkit](entries/pr-review-toolkit.md), [pstack](entries/pstack.md), [railway](entries/railway.md), [sentry](entries/sentry.md), [sprites](entries/sprites.md), [supabase](entries/supabase.md), [superpowers](entries/superpowers.md) |
| watch (14) | [axiorank](entries/axiorank.md), [claude-mem](entries/claude-mem.md), [epic](entries/epic.md), [figma](entries/figma.md), [firecrawl](entries/firecrawl.md), [hindsight-memory](entries/hindsight-memory.md), [last30days](entries/last30days.md), [libre-geo](entries/libre-geo.md), [libre-secops-hooks](entries/libre-secops-hooks.md), [oh-my-grok](entries/oh-my-grok.md), [security-guidance](entries/security-guidance.md), [stripe](entries/stripe.md), [unity](entries/unity.md), [vercel](entries/vercel.md) |

Gold and assayed entries are in the marketplace. Watch entries are not: each card says what holds it back, from a license that is missing to a privacy promise the code does not keep.

The full table, with domains and install lines, is in [CATALOG.md](CATALOG.md). Each name links to its card: what it does, who it is for, what it can execute, the assay, and the ledger.

## How an entry earns gold

Five stages, in order, each ending on a check: ready the vessel (a full SHA, a clean Grok home), trace the cracks (the gates, the reading, and optionally the hands), keep the ledger, seal with gold, and hallmark. The levels:

- **gold**: hallmarked. Installs clean at the pin, nothing it executes is hidden, no break or fracture left open.
- **assayed**: admitted. Installs clean, no break open, and every open fracture carries a workaround in the card and a seal draft.
- **watch**: promising, not admitted. The card says what holds it back.

The full rubric is in [RUBRIC.md](RUBRIC.md). `scripts/verify.sh` re-proves every marketplace entry in CI on every change, and `scripts/repin.sh <entry>` shows what moved upstream before a pin is allowed to move. New candidates come from a public mine: `scripts/mine.py` lists the plugins in xAI's catalog and on GitHub that have no card yet, and a scheduled run restocks the [pantry](pantry/) with that list and a drift report from `scripts/repin.sh --all`.

## Feedback

Tell us what worked and what is missing: [open a feedback issue](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=feedback.yml). Every piece of feedback gets an answer, and changes that come from it are credited.

## Contribute

Pick a crack. Seal it with gold.

- [Nominate a plugin](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=nominate.yml), or [report a crack](https://github.com/HermeticOrmus/liquid-gold-grok/issues/new?template=crack.yml) in an entry.
- Take the next item on the [Menu](pantry/MENU.md) or a [good first issue](https://github.com/HermeticOrmus/liquid-gold-grok/contribute).
- Ask and share in [Discussions](https://github.com/HermeticOrmus/liquid-gold-grok/discussions).

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to seal a crack, re-assay a pinned entry, and test your change locally.

## License

The library (cards, rubric, scripts) is MIT. Each entry keeps its own license, linked from its card; installing an entry installs the author's code under the author's terms.

MIT © 2026 [Diego Bodart](https://github.com/HermeticOrmus). See [LICENSE](LICENSE). Built under the [Gold Hat principle](GOLD_HAT.md).

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
