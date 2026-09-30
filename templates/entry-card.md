# <plugin name>

<One or two plain sentences: what it does, in the reader's words.>

| | |
|---|---|
| Level | **gold** / **assayed** / **watch** |
| Domain | <domain> |
| Author | [<name>](<profile or site>) |
| License | [<SPDX id>](https://github.com/<owner>/<repo>/blob/<sha>/<license path>) |
| Source | [<owner>/<repo>](https://github.com/<owner>/<repo>/tree/<sha>/<path>) |
| Pinned SHA | `<40-character sha>` (committed <YYYY-MM-DD>) |
| Components at the pin | skills <n>, agents <n>, commands <n>, hook events <n>, MCP servers <n> (what `grok inspect` lists, not what the folder holds) |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

<One short paragraph.>

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install <plugin name>@liquid-gold-grok
```

<For a watch entry: "Not in the marketplace yet. The upstream install line is below, for reference only.">

## Why it is <level>

<The proof, not a claim: what was broken, and the seal. Or, for watch, what holds it back.>

## What it can execute

- **Hooks:** <events and scripts, or none>
- **Scripts:** <scripts it ships or tells the agent to run, or none>
- **MCP servers:** <name, how it starts, or none>
- **Network:** <every call it makes and where to, or none found>
- **Disclosed in its README:** <yes / partly / no, with a link>

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `<short sha>`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass / fail | `grok plugin validate`: <components line> |
| Gate: install at the pin | pass / fail | `grok plugin install <spec> --trust` |
| Gate: details | pass / fail | <what details listed> |
| Gate: inspect | pass / fail | `grok inspect --json`: <what Grok loaded for the plugin> |
| Reading: promises against components | <result> | <links> |
| Reading: license | <result> | <link> |
| Reading: what it can execute | <result> | <links> |
| Reading: maintenance | <last push, open issues, stars> | GitHub API, 2026-09-30 |
| Hands | not run | <why> |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 |  |  |  |  |  |  |

## Workarounds

<Only for open fractures: the exact steps a Grok user takes.>

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
