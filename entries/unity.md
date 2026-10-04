# unity

Unity's official plugin for coding agents: 33 skills for Unity 6 game work (UI Toolkit and uGUI, 2D, tilemaps, shaders, localization, multiplayer, in-app purchases, LevelPlay ads, live-game services) and a skill that drives the Unity Editor through the Unity CLI.

| | |
|---|---|
| Level | **watch** |
| Domain | Game development |
| Author | [Unity Technologies](https://unity.com) |
| License | [named in LICENSE.md](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/LICENSE.md) as the Unity Companion License; the file does not contain the terms (GitHub reports NOASSERTION) |
| Source | [Unity-Technologies/unity-agent-plugin](https://github.com/Unity-Technologies/unity-agent-plugin/tree/de668bfd2e4ece0613c331e653c8c48b03e7238d) |
| Pinned SHA | `de668bfd2e4ece0613c331e653c8c48b03e7238d` (committed 2026-10-01, version 0.1.8-beta) |
| Components at the pin | skills 33, agents 0, commands 0, hook events 0, MCP servers 0 (folder count; `grok inspect` was not run) |
| Assayed | 2026-10-04; the Grok CLI was not installed, so the gates were not run |

## Who it is for

People building a Unity 6 game from an agent: a new project, a settings screen, pixel-perfect 2D, tilemaps, IAP, ads, multiplayer, or a pass over an existing scene through the Unity CLI.

## Install

Not in the marketplace yet. The README's Grok line is below, for reference only. It names no commit, and it was not run for this assay.

```bash
grok plugin install Unity-Technologies/unity-agent-plugin --trust
```

## Why it waits

The plugin is a skills folder with a manifest Grok can read (`.claude-plugin/plugin.json`, name `unity`, version `0.1.8-beta`), and the folder holds no hooks and no MCP server. It waits on the license, and on gates that were not run.

`LICENSE.md` at the pin is five lines. It does not contain a grant. It says the plugin is "Licensed under the Unity Companion License for Unity-dependent projects" and points at `https://unity3d.com/legal/licenses/unity_companion_license`. The manifest's license field is `LicenseRef-Unity-Companion-License`. `gh api repos/Unity-Technologies/unity-agent-plugin/license` reports `spdx_id` `NOASSERTION` and `path` `LICENSE.md`.

The page at that URL, read on 2026-10-04, is Unity Companion License v1.4 (dated 10.29.2024). Section 1 allows reproducing and distributing the work only "in connection with the authoring and/or distribution of applications, software, or other content under a valid Unity content authoring and rendering engine software license," and then says "No other exercise of the license granted herein is permitted." Section 7 says Unity may modify the license and that later use follows the updated text. The pin does not freeze those terms: they live at a URL. This marketplace would offer the plugin to any Grok user, with no check for an engine license, which is not clearly inside that grant. The entry stays out until the terms are in the repository at a commit and clearly allow that offer, or Unity says a catalog pointer is companion use. A workaround in this card cannot relicense Unity's code.

The Grok gates were not run. `command -v grok` found nothing, and `~/.grok/bin/grok` is not on this machine, so there is no clean-home install, validate, details, or inspect result to record. The rubric does not admit an entry whose gates were not run.

## What it can execute

- **Hooks:** none. No `hooks/hooks.json`.
- **Scripts:** none that install with the plugin and run on their own. `scripts/check-skill-frontmatter.mjs` is the repository's own frontmatter check. Skills ship C# and Markdown the agent is told to copy into a Unity project, and `skills/optimize-web/resources/toktx-examples.sh` is a list of `toktx` examples, not a hook. The `unity-cli` skill tells the agent to run the Unity CLI, and to install it when `which unity` fails.
- **MCP servers:** none in the plugin. No `.mcp.json`, and the manifest has no `mcpServers`. The `unity-cli` skill documents `unity mcp` and `unity mcp configure` for 16 other clients (K-03).
- **Network:** when the agent follows `unity-cli`, an install is `curl -fsSL https://unity.com/install.sh | bash` or, on Windows, `irm https://unity.com/install.ps1 | iex` ([SKILL.md:67](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L67), [line 72](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L72)). The skill's security note says that script downloads the binary from `public-cdn.cloud.unity3d.com` and checks a SHA-256 from the same origin ([SECURITY.md:56](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SECURITY.md#L56)). A local-git recipe downloads `https://raw.githubusercontent.com/github/gitignore/main/Unity.gitignore` ([SKILL.md:450](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L450)). The same skill says the CLI reports anonymous crashes to Sentry unless `UNITY_NO_CRASH_REPORT` is set, and that every `unity` run sends one anonymous `cli telemetry` usage ping even when analytics are opted out, unless `UNITY_NO_CLI_INVOKED_TELEMETRY=1` ([SKILL.md:627](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L627), [diagnostics-maintenance.md:298](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/references/diagnostics-maintenance.md#L298)). Those calls were not executed here.
- **Disclosed in its README:** partly. The README says the agent can install the CLI and run C# in the open Editor ([README.md:94](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/README.md#L94), [line 124](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/README.md#L124)). It does not name the install URL, Sentry, or the telemetry ping (K-02).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pin verified; clean home not run | `git ls-remote` HEAD and `origin/main` are `de668bfd2e4ece0613c331e653c8c48b03e7238d` (committed 2026-10-01). `command -v grok` printed nothing; `~/.grok/bin/grok` is absent |
| Gate: validate | not run | no `grok` binary on this machine |
| Gate: install at the pin | not run | same |
| Gate: details | not run | same |
| Gate: inspect | not run | same. `python3 scripts/count_components.py` on the pin prints `skills=33 agents=0 commands=0 hooks=0 mcp=0`. There are 33 `SKILL.md` files, no `hooks/hooks.json`, no `.mcp.json` |
| Reading: promises against components | not checked under Grok | the README describes skills and the CLI, not hooks or a bundled MCP server. Grok's manifest order would read `.claude-plugin/plugin.json` (no root `plugin.json`, no `.grok-plugin/`). That was not confirmed with `grok plugin validate` |
| Reading: license | holds the entry out | `LICENSE.md` is a pointer, not the grant; GitHub reports `NOASSERTION`; the terms at the URL do not clearly allow this marketplace to offer the plugin (K-01) |
| Reading: what it can execute | pass, with a README gap | no hooks and no bundled MCP server; the CLI install, crash reports and telemetry ping are in the `unity-cli` skill and not in the plugin README (K-02) |
| Reading: maintenance | last push 2026-10-02, 0 open issues, 2 open pull requests, 379 stars | GitHub API, 2026-10-04. `pushed_at` is `2026-10-02T14:45:11Z`. The open list is pull requests #79 and #51; no issue is open |
| Hands | not run | the Grok CLI is not installed, and a session would also download and run the Unity CLI |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `LICENSE.md` does not contain the license. It names the Unity Companion License and a URL. The text at that URL (v1.4, read 2026-10-04) allows reproduction and distribution only in connection with content authored under a Unity engine license, and says no other exercise is permitted. The terms can change without a new commit. GitHub reports `NOASSERTION`. | [LICENSE.md:1](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/LICENSE.md#L1), [.claude-plugin/plugin.json:10](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/.claude-plugin/plugin.json#L10); `gh api repos/Unity-Technologies/unity-agent-plugin/license` returns `spdx_id` `NOASSERTION`, `path` `LICENSE.md`; [Companion License v1.4 §1 and §7](https://unity3d.com/legal/licenses/unity_companion_license), read 2026-10-04 | fracture | new (no issue mentions the license) | put the terms in the repository, and say whether a catalog may offer the plugin, small | drafted ([seal](../seals/unity/K-01.md)) |
| K-02 | The README says the agent can install the Unity CLI and does not say that the install is an unpinned script from `unity.com`, that crash reports go to Sentry unless `UNITY_NO_CRASH_REPORT` is set, or that every `unity` run sends an anonymous telemetry ping unless `UNITY_NO_CLI_INVOKED_TELEMETRY=1`. The skill states all three. | [README.md:124](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/README.md#L124), [SKILL.md:67](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L67), [line 627](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/SKILL.md#L627), [diagnostics-maintenance.md:298](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/references/diagnostics-maintenance.md#L298) | hairline | new | name the install URL, Sentry and the ping, with the opt-outs, in the README, small | drafted ([seal](../seals/unity/K-02.md)) |
| K-03 | `unity mcp configure` lists 16 clients and not Grok, while `unity skill install` includes `grok`. The README's Grok line installs the moving default branch, not a commit. | [integration-advanced.md:86](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/references/integration-advanced.md#L86), [line 156](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/skills/unity-cli/references/integration-advanced.md#L156), [README.md:45](https://github.com/Unity-Technologies/unity-agent-plugin/blob/de668bfd2e4ece0613c331e653c8c48b03e7238d/README.md#L45). The install line was not run | hairline | new | add `grok` to `unity mcp configure`, and pin the README's Grok install, small | drafted ([seal](../seals/unity/K-02.md)) |

## Workarounds

None admits the entry. The license is Unity's to state.

Someone who already accepts the Unity Companion License, and who holds a Unity engine license, can install this pin with `grok plugin install https://github.com/Unity-Technologies/unity-agent-plugin.git@de668bfd2e4ece0613c331e653c8c48b03e7238d --trust`. That command was not run.

The skill's own opt-outs for the CLI, not run here, are `UNITY_NO_CRASH_REPORT=1` and `UNITY_NO_CLI_INVOKED_TELEMETRY=1` in the environment of the shell that runs `unity`.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
