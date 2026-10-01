# mongodb

MongoDB's own plugin for self-managed deployments: seven skills for writing read-only queries and aggregations, schema design, query and index optimization, Atlas Search and Vector Search, driver connection tuning, Atlas Stream Processing and server setup, plus the MongoDB MCP server, started locally through `npx` against your connection string.

| | |
|---|---|
| Level | **gold** |
| Domain | Database |
| Author | [MongoDB](https://www.mongodb.com) |
| License | [Apache-2.0](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/LICENSE) |
| Source | [mongodb/agent-skills, plugins/mongodb](https://github.com/mongodb/agent-skills/tree/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb) |
| Pinned SHA | `d1d2d86754ff303ac441624b2ac8e0380465aa9b` (committed 2026-09-22, version 1.2.1) |
| Components at the pin | skills 7, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers who work against MongoDB Community, Enterprise Advanced, a local Atlas container or an Atlas cluster by connection string, and want Grok to read the real schema and indexes before it writes a query, an index or a schema change. For the hosted Atlas server with OAuth, MongoDB ships a separate `mongodb-atlas` plugin from the same repository.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install mongodb@liquid-gold-grok
```

Then ask Grok to set up the connection; the `mongodb-mcp-setup` skill walks through it. Set the variables in the shell that starts Grok: Grok passes that environment to the server (measured, see the assay). To keep the server at the version checked here, use the override under Workarounds.

## Why it is gold

Every gate passed at the pin, and the MCP server starts under Grok: `grok mcp doctor mongodb` reports `handshake OK` and `31 tools discovered`. The setup skill's method works in Grok as written: with `MDB_MCP_READ_ONLY=true` exported before Grok starts, the same check reports 20 tools, the 11 write and drop tools gone, so the shell environment reaches the server. The license file is at the repository root, and every skill carries `license: Apache-2.0`.

The skills draw their approval lines where they belong. `mongodb-mcp-setup` "never asks for or handles credentials" and redacts every value it checks ([SKILL.md:32](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-mcp-setup/SKILL.md#L32), [line 56](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-mcp-setup/SKILL.md#L56)). `mongodb-search-and-ai` says "Explain before executing ... require explicit approval" before it creates an index ([SKILL.md:18](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-search-and-ai/SKILL.md#L18)), `mongodb-query-optimizer` says "Do not create indexes directly via MCP unless the user gives approval" ([SKILL.md:150](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-query-optimizer/SKILL.md#L150)), and the stream-processing skill warns about billing before it starts a processor and confirms before teardown ([SKILL.md:265](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-atlas-stream-processing/SKILL.md#L265), [line 273](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-atlas-stream-processing/SKILL.md#L273)).

The one fracture is the server line itself: `npx -y mongodb-mcp-server@<3` runs whatever 2.x release npm serves when the session starts, so the pinned commit does not pin the code that runs (K-05). An override in Grok's config that pins 2.1.2 was run at the pin: the server starts with the same 31 tools and all 7 skills still load. That seal is in this card. What is left open are hairlines: the plugin's README does not say that the server sends usage telemetry to MongoDB by default, which MongoDB's server documentation does say with an opt-out (K-01); there is no Grok install line for this plugin (K-02); two skills spell tools the Claude Code way (K-03); and one pool-size example contradicts itself, already fixed in an open pull request (K-04).

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. The setup skill runs read-only checks (`env | grep "^MDB_MCP"` with values redacted, `docker info`) and shows the user what to add to `~/.mcp-env` and their shell profile; the user adds the credentials.
- **MCP servers:** `mongodb`, stdio: `npx -y mongodb-mcp-server@<3` ([mcp.json:5](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/mcp.json#L5)), which npm resolved to 2.1.2 on 2026-10-01 (`npm view mongodb-mcp-server@'<3' version`; the `latest` tag is 3.0.5). It is read-write by default: 31 tools, including `delete-many`, `drop-database`, `drop-collection`, `update-many` and `rename-collection`. The server asks for confirmation through MCP elicitation before `drop-database`, `drop-collection`, `delete-many` and `drop-index` by default ([server README.md:537](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L537), at v2.1.2), and Grok shows elicitation requests as a card ([03-keyboard-shortcuts.md:131](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/03-keyboard-shortcuts.md#L131)). `MDB_MCP_READ_ONLY=true` removes the 11 tools that write.
- **Network:** npm, to fetch the server at each start; the MongoDB deployment in the connection string; with service-account credentials, the Atlas Admin API. The server sends usage telemetry to MongoDB unless `MDB_MCP_TELEMETRY=disabled` or `DO_NOT_TRACK=1` is set ([server README.md:588](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L588)): tool names, durations and results, a device id and machine metadata, and the cluster name for Atlas tools ([types.ts:27](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/src/telemetry/types.ts#L27)). Its `search-knowledge` tool sends queries to `https://knowledge.mongodb.com/api/v1/` ([server README.md:430](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L430)). Every server run in this assay had telemetry turned off.
- **Writes:** the server's logs under `~/.mongodb/mongodb-mcp/.app-logs` (seen in the scratch home), and exported query results under `~/.mongodb/mongodb-mcp/exports` when the `export` tool runs ([server README.md:578](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L578)).
- **Disclosed in its README:** mostly. The plugin README says the server runs locally through `npx` and lists every skill ([README.md:3](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/README.md#L3)). Telemetry and the knowledge-base calls are disclosed in MongoDB's server README and in its docs page [Enable or disable features](https://www.mongodb.com/docs/mcp-server/local-mcp/configuration/enable-or-disable-features), not in the plugin's own README (K-01).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `d1d2d86`, clean `GROK_HOME` and `HOME` (`No plugins installed`, `No marketplace sources configured`) |
| Gate: validate | pass | `plugins/mongodb`: `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/mongodb/agent-skills.git@d1d2d86...#plugins/mongodb: mongodb`; the registry records commit `d1d2d86754ff303ac441624b2ac8e0380465aa9b`, subdir `plugins/mongodb` |
| Gate: details | pass | `mongodb v1.2.1 (subdir: plugins/mongodb)` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 7, MCP server `mongodb` (stdio, `npx`), the same as the files on disk |
| MCP server under Grok | pass | `grok mcp doctor mongodb`: `command found`, `server started`, `handshake OK (protocol 2025-11-25)`, `31 tools discovered`; the `npx` cache in the scratch home holds `mongodb-mcp-server` 2.1.2 |
| Environment reaches the server | pass | `MDB_MCP_READ_ONLY=true` exported before Grok: `grok mcp doctor mongodb` reports `20 tools discovered` |
| Reading: promises against components | pass | the plugin README lists 7 skills and the `npx` server ([README.md:7](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/README.md#L7)); all load, and the manifest Grok reads declares them ([.grok-plugin/plugin.json:19](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/.grok-plugin/plugin.json#L19)) |
| Reading: license | pass | Apache-2.0 `LICENSE` at the repository root, `"license": "Apache-2.0"` in the Grok manifest and `license: Apache-2.0` in every skill |
| Reading: what it can execute | pass, with K-01 and K-05 | one `npx` server, range-pinned (K-05); its telemetry is disclosed by MongoDB's server docs, not the plugin README (K-01) |
| Reading: maintenance | last push 2026-09-30, 0 open issues, 9 open pull requests, 188 stars | GitHub API, 2026-10-01 |
| Hands | not run | a Grok session costs model time, and no database was connected for this assay |

Grok's own behavior is cited from Grok's user guide (grok 1.0.44 writes it into every fresh `GROK_HOME`; the links go to the same text in xai-org/grok-build at `2bdd1d6`). The server's behavior is cited from mongodb-js/mongodb-mcp-server at the `v2.1.2` tag (`aa95f17`), the version `npx` resolved.

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The plugin's README and setup guide do not say what the server sends to MongoDB: usage telemetry is on by default, and `search-knowledge` sends queries to MongoDB's knowledge service. MongoDB's server README and docs disclose both with opt-outs, but the guide's link for "a full list of configuration options" returns 404. | [plugins/mongodb/README.md:3](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/README.md#L3), [README.community.md:69](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/README.community.md#L69) (`https://www.mongodb.com/docs/mcp-server/configuration/options/`: HTTP 404 on 2026-10-01); server: [README.md:466](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L466) (`"enabled"`), [README.md:588](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L588), [README.md:430](https://github.com/mongodb-js/mongodb-mcp-server/blob/aa95f17c0f3ae19eb4dba140373d435430389cd1/README.md#L430) | hairline | new | one README paragraph on telemetry and the knowledge calls with the opt-outs, a working link, and the opt-out offered in the setup skill, small | drafted ([seal](../seals/mongodb/K-01.md)) |
| K-02 | There is no Grok install line for this plugin: the setup guide covers Claude, Cursor, Codex, Gemini and Copilot CLI, and the README's Grok section covers `mongodb-atlas` only; the name alone does not install in a clean Grok home. | [README.community.md:7](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/README.community.md#L7), [README.md:63](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/README.md#L63); `grok plugin install mongodb --trust`: `No marketplace plugin named "mongodb" in any registered marketplace`; `grok plugin marketplace add mongodb/agent-skills` then `grok plugin install mongodb@agent-skills --trust`: `Installed 1 plugin(s) from agent-skills: mongodb` | hairline | new | a Grok section in the setup guide, small | drafted ([seal](../seals/mongodb/K-02.md)) |
| K-03 | Two skills spell tools in Claude Code's form (`mcp__mongodb__find`, `mcp__mongodb__collection-schema`); in Grok the tool is `mongodb__find`, and `use_tool` takes that qualified key. `allowed-tools: mcp__mongodb__*` is fine, since Grok accepts that spelling in rules. Whether the model stumbles on the names is *inferred*; the query-optimizer skill already names tools by their plain server names. | [mongodb-natural-language-querying/SKILL.md:19](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-natural-language-querying/SKILL.md#L19), [mongodb-schema-design/SKILL.md:148](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-schema-design/SKILL.md#L148); Grok: [07-mcp-servers.md:211](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md#L211), [22-permissions-and-safety.md:368](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md#L368) | hairline | new | name tools by their server names, as `mongodb-query-optimizer` does, small | drafted ([seal](../seals/mongodb/K-02.md), same draft) |
| K-04 | `mongodb-connection` gives the same example (10 clients, pool size 5, 3 members) two totals, 210 connections at line 28 and 150 at line 51; the second leaves out the two monitoring connections per member. | [mongodb-connection/SKILL.md:28](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-connection/SKILL.md#L28), [line 51](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/skills/mongodb-connection/SKILL.md#L51) | hairline | open pull request [#69](https://github.com/mongodb/agent-skills/pull/69) by an outside contributor | #69 reconciles the example to 210, small | open (held in #69) |
| K-05 | The server starts as `npx -y mongodb-mcp-server@<3`, so the pinned commit does not pin the code that runs: any newer 2.x release on npm runs under this pin without review. | [mcp.json:5](https://github.com/mongodb/agent-skills/blob/d1d2d86754ff303ac441624b2ac8e0380465aa9b/plugins/mongodb/mcp.json#L5); `npm view mongodb-mcp-server@'<3' version`: newest 2.1.2 on 2026-10-01 | fracture | new | an exact version in `mcp.json` upstream, small; in this card, the override below, run at the pin | sealed (card): the override ran at the pin |

## Workarounds

- **K-05:** pin the server in `~/.grok/config.toml`. A server of the same name replaces the plugin's entry:

  ```toml
  [mcp_servers.mongodb]
  command = "npx"
  args = ["-y", "mongodb-mcp-server@2.1.2"]
  ```

  Run at the pin in a clean Grok home with the plugin installed: `grok mcp doctor mongodb` reads the server from `~/.grok/config.toml` (`stdio: npx -y mongodb-mcp-server@2.1.2`), reports `handshake OK` and `31 tools discovered`, and `grok inspect --json` still lists the plugin's 7 skills. Move the version only after reading what changed.
- **K-01:** `export MDB_MCP_TELEMETRY=disabled` (or `DO_NOT_TRACK=1`) in the shell that starts Grok. Grok passes that environment to the plugin's server, as the read-only check above shows; the telemetry traffic itself was not observed.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
