# epic

The epic-harness plugin: 27 auto-triggering skills for a spec, build, check and ship pipeline, and six hooks that guard shell commands, format after edits, log every tool call and "evolve" new skills from what went wrong. The hooks and the memory MCP server run a separate `epic` binary.

| | |
|---|---|
| Level | **watch** |
| Domain | Engineering workflow |
| Author | [epicsagas](https://github.com/epicsagas) |
| License | [Apache-2.0](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/LICENSE) |
| Source | [epicsagas/epic-harness](https://github.com/epicsagas/epic-harness/tree/7abf3f1404242815dd99f03b5f417c188b7cde5a) |
| Pinned SHA | `7abf3f1404242815dd99f03b5f417c188b7cde5a` (committed 2026-09-20, version 0.8.8) |
| Components at the pin | skills 27, agents 0, commands 0, hook events 6, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

People who want one harness across Claude Code, Codex, Antigravity and Grok that ships features end to end and adapts its own skills from session history.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install epicsagas/epic-harness --trust
```

The pinned commit installs cleanly with `grok plugin install https://github.com/epicsagas/epic-harness.git@7abf3f1404242815dd99f03b5f417c188b7cde5a --trust`.

## Why it is watch

The plugin at the pin installs and its skills load, but everything that makes it a harness runs in the `epic` binary, which the plugin does not ship. In a clean Grok home the hooks print `[harness] epic not found` and do nothing, and `grok mcp doctor` reports the `harness-mem` server failing with `exec: epic: not found` (K-01). Assaying the binary means installing it from the latest GitHub release or crates.io, outside the pin, and it turns on usage telemetry to PostHog the first time it runs unless consent was already set. That is something this assay could not do safely, so the entry waits until the binary can be assayed at a pinned version.

## What it can execute

- **Hooks:** six events in [`.grok-plugin/hooks.json`](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/.grok-plugin/hooks.json), each running `epic <subcommand>` if `epic` is on `PATH`: `SessionStart` (`resume`), `PreToolUse` on shell commands (`guard`), `PostToolUse` on edits (`polish`: format and typecheck) and on every tool (`observe`), `SubagentStart` (`observe`), `PreCompact` (`snapshot`), `SessionEnd` (`reflect`).
- **Scripts:** none run from the plugin folder itself; the repository also holds `install.sh`, which downloads the latest release from GitHub.
- **MCP servers:** `harness-mem`, stdio, `sh -c` that looks for `target/release/epic` in the plugin folder and falls back to `epic mem mcp` on `PATH`.
- **Network:** none from the plugin folder. The binary, per its README, sends anonymous usage telemetry to PostHog by default ([README.md:159](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L159); consent defaults to on at [src/telemetry.rs:301](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/src/telemetry.rs#L301)) and auto-launches a local web dashboard on port 7700 that opens a browser on the first session ([README.md:35](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L35)).
- **Writes (binary):** tool-use observations and session snapshots under `~/.harness/projects/<slug>/`, an install id and telemetry consent under `~/.config/epic-harness/` ([README.md:410](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L410)).
- **Disclosed in its README:** yes for the binary (telemetry, dashboard, data folders). The README has no Grok Build section at all (K-02).

## Assay

Grok's own behavior is cited from Grok's hooks guide (grok 1.0.44, `docs/user-guide/10-hooks.md`, which grok writes into every fresh `GROK_HOME`; the links go to the same text in the public xai-org/grok-build repository at `2bdd1d6`) and from Grok's source at that commit. That is vendor documentation and source, not an observed session.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `7abf3f1`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/epicsagas/epic-harness.git@7abf3f1...: epic` |
| Gate: details | pass | `epic v0.8.8`; `grok inspect` loads 27 skills, 1 hook file and 1 MCP server for it, the same as the files on disk |
| MCP server under Grok | fail | `grok mcp doctor`: `harness-mem` handshake failed; log `sh: line 1: exec: epic: not found` |
| Reading: promises against components | fail | hooks and memory need a binary outside the plugin (K-01); `/check` has no skill of that name (K-06) |
| Reading: license | pass | Apache-2.0 `LICENSE` at the root; the manifest Grok reads first has no `license` field, the `.grok-plugin` one says Apache-2.0 |
| Reading: what it can execute | partial | the binary's behavior is documented; its Grok install path is not |
| Reading: maintenance | last push 2026-09-24, 6 open issues, 19 stars | GitHub API, 2026-09-30 |
| Hook commands, outside a session | pass | each of the seven hook commands run with no `epic` on `PATH`: exit 0; three print `[harness] epic not found, skipping ...`, four print nothing |
| Hands | not run | a Grok session costs model time, and the binary was not installed; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | In Grok the hooks and the `harness-mem` MCP server need an `epic` binary that the plugin does not ship, and nothing in the Grok install puts it there; the Claude Code path is the one that "auto-installs the binary". | [.grok-plugin/hooks.json](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/.grok-plugin/hooks.json), [.mcp.json](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/.mcp.json), [README.md:93](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L93); `grok mcp doctor`: `exec: epic: not found` | fracture | new (no Grok issue in the tracker) | a Grok install section that installs a pinned binary, or a first-run check that says what is missing, small | drafted ([seal](../seals/epic/K-01.md)) |
| K-02 | The README never mentions Grok Build, though the repository ships a Grok manifest and Grok hooks; the manifest Grok reads first (`plugin.json`, [manifest.rs:261](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/plugins/manifest.rs#L261)) describes it as loaded by agy, Claude Code and codex. | `grep -ci grok README.md` returns 0; [plugin.json](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/plugin.json) | hairline | new | add Grok to the install section and the manifest description, small | drafted ([seal](../seals/epic/K-01.md), same draft) |
| K-03 | The MCP launcher's in-plugin candidates `${GROK_PLUGIN_ROOT:-}` and `${CLAUDE_PLUGIN_ROOT:-}` expand to empty in Grok, so a binary under the plugin's `target/release/` is never found. | `grok mcp doctor` prints the command as `for d in "" "" .; do ...`; Grok substitutes only the plain `${GROK_PLUGIN_ROOT}` token ([mcp_servers.rs:157](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-config/src/mcp_servers.rs#L157)) | hairline | new | use `${GROK_PLUGIN_ROOT}` without the `:-` default, small | open |
| K-04 | `epic resume` returns its restored context as `SessionStart` output, which Grok ignores, so session memory would not reach the model at start. | [src/main.rs:367](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/src/main.rs#L367); Grok: [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505); *inferred*, the binary was not run | hairline | new | deliver resume context on the first `PreToolUse` or `PostToolUse`, medium | open |
| K-05 | The hooks run the first program named `epic` on `PATH` on every shell command and every tool call, whatever it is. | [.grok-plugin/hooks.json](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/.grok-plugin/hooks.json) (`EH=$(command -v epic)`) | hairline | new | check the binary's `--version` output before running it, small | open |
| K-06 | The README's pipeline uses `/check`, but no skill named `check` ships; legacy names route through the binary. | [README.md:70](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L70), [README.md:187](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/README.md#L187); the 27 skill names at the pin include `verify` and `audit`, not `check` | hairline | new | name the skill that runs the check stage, small | open |
| K-07 | The hooks' runtime inside a Grok session is unverified. | [.grok-plugin/hooks.json](https://github.com/epicsagas/epic-harness/blob/7abf3f1404242815dd99f03b5f417c188b7cde5a/.grok-plugin/hooks.json) | hairline | new | run one Grok session with a pinned binary, small | open |

## Workarounds

- **K-01:** install the binary the README documents for hosts without a plugin installer (`brew install epicsagas/tap/epic-harness`, `cargo binstall epic-harness` or `cargo install epic-harness`), then run `epic-harness telemetry status` and turn telemetry off if you do not want it. Not run at the pin: it installs code from outside the pin and enables telemetry by default.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
