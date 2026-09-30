# modern-web-guidance

Two skills that steer the agent toward current web platform features instead of legacy patterns and heavy libraries. `modern-web-guidance` searches and retrieves one of the 162 guide files it bundles (dialogs, popovers, anchor positioning, view transitions, container queries, INP, forms and autofill) through a small CLI; `chrome-extensions` covers Manifest V3 extensions and Chrome Web Store publishing.

| | |
|---|---|
| Level | **assayed** |
| Domain | Web platform |
| Author | [Google Chrome](https://github.com/GoogleChrome) |
| License | [Apache-2.0](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/LICENSE) |
| Source | [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance/tree/84ae7251ee919239d5ea85aef25897983f26601e) |
| Pinned SHA | `84ae7251ee919239d5ea85aef25897983f26601e` (committed 2026-09-28, release v0.0.191) |
| Components at the pin | skills 2, agents 0, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone building web UI with Grok who wants native HTML, CSS and browser APIs used where they now exist, with the fallbacks spelled out.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install modern-web-guidance@liquid-gold-grok
```

## Why it is assayed

It installs clean at the pin, both skills load (`grok inspect` lists `modern-web-guidance` and `chrome-extensions`), and its telemetry is disclosed with an opt-out. Two fractures are open. The README promises search that is "completely private and local" while the CLI's telemetry, on by default and disclosed further down the same README, sends search queries to Google (K-02; the opt-out is the workaround). And the skill tells the agent to run `npx -y modern-web-guidance@latest`, so the code that runs is whatever npm serves when the agent calls it, not the commit this library pinned. On the assay date `latest` is 0.0.191, the same version as the pin; the K-01 workaround below keeps it that way. A seal is drafted for upstream.

## What it can execute

- **Hooks:** none.
- **Scripts:** the skill runs the `modern-web-guidance` CLI through `npx -y ...@latest` for `search`, `list` and `retrieve` ([skills/modern-web-guidance/SKILL.md:38](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L38)). `-y` installs the package without asking. The npm package (0.0.191, read, not run) has no dependencies and ships the guides, a local TensorFlow.js search model and a telemetry watchdog.
- **MCP servers:** none.
- **Network:** npm, to fetch the package. The CLI's watchdog posts search queries, guide IDs, OS, version and bucketed latency to `play.googleapis.com/log` unless `DISABLE_TELEMETRY=1` is set (`skills/modern-web-guidance/watchdog/main.js` in the npm package).
- **Disclosed in its README:** yes for telemetry, with the opt-out ([README.md:504](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L504)), and for the network access `npx` needs ([SKILL.md:96](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L96)). Two earlier README lines contradict the telemetry section (K-02).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `84ae725`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `grok plugin validate`: `version: 0.0.191`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/GoogleChrome/modern-web-guidance.git@84ae725... --trust`: `Installed 1 plugin(s) ... modern-web-guidance` |
| Gate: details | pass | `modern-web-guidance v0.0.191`, `components: 1 skill dir(s)`; 2 skills in the installed folder; `grok inspect` lists both |
| Reading: promises against components | pass | the README names two skills ([README.md:501](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L501)); both load. Its Grok section uses a direct install, which works ([README.md:425](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L425)) |
| Reading: license | pass | Apache-2.0 [LICENSE](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/LICENSE) at the root; the npm package `license` is Apache-2.0 too |
| Reading: what it can execute | pass, with K-01 | an unpinned `npx` package; disclosed telemetry |
| Reading: maintenance | last push 2026-09-28, 2,361 stars; issues are off in this repository and live in [modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src), 389 open | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; the CLI was read from the npm tarball, not run |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The skill runs `npx -y modern-web-guidance@latest`, so the pinned commit does not pin the code that executes: a later npm release runs under this pin without review. | [SKILL.md:38](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L38), [:65](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L65), [:75](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L75), [:94](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/skills/modern-web-guidance/SKILL.md#L94); `npm view modern-web-guidance dist-tags` shows `latest: 0.0.191` | fracture | new (no issue in modern-web-guidance-src mentions pinning the `npx` version) | write the release version into SKILL.md at release time, small | drafted ([seal](../seals/modern-web-guidance/K-01.md)) |
| K-02 | The README says the search makes "no network calls" and the CLI is "completely private and local", while its own Telemetry section, and the CLI, send search queries and guide IDs to Google unless `DISABLE_TELEMETRY=1` is set. | [README.md:368](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L368), [README.md:372](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L372), [README.md:506](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/README.md#L506) | fracture | new | say "search runs locally; usage telemetry is on by default, see Telemetry", small | drafted ([seal](../seals/modern-web-guidance/K-02.md)) |
| K-03 | The repository ships `.grok-plugin/marketplace.json` listing its own root (`"source": "./"`), which Grok cannot install: adding it as a marketplace and installing gives `No marketplace plugin named "modern-web-guidance"`. | [.grok-plugin/marketplace.json](https://github.com/GoogleChrome/modern-web-guidance/blob/84ae7251ee919239d5ea85aef25897983f26601e/.grok-plugin/marketplace.json); `grok plugin marketplace add` on the pinned tree, then `grok plugin install` | hairline | added in modern-web-guidance-src [#1272](https://github.com/GoogleChrome/modern-web-guidance-src/issues/1272) (closed) | drop the file; the direct install in the README is the Grok path, small | drafted ([seal](../seals/modern-web-guidance/K-02.md), same draft) |

## Workarounds

- **K-02:** `export DISABLE_TELEMETRY=1` in the shell that starts Grok, so the CLI keeps search queries on your machine as the README's opening sections promise.
- **K-01:** keep the CLI at the pinned version. Tell Grok once per project, or put it in `AGENTS.md`: "When the modern-web-guidance skill says `npx -y modern-web-guidance@latest`, run `npx -y modern-web-guidance@0.0.191` instead."

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
