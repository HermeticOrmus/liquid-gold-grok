# design-mastery

Design principles, the work of named designers, and the history of design movements, turned into agents and commands for UI work: design audits, brand identity builds, style guides, and premium landing pages.

| | |
|---|---|
| Level | **gold** |
| Domain | Design |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/LICENSE) |
| Source | [HermeticOrmus/design-mastery-claude-code](https://github.com/HermeticOrmus/design-mastery-claude-code/tree/e07686b7fced53664249503ed98c38640ae422b5) |
| Pinned SHA | `e07686b7fced53664249503ed98c38640ae422b5` (committed 2026-09-30, release v1.1.0) |
| Components at the pin | skills 5, agents 3, commands 4, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Developers who build interfaces and want design decisions with a reason behind them: a hierarchy fix that cites Gestalt, a palette that passes contrast, a brand that starts from positioning instead of a logo.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install design-mastery@liquid-gold-grok
```

## Why it is gold

Every gate passed at the pin, and the plugin runs nothing on its own: no hooks, no MCP servers, no scripts it asks the agent to execute. The gold is already in the vessel. Before v1.1.0 the documented install did not install anything, the skills promised reference files that did not exist, and the knowledge base carried wrong facts about Vignelli, Scher, Rand and Bass, wrong WCAG thresholds, and wrong Tailwind sizes. Release [#2](https://github.com/HermeticOrmus/design-mastery-claude-code/pull/2) sealed each one, and the corrected lines are visible at the pin (for example the WCAG large text rule at [skills/design-principles/SKILL.md:220](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/skills/design-principles/SKILL.md#L220)). What stays open is hairline, and both are already held in the tracker: a README that shows only the Claude Code install, and an eval suite with no recorded run.

## What it can execute

- **Hooks:** none.
- **Scripts:** `setup.sh` at the repository root installs the plugin through the Claude Code CLI. Grok never runs it; it runs only if you run it yourself.
- **MCP servers:** none.
- **Network:** none from the plugin. `setup.sh` prints two links and fetches nothing.
- **Disclosed in its README:** yes. There is nothing to disclose beyond `setup.sh`, which the README describes ([README.md:47](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/README.md#L47)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `e07686b`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/design-mastery-claude-code.git@e07686b... --trust`: `Installed 1 plugin(s) ... design-mastery` |
| Gate: details | pass | `design-mastery v1.1.0`, the install registry records commit `e07686b`; the installed folder holds 5 skills, 3 agents, 4 commands |
| Reading: promises against components | pass | the README tables name 3 agents, 4 commands and 5 skills ([README.md:58](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/README.md#L58)); all load. Every `references/` and `assets/` path named in a `SKILL.md` exists at the pin (27 reference files). `/design-audit` scores the eight dimensions the README names ([commands/design-audit.md:11](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/commands/design-audit.md#L11)) |
| Reading: license | pass | MIT, `LICENSE` at the root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only; no hooks, MCP servers or agent-run scripts |
| Reading: maintenance | last push 2026-09-30, 4 open issues and pull requests, 17 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The documented install did not install: `claude plugin add design-mastery` is not a command, and a clone in `~/.claude/plugins/` is never registered as a plugin. | [CHANGELOG.md:35](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L35) | break | release PR #2 | a root `plugin.json` and a marketplace install, medium | sealed #2 |
| K-02 | The skills' Resources sections promised reference files that were not shipped (3 existed). | [CHANGELOG.md:14](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L14), [:19](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L19); at the pin no `SKILL.md` names a missing file | fracture | release PR #2 | 24 reference files added, large | sealed #2 |
| K-03 | Facts about the masters were wrong: the Vignelli Canon principles, his four typefaces, Scher and the Windows 8 logo, Rand's logo criteria, and Bass's Shining poster and client dates. | [CHANGELOG.md:36](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L36) to :40; the seal shows at [massimo-vignelli.md:50](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/skills/design-masters/references/massimo-vignelli.md#L50) and [paula-scher.md:22](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/skills/design-masters/references/paula-scher.md#L22) | fracture | release PR #2 | corrected; Rand's criteria now follow his essay "Logos, Flags, and Escutcheons", medium | sealed #2 |
| K-04 | Numbers a UI ships with were wrong: WCAG large text (said 18px), touch targets, Tailwind `text-4xl` (said 40px), and two contrast figures. | [CHANGELOG.md:41](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L41) to :43; the seal shows at [design-principles/SKILL.md:220](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/skills/design-principles/SKILL.md#L220) and [commands/design-audit.md:89](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/commands/design-audit.md#L89) | fracture | release PR #2 | WCAG 2.2 figures and the real Tailwind scale, small | sealed #2 |
| K-05 | Movement history was wrong: grunge origins, the year Memphis was founded, a Bowie cover credited to Memphis, Bauhaus legacy claims, and a revival cycle stated as fact. | [CHANGELOG.md:44](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L44) | fracture | release PR #2 | corrected, and the cycle labelled as speculation, small | sealed #2 |
| K-06 | A pronoun slip in the design-master agent, an overstated "father of Swiss style" claim, and a misdescribed Stanford credibility statistic. | [CHANGELOG.md:45](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L45), [:46](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/CHANGELOG.md#L46) | hairline | release PR #2 | copy fixes, small | sealed #2 |
| K-07 | The README installs only through Claude Code (`/plugin`, `claude plugin`, or a copy into `.claude/`); a Grok user finds no Grok line. | [README.md:31](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/README.md#L31) to :56 | hairline | held by HermeticOrmus ([#6](https://github.com/HermeticOrmus/design-mastery-claude-code/issues/6)) | add `grok plugin install HermeticOrmus/design-mastery-claude-code`, small | open |
| K-08 | The eval suite has no recorded run, so nothing shows what the plugin adds over a no-plugin baseline; the suite runs only under `claude plugin eval`. | [README.md:182](https://github.com/HermeticOrmus/design-mastery-claude-code/blob/e07686b7fced53664249503ed98c38640ae422b5/README.md#L182) to :190 | hairline | held by HermeticOrmus ([#4](https://github.com/HermeticOrmus/design-mastery-claude-code/issues/4)) | `evals/BASELINE.md` with one recorded run, medium | open |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
