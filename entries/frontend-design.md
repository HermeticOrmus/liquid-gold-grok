# frontend-design

A single skill that pushes the agent toward distinctive visual design when it builds or reshapes a UI: a subject-grounded design plan first (palette, type, layout, principles), a review of that plan against the brief, then the build and a self-critique.

| | |
|---|---|
| Level | **gold** |
| Domain | Frontend design |
| Author | [Anthropic](https://github.com/anthropics) (README credits Prithvi Rajasekaran and Alexander Bricken) |
| License | [Apache-2.0](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/LICENSE) |
| Source | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design) |
| Pinned SHA | `ab024cdcfa7ca80be204acd4907656ba5a968589` (committed 2026-09-30) |
| Components at the pin | skills 1, agents 0, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone asking Grok for a landing page, dashboard or component who wants a considered point of view instead of the default gradient-and-card look.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install frontend-design@liquid-gold-grok
```

## Why it is gold

Every gate passed at the pin, and there is nothing to run: the plugin is one Markdown skill with no hooks, scripts, MCP servers or network calls. `grok inspect` in a clean Grok home lists the skill `frontend-design` from this plugin. The cracks left are hairline and all in metadata or copy: the manifest carries no version (upstream already holds that, [#4364](https://github.com/anthropics/claude-plugins-official/issues/4364)), no license field, and the README speaks only of Claude.

## What it can execute

- **Hooks:** none.
- **Scripts:** none.
- **MCP servers:** none.
- **Network:** none found. The skill suggests taking screenshots of your own work "if your environment supports it"; that uses whatever tools the session already has.
- **Disclosed in its README:** nothing to disclose.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `ab024cd`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `grok plugin validate`: `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/anthropics/claude-plugins-official.git@ab024cd...#plugins/frontend-design --trust`: `Installed 1 plugin(s) ... frontend-design` |
| Gate: details | pass | `frontend-design (subdir: plugins/frontend-design)` at commit `ab024cd`, no version shown (K-01); 1 skill in the installed folder; `grok inspect` lists skill `frontend-design` |
| Reading: promises against components | pass | the README promises one skill for frontend work; one skill loads ([SKILL.md](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/skills/frontend-design/SKILL.md)) |
| Reading: license | pass | Apache-2.0 [LICENSE](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/LICENSE) in the plugin folder, and the skill frontmatter points to `LICENSE.txt` next to it; the manifest has no license field (K-02) |
| Reading: what it can execute | pass | Markdown only |
| Reading: maintenance | last push 2026-09-30, 1,044 open issues, 37,242 stars (whole marketplace repository) | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The manifest has no `version`, so `grok plugin details` shows none and an update cannot be told apart from the pinned copy by version. | [.claude-plugin/plugin.json](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/.claude-plugin/plugin.json) | hairline | held by anthropics ([#4364](https://github.com/anthropics/claude-plugins-official/issues/4364), [#3762](https://github.com/anthropics/claude-plugins-official/issues/3762)) | add `"version"` to the manifest, small | open |
| K-02 | The manifest has no `license` field; the license is only in the files next to it. | [.claude-plugin/plugin.json](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/.claude-plugin/plugin.json) | hairline | new | add `"license": "Apache-2.0"`, small | open |
| K-03 | The README describes the plugin only in terms of Claude ("Claude automatically uses this skill"), though the skill itself is agent-neutral and loads in Grok. | [README.md:7](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/frontend-design/README.md#L7) | hairline | new | say "your coding agent", small | open |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
