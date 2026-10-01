# railway

Railway's plugin for Grok Build: one route-first skill, `use-railway`, that drives the Railway CLI, Railway's hosted MCP server and Railway's GraphQL API for projects, services, databases, buckets, deploys, variables, domains, logs, metrics, tracing and feature flags, plus a hook meant to auto-approve Railway commands.

| | |
|---|---|
| Level | **assayed** |
| Domain | Cloud platform |
| Author | [Railway](https://railway.com) |
| License | [MIT](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/LICENSE) |
| Source | [railwayapp/railway-skills, plugins/railway](https://github.com/railwayapp/railway-skills/tree/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway) (`plugins/railway`) |
| Pinned SHA | `4db2ee90245d61be0ffea28280164373ac3f96c0` (committed 2026-09-29, version 1.6.1) |
| Components at the pin | skills 1, agents 0, commands 0, hook events 1, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers who deploy and run apps on Railway and want Grok to read deploy state, logs and metrics, fix a failed build, add a database or a bucket, or change variables and domains through the CLI or the hosted MCP server.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install railway@liquid-gold-grok
```

Then read the Workarounds below: one line in `AGENTS.md` keeps the skill to Railway requests (K-01), and four permission rules give Grok users the read-only half of what the hook promises (K-02).

## Why it is assayed

Every gate passed at the pin, the skill and the hosted MCP server load, and the README discloses both. The skill is careful where it counts: the scripts that change a Postgres server are user-only ("Do NOT execute these with Bash", [SKILL.md:324](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L324)), destructive actions need confirmed intent ([SKILL.md:318](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L318)), a deploy is never reported as done without observing SUCCESS ([SKILL.md:320](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L320)), and the API helper keeps the token out of the process list ([railway-api.sh:51](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/scripts/railway-api.sh#L51)).

Two fractures keep it from gold. First, the skill claims requests that never mention Railway: "Use this skill whenever the user mentions Railway, feature flags, flag rollout, targeting rules, signing up, creating an account, registering, logging in, deployments, services, environments, ... MCP, or infrastructure operations, even if they don't say \"Railway\" explicitly." For a sign-up request it tells the agent to run `railway up`, which uploads and deploys the current directory, and to "Use it even when the user only said \"sign me up\"" (K-01). Second, the `PreToolUse` hook that auto-approves Railway commands does nothing in Grok: the script checks for Claude's tool name `Bash` while Grok sends `run_terminal_command`, and Grok treats a hook's `allow` as "not blocked", never as approval (K-02). In Grok's default mode both fall back to a permission prompt, which is the safe direction. Each fracture has a workaround below and a seal draft; the workarounds were not run in a Grok session, so the entry is assayed.

## What it can execute

- **Hooks:** `PreToolUse` with matcher `Bash`, which Grok maps to `run_terminal_command`: [auto-approve-api.sh](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/hooks/auto-approve-api.sh) reads the event with `jq` and prints an `allow` decision for one simple `railway ...` command or the bundled `railway-api.sh`. Under Grok it exits 0 with no output (K-02). Under Claude Code the same script allows any single `railway` command, `railway down -y` included (checked outside a session); merged pull requests [#68](https://github.com/railwayapp/railway-skills/pull/68), [#72](https://github.com/railwayapp/railway-skills/pull/72) and [#73](https://github.com/railwayapp/railway-skills/pull/73) already stopped chained commands and look-alike helpers, and the open [#76](https://github.com/railwayapp/railway-skills/pull/76) declines subcommands that run another command.
- **Scripts:** `railway-api.sh` posts GraphQL to `https://backboard.railway.com/graphql/v2` with the token from `~/.railway/config.json`, passed through a pipe rather than argv. Seven Python files (four analyzers for Postgres, MySQL, Redis and MongoDB, a shared helper, and two Postgres tools) work through `railway ssh`; the two Postgres tools change settings or extensions and are marked user-only.
- **MCP servers:** `railway`, type `http`, at `https://mcp.railway.com`, declared by [.grok-plugin/plugin.json:12](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/.grok-plugin/plugin.json#L12) in `.grok-plugin/mcp.json`; Railway OAuth.
- **Network:** the hosted MCP server; the Railway CLI and API, with each CLI call tagged `RAILWAY_CALLER=skill:use-railway@1.6.1` and a per-request `RAILWAY_AGENT_SESSION`, prefixes the skill describes as telemetry ([SKILL.md:131](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L131)) and each helper call carrying `X-Railway-Skill-*` headers (K-04); `curl -fsSL agents.railway.com | sh` when the CLI is missing; `railway up` uploads the working directory.
- **Skill permissions:** the frontmatter lists `Bash(railway:*)`, `Bash(npx:*)`, `Bash(curl:*)`, `Bash(python3:*)` and three more ([SKILL.md:20](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L20)). Grok documents `allowed-tools` as "Tools the skill uses" ([08-skills.md:108](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/08-skills.md#L108)); this assay found no code in Grok that turns it into a grant (*inferred*).
- **Disclosed in its README:** partly. The README names the skill and the hosted MCP server ([README.md:5](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/README.md#L5)) and has a Grok Build section ([README.md:117](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/README.md#L117)); it does not say what the hook does or that calls are tagged for telemetry.

## Assay

Grok's own behavior is cited from Grok's documentation and source at [xai-org/grok-build@2bdd1d6](https://github.com/xai-org/grok-build/tree/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8), not from an observed session.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `4db2ee9`, the head of `main` and the same SHA and path xAI's catalog pins; clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `name: railway`, `version: 1.6.1`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), hooks, MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/railwayapp/railway-skills.git@4db2ee9...#plugins/railway --trust`: `Installed 1 plugin(s) from ...: railway` |
| Gate: details | pass | `railway v1.6.1 (subdir: plugins/railway)` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skill `use-railway`, the hook file `plugins/railway/hooks/hooks.json` (one event, `PreToolUse`), MCP server `railway` (`http`, `https://mcp.railway.com`); the folder holds the same counts |
| Reading: promises against components | fracture | the skill claims requests outside Railway (K-01); the hook's promise does not hold in Grok (K-02) |
| Reading: license | pass | MIT, `LICENSE` at the repository root (Copyright (c) 2026 Railway Corporation), `"license": "MIT"` in the Grok manifest, a License section in the README |
| Reading: what it can execute | partial | hosted MCP and the CLI, disclosed; the hook's behavior and the telemetry tags are not in the README (K-02, K-04) |
| Reading: maintenance | last push 2026-10-01, 22 open issues and 9 open pull requests, 327 stars | GitHub API, 2026-10-01 |
| Hook script, outside a session | inert under Grok input | Grok-shaped `PreToolUse` input (`toolName`/`tool_name` `run_terminal_command`, command `railway status --json`): exit 0, no output. Claude-shaped input (`tool_name` `Bash`): `"permissionDecision": "allow"`, also for `railway down -y`. The repository's own `auto-approve-api.test.sh`: `32 passed, 0 failed` |
| Workaround K-02, at the pin | loads | the four rules below in a clean `GROK_HOME/config.toml`: `grok inspect` reports `4 loaded, 0 skipped`. Not exercised in a session |
| xAI catalog install | pass | clean home, `grok plugin install railway@xai-official --trust`: `Installed 1 plugin(s) from xAI Official: railway` at `4db2ee9` |
| Hands | not run | a Grok session costs model time, and a real run would act on a Railway account; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The skill description claims requests that do not mention Railway ("feature flags", "signing up", "logging in", "deployments", "MCP", "even if they don't say \"Railway\" explicitly"), and for a sign-up request it tells the agent to run `railway up`, which uploads and deploys the current directory, "even when the user only said \"sign me up\"". | [SKILL.md:10](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L10), [line 15](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L15), [line 91](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L91), [line 187](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L187) ("the agent invocation is treated as consent") | fracture | new (no issue on trigger scope or sign-up deploys) | trigger on Railway requests only, and ask before deploying on a sign-up request, small | drafted ([seal](../seals/railway/K-01.md)) |
| K-02 | The `PreToolUse` hook never auto-approves in Grok: the script exits unless `tool_name` is `Bash`, and Grok sends its own name `run_terminal_command`; even a matching `allow` would only mean "not blocked" in Grok. | [auto-approve-api.sh:13](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/hooks/auto-approve-api.sh#L13), [line 17](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/hooks/auto-approve-api.sh#L17); Grok: [event.rs:383](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-hooks/src/event.rs#L383) (`tool_name` carries Grok's name), [10-hooks.md:277](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L277), [10-hooks.md:296](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L296); the script run in the assay table | fracture | new | say in the README's Grok section that the hook has no effect there and point to Grok permission rules, small | drafted ([seal](../seals/railway/K-02.md)) |
| K-03 | Grok cuts the skill description at 1,024 characters, so it ends mid-word ("which creates new accou"); the folded description is 1,040 characters. | `grok inspect --json`: description length 1024; [SKILL.md:3](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L3) | hairline | filed #96 upstream, open | shorten the description, small | open |
| K-04 | The README does not say that the skill tags every Railway CLI call with the skill version and a session id for telemetry, or that the helper sends `X-Railway-Skill-Id`, `X-Railway-Skill-Version` and `X-Railway-Agent-Session` headers; the helper's default version tag is `1.2.3` while the skill is `1.6.1`. | [SKILL.md:131](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L131), [railway-api.sh:8](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/scripts/railway-api.sh#L8), [railway-api.sh:46](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/scripts/railway-api.sh#L46) | hairline | new | one README line on the tags; take the version from the skill, small | drafted ([seal](../seals/railway/K-02.md), same draft) |
| K-05 | The skill's freshness check tells the agent to run `railway skills update` or `railway setup agent -y` and ask the user to restart, but the listed targets are Claude Code, Cursor, Codex, OpenCode, Copilot and Factory Droid; a Grok install updates through its marketplace, so from a Grok session the remedy writes to other tools. *Inferred*: the Railway CLI was not run. | [SKILL.md:124](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L124), [line 125](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L125), [line 242](https://github.com/railwayapp/railway-skills/blob/4db2ee90245d61be0ffea28280164373ac3f96c0/plugins/railway/skills/use-railway/SKILL.md#L242) | hairline | new | skip the freshness remedy under Grok and name `grok plugin update railway`, small | open |

## Workarounds

- **K-01:** add one line to the project's `AGENTS.md`: `Use the use-railway skill only when I mention Railway, and never run railway up unless I ask for a deploy.` In Grok's default permission mode `railway up` is not on the read-only list, so Grok asks before it runs ([22-permissions-and-safety.md:154](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md#L154)); decline it when you only asked for an account, and ask for `railway login`. The `AGENTS.md` line was not run in a Grok session.
- **K-02:** give Grok the read-only half of the promise with permission rules in `~/.grok/config.toml` (or `.grok/config.toml` for one project). Grok strips leading environment assignments such as `RAILWAY_CALLER=...` before it matches a rule ([22-permissions-and-safety.md:336](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md#L336)). Leave `railway up`, `railway down`, `railway run` and deletes to the prompt.

  ```toml
  [permission]
  allow = [
    "Bash(railway status *)",
    "Bash(railway whoami *)",
    "Bash(railway logs *)",
    "Bash(railway deployment list *)",
  ]
  ```

  In a clean Grok home these rules load (`4 loaded, 0 skipped`); they were not exercised in a session.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
