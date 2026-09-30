# libre-secops-hooks

Three security hooks for everyday editing: a one-line security profile of the project at session start, a confirmation prompt before an edit touches a secrets or key file, and a local pattern scan of each edited file for injection, XSS, hardcoded secrets, weak crypto and similar mistakes.

| | |
|---|---|
| Level | **watch** |
| Domain | Security |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/LICENSE) |
| Source | [HermeticOrmus/LibreSecOps-Claude-Code](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/tree/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks) (`plugins/libre-secops-hooks`) |
| Pinned SHA | `a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7` (committed 2026-09-30, release v1.0.1) |
| Components at the pin | skills 0, agents 0, commands 0, hook events 3, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Developers who want a second pair of eyes on every edit: a prompt before a `.env`, key or credentials file changes, and a short list of likely vulnerabilities after each write, all local, with no network and no files written.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/HermeticOrmus/LibreSecOps-Claude-Code.git@a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7#plugins/libre-secops-hooks --trust
```

## Why it waits

It installs clean, and the scripts are sound: fed Claude Code's hook input, the PreToolUse hook asks before a `.env` edit and the PostToolUse scan reports an embedded private key as CRITICAL. The vessel also carries real gold from release [#2](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/pull/2): before 1.0.0 these hooks were never registered and never ran, answered in a format nobody read, and the private key check itself never ran because grep read its pattern as an option. All of that is sealed and was checked again at the pin.

What holds it at watch is Grok's side of the wire. Grok sends its own tool names in the hook input (an edit is `search_replace`, not `Edit`), and its hooks guide says a SessionStart hook's output is ignored. The scripts check for Claude Code's tool names inside their own code, so under Grok both safety hooks fire and print nothing (K-09), and the session profile has no way to reach the model (K-10). That breaks the plugin's safety promise for Grok users. It stays open until the scripts accept Grok's tool names and one Grok session shows the ask and the finding arrive. The seal is drafted.

## What it can execute

- **Hooks:** `SessionStart` (matcher `startup|resume|clear|compact`) runs `hooks/session-start.sh`; `PreToolUse` and `PostToolUse` (matcher `Edit|Write|MultiEdit`, which Grok maps to its `search_replace` tool) run `hooks/pre-tool-use.sh` and `hooks/post-tool-use.sh` ([hooks/hooks.json](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/hooks.json)).
- **Scripts:** the three bash scripts above. They read the project's manifests and the edited file (first 100 KB), and run `git rev-parse`, `git ls-files` and `find` in the project. They need `bash` and `jq`; without `jq` they exit quietly.
- **MCP servers:** none.
- **Network:** none found. No script writes a file.
- **Disclosed in its README:** yes. The plugin README names every hook, what it reads, the `jq` dependency, and "They make no network calls and write no files" ([README.md:14](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/README.md#L14), [:18](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/README.md#L18)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `a874d37`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 0 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreSecOps-Claude-Code.git@a874d37...#plugins/libre-secops-hooks --trust`: `Installed 1 plugin(s) ... libre-secops-hooks` |
| Gate: details | pass | `libre-secops-hooks v1.0.0 (subdir: plugins/libre-secops-hooks)`, install registry commit `a874d37` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: the plugin's hook file, 3 hook events loaded, the same as the files on disk |
| Reading: promises against components | pass for Claude Code input, fail for Grok's documented input | the three hooks the README describes are the three that load; see K-09 and K-10 for what Grok feeds them |
| Hook scripts, outside a session, Claude Code input | pass | with `CLAUDE_PLUGIN_ROOT` and `GROK_PLUGIN_ROOT` set, jq 1.8.2: SessionStart in a sample Express project exits 0 and prints one line (`LibreSecOps: JavaScript/TypeScript (Express). Gaps: ...`); PreToolUse `Edit` of `.env` exits 0 with `hookSpecificOutput.permissionDecision: "ask"`; PreToolUse `Bash` prints nothing; PostToolUse `Write` of a file holding a private key header exits 0 with `hookSpecificOutput.additionalContext` and a `systemMessage` naming one CRITICAL finding |
| Hook scripts, outside a session, Grok's documented input | fail | the same `.env` and private-key cases sent as `{"hookEventName":..., "toolName":"search_replace","toolInput":{"file_path":...}}` exit 0 with no output from either script |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | three local bash hooks, no network, no writes, all disclosed |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 4 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay. That is exactly the check K-09 needs |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Before 1.0.0 the hook scripts were never registered, so they never ran; their wiring pointed at a `LIBRESECOPS_HOOKS_DIR` variable that nothing set. | [CHANGELOG.md:34](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L34), [plugin README.md:37](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/README.md#L37) | break | release PR #2 | this plugin wires them through `hooks/hooks.json` and `${CLAUDE_PLUGIN_ROOT}`, medium | sealed #2 |
| K-02 | The hooks returned context as a top-level `additionalContext` array, which the hook runtime does not read. | [CHANGELOG.md:34](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L34); the output now goes through `hookSpecificOutput` ([post-tool-use.sh:461](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L461)) | break | release PR #2 | `hookSpecificOutput.additionalContext`, small | sealed #2 |
| K-03 | The hook scripts wrote log files inside the hooks folder. | [CHANGELOG.md:34](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L34); at the pin no script redirects output to a file | fracture | release PR #2 | write nothing to disk, small | sealed #2 |
| K-04 | Hook timeouts were written as 5000 and 2000 in a field read as seconds. | [CHANGELOG.md:34](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L34); now 10, 5 and 10 ([hooks/hooks.json:11](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/hooks.json#L11)) | fracture | release PR #2 | timeouts in seconds, small | sealed #2 |
| K-05 | The PreToolUse hook printed advice before an edit to a secret file instead of asking for confirmation. | [CHANGELOG.md:28](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L28); [pre-tool-use.sh:63](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/pre-tool-use.sh#L63) now returns `permissionDecision: "ask"`, checked at the pin | fracture | release PR #2 | ask for `.env`, key and credentials files, small | sealed #2 |
| K-06 | The private key check never ran: its pattern starts with `-`, so grep read it as an option. | [CHANGELOG.md:35](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L35); the matcher now passes `--` ([post-tool-use.sh:89](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L89)); at the pin a file holding `-----BEGIN RSA PRIVATE KEY-----` gets `[CRITICAL] Secrets: private key embedded in the file` | break | release PR #2 | `grep -qE -- "$1"`, small | sealed #2 |
| K-07 | The scan raised false findings: `Math.random()` on every use, any `.update(...).digest()` chain (SHA-256 included) as MD5, `TLSv1_2` as TLS 1.0, and Python-only or PHP-only deserialization checks on other languages. | [CHANGELOG.md:35](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L35); [post-tool-use.sh:200](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L200), [:208](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L208), [:214](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L214), [:305](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L305); at the pin `minVersion: "TLSv1_2"`, `createHash("sha256")...digest()`, a bare `Math.random()` and a JavaScript `unserialize` each produce no finding | fracture | release PR #2 | tighter patterns, gated by file extension, small | sealed #2 |
| K-08 | Lowercase `aes-128-ecb` was missed. | [CHANGELOG.md:35](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/CHANGELOG.md#L35); case-insensitive match at [post-tool-use.sh:217](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L217); at the pin `createCipheriv("aes-128-ecb", ...)` gets `[HIGH] Crypto: ECB cipher mode` | fracture | release PR #2 | `hasi`, small | sealed #2 |
| K-09 | Under Grok the PreToolUse and PostToolUse scripts exit before doing anything. They require `.tool_name` to be `Edit`, `Write` or `MultiEdit`. Grok does add snake_case aliases (`tool_name`, `tool_input`) next to its camelCase keys ([event.rs:377](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-hooks/src/event.rs#L377)), but the value is Grok's own tool name: an edit arrives as `search_replace`, `write` or `hashline_edit` ([claude_alias.rs:47](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-tools/src/types/claude_alias.rs#L47) to :52). Grok maps Claude names only in `matcher` patterns, so the hooks fire and then exit. *Inferred* for the file path: the key Grok uses inside `tool_input` for an edit was not confirmed. | [pre-tool-use.sh:27](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/pre-tool-use.sh#L27) to :33, [post-tool-use.sh:39](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/post-tool-use.sh#L39) to :47; fed the documented envelope, both scripts exit 0 with no output where Claude Code's input gets `ask` and a CRITICAL finding; the snake_case alias table is also in the grok 1.0.44 binary's strings | break | held by HermeticOrmus ([PR #8](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/pull/8), its ledger K-22, graded hairline there) | read both envelopes and Grok's tool names, then record one Grok session, small ([draft](../seals/libre-secops-hooks/K-09.md)) | drafted |
| K-10 | *Inferred*: the session-start profile never reaches the model in Grok. The script prints a plain line, and the same Grok hooks guide says "For events like `SessionStart` or `Notification`, stdout is ignored" (line 505). | [session-start.sh:209](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/hooks/session-start.sh#L209) | fracture | new | say so in the plugin README and give the manual command, small ([draft](../seals/libre-secops-hooks/K-10.md)) | sealed (card, run at the pin); upstream drafted |
| K-11 | The hooks have not run inside a Grok session, so their runtime there is unverified; everything above ran outside a session. | the assay rows above; Grok documents `hookSpecificOutput.permissionDecision` (guide line 296) but no session ran | hairline | held by HermeticOrmus ([PR #8](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/pull/8), ledger K-22) | one Grok session with a logging hook, small | open |
| K-12 | The install and upgrade steps are Claude Code only: the plugin README gives `/plugin` and `claude plugin` lines and "Restart Claude Code", and the repository README never mentions Grok. | [plugin README.md:7](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/plugins/libre-secops-hooks/README.md#L7) to :12, [README.md:124](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/blob/a874d37f7d9b5ea6c27f4fc5185dd2dc4fdc83f7/README.md#L124) | hairline | repository README held by HermeticOrmus ([PR #8](https://github.com/HermeticOrmus/LibreSecOps-Claude-Code/pull/8)); the plugin README is not in that PR | add a Grok install line to the plugin README, small ([draft](../seals/libre-secops-hooks/K-10.md)) | drafted |

## Workarounds

K-10, run at the pin: Grok drops the SessionStart line, so read it yourself. From a clone of the repository at the pin, in your project's root:

```bash
bash /path/to/LibreSecOps-Claude-Code/plugins/libre-secops-hooks/hooks/session-start.sh </dev/null
```

With no input the script profiles the current folder. Recorded result in a sample Express project: exit 0 and one line, `LibreSecOps: JavaScript/TypeScript (Express). Gaps: no lockfile, no security headers setup, no security tooling configured. Relevant plugins: ...`.

K-09 has no workaround a Grok user can apply without editing the scripts, which is why the entry waits.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
