# vercel

Vercel's plugin for coding agents: 34 skills across the Vercel platform (AI SDK, AI Gateway, Functions, Queues, Workflow, Sandbox, storage, caching, firewall, flags, the CLI, deploys and env vars), three specialist agents, four commands, session hooks, and Vercel's hosted MCP server.

| | |
|---|---|
| Level | **watch** |
| Domain | Cloud platform |
| Author | [Vercel](https://github.com/vercel) |
| License | [Apache-2.0](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/LICENSE) |
| Source | [vercel/vercel-plugin](https://github.com/vercel/vercel-plugin/tree/2b7e8732ac22aafa8319459a881631dd5cff3878) |
| Pinned SHA | `2b7e8732ac22aafa8319459a881631dd5cff3878` (committed 2026-10-01, version 0.52.0) |
| Components at the pin | skills 35, agents 0, commands 0, hook events 3, MCP servers 1 (the folder holds 34 skills, 3 agents and 4 commands; see K-03 and K-07) |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers building on Vercel from Grok: Next.js apps on Functions, AI features on the AI SDK and AI Gateway, durable jobs on Queues and Workflow, untrusted code in Sandbox, and the CLI work around deploys, domains and environment variables.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/vercel/vercel-plugin.git@2b7e8732ac22aafa8319459a881631dd5cff3878 --trust
```

xAI's catalog lists it as `vercel` (`grok plugin install vercel@xai-official --trust`) at an older pin, `c632a50` (0.51.0), with the same hooks, manifest and session-start profiler.

## Why it is watch

One break holds it back. At session start in a Vercel, Next.js or eve project, or in an empty folder, with the Vercel CLI on `PATH`, the profiler hook runs `vercel --version` and then `npm view vercel version`, a query to the npm registry, so it can tell the agent the CLI is outdated ([session-start-profiler.mjs:653](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/session-start-profiler.mjs#L653)). The README's hook list says the profiler "Scans config files and dependencies to set likely-skill hints" ([README.md:112](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L112)) and never mentions the query; `VERCEL_PLUGIN_TELEMETRY=off` does not stop it; and Grok, which ignores `SessionStart` output, throws the resulting advice away. The query carries no project data, but under this library's rubric an undisclosed network call is a break (K-02).

Two fractures follow, each with a workaround in this card. The three agents and four commands the README lists do not load in Grok, because the manifest names them as files and Grok reads each entry as a folder (K-03). The session context the plugin injects at start, including the `knowledge-update` guidance that corrects outdated model knowledge, never reaches Grok's model (K-04).

The vessel already carries gold, and it matters. The plugin once sent every bash command to Vercel as telemetry ([#41](https://github.com/vercel/vercel-plugin/issues/41)) and asked for telemetry consent through text injected into the model's context ([#34](https://github.com/vercel/vercel-plugin/issues/34)); [#42](https://github.com/vercel/vercel-plugin/pull/42) and [#47](https://github.com/vercel/vercel-plugin/pull/47) removed both. At the pin the telemetry sends what the README lists and nothing more, and the off switch works (both checked outside a session, below). When the CLI check is disclosed with an off switch, or skipped where its output is ignored, a re-assay can admit this entry.

## What it can execute

- **Hooks** (all `node`, from [hooks/hooks.json](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/hooks.json)):
  - `SessionStart` (`startup|resume|clear|compact`): `session-start-seen-skills.mjs` clears per-session temp files; `session-start-profiler.mjs` detects the harness (it reports `grok` when `GROK_PLUGIN_ROOT` is set), refreshes `~/.config/vercel-plugin/active-session.json`, sends the daily telemetry ping, and in a Vercel, Next.js or eve project or an empty folder runs `vercel --version` and `npm view vercel version` (K-02) and profiles `package.json` and config files for likely skills; `inject-claude-md.mjs` prints the session context (K-04).
  - `PostToolUse` on `Skill`: `posttooluse-skill-telemetry.mjs` reports the name of a plugin skill the agent loads through Claude's `Skill` tool. It does not fire for Grok's tools (K-05).
  - `SessionEnd`: `session-end-cleanup.mjs` removes the session's temp files.
- **Scripts:** none the plugin tells the agent to run beyond the Vercel CLI. The commands (not loaded in Grok, K-03) drive `vercel`; `deploy` asks for "explicit confirmation" before a production deploy ([commands/deploy.md:45](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/commands/deploy.md#L45)). The repository's `scripts/`, `src/` and `tests/` are build and test tools that Grok does not run.
- **MCP servers:** `vercel`, type `http`, at `https://mcp.vercel.com` ([.mcp.json](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/.mcp.json)), OAuth on first connection; the file's note calls it read-only in its initial release.
- **Network:** `https://telemetry.vercel.com/api/vercel-plugin/v1/events` ([telemetry.mjs:6](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/telemetry.mjs#L6)): at most one daily ping (`dau:active_today`, `plugin:first_use`, version, a random install ID, harness), sent from every project, and skill names from Claude's `Skill` tool; off with `VERCEL_PLUGIN_TELEMETRY=off`. The npm registry, through `npm view vercel version`, with no off switch (K-02). The hosted MCP server.
- **Writes:** `~/.config/vercel-plugin/` (`installation-id`, day stamps, `active-session.json`, which Vercel CLI telemetry reads) and session files in the system temp folder.
- **Disclosed in its README:** partly. Telemetry is disclosed field by field, with its endpoint, its stamp files and its off switch ([README.md:124](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L124)). The npm registry query (K-02) and the MCP server (K-08) are not.

## Assay

Grok's own behavior is cited from Grok's documentation and source at [xai-org/grok-build@2bdd1d6](https://github.com/xai-org/grok-build/tree/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8), not from an observed session. The hook runs below are evidence about the scripts, not about Grok's hook runtime.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `2b7e873`, the head of `main`; clean `GROK_HOME` and `HOME`. xAI's catalog pins `c632a50` (0.51.0), 15 commits behind |
| Gate: validate | pass | `name: vercel`, `version: 0.52.0`, `components: 1 skill dir(s), 4 command dir(s), 3 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/vercel/vercel-plugin.git@2b7e873... --trust`: `Installed 1 plugin(s) from ...: vercel` |
| Gate: details | pass | `vercel v0.52.0`, the same components line |
| Gate: inspect | pass, with a gap | `grok inspect --json` from an empty folder: 35 skills (`ai-sdk` twice, K-07), the hook file with 3 events, MCP server `vercel` (`http`, `https://mcp.vercel.com`); no agents and no commands from the plugin, against 3 and 4 in the manifest (K-03) |
| Reading: promises against components | fracture | agents and commands do not load (K-03); the session context does not arrive (K-04) |
| Reading: license | pass, with a hairline | `LICENSE` holds the Apache-2.0 notice (Copyright 2026 Vercel, Inc.); `"license": "Apache-2.0"` in the manifest and `package.json`; a License line in the README. GitHub's API reports `NOASSERTION` because the file is the notice, not the license text (K-06) |
| Reading: what it can execute | break | an undisclosed npm registry query at session start, with no off switch (K-02) |
| Reading: maintenance | last push 2026-10-01, 57 open issues and 28 open pull requests, 295 stars | GitHub API, 2026-10-01 |
| Profiler, outside a session | runs the CLI check and the ping | Grok-shaped `SessionStart` input in a folder whose `package.json` depends on `next`, scratch `HOME`, stand-in `vercel` and `npm` on `PATH` that log their arguments, and `fetch` stubbed so nothing left the machine: it ran `vercel --version`, then `npm view vercel version`, printed "IMPORTANT: The Vercel CLI is outdated", and queued one POST to `telemetry.vercel.com` with `dau:active_today`, `plugin:first_use`, `plugin:version`, `plugin:install_id` and `plugin:agent_harness` = `grok`. With `VERCEL_PLUGIN_TELEMETRY=off`: no POST, and both commands still ran. In a folder with no Vercel markers: no commands, and the POST still queued, as the README says |
| Session context, outside a session | printed to stdout | `inject-claude-md.mjs` in the same folder printed 9,943 bytes (session context, `knowledge-update` body) |
| Skill telemetry, outside a session | inert under Grok input | `tool_name` `read_file` on a plugin `SKILL.md`, or `skill`: no POST. Claude's `tool_name` `Skill` with `vercel:ai-sdk`: one POST, `skill:invoked` = `ai-sdk` |
| Workaround K-03, at the pin | loads | the three agent files and four command files copied into `$GROK_HOME/agents/` and `$GROK_HOME/commands/`: `grok inspect` lists `ai-architect`, `deployment-expert`, `performance-optimizer` and `vercel-bootstrap`, `vercel-deploy`, `vercel-env`, `vercel-status`. Not exercised in a session |
| xAI catalog install | pass | clean home, `grok plugin install vercel@xai-official --trust`: `Installed 1 plugin(s) from xAI Official: vercel`, `vercel v0.51.0` at `c632a50` |
| Hands | not run | a Grok session costs model time, and a real run would send telemetry; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Telemetry used to send every bash command the agent ran to Vercel, and a prompt hook asked for telemetry consent by injecting instructions into the model's context. | [#41](https://github.com/vercel/vercel-plugin/issues/41), [#34](https://github.com/vercel/vercel-plugin/issues/34); fixed by [#42](https://github.com/vercel/vercel-plugin/pull/42) (merged 2026-04-09) and [#47](https://github.com/vercel/vercel-plugin/pull/47) (merged 2026-04-12); at the pin, [README.md:153](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L153) and the telemetry runs above | break | closed upstream #41, #34 | remove bash and prompt telemetry and the injected consent, small | sealed |
| K-02 | At session start in a Vercel, Next.js or eve project or an empty folder, the profiler runs `vercel --version` and `npm view vercel version`, a query to the npm registry. The README does not mention it, `VERCEL_PLUGIN_TELEMETRY=off` does not stop it, and in Grok its output is discarded. | [session-start-profiler.mjs:564](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/session-start-profiler.mjs#L564), [line 653](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/session-start-profiler.mjs#L653), [line 851](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/session-start-profiler.mjs#L851), [README.md:112](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L112); Grok: [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505); the profiler run above | break | new; Windows detection bugs in the same check are held in [#152](https://github.com/vercel/vercel-plugin/issues/152) and [#175](https://github.com/vercel/vercel-plugin/issues/175) | disclose the check, give it an off switch, and skip it where `SessionStart` output is ignored, small | drafted ([seal](../seals/vercel/K-02.md)) |
| K-03 | The three agents and four commands do not load in Grok: `.claude-plugin/plugin.json` lists each as a file, and Grok reads every `commands` and `agents` entry as a folder to list, so it finds nothing. `grok plugin details` still prints `4 command dir(s), 3 agent dir(s)`. | [.claude-plugin/plugin.json:21](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/.claude-plugin/plugin.json#L21), [line 27](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/.claude-plugin/plugin.json#L27), [README.md:90](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L90); Grok: [manifest.rs:47](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/plugins/manifest.rs#L47), [discovery.rs:336](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/discovery.rs#L336), [registry.rs:453](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/plugins/registry.rs#L453); `grok inspect` lists none of them | fracture | new | move `commands/_conventions.md` out of `commands/`, then name the folders instead of the files, small | drafted ([seal](../seals/vercel/K-03.md)) |
| K-04 | The session context never reaches the model in Grok: `inject-claude-md.mjs` prints it (the thin session context, the `knowledge-update` guidance and, in an empty folder, the greenfield guidance) to stdout, and Grok ignores `SessionStart` stdout. | [inject-claude-md.mjs:84](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/inject-claude-md.mjs#L84), [README.md:111](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L111); Grok: [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505); not observed in a session | fracture | new | a README line for Grok users: run `/knowledge-update` at session start, small | drafted ([seal](../seals/vercel/K-04.md)) |
| K-05 | The skill telemetry hook does nothing in Grok: its matcher `Skill` maps to Grok's `skill` tool, which belongs to the opencode tool set (Grok's default agent reads `SKILL.md` with `read_file`), and the script itself accepts only the tool name `Skill`. Grok usage is not counted; nothing is lost for the user. | [hooks/hooks.json:24](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/hooks.json#L24), [posttooluse-skill-telemetry.mjs:21](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/hooks/posttooluse-skill-telemetry.mjs#L21), [README.md:163](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L163); Grok: [claude_alias.rs:70](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-tools/src/types/claude_alias.rs#L70); the skill telemetry run above | hairline | new | name Grok next to Cursor in "Coverage by harness", small | drafted ([seal](../seals/vercel/K-04.md), same draft) |
| K-06 | `LICENSE` holds only the 13-line Apache-2.0 notice, not the license text, so GitHub's license detection reports `NOASSERTION`. | [LICENSE](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/LICENSE); `gh api repos/vercel/vercel-plugin --jq .license.spdx_id`: `NOASSERTION` | hairline | new | ship the full Apache-2.0 text, small | drafted ([seal](../seals/vercel/K-06.md)) |
| K-07 | `skills/ai-sdk/upstream/SKILL.md`, the synced upstream copy, loads in Grok as a second `ai-sdk` skill: Grok lists 35 skills where the README lists 34. | [skills/ai-sdk/upstream/SKILL.md](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/skills/ai-sdk/upstream/SKILL.md); `grok inspect --json` | hairline | filed #77 upstream, open | keep upstream copies out of skill folders, small | open |
| K-08 | The README's Components section lists skills, agents, commands and hooks but not the bundled MCP server; only the `note` in `.mcp.json` describes it. | [README.md:38](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/README.md#L38), [.mcp.json](https://github.com/vercel/vercel-plugin/blob/2b7e8732ac22aafa8319459a881631dd5cff3878/.mcp.json) | hairline | new | one Components entry for the MCP server, small | drafted ([seal](../seals/vercel/K-06.md), same draft) |

## Workarounds

None admits the entry while K-02 is open. A Grok user who installs it anyway can:

- **K-02:** open `/hooks`, select the plugin's `session-start-profiler.mjs` `SessionStart` hook and press `Space` to disable it. That also stops the profiler's telemetry ping and its likely-skill hints. Not run for this assay.
- **K-03:** copy the agents and commands into Grok's own folders, from the installed plugin under `~/.grok/installed-plugins/vercel-plugin-<id>/`:

  ```bash
  P=$(ls -d ~/.grok/installed-plugins/vercel-plugin-*)
  mkdir -p ~/.grok/agents ~/.grok/commands
  cp "$P"/agents/*.md ~/.grok/agents/
  for c in bootstrap deploy env status; do cp "$P/commands/$c.md" ~/.grok/commands/vercel-$c.md; done
  ```

  In a clean Grok home this made `grok inspect` list all three agents and the four commands (`/vercel-bootstrap`, `/vercel-deploy`, `/vercel-env`, `/vercel-status`). The copies do not update with the plugin. Not exercised in a session.
- **K-04:** run `/knowledge-update` at the start of a session, or add `At session start, load the vercel knowledge-update skill.` to the project's `AGENTS.md`. Not run in a Grok session.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
