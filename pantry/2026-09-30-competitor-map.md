# Competitor map: Liquid Gold for Grok Build

Other catalogs, marketplaces and awesome lists that point people at Grok Build or Claude Code plugins, and what each one checks before an entry reaches a user. Every claim cites the file it came from, read on 2026-09-30 at the commit named in the row.

## Product

- Name: Liquid Gold for Grok Build (`HermeticOrmus/liquid-gold-grok`)
- Flagship: the kintsugi assay. Each entry is pinned to one commit, installed into a clean Grok home, read for what it can execute, and published with its ledger of cracks and seals.
- Our surfaces: `.grok-plugin/marketplace.json` (gold and assayed entries only), `entries/<name>.md` cards with ledgers, `seals/` drafts for upstream fixes, `RUBRIC.md`, `scripts/verify.sh` in CI, `scripts/repin.sh`.

## Map

| Competitor | What it is | Overlap with us | Watch / differentiator | Source URL |
|------------|------------|-----------------|------------------------|------------|
| xai-org/plugin-marketplace | The official Grok Build marketplace (`xai-official`), 29 entries, 272 stars | The same install path and the same pinned remote source format; several of our entries are also listed there | Code-owner static review for supply-chain and execution risk, SHA pins required, automated SHA-bump PRs. Its README says xAI does not verify third-party plugins, and it publishes no per-entry findings | https://github.com/xai-org/plugin-marketplace/blob/a67139612115886e94ec393a1f151bb47c04554a/CONTRIBUTING.md |
| anthropics/claude-plugins-official | Anthropic's directory for Claude Code, 315 entries, 37,244 stars | Grok reads Claude plugins as they are, so many of its entries install in Grok; four of our entries come from it | A Claude policy scan per plugin and SHA, license and frontmatter checks, MCP URL probes. Nothing is tested under Grok, and scan verdicts are CI artifacts, not published per entry | https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/.github/workflows |
| DominikTobureto/awesome-grok-build | An awesome list and starter kit for Grok Build, 64 stars | The closest Grok-specific list of community resources | Checks its own Markdown links and its own skills' frontmatter; listed third-party resources are not installed or read | https://github.com/DominikTobureto/awesome-grok-build/tree/9125e026dddc2c3e5884f2db5cc56436c7e71665/.github/workflows |
| hesreallyhim/awesome-claude-code | The largest hand-picked Claude Code resource list, 54,850 stars | Discovery of Claude plugins, many of which run in Grok | Eligibility rules (age, activity, or 100 stars) and a bot that reports the license; no install, no execution review, no Grok | https://github.com/hesreallyhim/awesome-claude-code/blob/6e3dec26184a083ec8c98ffa9d40df8e825ddfc7/CONTRIBUTING.md |
| composio-community/awesome-claude-plugins | A curated list and a marketplace file of Claude Code plugins, 1,985 stars | Plugin discovery with a marketplace file | No CI workflows in the repository at the read commit | https://github.com/composio-community/awesome-claude-plugins/tree/e521f7ada8d89abea888e67b93b4dcfbb977041f |
| davepoon/buildwithclaude | A hub for Claude skills, agents, commands, hooks and plugins, 3,572 stars | Discovery across component types | Schema validation of submitted plugins and subagents; no Grok, no pins to upstream commits | https://github.com/davepoon/buildwithclaude/tree/b90e2de83662891c78c95b051fa109ab37b5b636/.github/workflows |
| wshobson/agents | A multi-harness plugin marketplace, 40,114 stars | The upstream of plugins some of our own packs derive from | JSON, hooks and entry-resolution checks plus a static eval sweep of its own content; it authors what it lists, so there is no third-party assay | https://github.com/wshobson/agents/tree/156b7a5e7a8b93642628a339ee4039c925b34c7f/.github/workflows |
| jeremylongshore/tons-of-skills-marketplace | A model-agnostic skills platform, 2,798 stars | A large catalog with a stated verification ambition | Many CI gates (skill conformance, e2e, secret scan). Its README names Claude Code as the only verified harness and says its certification program has not certified anything yet | https://github.com/jeremylongshore/tons-of-skills-marketplace/blob/0e2cabe39aca29588e86ab755ca9e2b73ac1d48d/README.md |

## Capabilities matrix

Mark Y / N / P (partial) / ?. Rows are what a person choosing a Grok Build plugin needs checked. "Us" is this repository as of the first-stock pull request.

| Capability | Us | xAI catalog | Anthropic directory | awesome-grok-build | awesome-claude-code | buildwithclaude | Source notes |
|------------|----|-------------|---------------------|--------------------|---------------------|-----------------|--------------|
| Pins every entry to a full commit SHA | Y | Y | Y | N | N | N | Us: `scripts/check_catalog.py`. xAI: CONTRIBUTING.md line 45 and README.md line 96. Anthropic: all 262 external entries in `.claude-plugin/marketplace.json` carry a `sha`; the other 53 are vendored in the repository. The lists link repositories, not commits |
| Installs every entry into a clean home in CI | Y | P | ? | N | N | N | Us: `scripts/verify.sh` in `.github/workflows/verify.yml`. xAI fetches each pinned source to build its index (README.md line 112), which is not a Grok install. Anthropic's `validate-plugins.yml` was not read in full |
| Tested under Grok Build | Y | P | N | N | N | N | Us: grok 1.0.44 in every assay. xAI's catalog is for Grok but its CI runs Python validators (`validate-catalog.yml`). No Grok mention in the Anthropic directory's Markdown |
| Reads what a plugin executes (hooks, scripts, MCP, network) | Y | Y | Y | N | N | N | xAI: code-owner static review (CONTRIBUTING.md lines 72 to 96). Anthropic: Claude policy scan per plugin and SHA (`scan-plugins.yml`) |
| Publishes per-entry findings with evidence | Y | N | N | N | N | N | Us: a ledger in every card. xAI review happens in PR threads. Anthropic verdicts are uploaded as CI artifacts (`scan-plugins.yml`) |
| Drafts fixes back to the upstream author | Y | N | N | N | N | N | Us: `seals/<entry>/K-NN.md` |
| Checks the license | Y | P | P | ? | P | ? | xAI: a checklist item (CONTRIBUTING.md line 49). Anthropic: Apache 2.0 file check for plugins it vendors (`validate-licenses.yml` line 21). awesome-claude-code: a bot reports the license (CONTRIBUTING.md line 55) |
| Shows upstream changes before a pin moves | Y | P | P | N | N | N | Us: `scripts/repin.sh`. xAI and Anthropic open SHA-bump pull requests (`bump-plugin-shas.yml`) |
| Keeps entries that did not pass, with the reason | Y | N | N | N | N | N | Us: watch entries have cards and CATALOG rows, and stay out of the marketplace file |
| Nomination and crack-report forms | Y | P | P | P | Y | P | Us: `.github/ISSUE_TEMPLATE/nominate.yml`, `crack.yml`. xAI and Anthropic take pull requests or an external form; awesome-claude-code has an issue form with a bot |

Rows for composio-community/awesome-claude-plugins, wshobson/agents and tons-of-skills-marketplace are in the map above; they check less than or differently from the columns shown, and none of them tests under Grok.
