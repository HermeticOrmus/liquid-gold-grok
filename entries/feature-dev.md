# feature-dev

A `/feature-dev` workflow in seven phases (discovery, codebase exploration, clarifying questions, architecture, implementation, quality review, summary) with three helper agents: `code-explorer`, `code-architect` and `code-reviewer`. It stops for your answers before designing and for your approval before writing code.

| | |
|---|---|
| Level | **assayed** |
| Domain | Engineering workflow |
| Author | [Anthropic](https://github.com/anthropics) (README credits Sid Bidasaria) |
| License | [Apache-2.0](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/LICENSE) |
| Source | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev) |
| Pinned SHA | `ab024cdcfa7ca80be204acd4907656ba5a968589` (committed 2026-09-30) |
| Components at the pin | skills 0, agents 3, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone adding a feature that touches several files in an existing codebase, who wants the agent to read the code and ask questions before it builds.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install feature-dev@liquid-gold-grok
```

## Why it is assayed

It installs clean and everything it ships loads in Grok: `grok inspect` in a clean Grok home lists the `/feature-dev` command (as skill `feature-dev`) and all three agents (`feature-dev:code-explorer`, `feature-dev:code-architect`, `feature-dev:code-reviewer`). It runs nothing on its own. One fracture stays open, and upstream already holds it: the three agents declare a tool list without `Bash`, yet `code-reviewer` is told to review `git diff` ([#4235](https://github.com/anthropics/claude-plugins-official/issues/4235)). Whether Grok enforces that list is unverified, so the crack is *inferred* for Grok; the workaround below avoids it either way.

## What it can execute

- **Hooks:** none.
- **Scripts:** none.
- **MCP servers:** none.
- **Network:** none of its own. The agents list `WebFetch` and `WebSearch` among their tools.
- **Disclosed in its README:** nothing to disclose.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `ab024cd`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `grok plugin validate`: `components: 0 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/anthropics/claude-plugins-official.git@ab024cd...#plugins/feature-dev --trust`: `Installed 1 plugin(s) ... feature-dev` |
| Gate: details | pass | `feature-dev (subdir: plugins/feature-dev)` at commit `ab024cd`; 3 agents and 1 command in the installed folder; `grok inspect` lists all of them |
| Reading: promises against components | pass | the README names one command and three agents ([README.md:19](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/README.md#L19)); all four load |
| Reading: license | pass | Apache-2.0 [LICENSE](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/LICENSE) in the plugin folder |
| Reading: what it can execute | pass | Markdown only |
| Reading: maintenance | last push 2026-09-30, 1,044 open issues, 37,242 stars (whole marketplace repository) | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | All three agents declare a `tools:` list without `Bash`, while `code-reviewer` is told to review unstaged changes from `git diff`; where the list is enforced, the reviewer cannot run it. *Inferred* for Grok: enforcement of this list in a Grok session is unverified. | [agents/code-reviewer.md:4](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/agents/code-reviewer.md#L4), [:13](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/agents/code-reviewer.md#L13) | fracture | held by anthropics ([#4235](https://github.com/anthropics/claude-plugins-official/issues/4235)) | add `Bash` to the three tool lists, small | open |
| K-02 | The agents and command use Claude Code names: `model: sonnet` on every agent, tool names such as `LS`, `NotebookRead`, `KillShell`, `BashOutput` and `TodoWrite`. How Grok maps them is unverified. | [agents/code-explorer.md:4](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/agents/code-explorer.md#L4), [commands/feature-dev.md:16](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/commands/feature-dev.md#L16) | hairline (*inferred*) | related: [#163](https://github.com/anthropics/claude-plugins-official/issues/163) asks the agents to inherit the session model | `model: inherit`, small | open |
| K-03 | `code-reviewer` and `code-architect` look for project rules in `CLAUDE.md`; a Grok project usually keeps them in `AGENTS.md`. The reviewer text says "CLAUDE.md or equivalent", so this is copy, not a hard failure. | [agents/code-reviewer.md:9](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/agents/code-reviewer.md#L9), [agents/code-architect.md:14](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/agents/code-architect.md#L14) | hairline | held by anthropics ([#6307](https://github.com/anthropics/claude-plugins-official/issues/6307)) | name `AGENTS.md` next to `CLAUDE.md`, small | open |
| K-04 | The README lists "Claude Code installed" as a requirement and gives version 1.0.0, while the manifest has no `version`. | [README.md:365](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/README.md#L365), [README.md:412](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/README.md#L412), [.claude-plugin/plugin.json](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/feature-dev/.claude-plugin/plugin.json) | hairline | the missing version is held by anthropics ([#1758](https://github.com/anthropics/claude-plugins-official/issues/1758)) | add `"version": "1.0.0"`, name the agents it runs in, small | open |

## Workarounds

- **K-01:** before Phase 6, run `git diff` yourself in the main session (or ask Grok to) and paste the diff into the review request, for example: "Launch code-reviewer on this diff: ...". The reviewer then has the changes without needing a shell.
- **K-03:** if your project keeps its rules in `AGENTS.md`, say so when you start: `/feature-dev <feature>. Project rules are in AGENTS.md.`

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
