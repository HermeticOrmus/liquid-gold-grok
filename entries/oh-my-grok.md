# oh-my-grok

A Grok-native workflow layer: a skill gate that holds edits until a skill has been read, Ralph and Ultrawork loops that keep the agent working until a task is done, todo and plan continuation at Stop, line-hash checks on edits, LSP diagnostics after edits, a handoff skill, and the obra/superpowers skills bundled in.

| | |
|---|---|
| Level | **watch** |
| Domain | Engineering workflow |
| Author | [mihazs](https://github.com/mihazs); bundles [obra/superpowers](https://github.com/obra/superpowers) skills by Jesse Vincent (MIT) and MCP runtimes from [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) by Yeongyu Kim |
| License | [MIT](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/LICENSE) for the plugin; see K-02 for the bundled MCP runtimes |
| Source | [mihazs/oh-my-grok](https://github.com/mihazs/oh-my-grok/tree/49f1365c286bd78d455b8c4ea738f9f4d750e0bf) |
| Pinned SHA | `49f1365c286bd78d455b8c4ea738f9f4d750e0bf` (committed 2026-06-09, version 0.2.0) |
| Components at the pin | skills 23, agents 3, commands 0, hook events 6, MCP servers 2 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Grok users who run long tasks and want the agent held to a loop: read the relevant skill, edit against fresh line hashes, fix LSP errors and finish the todo list before it stops.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install mihazs/oh-my-grok --trust
```

The pinned commit installs cleanly with `grok plugin install https://github.com/mihazs/oh-my-grok.git@49f1365c286bd78d455b8c4ea738f9f4d750e0bf --trust`.

## Why it is watch

The gates pass, both bundled MCP servers start and answer, and the hook binary runs cleanly on Grok's event shape. What it promises does not hold up in Grok as documented. Its first feature, the skill gate, never holds an edit after the first prompt: the plugin injects the `using-superpowers` skill as `UserPromptSubmit` context, which Grok drops, and records that skill as read anyway, which unlocks every edit (K-01). The rest of its per-prompt and session-start guidance is dropped the same way. Most of its other hooks check for Cursor-style tool names (`Read`, `StrReplace`, `TodoWrite`), while the names Grok documents are `read_file`, `search_replace` and `todo_write`; under those, reads never build the line-hash cache, stale-anchor edits pass and the todo mirror stays empty (K-08). The README says the plugin was adapted for Grok Composer, whose tool names may match; this assay could not observe that. And one bundled MCP runtime comes from a project under a non-commercial license the plugin does not carry (K-02). With a break open, the entry waits.

## What it can execute

- **Hooks:** six events, all through [`hooks/run-hook.sh`](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/hooks/run-hook.sh), which picks a prebuilt Go binary `bin/omg-hook-<os>-<arch>`: `SessionStart`, `UserPromptSubmit`, `PreToolUse` (edits, writes, deletes), `PostToolUse` (reads, todo writes, edits), `Stop`, `SessionEnd`. The binaries are disclosed ([docs/installation.md](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/docs/installation.md)).
- **Programs the hooks start:** `grok inspect --json` (to build the skill catalog) and `node` (for LSP diagnostics after edits).
- **MCP servers:** `ast_grep` and `lsp`, both `node` running vendored `dist/cli.js` files from `vendor/`.
- **Network:** none found in the hook source (`cmd/`, `internal/`: no HTTP client); the MCP runtimes were not read line by line.
- **Writes:** session state under `$GROK_HOME/state/` (skill gate, hashline, LSP, todo, stop continuation) and workspace state in `.omg/`, both documented in [docs/configuration.md](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/docs/configuration.md).
- **Disclosed in its README:** yes, across the README, `docs/installation.md` and `docs/configuration.md`.

## Assay

Grok's own behavior is cited from Grok's hooks guide (grok 1.0.44, `docs/user-guide/10-hooks.md`, which grok writes into every fresh `GROK_HOME`; the links go to the same text in the public xai-org/grok-build repository at `2bdd1d6`) and from Grok's source at that commit. That is vendor documentation and source, not an observed session.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `49f1365`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 2 skill dir(s), 0 command dir(s), 1 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/mihazs/oh-my-grok.git@49f1365...: oh-my-grok` |
| Gate: details | pass | `oh-my-grok v0.2.0`; `grok inspect` loads 23 skills, 3 agents, 1 hook file and 2 MCP servers for it, the same as the files on disk |
| MCP servers under Grok | pass | `grok mcp doctor`: `ast_grep` handshake OK, 2 tools; `lsp` handshake OK, 7 tools |
| Reading: promises against components | fail | the skill gate, IntentGate and first-prompt bootstrap depend on output Grok drops (K-01); hashline, todo mirror and LSP-after-edit depend on tool names Grok does not document (K-08) |
| Reading: license | fracture | MIT `LICENSE` for the plugin; vendored superpowers keeps its MIT `LICENSE`; the vendored MCP runtimes carry no license (K-02) |
| Reading: what it can execute | pass | hooks, binaries, `grok inspect`, `node` and state folders are documented |
| Reading: maintenance | last push 2026-06-09, 2 open (issue #1, PR #2), 10 stars | GitHub API, 2026-09-30 |
| Hook binary, outside a session | pass, with findings | Grok-shaped input (camelCase keys plus the snake-case aliases grok 1.0.44 adds), scratch `GROK_HOME`: `session-start` exit 0 (2,802 bytes of context); `pre-tool-use` on `search_replace` before any read: `deny` (skill gate); `user-prompt` exit 0 (16,865 bytes of context) and `skills.loaded` then held `using-superpowers`; `post-tool-read` on `read_file`: no output, no hash cache; a stale `LINE#ID` edit was denied as `StrReplace` and allowed as `search_replace`; `stop` exit 0, `{}` |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The skill-gate banner, the first-prompt `using-superpowers` bootstrap, IntentGate banners and per-prompt reminders are sent as `SessionStart` output and `UserPromptSubmit` context, which Grok drops; the gate marks `using-superpowers` as read when it builds that context, so from the first prompt on the skill gate never holds an edit. | [internal/cmd/session_start.go:37](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/cmd/session_start.go#L37), [internal/cmd/user_prompt.go:52](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/cmd/user_prompt.go#L52), [internal/usingpowers/first.go:93](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/usingpowers/first.go#L93); Grok's hooks guide (grok 1.0.44, `docs/user-guide/10-hooks.md` [line 481](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L481) and [line 505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505)); dry run above | break | new | mark a skill read only on a real read of its `SKILL.md`, and deliver guidance through `PreToolUse`/`PostToolUse` context or rules files, medium | drafted ([seal](../seals/oh-my-grok/K-01.md)) |
| K-02 | `vendor/ast-grep-mcp` comes from oh-my-openagent, whose own code is under the Sustainable Use License 1.0 (non-commercial use, keep notices); `vendor/lsp-tools-mcp` is MIT upstream. The plugin ships both with no upstream license or notice, under its own MIT `LICENSE`. | [scripts/build-mcp-runtimes.sh:2](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/scripts/build-mcp-runtimes.sh#L2), [vendor/ast-grep-mcp](https://github.com/mihazs/oh-my-grok/tree/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/vendor/ast-grep-mcp) (only `dist/`); upstream [LICENSE.md](https://github.com/code-yeongyu/oh-my-openagent/blob/42ec97ee455f08704833298f69eeeb15f38c0093/LICENSE.md) (adopted 2025-12-24) and [THIRD-PARTY-NOTICES.md](https://github.com/code-yeongyu/oh-my-openagent/blob/42ec97ee455f08704833298f69eeeb15f38c0093/THIRD-PARTY-NOTICES.md) (lists `lsp-tools-mcp` as MIT, not `ast-grep-mcp`) | fracture | new | add the upstream license texts and a NOTICE under `vendor/`, or replace `ast-grep-mcp` with a permissively licensed server, small | drafted ([seal](../seals/oh-my-grok/K-02.md)) |
| K-03 | Both README install lines fail in grok 1.0.44: `grok plugin install github.com/mihazs/oh-my-grok` is read as a local path. | [README.md:18](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/README.md#L18); `Error: install failed: local path is not a directory` | hairline | held by mihazs ([PR #2](https://github.com/mihazs/oh-my-grok/pull/2)) | use `mihazs/oh-my-grok`, small | open |
| K-04 | Custom slash commands such as `/ulw-loop` need a manual plugin reload before they appear. | reported upstream | hairline | held by mihazs ([#1](https://github.com/mihazs/oh-my-grok/issues/1)) | left to the owner | open |
| K-05 | The hooks' runtime inside a Grok session is unverified; the binary was run only outside a session. | [hooks/hooks.json](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/hooks/hooks.json) | hairline | new | run one Grok session and record a gate deny and a Stop continuation, small | open |
| K-06 | The hook binaries are rebuilt by a pre-commit hook; their build info names commit `24e5ff6` with a modified tree, and no checksum ties them to source. The Go source in `cmd/` and `internal/` is identical between `24e5ff6` and the pin. | `go version -m bin/omg-hook-linux-amd64`: `vcs.revision=24e5ff6... vcs.modified=true`, go1.22.2; [lefthook.yml:8](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/lefthook.yml#L8); `git diff 24e5ff6 49f1365 -- cmd internal go.mod` is empty | hairline | new | build binaries in the release workflow with `-trimpath` from a clean tree and publish checksums, small | open |
| K-07 | The bundled superpowers skills are v5.1.0, while upstream is at v6.4.2; installed next to the superpowers plugin, the same skill names load twice. | [vendor/superpowers/VERSION](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/vendor/superpowers/VERSION); the duplicate is noted in [docs/configuration.md:47](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/docs/configuration.md#L47) | hairline | new | refresh the vendored copy, small | open |
| K-08 | The hooks act only on Cursor-style tool names: `post-tool-read` returns unless the tool is `read`, the todo mirror unless it is `todowrite`, the hashline check covers `strreplace`, `edit` and `multiedit`, LSP-after-edit covers names such as `write`, `edit` and `strreplace`. Grok documents `read_file`, `search_replace` and `todo_write`, so under those names reads never mark skills or build hash caches, stale-anchor edits pass and no LSP check follows a `search_replace`. | [internal/cmd/post_tool_read.go:21](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/cmd/post_tool_read.go#L21), [internal/cmd/post_tool_todo.go:20](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/cmd/post_tool_todo.go#L20), [internal/hashline/validate.go:18](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/hashline/validate.go#L18), [internal/lsp/posttool.go:15](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/internal/lsp/posttool.go#L15); Grok's names: hooks guide [line 172](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L172) and [claude_alias.rs:47](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-tools/src/types/claude_alias.rs#L47); dry run above. Whether Grok Composer sessions use the Cursor-style names is *inferred* from the plugin's docs ([AGENTS.md:5](https://github.com/mihazs/oh-my-grok/blob/49f1365c286bd78d455b8c4ea738f9f4d750e0bf/AGENTS.md#L5)) | fracture | new | accept both name sets (`read`/`read_file`, `strreplace`/`search_replace`, `todowrite`/`todo_write`), small | drafted ([seal](../seals/oh-my-grok/K-08.md)) |

## Workarounds

- **K-01:** start a session by asking Grok to read `vendor/superpowers/skills/using-superpowers/SKILL.md` and the skill that fits the task, so the guidance the hooks cannot deliver arrives through a real read. This does not restore the gate. Not run at the pin.
- **K-02:** if you cannot use code under the Sustainable Use License, turn the bundled runtime off with `grok mcp disable ast_grep` (and `grok mcp disable lsp` for the other one). Run at the pin in a clean Grok home: both exit 0 and are written to `disabled_mcp_servers`. The files stay on disk; this only stops Grok from starting them.
- **K-08:** the plugin's docs target Grok Composer; if your model uses the Cursor-style tool names, these hooks may apply. Not observed.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
