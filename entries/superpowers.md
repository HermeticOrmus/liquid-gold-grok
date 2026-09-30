# superpowers

A skills library for disciplined software work: brainstorming before code, written plans, test-driven development, systematic debugging, code review in both directions, git worktrees, and verification before calling anything done.

| | |
|---|---|
| Level | **assayed** |
| Domain | Engineering workflow |
| Author | [Jesse Vincent](https://github.com/obra) |
| License | [MIT](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/LICENSE) |
| Source | [obra/superpowers](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d) |
| Pinned SHA | `8ca22dba9a94f28898bbce59f2537ff4d87c747d` (committed 2026-09-25, release v6.4.2) |
| Components at the pin | skills 15, agents 0, commands 0, hook events 1, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone who wants Grok to slow down in the right places: ask before building, plan before coding, write the failing test first, and prove a fix before claiming it.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install superpowers@liquid-gold-grok
```

## Why it is assayed

Every gate passed at the pin, all 15 skills load, the one thing it runs on its own (a SessionStart hook) is local and documented, and its one network call is disclosed with an opt-out. The vessel already carries gold: the session-start hook once hung on bash 5.3 and later ([#571](https://github.com/obra/superpowers/issues/571), closed), and the pinned hook works around it with `printf` instead of a heredoc ([hooks/session-start:37](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/hooks/session-start#L37)).

One fracture keeps it from gold. The SessionStart hook works by printing the `using-superpowers` skill as session context, and Grok's own hooks guide says SessionStart output is ignored ([10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505)). In Grok the skills load and trigger on their descriptions, but the bootstrap that tells the agent to check for a skill before every task does not arrive. The workaround is one slash command or one line in `AGENTS.md` (below); it was not run in a Grok session, so the entry is assayed until it is.

## What it can execute

- **Hooks:** one `SessionStart` hook (matcher `startup|clear|compact`) runs [`hooks/run-hook.cmd session-start`](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/hooks/hooks.json), which reads `skills/using-superpowers/SKILL.md` and prints it as session context. No network, no writes.
- **Scripts:** the brainstorming skill can start a local visual companion server ([`skills/brainstorming/scripts/start-server.sh`](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/scripts/start-server.sh)), bound to `127.0.0.1` by default, only after the user agrees to it. `find-polluter.sh` in systematic-debugging runs your tests one at a time to find the one that leaves unwanted files behind.
- **MCP servers:** none.
- **Network:** the visual companion page loads a logo from `primeradiant.com` that carries the Superpowers version ([server.cjs:106](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/scripts/server.cjs#L106)). Set `SUPERPOWERS_DISABLE_TELEMETRY` to turn it off.
- **Disclosed in its README:** yes. The SessionStart bootstrap is described under Muse ([README.md:282](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/README.md#L282)) and the logo call under "Visual companion telemetry" ([README.md:397](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/README.md#L397)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `8ca22db`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/obra/superpowers.git@8ca22db... --trust`: `Installed 1 plugin(s) ... superpowers` |
| Gate: details | pass | `superpowers v6.4.2`, git commit `8ca22db`, 15 skills in the installed folder |
| Gate: inspect | pass | `grok inspect --json` from an empty folder lists the 15 skills and the hook file from `superpowers` |
| Reading: promises against components | pass | README lists 15 skills under What's Inside; all 15 load. The README has a Grok Build section ([README.md:187](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/README.md#L187)) |
| Reading: license | pass | MIT, `LICENSE` at the root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | one local SessionStart hook; one disclosed network call with an opt-out |
| Reading: maintenance | last push 2026-09-27, 279 open issues, 293,424 stars | GitHub API, 2026-09-30 |
| Grok's hooks guide | fracture | [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505): for `SessionStart`, stdout is ignored (vendor documentation, not an observed session) |
| Hook script, outside a session | pass | `run-hook.cmd session-start` with `CLAUDE_PLUGIN_ROOT` and `GROK_PLUGIN_ROOT` set exits 0 and prints valid JSON with `hookSpecificOutput.additionalContext` (3,617 bytes) |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The session-start hook hung on bash 5.3 and later. | [#571](https://github.com/obra/superpowers/issues/571); the fix is at [hooks/session-start:37](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/hooks/session-start#L37) | fracture | closed upstream #571 | `printf` instead of a heredoc, small | sealed |
| K-02 | In Grok the `using-superpowers` bootstrap never reaches the model: the SessionStart hook delivers it as stdout, and Grok ignores SessionStart stdout. The script itself works (it prints valid `hookSpecificOutput` JSON outside a session). | [hooks/hooks.json](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/hooks/hooks.json); Grok's hooks guide, [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505) (also written into `$GROK_HOME/docs/` by grok 1.0.44); no Grok session was run to observe it | fracture | new (no upstream issue mentions Grok hooks) | tell Grok users to load `using-superpowers` at session start (README Grok section), small | drafted ([seal](../seals/superpowers/K-02.md)) |
| K-03 | `using-superpowers` tells each agent to read its platform reference file and lists Claude Code, Codex, Pi, Antigravity, Hermes and Muse; there is no Grok entry. | [skills/using-superpowers/SKILL.md:52](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/using-superpowers/SKILL.md#L52) | hairline | new (no open issue mentions Grok tools) | add `references/grok-tools.md` and list it, small | drafted ([seal](../seals/superpowers/K-03.md)) |
| K-04 | The manifest calls it a "Core skills library for Claude Code", and Grok prints that line in `grok plugin details`. | [.claude-plugin/plugin.json:3](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/.claude-plugin/plugin.json#L3) | hairline | new | name the harnesses generically, small | open |

## Workarounds

- **K-02:** start each Grok session with `/using-superpowers`, or add this line to the project's `AGENTS.md` so Grok reads it every session: `Before any task, load the superpowers using-superpowers skill and follow it.` Not yet run in a Grok session.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
