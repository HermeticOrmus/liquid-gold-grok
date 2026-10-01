# datadog

Datadog's Grok Build plugin: Datadog's hosted MCP server for asking about logs, metrics, traces, monitors and dashboards in plain language, a `/ddconfig` skill for checking and troubleshooting the connection, and a skill that scaffolds a new Datadog App. The manifest marks the plugin as a preview.

| | |
|---|---|
| Level | **assayed** |
| Domain | Observability |
| Author | [Datadog](https://www.datadoghq.com/) |
| License | [Apache-2.0](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/LICENSE) |
| Source | [datadog-labs/grok-plugin](https://github.com/datadog-labs/grok-plugin/tree/083b4783095520f562534956578c8826613292a9) |
| Pinned SHA | `083b4783095520f562534956578c8826613292a9` (committed 2026-08-28, version 0.7.21) |
| Components at the pin | skills 2, agents 0, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-10-01 with grok 1.0.44 |

The one MCP server the plugin declares is not in that count: Grok holds it back until you pick your Datadog site, and lists it from then on (K-02).

## Who it is for

Teams on Datadog who want Grok to pull error logs for a service, list alerting monitors, or find slow traces while they work on the code.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install datadog@liquid-gold-grok
```

Then open `/mcps`, select `datadog-grok` and press `i`: Grok asks for your Datadog site once, then starts the OAuth sign-in. To use API and application keys instead, start Grok with `DD_API_KEY` and `DD_APPLICATION_KEY` set, as the README says.

## Why it is assayed

The gates pass, and the plugin does its main job by Grok's own rules. Its server config carries a one-field `setup` form (seven Datadog sites), a Grok feature: the server stays out of the session until a site is saved, then resolves to that site's MCP endpoint. With US1 saved, Grok resolved it to `https://mcp.datadoghq.com/v1/mcp`, and that host publishes the OAuth metadata Grok's sign-in flow discovers. Before a site is saved, `grok inspect` lists no server for the plugin, which is why the components row says 0 (K-02).

One fracture is open. The README sends you to the agent or `/ddconfig` to change the Datadog domain, and the skill's Domain Flow reads and edits "the registration file" by "the editing rule in `mcp-settings.md`". Release v0.7.19 ([c890dfc](https://github.com/datadog-labs/grok-plugin/commit/c890dfc06e5b0b4fc46084e36b22f225076308c6)) moved the domain into Grok's setup preference and removed that file format and rule from `mcp-settings.md`, but left the two steps that use them. In Grok the site is saved only by the `/mcps` form, which opens only while no site is saved, and the model has no tool for it; so the flow has nothing to follow (K-01, *inferred* for a live session). The README's own `DD_MCP_DOMAIN` override is the workaround, and it ran at the pin. A seal draft rewrites the flow; when it lands, a re-assay can move this entry to gold.

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. `datadog-app` has the agent run `npm create @datadog/apps@latest` (first with `-- --help`, then with explicit flags) to scaffold a new Datadog App, and only when the user asks for one ([references/getting-started.md:23](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/datadog-app/references/getting-started.md#L23)). `ddconfig` reads the server's `datadog://mcp/whoami` resource through Grok's MCP resource tool and tells the agent not to reveal what it checked, file paths or variable names ([mcp-settings.md:9](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/ddconfig/references/mcp-settings.md#L9)).
- **MCP servers:** `datadog-grok`, type `http`, at `https://${DD_MCP_DOMAIN:-{{domain}}}/v1/mcp`, declared in `.dd_grok_mcp.json` through the manifest's `mcpServers` ([.dd_grok_mcp.json:5](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/.dd_grok_mcp.json#L5)). `{{domain}}` comes from the site form. It sends `DD_API_KEY` and `DD_APPLICATION_KEY` headers from the environment, empty when unset ([line 7](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/.dd_grok_mcp.json#L7)), and `X-Datadog-MCP-Toolsets: all` ([line 9](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/.dd_grok_mcp.json#L9)), which turns on every toolset the server offers; which tools that includes was not assessed. Nothing is installed locally.
- **Network:** the Datadog MCP server for the chosen site, tagged `X-Datadog-MCP-Referrer-Name: grok-plugin`; npm when scaffolding a Datadog App.
- **Disclosed in its README:** partly. The README covers the server, the OAuth default, key authentication and the `DD_MCP_DOMAIN` override ([README.md:46](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/README.md#L46)) and says no Datadog credentials go to the model provider; it does not mention the `datadog-app` skill or its npm scaffold (K-03), or the toolset header.

## Assay

Grok's behavior is cited from Grok's MCP guide (grok 1.0.44, `docs/user-guide/07-mcp-servers.md`, which grok writes into every fresh `GROK_HOME`) and from Grok's source at [xai-org/grok-build@2bdd1d6](https://github.com/xai-org/grok-build/tree/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8). The site choice was simulated by writing the record the `/mcps` form saves; the form itself was not driven.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `083b478`, clean `GROK_HOME` and `HOME`: `No plugins installed`, `No marketplace sources configured`; xAI's own catalog pins the same commit |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/datadog-labs/grok-plugin.git@083b478... --trust`: `Installed 1 plugin(s) ... datadog` |
| Gate: details | pass | `datadog v0.7.21`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 2 (`datadog-app`, `ddconfig`) and no MCP server; the plugin record says `"mcpServers": 1` (K-02) |
| MCP server before a site is saved | held | `grok mcp list`: `No MCP servers configured`; `grok mcp doctor` shows no `plugin: datadog` source; Grok's [`resolve_setup`](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-config/src/mcp_server_config.rs#L238) returns `Required` until a site is saved |
| MCP server after a site is saved | starts, sign-in needed | `{"version":1,"servers":{"datadog-grok":{"values":{"site":"us1"}}}}` written to `mcp_preferences.json` in the clean Grok home: `grok inspect` lists `datadog-grok` at `https://mcp.datadoghq.com/v1/mcp`; `grok mcp doctor`: `plugin: datadog 1 server`, `server started (0.2s)`, then `handshake failed (... HTTP 401 Unauthorized ...)`; `https://mcp.datadoghq.com/.well-known/oauth-authorization-server` answers with an issuer, PKCE and `scopes_supported: ["mcp_all"]` |
| Domain override, outside a session | pass | with US1 saved, `DD_MCP_DOMAIN=mcp.datadoghq.eu grok inspect --json` lists `datadog-grok` at `https://mcp.datadoghq.eu/v1/mcp`; with no site saved, the variable alone lists no server, as README line 64 says |
| Reading: promises against components | partial | the server attaches after the one-time site choice; changing the domain through the agent has no path in Grok (K-01) |
| Reading: license | pass | Apache-2.0 `LICENSE` and a `NOTICE` at the root, `"license": "Apache-2.0"` in the manifest |
| Reading: what it can execute | partial | the npm scaffold is named in its skill and not in the README (K-03) |
| Reading: maintenance | last push 2026-08-28, 0 open issues, 1 star | GitHub API, 2026-10-01 |
| Hands | not run | a Grok session costs model time, and the server needs a Datadog account; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `/ddconfig`'s Domain Flow reads the current domain from "the registration file" and edits it "following the editing rule in `mcp-settings.md`"; v0.7.19 removed that file format and rule, and `mcp-settings.md` says to "ask Grok to update the preference setting". Grok saves the site only from its `/mcps` form (the `x.ai/mcp/setup` request comes from the UI, not from a model tool), and the form opens only while no site is saved, so the agent cannot change the domain as the README promises. | [ddconfig/SKILL.md:42](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/ddconfig/SKILL.md#L42), [line 48](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/ddconfig/SKILL.md#L48), [mcp-settings.md:34](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/ddconfig/references/mcp-settings.md#L34), [README.md:18](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/README.md#L18), [c890dfc](https://github.com/datadog-labs/grok-plugin/commit/c890dfc06e5b0b4fc46084e36b22f225076308c6); Grok: [mcp.rs:34](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-shell/src/extensions/mcp.rs#L34), [modals.rs:1755](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/src/app/agent_view/modals.rs#L1755), [extensions_modal.rs:1076](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/src/views/extensions_modal.rs#L1076); *inferred* for a live session | fracture | new (the tracker holds no issues) | have the Domain Flow use `DD_MCP_DOMAIN` or a fresh site choice in `/mcps`, small | drafted ([seal](../seals/datadog/K-01.md)); workaround run at the pin |
| K-02 | Until a site is saved, Grok registers no MCP server for the plugin: `grok inspect`, `grok mcp list` and `grok mcp doctor` show none, so a fresh install looks like a skills-only plugin. README line 64 says the choice is needed once; line 18 says "The agent will guide you through selecting the correct Datadog MCP domain", while it is Grok's `/mcps` form that asks. | [.dd_grok_mcp.json:13](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/.dd_grok_mcp.json#L13), [README.md:18](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/README.md#L18), [line 64](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/README.md#L64); inspect and doctor output above | hairline | new | README: Grok asks for the site on the first `i` in `/mcps`, and the server appears after that, small | drafted ([seal](../seals/datadog/K-02.md)) |
| K-03 | The README and the manifest describe only the MCP server. Neither mentions the `datadog-app` skill, which runs `npm create @datadog/apps@latest`, an unpinned scaffolder from npm, when the user asks for a new Datadog App. | [datadog-app/SKILL.md:3](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/datadog-app/SKILL.md#L3), [references/getting-started.md:23](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/skills/datadog-app/references/getting-started.md#L23), [README.md:3](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/README.md#L3), [.grok-plugin/plugin.json:4](https://github.com/datadog-labs/grok-plugin/blob/083b4783095520f562534956578c8826613292a9/.grok-plugin/plugin.json#L4) | hairline | new | list both skills in the README, small | drafted ([seal](../seals/datadog/K-02.md), same draft) |

## Workarounds

- **K-01:** pick the site once in `/mcps` (select `datadog-grok`, press `i`, choose the site, sign in). To change it, start Grok with the MCP domain of the new site from the table in `skills/ddconfig/references/mcp-settings.md`, then sign in again from `/mcps`:

  ```bash
  DD_MCP_DOMAIN=mcp.datadoghq.eu grok
  ```

  Run at the pin: with US1 saved, `DD_MCP_DOMAIN=mcp.datadoghq.eu grok inspect --json` listed `datadog-grok` at `https://mcp.datadoghq.eu/v1/mcp`. By Grok's source, removing the `datadog-grok` entry from `mcp_preferences.json` in the Grok home brings the site form back on the next `i`; that path was not run in the UI.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
