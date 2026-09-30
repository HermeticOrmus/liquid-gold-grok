# api-documentation

API documentation from the docs-set level down to one operation: Diátaxis information architecture, OpenAPI 3.1 reference generated from routes and types, spec linting and breaking-change diffs, error catalogs, getting-started pages, changelogs, and SDK guides with idiomatic examples per language.

| | |
|---|---|
| Level | **gold** |
| Domain | Technical writing |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/LICENSE) |
| Source | [HermeticOrmus/LibreCopy-Claude-Code](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/tree/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation) (`plugins/api-documentation`) |
| Pinned SHA | `8ec68f353913bfd5cb087c621247a71f6448efe7` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 3, agents 2, commands 2, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Teams shipping a public or cross-team API who want the reference, the guides and the error catalog to agree with the code, and SDK maintainers who need per-language client docs.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install api-documentation@liquid-gold-grok
```

## Why it is gold

Every gate passed at the pin, and the plugin executes nothing on its own. The gold in the vessel came from release [#2](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/pull/2): before it the plugin never loaded, carried a second copy of its agent and command in an old nested layout, and pinned a model by name. Two commands with near-identical names, `/api-docs` and `/api-doc`, now say in their descriptions which one to use for what. What is left open is hairline: the README promises AsyncAPI 3.0 patterns the skills do not carry, and one fenced block is labelled YAML but is not YAML.

## What it can execute

- **Hooks:** none. (The pack's optional `libre-copy-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none. `/api-doc validate` has the agent lint a spec against a Spectral ruleset when you ask for it; the plugin ships no script of its own.
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** nothing the plugin runs needs disclosing.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `8ec68f3`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreCopy-Claude-Code.git@8ec68f3...#plugins/api-documentation --trust`: `Installed 1 plugin(s) ... api-documentation` |
| Gate: details | pass | `api-documentation v1.0.0 (subdir: plugins/api-documentation)`, install registry commit `8ec68f3` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 3, agents 2, commands 2 loaded, the same as the files on disk |
| Reading: promises against components | pass, one hairline | the two agents, two commands and three skills the README lists all load ([README.md:6](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/README.md#L6) to :12); AsyncAPI coverage is thinner than promised (K-05) |
| Reading: code blocks, parsed | one hairline | every YAML, JSON and Python block in the plugin was parsed; one block labelled `yaml` fails (K-06) |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 0 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | None of the pack's plugins loaded: the old `setup.sh` copied folders into `~/.claude/plugins`, where plugins are not loaded from. | [CHANGELOG.md:5](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L5) | break | release PR #2 | a marketplace and a `plugin.json` per plugin, large | sealed #2 |
| K-02 | The plugin carried a second copy of its agent and command in the old nested layout: `api-doc-specialist` next to `api-doc-writer`, and `/doc-api` next to `/api-doc`. | [CHANGELOG.md:17](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L17) to [:19](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L19) | hairline | release PR #2 | one file each, every unique section merged, medium | sealed #2 |
| K-03 | `/api-docs` and `/api-doc` differ by one letter and do different jobs; before 1.0.0 no command carried a routing description, so nothing told the agent which one to pick. | [CHANGELOG.md:9](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L9), [:21](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L21); the descriptions now point at each other ([commands/api-docs.md:2](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/commands/api-docs.md#L2), [commands/api-doc.md:2](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/commands/api-doc.md#L2)) | hairline | release PR #2 | routing descriptions that name the sibling, small | sealed #2 |
| K-04 | `api-doc-writer` was pinned to Sonnet instead of the session's model, a name that means nothing to Grok. | [CHANGELOG.md:22](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/CHANGELOG.md#L22); now `model: "inherit"` ([agents/api-doc-writer.md:4](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/agents/api-doc-writer.md#L4)) | hairline | release PR #2 | `model: inherit`, small | sealed #2 |
| K-05 | The README promises AsyncAPI 3.0 documentation for Kafka, Pub/Sub and WebSocket, and names AsyncAPI in the `api-documentation` skill's pattern library; none of the three skills mentions AsyncAPI. It appears only as one line in the agent and one heading in `/api-docs`. | [README.md:10](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/README.md#L10), [:18](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/README.md#L18); `grep -c -i asyncapi` on each `SKILL.md`: 0, 0, 0; [agents/api-doc-writer.md:254](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/agents/api-doc-writer.md#L254), [commands/api-docs.md:64](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/commands/api-docs.md#L64) | hairline | new | add an AsyncAPI 3.0 section to the `api-documentation` skill, or trim the README, small ([draft](../seals/api-documentation/K-05.md)) | drafted |
| K-06 | A list of URL paths is fenced as `yaml` but is not YAML, so it highlights and parses wrong. | [skills/openapi-patterns/SKILL.md:27](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/plugins/api-documentation/skills/openapi-patterns/SKILL.md#L27); `yaml.safe_load_all` on it: `expected '<document start>', but found '<scalar>'` | hairline | new | fence it as `text`, small ([draft](../seals/api-documentation/K-05.md)) | drafted |
| K-07 | The repository README installs only through Claude Code; no Grok line. | [README.md:59](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/blob/8ec68f353913bfd5cb087c621247a71f6448efe7/README.md#L59) (`/plugin marketplace add`; the README never mentions Grok) | hairline | held by HermeticOrmus ([#5](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/issues/5), PR [#6](https://github.com/HermeticOrmus/LibreCopy-Claude-Code/pull/6)) | add the Grok install, small | open |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
