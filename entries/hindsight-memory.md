# hindsight-memory

Long-term memory for Grok through Hindsight: hooks save the conversation transcript to a Hindsight memory bank and try to recall relevant memories before each prompt, and an MCP server offers knowledge-page and search tools.

| | |
|---|---|
| Level | **watch** |
| Domain | Memory |
| Author | [Vectorize](https://github.com/vectorize-io) (Hindsight team) |
| License | [MIT](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/LICENSE) |
| Source | [vectorize-io/hindsight-grok-plugin](https://github.com/vectorize-io/hindsight-grok-plugin/tree/31a126047666fc569e83069a07a7953607170214) |
| Pinned SHA | `31a126047666fc569e83069a07a7953607170214` (committed 2026-06-25, version 0.7.1) |
| Components at the pin | skills 1, agents 0, commands 0, hook events 4, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

People who want Grok to carry decisions and project context from one session to the next, and who are willing to run a Hindsight server (local or hosted) and an LLM key for fact extraction.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install vectorize-io/hindsight-grok-plugin --trust
```

The pinned commit installs cleanly with `grok plugin install https://github.com/vectorize-io/hindsight-grok-plugin.git@31a126047666fc569e83069a07a7953607170214 --trust`.

## Why it is watch

The plugin's first promise is auto-recall: memories injected as context on every prompt. It delivers them as `additionalContext` from a `UserPromptSubmit` hook ([scripts/recall.py:216](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/recall.py#L216)). Grok documents that it discards that output from an allowing `UserPromptSubmit` hook ([10-hooks.md:481](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L481)), and its prompt gate returns only the allow or block decision ([hook_dispatch.rs:444](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-shell/src/session/acp_session_impl/hook_dispatch.rs#L444)). So in Grok the plugin can store memories but cannot bring them back on its own (K-01). The MCP tools that could recall on request do not start either: `grok mcp doctor hindsight` fails the handshake because the launcher reads `CLAUDE_PLUGIN_DATA` and `CLAUDE_PLUGIN_ROOT` from its environment and Grok sets neither for MCP servers (K-02). And the half that stores memories likely stores nothing: `retain.py` parses Claude Code's transcript format, while the `transcript_path` Grok hands to hooks is its own `updates.jsonl` stream, which Grok's docs say another tool's parser will not read (K-10, *inferred*). Breaks are open, so the plugin is not admitted.

## What it can execute

- **Hooks** (all `python3`, standard library only):
  - `SessionStart`: [session_start.py](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/session_start.py) checks `http://127.0.0.1:9077/health`; if nothing answers and `uvx` is on `PATH` and an LLM key is found, it starts `uvx hindsight-embed@latest profile create ... && ... daemon start` in the background.
  - `UserPromptSubmit`: [recall.py](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/recall.py) sends the prompt (and recent turns) to the Hindsight server and prints the memories it gets back.
  - `Stop` (async): [retain.py](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/retain.py) reads the session transcript file and, every 10th turn by default, posts the whole session transcript to the Hindsight server, starting the local daemon if needed.
  - `SessionEnd`: [session_end.py](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/session_end.py) forces a final retain, then stops the daemon if the plugin started it.
- **Scripts:** [setup_hooks.py](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/setup_hooks.py) writes the hooks into `~/.claude/settings.json` when run by hand (K-07).
- **MCP servers:** `hindsight`, stdio: `bash scripts/run_mcp.sh` creates a virtualenv in the plugin data folder, runs `pip install "mcp>=1.0.0"`, then runs `mcp_server.py` with nine `agent_knowledge_*` tools.
- **Network:** by default only `127.0.0.1:9077`, the local `hindsight-embed` daemon. The daemon is not part of the plugin: `uvx` downloads the latest `hindsight-embed` from PyPI, and it sends conversation content to the LLM provider whose key it finds (OpenAI, Anthropic, Gemini or Groq, in that order) to extract facts. With `hindsightApiUrl` set, transcripts go to that server instead. `pip` downloads `mcp` on the MCP server's first start.
- **Writes:** turn counters and recall state in the plugin data folder (`state/`), the MCP virtualenv, and whatever `hindsight-embed` stores (not assessed).
- **Disclosed in its README:** mostly. "Network & credentials" names the loopback daemon, the provider key and the `uvx` download ([README.md:96](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L96)); the key on the command line (K-03) and the setup script's write to Claude Code settings (K-07) are not.

## Assay

Grok's own behavior is cited from Grok's hooks guide (grok 1.0.44, `docs/user-guide/10-hooks.md`, which grok writes into every fresh `GROK_HOME`; the links go to the same text in the public xai-org/grok-build repository at `2bdd1d6`) and from Grok's source at that commit. That is vendor documentation and source, not an observed session.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `31a1260`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/vectorize-io/hindsight-grok-plugin.git@31a1260...: hindsight-memory` |
| Gate: details | pass | `hindsight-memory v0.7.1`, hooks and MCP servers listed; 1 skill (`create-agent`) in the installed folder |
| Reading: promises against components | fail | auto-recall cannot reach the model in Grok (K-01); the knowledge tools do not start (K-02); retain likely reads nothing (K-10) |
| Reading: license | pass | MIT, `LICENSE` at the root, `"license": "MIT"` in the manifest |
| Reading: what it can execute | partial | disclosed except K-03 and K-07 |
| Reading: maintenance | last push 2026-06-25, 0 open issues, 5 stars | GitHub API, 2026-09-30 |
| Hook scripts, outside a session | pass | all four hooks with Grok-shaped input, scratch `HOME`, no keys, no server: each exits 0 and degrades cleanly (`No Hindsight server on port 9077`, `hindsight-embed not available, skipping pre-start`); only `state/turns.json` was written. The daemon path (PyPI download, LLM calls) was not run |
| MCP server under Grok | fail | `grok mcp doctor hindsight` in a clean Grok home: `server started`, then `handshake failed (connection closed: initialize response)`; the server log reads `mkdir: cannot create directory ''`. With `CLAUDE_PLUGIN_DATA` exported by hand the venv is created, then pip fails on `/requirements.txt` because `CLAUDE_PLUGIN_ROOT` is empty too |
| Hands | not run | a Grok session costs model time, and a real run would send transcripts to an LLM provider; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Auto-recall prints memories as `UserPromptSubmit` `additionalContext`, which Grok discards for an allowing hook, so recalled memories never reach the model. | [scripts/recall.py:216](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/recall.py#L216), [README.md:32](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L32); Grok: [10-hooks.md:481](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L481), [hook_dispatch.rs:444](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-shell/src/session/acp_session_impl/hook_dispatch.rs#L444); not observed in a live session | break | new (tracker empty) | deliver recall through a channel Grok keeps (for example the first `PreToolUse` or `PostToolUse` of the turn), or ask xAI to keep `UserPromptSubmit` context, medium | drafted ([seal](../seals/hindsight-memory/K-01.md)) |
| K-02 | The MCP server never starts in Grok: `run_mcp.sh` reads `CLAUDE_PLUGIN_DATA` and `CLAUDE_PLUGIN_ROOT` from its environment, and Grok substitutes those tokens inside `.mcp.json` strings but does not set them for MCP processes. | [scripts/run_mcp.sh:6](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/run_mcp.sh#L6), [.mcp.json](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/.mcp.json); Grok: [mcp_servers.rs:157](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-config/src/mcp_servers.rs#L157); `grok mcp doctor hindsight`: handshake failed, server log `mkdir: cannot create directory ''` | break | new | pass both in `.mcp.json`: `"env": {"CLAUDE_PLUGIN_ROOT": "${CLAUDE_PLUGIN_ROOT}", "CLAUDE_PLUGIN_DATA": "${CLAUDE_PLUGIN_DATA}"}`, small | drafted ([seal](../seals/hindsight-memory/K-02.md)) |
| K-03 | When the plugin starts the local daemon, it passes the detected LLM API key as `--env HINDSIGHT_API_LLM_API_KEY=<key>` on the `hindsight-embed profile create` command line, where other local users can read it in the process list. | [scripts/lib/daemon.py:195](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/daemon.py#L195), [scripts/lib/daemon.py:297](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/daemon.py#L297) | fracture | new | pass the key through the child's environment only, small | drafted ([seal](../seals/hindsight-memory/K-03.md)) |
| K-04 | "Outbound calls happen only when you configure them", but an existing `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` or `GROQ_API_KEY` in the environment is picked up automatically, and transcripts then go to that provider. | [README.md:99](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L99), [scripts/lib/llm.py:91](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/llm.py#L91); install step 2 does say "auto-detected" ([README.md:16](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L16)) | hairline | new | say that an ambient key counts as configured, small | drafted ([seal](../seals/hindsight-memory/K-03.md), same draft) |
| K-05 | The memory backend is fetched as `hindsight-embed@latest` from PyPI at session start by default, and the MCP server installs `mcp>=1.0.0`; neither is pinned. | [scripts/lib/daemon.py:41](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/daemon.py#L41), [settings.json](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/settings.json), [requirements.txt](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/requirements.txt); disclosed at [README.md:79](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L79) | hairline | new | ship a pinned default `embedVersion` and an exact `mcp` version, small | open |
| K-06 | The README's install steps use `/plugin` search and `/mcp`; the plugin is not in xAI's catalog, the repo has no marketplace file, and Grok documents `/plugins`, `/marketplace` and `/mcps`. | [README.md:9](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/README.md#L9); Grok's slash commands: [04-slash-commands.md](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/04-slash-commands.md) | hairline | new | document `grok plugin install vectorize-io/hindsight-grok-plugin`, small | sealed (card): the direct install above ran at the pin |
| K-07 | `setup_hooks.py`, offered by `skills/setup.md`, looks for the plugin in Claude Code's plugin cache and writes the hooks into `~/.claude/settings.json`; Grok already loads plugin hooks and also reads that file, so running it would register the hooks twice. `skills/setup.md` is not in a skill folder, so Grok does not load it. | [scripts/setup_hooks.py:16](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/setup_hooks.py#L16), [skills/setup.md](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/skills/setup.md); Grok reads `~/.claude/settings.json` hooks: [10-hooks.md:67](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L67); double registration *inferred* | hairline | new | remove the script from the Grok edition, small | open |
| K-08 | Grok sessions use Claude Code names: bank `claude_code`, config file `~/.hindsight/claude-code.json`, retain context `claude-code`, and a state fallback under `~/.claude/plugins/data/`. A Claude Code install of Hindsight on the same machine writes to the same bank. | [settings.json:3](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/settings.json#L3), [scripts/lib/config.py:135](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/config.py#L135), [scripts/lib/state.py:21](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/lib/state.py#L21) | hairline | new | Grok-specific defaults, or a README line saying the bank is shared on purpose, small | open |
| K-09 | The four hooks' runtime inside a Grok session is unverified; the scripts were checked only outside a session. | [hooks/hooks.json](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/hooks/hooks.json) | hairline | new | run one Grok session against a local Hindsight server, small | open |
| K-10 | `retain.py` reads the transcript as Claude Code JSONL (`{type: user, message: {role, content}}`), but in Grok `transcript_path` is the session's own `updates.jsonl` update stream, so the retain hook likely finds no messages and stores nothing. | [scripts/retain.py:38](https://github.com/vectorize-io/hindsight-grok-plugin/blob/31a126047666fc569e83069a07a7953607170214/scripts/retain.py#L38); Grok: [compaction.rs:518](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-shell/src/session/compaction.rs#L518) (`updates.jsonl`), [25-status-line.md:90](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/25-status-line.md#L90) ("a script that parses another tool's transcript format will not read it"); *inferred*, no Grok transcript was read | break | new | parse Grok's `updates.jsonl`, or build the transcript from hook events, medium | drafted ([seal](../seals/hindsight-memory/K-01.md), same draft) |

## Workarounds

No workaround was found for K-01, K-02 or K-10. Exporting `CLAUDE_PLUGIN_DATA` before launching Grok gets the MCP launcher one step further (Grok passes its own environment through), but it then needs `CLAUDE_PLUGIN_ROOT` set to the installed plugin folder, which changes with every install; that is not a workaround to recommend.

For K-03, run Hindsight in external API mode (`hindsightApiUrl`), so the plugin never starts the daemon with a key on the command line.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
