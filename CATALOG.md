# Catalog

Every entry in the library, with its level. Each name links to its card: what it does, who it is for, what it can execute, the assay, and the ledger of cracks and seals. The rules behind the levels are in [RUBRIC.md](RUBRIC.md).

- **gold** (9): hallmarked, no break or fracture open.
- **assayed** (9): admitted, open fractures carry a workaround in the card.
- **watch** (9): not admitted yet; the card says why. Watch entries are not in the marketplace.

27 entries: 11 from the HermeticOrmus Libre packs and design-mastery, 16 by other authors. All assayed on 2026-09-30 with grok 1.0.44. Their ledgers hold 160 cracks, 55 of them sealed; the rest carry a workaround, a seal draft in [`seals/`](seals/), or the reason an entry waits.

Install any gold or assayed entry after adding the marketplace once:

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
```

| Entry | Level | Domain | Author | Cracks | Install | Pin |
|-------|-------|--------|--------|--------|---------|-----|
| [api-documentation](entries/api-documentation.md) | gold | Technical writing | [Diego Bodart](https://github.com/HermeticOrmus) | 7 found, 4 sealed | `grok plugin install api-documentation@liquid-gold-grok` | `8ec68f3` |
| [cloudflare](entries/cloudflare.md) | gold | Cloud platform | [Cloudflare](https://www.cloudflare.com/) | 2 found, 1 sealed | `grok plugin install cloudflare@liquid-gold-grok` | `626547c` |
| [communication-buses](entries/communication-buses.md) | gold | Embedded | [Diego Bodart](https://github.com/HermeticOrmus) | 6 found, 4 sealed | `grok plugin install communication-buses@liquid-gold-grok` | `8788082` |
| [design-mastery](entries/design-mastery.md) | gold | Design | [Diego Bodart](https://github.com/HermeticOrmus) | 8 found, 6 sealed | `grok plugin install design-mastery@liquid-gold-grok` | `e07686b` |
| [frontend-design](entries/frontend-design.md) | gold | Frontend design | [Anthropic](https://github.com/anthropics) | 3 found, 0 sealed | `grok plugin install frontend-design@liquid-gold-grok` | `ab024cd` |
| [ledger-design](entries/ledger-design.md) | gold | Fintech | [Diego Bodart](https://github.com/HermeticOrmus) | 7 found, 4 sealed | `grok plugin install ledger-design@liquid-gold-grok` | `b49616e` |
| [mattpocock-skills](entries/mattpocock-skills.md) | gold | Engineering workflow | [Matt Pocock](https://www.aihero.dev) | 3 found, 2 sealed | `grok plugin install mattpocock-skills@liquid-gold-grok` | `d81f3a1` |
| [multiplayer-networking](entries/multiplayer-networking.md) | gold | Game development | [Diego Bodart](https://github.com/HermeticOrmus) | 7 found, 3 sealed | `grok plugin install multiplayer-networking@liquid-gold-grok` | `6959bed` |
| [rag-architecture](entries/rag-architecture.md) | gold | ML and LLM ops | [Diego Bodart](https://github.com/HermeticOrmus) | 6 found, 4 sealed | `grok plugin install rag-architecture@liquid-gold-grok` | `d129bee` |
| [chrome-devtools](entries/chrome-devtools.md) | assayed | Browser debugging | [Google Chrome](https://developer.chrome.com/) | 3 found, 0 sealed | `grok plugin install chrome-devtools@liquid-gold-grok` | `02c0112` |
| [domain-driven-design](entries/domain-driven-design.md) | assayed | Architecture | [Diego Bodart](https://github.com/HermeticOrmus) | 5 found, 2 sealed | `grok plugin install domain-driven-design@liquid-gold-grok` | `c493984` |
| [feature-dev](entries/feature-dev.md) | assayed | Engineering workflow | [Anthropic](https://github.com/anthropics) | 4 found, 0 sealed | `grok plugin install feature-dev@liquid-gold-grok` | `ab024cd` |
| [handoff](entries/handoff.md) | assayed | Session workflow | [Diego Bodart](https://github.com/HermeticOrmus) | 9 found, 6 sealed | `grok plugin install handoff@liquid-gold-grok` | `c5822d8` |
| [kubernetes-operations](entries/kubernetes-operations.md) | assayed | DevOps | [Diego Bodart](https://github.com/HermeticOrmus) | 9 found, 4 sealed | `grok plugin install kubernetes-operations@liquid-gold-grok` | `a810d2f` |
| [modern-web-guidance](entries/modern-web-guidance.md) | assayed | Web platform | [Google Chrome](https://github.com/GoogleChrome) | 3 found, 0 sealed | `grok plugin install modern-web-guidance@liquid-gold-grok` | `84ae725` |
| [pr-review-toolkit](entries/pr-review-toolkit.md) | assayed | Code review | [Anthropic](https://github.com/anthropics) | 5 found, 0 sealed | `grok plugin install pr-review-toolkit@liquid-gold-grok` | `ab024cd` |
| [pstack](entries/pstack.md) | assayed | Engineering workflow | [Lauren Tan | 4 found, 0 sealed | `grok plugin install pstack@liquid-gold-grok` | `2eb7ed4` |
| [superpowers](entries/superpowers.md) | assayed | Engineering workflow | [Jesse Vincent](https://github.com/obra) | 4 found, 1 sealed | `grok plugin install superpowers@liquid-gold-grok` | `8ca22db` |
| [axiorank](entries/axiorank.md) | watch | Agent safety | [AxioRank](https://github.com/AxioRank) | 7 found, 0 sealed | not in the marketplace | `08fe4b8` |
| [epic](entries/epic.md) | watch | Engineering workflow | [epicsagas](https://github.com/epicsagas) | 7 found, 0 sealed | not in the marketplace | `7abf3f1` |
| [figma](entries/figma.md) | watch | Design to code | [Figma](https://www.figma.com) | 2 found, 0 sealed | not in the marketplace | `2c8af03` |
| [hindsight-memory](entries/hindsight-memory.md) | watch | Memory | [Vectorize](https://github.com/vectorize-io) | 10 found, 1 sealed | not in the marketplace | `31a1260` |
| [libre-geo](entries/libre-geo.md) | watch | SEO and GEO | [Diego Bodart](https://github.com/HermeticOrmus), building on [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) by [Zubair Trabzada](https://github.com/zubair-trabzada) | 10 found, 4 sealed | not in the marketplace | `79e6aaa` |
| [libre-secops-hooks](entries/libre-secops-hooks.md) | watch | Security | [Diego Bodart](https://github.com/HermeticOrmus) | 12 found, 9 sealed | not in the marketplace | `a874d37` |
| [oh-my-grok](entries/oh-my-grok.md) | watch | Engineering workflow | [mihazs](https://github.com/mihazs); bundles [obra/superpowers](https://github.com/obra/superpowers) skills by Jesse Vincent | 8 found, 0 sealed | not in the marketplace | `49f1365` |
| [security-guidance](entries/security-guidance.md) | watch | Security | David Dworken, [Anthropic](https://github.com/anthropics) | 7 found, 0 sealed | not in the marketplace | `ab024cd` |
| [stripe](entries/stripe.md) | watch | Payments | [Stripe](https://stripe.com) | 2 found, 0 sealed | not in the marketplace | `9a36da0` |
