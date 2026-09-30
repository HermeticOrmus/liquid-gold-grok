# pstack

Lauren Tan's engineering playbooks: `poteto-mode` picks one of twenty-three playbooks (bug fix, perf, refactoring, feature, review, shipping, orchestration and more) and pulls in the skills each step needs, alongside twenty-three principle skills such as prove-it-works, fix-root-causes and subtract-before-you-add.

| | |
|---|---|
| Level | **assayed** |
| Domain | Engineering workflow |
| Author | [Lauren Tan (poteto)](https://x.com/poteto), published in [cursor/plugins](https://github.com/cursor/plugins) |
| License | [MIT](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/LICENSE) |
| Source | [cursor/plugins, pstack](https://github.com/cursor/plugins/tree/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack) |
| Pinned SHA | `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e` (committed 2026-09-30, pstack 0.15.5) |
| Components at the pin | skills 47, agents 2, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Engineers who want the agent to go deep before it goes fast: reproduce first, name the data shape, verify with evidence, and write less code.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install pstack@liquid-gold-grok
```

## Why it is assayed

The gates pass and the principle skills are plain Markdown that any agent can follow, so most of the value arrives in Grok intact. Two fractures keep it from gold, both in the orchestration layer and both already raised upstream. First, pstack is written for Cursor: `/setup-pstack` writes `~/.cursor/rules/pstack-models.mdc`, asks through `AskQuestion`, and `poteto-mode` spawns `Task` subagents and runs watchers under `/loop`, while the README documents only the Cursor install (the open question [#446](https://github.com/cursor/plugins/issues/446) asks whether Grok Build is a supported target). Second, the subagent steps hard-code Cursor model slugs; an open issue reports that an earlier set of these defaults failed to resolve even in Cursor ([#335](https://github.com/cursor/plugins/issues/335)), and nothing at the pin maps them to Grok. Both have a workaround below; neither workaround was run in a Grok session.

## What it can execute

- **Hooks:** none.
- **Scripts:** `poteto-mode` ships TypeScript helpers run with Bun: `watch-pr` reads pull request state through the `gh` CLI, `orch` keeps orchestration state in local files, `check-plan.mjs` checks a pull request plan for its required blocks, and `worktree-audit.sh` is a read-only audit of git worktrees that never deletes anything. On first use, `bootstrap.ts` runs `bun install --frozen-lockfile` for one pinned dependency, `commander` 14.0.0 ([bootstrap.ts:35](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/scripts/bootstrap.ts#L35)). `show-me-your-work` ships `log.sh`, which appends a row to a decision log file.
- **MCP servers:** none.
- **Network:** the one-time `bun install` from npm; `gh` calls against your own GitHub repositories. No user data is sent anywhere else.
- **Disclosed in its README:** mostly. The playbooks, including shipping and babysitting pull requests to merge, are listed in the README; the first-run `bun install` is not (K-04).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `2eb7ed4`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `No plugin.json found. Grok discovers skills, agents, and hooks automatically from standard directories.` (exit 0); the only manifest is `.cursor-plugin/plugin.json` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/cursor/plugins.git@2eb7ed4...#pstack --trust`: `Installed 1 plugin(s) ... pstack` |
| Gate: details | pass | `pstack (subdir: pstack)`, no version shown; the installed folder holds 47 skills and 2 agents |
| Reading: promises against components | fracture | the README's skills and playbooks all load; the orchestration steps assume Cursor tools and model slugs (K-01, K-02) |
| Reading: license | pass | MIT, [`pstack/LICENSE`](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/LICENSE) (Copyright 2026 Lauren Tan), `"license": "MIT"` in `.cursor-plugin/plugin.json`. The `cursor/plugins` repository has no root license; each plugin carries its own |
| Reading: what it can execute | pass | local helper scripts and `gh`; one pinned dependency fetch not named in the README (K-04) |
| Reading: maintenance | last push 2026-09-30, 165 open issues, 9,160 stars (whole `cursor/plugins` repository) | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The orchestration skills rely on Cursor-only mechanics (`Task` subagents with Cursor model slugs, `AskQuestion`, a rule file at `~/.cursor/rules/pstack-models.mdc`, a same-run `/loop`), and the README documents only the Cursor install. | [setup-pstack/SKILL.md:8](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/setup-pstack/SKILL.md#L8), [line 22](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/setup-pstack/SKILL.md#L22), [poteto-mode/SKILL.md:93](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/SKILL.md#L93), [playbooks/babysit.md:12](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/playbooks/babysit.md#L12), [README.md:15](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/README.md#L15) | fracture | filed #446 (open question, no maintainer reply at assay) | a README note on Grok Build, and harness-neutral wording for the subagent steps, medium | drafted ([seal](../seals/pstack/K-01.md)) |
| K-02 | The default subagent model slugs (`grok-4.7-xhigh-fast`, `claude-opus-5-5-max`, `gpt-5.6-sol-max`) are hard-coded Cursor slugs with no Grok mapping, so a Grok subagent call with them is unlikely to resolve (*inferred*: no Grok session ran). An earlier set of the same defaults failed in Cursor itself. | [poteto-mode/SKILL.md:93](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/SKILL.md#L93), [setup-pstack/SKILL.md:39](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/setup-pstack/SKILL.md#L39) | fracture | filed #335 (open, about the earlier slugs) | default every role to `inherit-parent`, small | drafted ([seal](../seals/pstack/K-02.md)) |
| K-03 | No manifest Grok reads: Grok names the plugin after its folder and `grok plugin details` shows no version. | `grok plugin validate` and `details` output above; [.cursor-plugin/plugin.json](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/.cursor-plugin/plugin.json) | hairline | new | add `.claude-plugin/plugin.json` or `.grok-plugin/plugin.json` with the same fields, small | drafted ([seal](../seals/pstack/K-01.md)) |
| K-04 | On first use the poteto-mode helpers run `bun install` from npm; the README does not mention it. The dependency is pinned by lockfile and no user data is sent. | [bootstrap.ts:35](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/scripts/bootstrap.ts#L35), [scripts/package.json](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/scripts/package.json) | hairline | new | one README line, small | open |

## Workarounds

K-01: use `poteto-mode` and the principle skills as written, and answer `AskQuestion` prompts in plain chat. Skip `/setup-pstack`: its rule file is written for Cursor. Where a playbook says to run a watcher under `/loop`, run the watcher command directly and re-run it when you want a fresh verdict.

K-02: start the task with an instruction such as "run every pstack role on the parent model (`inherit-parent`)". `poteto-mode` defines `inherit-parent` as always valid and treats it as "omit the Task model" ([poteto-mode/SKILL.md:93](https://github.com/cursor/plugins/blob/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack/skills/poteto-mode/SKILL.md#L93)).

Neither workaround was run in a Grok session for this assay.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
