# axiom

Axiom's plugin for querying production logs, metrics and traces from Grok: seven skills for incident investigation, Splunk-to-APL translation, dashboards, monitors and notifiers, cost control and metrics charts, plus Axiom's hosted MCP server.

| | |
|---|---|
| Level | **gold** |
| Domain | Observability |
| Author | [Axiom](https://axiom.co) |
| License | [MIT](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/LICENSE) |
| Source | [axiomhq/skills](https://github.com/axiomhq/skills/tree/8f26649612042662c1ea8318ff27a49a7c24531f) |
| Pinned SHA | `8f26649612042662c1ea8318ff27a49a7c24531f` (committed 2026-10-02, version 1.1.0). xAI's catalog pins `0e98ebaeec76a70c8fda9a7737605800c2f1245d` (committed 2026-06-26, Grok manifest version 1.0.0). Forty commits sit between them, including the metrics-chart skill and the removal of writing-evals. This assay covers 1.1.0 only. |
| Components at the pin | skills 7, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-04 with grok 1.0.46 |

## Who it is for

People who keep logs, metrics or traces in Axiom and want Grok to query them, build a dashboard, or wire a monitor while they work on the code. The MCP server signs in with OAuth. The skills' scripts use a separate API token in `~/.axiom.toml`, and the SRE skill uses `~/.config/axiom-sre/config.toml`.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install axiom@liquid-gold-grok
```

Then open `/mcps`, select `axiom` and press `i` to sign in. Script credentials are separate from that sign-in; the root README says so.

## Why it is gold

Every gate passed at the pin. Grok loads all 7 skills and the hosted MCP server. `grok mcp doctor`, from an empty folder, starts that server and stops on Axiom's OAuth challenge, which is the sign-in the README describes. The license file at the pin is the MIT License, copyright 2026 Axiom, Inc., and the Grok manifest states MIT.

What the plugin runs is in the root README: the MCP server, API tokens for Axiom and for optional Grafana, Pyroscope, Sentry, Slack and Kubernetes, dashboard and alert updates, and SRE memory that stays local unless you point it at a git repository. The skills' approval lines sit next to the dangerous steps. Delete scripts for monitors, notifiers and dashboards prompt before they send DELETE. The SRE skill tells the agent not to put a token in the command it types, and to pass secrets through `scripts/curl-auth`.

What is left open are hairlines. There is no Grok install section, and adding the GitHub repository as a marketplace does not list a plugin named `axiom` (K-01). The alerting skill names a project-root `.axiom.toml` that the script never reads (K-02). `scripts/init` says it makes no network calls, then runs `git pull` when an org memory repo is configured (K-03). Three API-client headers still describe an older layout (K-04). `curl-auth` keeps the token out of the command the agent types, and still places it in `curl`'s arguments (K-05).

## What it can execute

- **Hooks:** none.
- **Scripts:** no hooks, and the agent is told to run the shell scripts under each skill. `spl-to-apl` ships none. `metrics-chart` runs `python3 scripts/metrics_chart.py` and uses gnuplot only when it is already installed; that script makes no network call. The others use `curl` and `jq`:
  - `axiom-alerting` creates, updates and deletes monitors and notifiers through `scripts/axiom-api` ([SKILL.md:47](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/axiom-alerting/SKILL.md#L47)). `monitor-delete` and `notifier-delete` prompt first.
  - `building-dashboards` creates and updates dashboards, and `dashboard-delete` prompts. Its `scripts/metrics/` tree queries MetricsDB.
  - `query-metrics` lists datasets and runs MPL. `scripts/metrics-spec` takes no credentials.
  - `controlling-costs` tells the agent to load `axiom-sre` and `building-dashboards`, then deploys a cost dashboard and monitors.
  - `axiom-sre` (folder `skills/sre`) runs `scripts/init` on activation, discovery scripts, `axiom-query`, and `curl-auth` for Axiom, Grafana, Pyroscope, Sentry and Slack. `discover-k8s` runs `kubectl` when it is on `PATH`.
- **MCP servers:** `axiom`, HTTP, at `https://mcp.axiom.co/mcp` ([.mcp.json:5](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/.mcp.json#L5)). Nothing is installed locally. Sign-in is OAuth against `https://authorization.axiom.co`. The Grok manifest does not set `mcpServers`; Grok still loaded `.mcp.json` because that field is absent. The Claude manifest points at the same file.
- **Network:** the MCP host, and `https://authorization.axiom.co` for OAuth. Script calls go to the `url` in the user's config (the README's example is `https://api.axiom.co`, v1 for queries and v2 for monitors, notifiers and dashboards). `metrics-spec` sends an unauthenticated `OPTIONS` to `https://us-east-1.aws.edge.axiom.co/v1/query/_mpl` ([metrics-spec:11](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/query-metrics/scripts/metrics-spec#L11)); metrics queries can be routed to `https://<region>.edge.axiom.co`. SRE can also call the Grafana, Pyroscope, Sentry and Slack hosts in its config, including Slack file upload, and `git pull` on an org memory repo. Some clients send `User-Agent: axiom-skills/1.0 (agent)` (K-04).
- **Writes:** the user creates `~/.axiom.toml`. `scripts/init` creates `~/.config/axiom-sre/` (config mode 600, memory notes). Dashboard, monitor and notifier scripts write to the Axiom API when the agent runs them. Slack scripts can post and upload when Slack is configured.
- **Disclosed in its README:** mostly. The MCP server, the third-party credentials, dashboard and alert updates, and git-backed memory are in the root README ([README.md:26](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L26), [line 101](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L101)). The unauthenticated spec fetch, `kubectl`, and the `git pull` inside `scripts/init` are named in the skills, not in that README section (K-03).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `8f26649`, clean `GROK_HOME` and `HOME`: `No plugins installed`, `No marketplace sources configured` |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/axiomhq/skills.git@8f26649612042662c1ea8318ff27a49a7c24531f --trust`: `Installed 1 plugin(s) ... axiom`. The registry records commit `8f26649612042662c1ea8318ff27a49a7c24531f` |
| Gate: details | pass | `axiom v1.1.0`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 7 (`axiom-alerting`, `building-dashboards`, `controlling-costs`, `metrics-chart`, `query-metrics`, `spl-to-apl`, `axiom-sre`) and MCP server `axiom` (`http`, `https://mcp.axiom.co/mcp`). The same counts are on disk |
| MCP server under Grok | starts, sign-in needed | `grok mcp doctor` from an empty folder: `plugin: axiom 1 server`, `server started (0.2s)`, then handshake failed (`Auth required`, `resource_metadata="https://mcp.axiom.co/.well-known/oauth-protected-resource"`). A direct `initialize` POST returned HTTP 401 with that header. The protected-resource document names `https://authorization.axiom.co`. That server's metadata lists scopes `email`, `offline_access`, `openid` and `profile` |
| Reading: promises against components | pass, with K-01 | the README table lists the 7 skills ([README.md:7](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L7)) and the MCP server; all load. There is no Grok install section (K-01) |
| Reading: license | pass | `LICENSE` line 1 is `MIT License` and line 3 is `Copyright (c) 2026 Axiom, Inc.` The Grok manifest has `"license": "MIT"` ([plugin.json:11](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/.grok-plugin/plugin.json#L11)). The README points at the file ([README.md:141](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L141)). The GitHub API reports SPDX `MIT`. No skill frontmatter sets `license` |
| Reading: what it can execute | pass, with K-03, K-04 and K-05 | scripts and the MCP server match the README's configuration section; the init sentence, the client headers and the token-in-argv detail do not |
| Reading: maintenance | last push 2026-10-02, 16 stars, 0 open issues, 2 open pull requests ([#60](https://github.com/axiomhq/skills/pull/60), [#53](https://github.com/axiomhq/skills/pull/53)). The repository object's `open_issues_count` was 5 | GitHub API, 2026-10-04 |
| Hands | not run | a Grok session costs model time, and the skills need an Axiom organization |

Grok 1.0.46 is `2765805b9442`. xAI's pin is the commit that added `.grok-plugin/plugin.json` (`0e98eba`, "Merge pull request #56"). This pin is release 1.1.0 (`8f26649`, "chore(main): release 1.1.0").

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | There is no Grok install section. The only Grok link is the marketplace submission doc. `grok plugin marketplace add axiomhq/skills` registers the source as `skills` (the repository name). `grok plugin install axiom@skills --trust` answers `No marketplace plugin named "axiom" in "skills"`, and `axiom@axiom` answers `Unknown marketplace "axiom"`. The marketplace files that do exist list the plugin at `./`. The git URL at the pin installs. | [README.md:30](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L30), [line 137](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L137), [.claude-plugin/marketplace.json:13](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/.claude-plugin/marketplace.json#L13); commands above, grok 1.0.46, clean home. No `.grok-plugin/marketplace.json` at the pin | hairline | new (no open issue) | a Grok section with the git URL install, small | drafted ([seal](../seals/axiom/K-01.md)) |
| K-02 | `axiom-alerting` says the API token is read from `.axiom.toml` in the project root or in the home directory. `scripts/axiom-api` reads only `$HOME/.axiom.toml`. With a project file and no home file the script exits 1: `Error: <home>/.axiom.toml not found`. The skill README and the root README already say to use the home file. | [SKILL.md:12](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/axiom-alerting/SKILL.md#L12), [axiom-api:14](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/axiom-alerting/scripts/axiom-api#L14), [README.md:15](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/axiom-alerting/README.md#L15); both paths run at the pin | hairline | new | drop the project-root path from that sentence, small | drafted ([seal](../seals/axiom/K-02.md)) |
| K-03 | `axiom-sre` says `scripts/init` "loads config and syncs memory (fast, no network calls)". Every run after the first, once a deployment exists, executes `scripts/mem-sync`, which runs `git pull --ff-only` in each org memory repo. A first run with no org repo called git zero times. A configured org repo called `git pull --ff-only`. The root README already says memory can sync to a git repository you configure. | [SKILL.md:46](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/SKILL.md#L46), [init:15](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/scripts/init#L15), [init:287](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/scripts/init#L287), [mem-sync:24](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/scripts/mem-sync#L24), [README.md:101](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L101); both runs at the pin, the pull against a stand-in `git` | hairline | new | say that init pulls org memory repos and otherwise stays on disk, small | drafted ([seal](../seals/axiom/K-03.md)) |
| K-04 | The query and dashboard API clients say `~/.axiom.toml` is "shared with axiom-sre". SRE reads `~/.config/axiom-sre/config.toml`, and the root README says the two files are separate. `building-dashboards/scripts/axiom-api` says it rewrites `api.*` to `app.*/api`; the code requests `${url}/v2`, and on 2026-10-04 `GET https://api.axiom.co/v2/dashboards` returned 401 (`auth token not provided`) while `GET https://app.axiom.co/api/dashboards` returned 406. The same clients send `User-Agent: axiom-skills/1.0 (agent)` at version 1.1.0. | [query-metrics axiom-api:6](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/query-metrics/scripts/axiom-api#L6), [line 64](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/query-metrics/scripts/axiom-api#L64), [building-dashboards axiom-api:4](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/building-dashboards/scripts/axiom-api#L4), [line 9](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/building-dashboards/scripts/axiom-api#L9), [metrics axiom-api:9](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/building-dashboards/scripts/metrics/axiom-api#L9), [README.md:103](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/README.md#L103) | hairline | new | correct the three comments and the user agent, small | drafted ([seal](../seals/axiom/K-04.md)) |
| K-05 | `curl-auth` and the alerting `axiom-api` put the bearer token in `curl`'s argument list (`Authorization: Bearer <token>`). The SRE skill says `curl-auth` handles secrets through environment variables and that a secret must not show up in the command. The command the agent is told to type does not contain the token, `scripts/config` refuses to print secrets to a terminal, and a real `curl` does not echo the header. A stand-in `curl` on `PATH` printed `Authorization: Bearer xaat-secret-token-value` as argument 9. The same shape appeared for the alerting client with `xaat-home-token`. | [SKILL.md:26](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/SKILL.md#L26), [curl-auth:135](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/sre/scripts/curl-auth#L135), [axiom-api:54](https://github.com/axiomhq/skills/blob/8f26649612042662c1ea8318ff27a49a7c24531f/skills/axiom-alerting/scripts/axiom-api#L54); stand-in `curl` at the pin | hairline | new | pass the header from a mode-600 curl config file so it is not an argument, small | drafted ([seal](../seals/axiom/K-05.md)) |

## Workarounds

None needed. No fracture is open.

K-01 is already the install at the top of this card: this marketplace pins the git URL, which is the install that succeeded. K-02: put the token in `~/.axiom.toml`, as the root README says. That path was run at the pin; the script then built `GET https://api.axiom.co/v2/monitors` with the home file's token. A `.axiom.toml` in the project directory was not read.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
