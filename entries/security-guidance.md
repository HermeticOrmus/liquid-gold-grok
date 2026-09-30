# security-guidance

Security review for agent-written code in three layers: regex warnings on edits for about 25 dangerous patterns (`yaml.load`, `pickle.load`, raw `innerHTML`, hardcoded secrets), an LLM review of the diff when the agent stops, and an SDK-driven reviewer on `git commit` that reads related files to trace data flow.

| | |
|---|---|
| Level | **watch** |
| Domain | Security |
| Author | David Dworken, [Anthropic](https://github.com/anthropics) |
| License | [Apache-2.0](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/LICENSE) |
| Source | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance) |
| Pinned SHA | `ab024cdcfa7ca80be204acd4907656ba5a968589` (committed 2026-09-30, version 2.0.8) |
| Components at the pin | skills 0, agents 0, commands 0, hook events 5, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Teams that want a security reviewer riding along with the agent, and who already have an Anthropic API key for the LLM layers.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/anthropics/claude-plugins-official.git@ab024cdcfa7ca80be204acd4907656ba5a968589#plugins/security-guidance --trust
```

## Why it is watch

It installs clean, and the pattern layer works: fed a `Write` of `yaml.load(data)`, the hook returned a `hookSpecificOutput` warning. It waits on one break. The first ordinary edit of a session, with no API key and even with `ENABLE_CODE_SECURITY_REVIEW=0` set, started a detached `pip install claude-agent-sdk` from PyPI, unpinned, that built a 302 MB virtual environment (3,680 files). The README describes the data sent to the model endpoint but never says the plugin downloads and installs a package. Upstream already tracks the SessionStart side of this, that the build ignores missing credentials and the kill switch ([#5331](https://github.com/anthropics/claude-plugins-official/issues/5331)); the undisclosed, unpinned install and the second trigger on `PostToolUse` are new, and a seal is drafted. Two further fractures are Grok-specific: the LLM layers need Anthropic credentials a Grok session does not provide, and they deliver findings through `asyncRewake`, a hook field grok 1.0.44 does not reference.

## What it can execute

- **Hooks:** five events, all running `hooks/sg-python.sh` with a Python script ([hooks/hooks.json](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/hooks.json)). `SessionStart` runs `ensure_agent_sdk.py`. `UserPromptSubmit` captures a git baseline. `PostToolUse` on `Edit|Write|MultiEdit|NotebookEdit` runs the pattern check; `PostToolUse` on `Bash` runs seven entries gated by `if` conditions on `git commit`, `git push`, `gt create`, `gt modify` and `gt submit`. `Stop` and `SubagentStop` run the diff review.
- **Scripts:** 8,098 lines of Python in `hooks/`, including a `pip install claude-agent-sdk` into a venv under `~/.claude/security/` ([ensure_agent_sdk.py:594](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/ensure_agent_sdk.py#L594)), spawned detached from `PostToolUse` as well ([security_reminder_hook.py:2296](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/security_reminder_hook.py#L2296)).
- **MCP servers:** none.
- **Network:** PyPI for the SDK install (undisclosed); `api.anthropic.com`, or `ANTHROPIC_BASE_URL`, or a configured cloud provider, for the diff and commit reviews ([llm.py:167](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/llm.py#L167)), sending changed paths, diff hunks and file contents.
- **Disclosed in its README:** partly. The model calls and what they send are disclosed under "Privacy and data handling" ([README.md:85](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/README.md#L85)), as is the debug log in `~/.claude/security/log.txt`. The package install is not. The hook output also carries a `metrics` object meant for Claude Code's plugin telemetry ([ensure_agent_sdk.py:67](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/ensure_agent_sdk.py#L67)), which the README does not mention.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `ab024cd`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `grok plugin validate`: `version: 2.0.8`, `components: 0 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/anthropics/claude-plugins-official.git@ab024cd...#plugins/security-guidance --trust`: `Installed 1 plugin(s) ... security-guidance` |
| Gate: details | pass | `security-guidance v2.0.8 (subdir: plugins/security-guidance)` at commit `ab024cd`; `grok inspect` lists one hooks file from this plugin |
| Reading: promises against components | partial | the pattern layer works outside a session; the two LLM layers depend on credentials and a hook field Grok lacks (K-03) |
| Reading: license | pass | Apache-2.0 [LICENSE](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/LICENSE) in the plugin folder |
| Reading: what it can execute | fail | undisclosed, unpinned package install from PyPI (K-01) |
| Reading: maintenance | last push 2026-09-30, 1,044 open issues, 37,242 stars (whole marketplace repository); 58 open issues carry `security-guidance` in the title | GitHub API and issue search, 2026-09-30 |
| Hook script, outside a session | pass for `Write`, silent for `StrReplace` | `sg-python.sh security_reminder_hook.py` with `CLAUDE_PLUGIN_ROOT` and `GROK_PLUGIN_ROOT` set, no API key, `ENABLE_CODE_SECURITY_REVIEW=0`, and a scratch state dir: a `PostToolUse` `Write` of `yaml.load(data)` exited 0 with a `yaml.load()` warning in `hookSpecificOutput.additionalContext`; the same edit named `StrReplace` exited 0 with no output (K-04). The same run started the SDK install (K-01) |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The plugin downloads and installs `claude-agent-sdk` from PyPI, unpinned, into a venv under the Claude config dir, and the README never says so. One `PostToolUse` call with no credentials and `ENABLE_CODE_SECURITY_REVIEW=0` spawned it detached and built 302 MB (claude-agent-sdk 0.2.163, mcp 2.2.0). | [ensure_agent_sdk.py:594](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/ensure_agent_sdk.py#L594), [security_reminder_hook.py:2289](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/security_reminder_hook.py#L2289), [README.md](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/README.md) (no mention); assay run above | break | new; the SessionStart gating is held by anthropics ([#5331](https://github.com/anthropics/claude-plugins-official/issues/5331)) | disclose the install in the README, pin the SDK version, gate the PostToolUse trigger like SessionStart, small | drafted ([seal](../seals/security-guidance/K-01.md)) |
| K-02 | The SDK build runs whether or not a review can ever use it: no credentials check, and the kill switch does not reach the SessionStart installer. | [#5331](https://github.com/anthropics/claude-plugins-official/issues/5331); [llm.py:124](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/llm.py#L124) | fracture | held by anthropics ([#5331](https://github.com/anthropics/claude-plugins-official/issues/5331)) | check credentials and the review toggles before building, small | open |
| K-03 | In Grok the two LLM layers are unlikely to work: they run only with `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` or a cloud provider flag, which a Grok session does not set, and they hand findings back through `asyncRewake`, `rewakeMessage` and `asyncTimeout`; none of those three strings appears in the grok 1.0.44 binary, which does contain `hookSpecificOutput` and `additionalContext`. *Inferred*: not observed in a session. | [llm.py:124](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/llm.py#L124), [hooks/hooks.json:41](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/hooks.json#L41); `strings` of the grok binary | fracture (*inferred*) | related: [#5067](https://github.com/anthropics/claude-plugins-official/issues/5067) (reviews silently skipped without credentials), [#3173](https://github.com/anthropics/claude-plugins-official/issues/3173) (the same hooks in Codex) | a Grok hook adapter upstream, large; see Workarounds | open |
| K-04 | The pattern check runs only for tool names `Edit`, `Write`, `MultiEdit` and `NotebookEdit`; an edit reported under another name gets no warning. Whether Grok's edit tools use these names is unverified. | [security_reminder_hook.py:2346](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/security_reminder_hook.py#L2346); the `StrReplace` run above | fracture (*inferred*) | new | accept the host's edit tool names, or read `file_path` and content from any tool input, small | drafted ([seal](../seals/security-guidance/K-04.md)) |
| K-05 | Hook runtime inside a Grok session is unverified: the `if` conditions, the five events and the `metrics` output were checked only outside a session. | [hooks/hooks.json](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/hooks.json) | hairline | new | run one Grok session and record which hooks fire, small | open |
| K-06 | The README is written for Claude Code only: the install line, "Claude Code CLI v2.1.144 or later", and state and logs under `~/.claude/security/`, which is where a Grok user's copy writes too. | [README.md:13](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/README.md#L13), [README.md:21](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/README.md#L21), [README.md:94](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/README.md#L94) | hairline | new | name the supported agents, small | open |
| K-07 | Every hook prints a `metrics` object that Claude Code forwards to its plugin telemetry, as the code comments describe; the README's privacy section does not mention it. What Grok does with the field is unverified. | [ensure_agent_sdk.py:67](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/ensure_agent_sdk.py#L67), [security_reminder_hook.py:276](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/security-guidance/hooks/security_reminder_hook.py#L276) | hairline | new | one README line on the metrics and how to turn them off, small | drafted ([seal](../seals/security-guidance/K-01.md), same draft) |

## Workarounds

These do not admit the entry; they are for anyone who installs it from upstream anyway.

- **K-01 and K-02:** install the SDK yourself at a version you choose before the first session (`python3 -m pip install claude-agent-sdk==<version>`, into the Python that `sg-python.sh` picks), so the installer finds it importable and does nothing. `SECURITY_GUIDANCE_DISABLE=1` stops every layer and the `PostToolUse` build, but not the `SessionStart` build ([#5331](https://github.com/anthropics/claude-plugins-official/issues/5331)); `ENABLE_CODE_SECURITY_REVIEW=0` stops neither.
- **K-03:** export `ANTHROPIC_API_KEY` in the shell that starts Grok if you want the LLM layers to try; whether their findings reach the session in Grok is unverified.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
