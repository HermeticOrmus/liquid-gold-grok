# domain-driven-design

Strategic and tactical Domain-Driven Design: finding bounded contexts, choosing context-map relationships, sizing aggregates, naming domain events, and running event storming, with Java and TypeScript reference code.

| | |
|---|---|
| Level | **assayed** |
| Domain | Architecture |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/LICENSE) |
| Source | [HermeticOrmus/LibreArch-Claude-Code](https://github.com/HermeticOrmus/LibreArch-Claude-Code/tree/c4939847c5c341a4b92b82fce885dbf5af59ffe3/plugins/domain-driven-design) (`plugins/domain-driven-design`) |
| Pinned SHA | `c4939847c5c341a4b92b82fce885dbf5af59ffe3` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Teams designing a new system, drawing microservice boundaries, or breaking up a big ball of mud, who want the model to push back with Evans and Vernon instead of generating entities from a database schema.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install domain-driven-design@liquid-gold-grok
```

## Why it is assayed

The gates pass and the plugin executes nothing. Before v1.0.0 none of its components were reachable, and it carried an older agent, command and skill beside the newer ones; release [#2](https://github.com/HermeticOrmus/LibreArch-Claude-Code/pull/2) sealed both. One fracture keeps it from gold: the skill's `Money` value object, its worked example of a value object, rounds money through JavaScript floats, so `Money.of(1.005, 'USD')` comes out as 1 (K-03). The workaround is below and the upstream fix is drafted.

## What it can execute

- **Hooks:** none. (The pack's optional `libre-arch-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none. The Java and TypeScript in the files are reference code.
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** nothing to disclose.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `c493984`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreArch-Claude-Code.git@c493984...#plugins/domain-driven-design --trust`: `Installed 1 plugin(s) ... domain-driven-design` |
| Gate: details | pass | `domain-driven-design v1.0.0 (subdir: plugins/domain-driven-design)`, the install registry records commit `c493984`; the installed folder holds 1 skill, 1 agent, 1 command |
| Reading: promises against components | pass | the plugin README names the `ddd-strategist` agent, the `/ddd` command and the skill ([README.md:5](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/plugins/domain-driven-design/README.md#L5)); all load. The four `/ddd` modes the command lists have a process section each. The cross-referenced plugins (`microservices`, `event-driven`, `cqrs-event-sourcing`, `migration-strategies`) exist in the same marketplace. |
| Reading: the code, run | one fracture | the `Money` rounding, run with Node v26.8.1 (K-03) |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 0 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | None of the pack's agents, commands or skills were reachable: `setup.sh` copied folders into `~/.claude/plugins`, which the loader ignores, in a nested layout it does not read. | [CHANGELOG.md:5](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/CHANGELOG.md#L5), [:17](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/CHANGELOG.md#L17) | break | release PR #2 | a marketplace, a `plugin.json` per plugin, the flat layout, large | sealed #2 |
| K-02 | An older `ddd-architect` agent, nested `/ddd` command and `ddd-patterns` skill covered the same ground as the newer files. | [CHANGELOG.md:18](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/CHANGELOG.md#L18) | hairline | release PR #2 | unique material merged into the newer files, medium | sealed #2 |
| K-03 | The TypeScript `Money` value object stores amounts as `number` and rounds with `Math.round(amount * 100) / 100`: `Money.of(1.005, 'USD')` yields 1, not 1.01, and every currency gets two decimals (a JPY amount of 100.5 stays 100.5). | [skills/domain-driven-design/SKILL.md:217](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/plugins/domain-driven-design/skills/domain-driven-design/SKILL.md#L217); Node v26.8.1: `Math.round(1.005 * 100) / 100` prints `1` | fracture | new | `bigint` minor units with the ISO 4217 exponent, medium ([draft](../seals/domain-driven-design/K-03.md)) | drafted |
| K-04 | The `/ddd model` worked example enforces "Total must be >= $10.00 when items are added", so an order can never start with an item under $10; the minimum belongs at confirmation. | [commands/ddd.md:134](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/plugins/domain-driven-design/commands/ddd.md#L134) | hairline | new | move the invariant to confirm, small ([draft](../seals/domain-driven-design/K-03.md)) | drafted |
| K-05 | The repository README installs only through Claude Code; no Grok line. | [README.md:57](https://github.com/HermeticOrmus/LibreArch-Claude-Code/blob/c4939847c5c341a4b92b82fce885dbf5af59ffe3/README.md#L57) (the README never mentions Grok) | hairline | held by HermeticOrmus ([#5](https://github.com/HermeticOrmus/LibreArch-Claude-Code/issues/5)) | add the Grok install, small | open |

## Workarounds

K-03: when you take the `Money` pattern from this skill, ask for integer minor units instead of `number`, for example "use the skill's Money value object, but store `minor: bigint` and the ISO 4217 exponent, and parse amounts from decimal strings". Never pass a float literal such as `1.005` into money code. This workaround was not run in a Grok session; the rounding it avoids was run and is recorded in K-03.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
