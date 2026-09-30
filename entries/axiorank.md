# axiorank

A guard for the Grok agent: on every tool call it scores the command, file write or tool result on your machine and denies or holds destructive commands, leaked secrets and prompt-injected results. With an AxioRank API key it also reports the session to an AxioRank workspace and mints a signed session seal.

| | |
|---|---|
| Level | **watch** |
| Domain | Agent safety |
| Author | [AxioRank](https://github.com/AxioRank) |
| License | [MIT](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/LICENSE) |
| Source | [AxioRank/grok-plugin](https://github.com/AxioRank/grok-plugin/tree/08fe4b8616c8b11a56d23c3cf1d68f12f25665de) |
| Pinned SHA | `08fe4b8616c8b11a56d23c3cf1d68f12f25665de` (committed 2026-07-01, version 0.1.0) |
| Components at the pin | skills 1, agents 0, commands 2, hook events 3, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

People who let Grok run shell commands and edit files with little supervision, and want a local tripwire in front of `rm -rf`, force pushes and secrets leaving the machine.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin marketplace add AxioRank/grok-plugin
grok plugin install axiorank --trust
```

The pinned commit installs cleanly with `grok plugin install https://github.com/AxioRank/grok-plugin.git@08fe4b8616c8b11a56d23c3cf1d68f12f25665de --trust`.

## Why it is watch

The local guard does what it says in Grok's own payload shape: with no API key it denied `rm -rf`, `git push --force`, `DROP TABLE` and a live API key in a file write, and it sent nothing anywhere. It is held back by its optional central audit. The README promises that only "redacted call metadata" leaves the machine when `AXIORANK_API_KEY` is set; pointed at a local listener, the guard sent the full shell command (including a database password it had just flagged as a secret) and the full text of a file it read (K-01). That is an open break of a privacy promise, so the entry is not admitted until the code or the README changes.

## What it can execute

- **Hooks:** `PreToolUse`, `PostToolUse` and `Stop`, with no matcher, so on every tool call. Each runs [`scripts/guard.sh`](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/scripts/guard.sh), which runs `node bin/guard.mjs --agent grok`. The guard needs `node`; without it the hook fails and Grok lets the call through (fail-open, as the README says).
- **Scripts:** [`bin/guard.mjs`](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs), a vendored build of `@axiorank/coding-guard` 0.1.3 (1,871 lines). If that file is missing, the shim runs `npx -y @axiorank/coding-guard` instead. The `/axiorank:verify-seal` command runs `npx -y @axiorank/audit-verify`.
- **MCP servers:** `axiorank`, HTTP, `https://app.axiorank.com/api/mcp-server/mcp`, with `Authorization: Bearer ${AXIORANK_API_KEY}`. Grok attaches trusted plugin MCP servers to every session ([09-plugins.md:154](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md#L154)), key or no key.
- **Network:** from the hooks, none unless `AXIORANK_API_KEY` is set ([bin/guard.mjs:1539](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs#L1539)). With a key: a POST to `/api/gateway/tool-call` on every PreToolUse and PostToolUse, and a POST to `/api/coding-sessions/<id>/seal` at Stop. `AXIORANK_CODING_GUARD_DISABLE_REMOTE` turns this off even with a key.
- **Writes:** a session state file in the system temp folder (`axiorank-coding-guard/<session>.json`: trace id, call counts, detector categories, working folder). With a key, a seal file in `<project>/.axiorank/`.
- **Disclosed in its README:** partly. The hooks, the vendored binary, the MCP server and the key-gated audit are described; the temp state file is not, and the Privacy section says nothing leaves the machine without a key while the MCP section registers a hosted server ([README.md:47](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/README.md#L47), [README.md:76](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/README.md#L76)).

## Assay

Grok's own behavior is cited from Grok's hooks guide (grok 1.0.44, `docs/user-guide/10-hooks.md`, which grok writes into every fresh `GROK_HOME`; the links go to the same text in the public xai-org/grok-build repository at `2bdd1d6`) and from Grok's source at that commit. That is vendor documentation and source, not an observed session.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `08fe4b8`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 0 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/AxioRank/grok-plugin.git@08fe4b8...: axiorank` |
| Gate: details | pass | `axiorank v0.1.0`, hooks and MCP servers listed; 1 skill, 2 commands in the installed folder |
| Reading: promises against components | fail | blocking works; `curl ... \| sh` is held, not blocked (K-02); central audit sends raw content (K-01) |
| Reading: license | pass | MIT, `LICENSE` at the root, `"license": "MIT"` in the manifest |
| Reading: what it can execute | fail | one undisclosed local write (K-05); a hosted MCP server that contradicts the Privacy section (K-03) |
| Reading: maintenance | last push 2026-07-01, 0 open issues, 0 stars | GitHub API, 2026-09-30 |
| Hook script, outside a session | pass | Grok-shaped `PreToolUse` input (`tool_name: run_terminal_command`; the guard reads `tool_name`, `tool_input` and `session_id`, snake-case aliases that Grok adds next to its camelCase keys: the alias table is in the grok 1.0.44 binary and in source at [event.rs:378](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-hooks/src/event.rs#L378)): `rm -rf /` and `git push --force` denied, `DROP TABLE` denied, a live key in a write denied; output is `{"decision":"deny",...,"hookSpecificOutput":{...}}`, exit 0 |
| Network, outside a session | pass without a key, fail with one | local listener on `127.0.0.1` via `AXIORANK_BASE_URL`: 0 requests with no key; with a test key, 2 requests carrying the raw command and the raw file text |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | With `AXIORANK_API_KEY` set, the guard sends the raw tool arguments and the raw tool result text to AxioRank, while the README says only redacted call metadata leaves the machine. | [bin/guard.mjs:1550](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs#L1550) (`arguments: call.arguments`), [bin/guard.mjs:1571](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs#L1571) (`resultText`), [README.md:76](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/README.md#L76); local listener capture: `export DB_PASSWORD=...` and a file's contents arrived verbatim | break | new (tracker empty) | send the redacted payload the guard already computes, or correct the Privacy section, small | drafted ([seal](../seals/axiorank/K-01.md)) |
| K-02 | The README and skill say `curl ... \| sh` is blocked; the guard returns `ask` for it, and an `ask` is approved automatically in a client that approves every prompt. | [README.md:9](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/README.md#L9), [skills/coding-guard/SKILL.md:14](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/skills/coding-guard/SKILL.md#L14); `curl ... \| sh`, `curl ... \| bash`, `wget -qO- ... \| sh` all returned `ask` (risk 68); Grok on `ask` under always-approve: [10-hooks.md:298](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L298) | fracture | new | deny pipe-to-shell, or say "held for approval" in the docs, small | drafted ([seal](../seals/axiorank/K-02.md)) |
| K-03 | The Privacy section says nothing leaves the machine without a key, but the plugin registers a hosted MCP server that Grok attaches to every session. | [.mcp.json](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/.mcp.json), [README.md:76](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/README.md#L76), [09-plugins.md:154](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/09-plugins.md#L154); the connection itself was not observed in a session | fracture | new | name the MCP connection in the Privacy section, or ship it disabled, small | drafted ([seal](../seals/axiorank/K-03.md)) |
| K-04 | The hooks' runtime inside a Grok session is unverified; the guard was checked only outside a session. | [hooks/hooks.json](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/hooks/hooks.json); output matches the decision shape in [10-hooks.md:289](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L289) | hairline | new | run one Grok session and record a denied `rm -rf`, small | open |
| K-05 | Every hook run writes session state to `axiorank-coding-guard/<session>.json` in the system temp folder, which the README does not mention. | [bin/guard.mjs:1663](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs#L1663); the file appeared in the scratch temp folder during the dry run | hairline | new | one line in the Privacy section, small | open |
| K-06 | The adapter maps only Claude Code tool names, so Grok calls are labelled `agent.run_terminal_command`, `agent.read_file` and so on in scores and audit records. | [bin/guard.mjs:36](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/bin/guard.mjs#L36); local detection still fired on every dangerous input tried | hairline | new | map Grok's tool names ([10-hooks.md:168](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L168)), small | open |
| K-07 | Two paths run unpinned npm packages: the shim's fallback and the verify-seal command. | [scripts/guard.sh:20](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/scripts/guard.sh#L20), [commands/verify-seal.md:15](https://github.com/AxioRank/grok-plugin/blob/08fe4b8616c8b11a56d23c3cf1d68f12f25665de/commands/verify-seal.md#L15) | hairline | new | pin both package versions, small | open |

## Workarounds

- **K-01:** leave `AXIORANK_API_KEY` unset, or set `AXIORANK_CODING_GUARD_DISABLE_REMOTE=1`. Run at the pin: with no key, a local listener received 0 requests while the guard still denied every dangerous input tried. This avoids the leak; it does not give you the redacted central audit the README describes.
- **K-02:** keep Grok's permission prompts on, so a held `curl ... | sh` reaches you instead of an auto-approval.
- **K-03:** `grok plugin install ...` then `grok mcp disable axiorank`. Run at the pin in a clean Grok home: exit 0 and `disabled_mcp_servers = ["axiorank"]` written to `config.toml`. Its effect inside a session was not observed.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
