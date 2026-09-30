# chrome-devtools

Google Chrome's DevTools server for coding agents: drive a live Chrome, record performance traces, read network requests and console messages, audit accessibility, cookies, LCP and memory leaks. The plugin carries seven skills that teach the agent to use those tools.

| | |
|---|---|
| Level | **assayed** |
| Domain | Browser debugging |
| Author | [Google Chrome](https://developer.chrome.com/) (ChromeDevTools) |
| License | [Apache-2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/LICENSE) |
| Source | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp/tree/02c0112cd57e4fa4bac31a1e69d7507601773b14) |
| Pinned SHA | `02c0112cd57e4fa4bac31a1e69d7507601773b14` (committed 2026-09-30, version 1.10.1) |
| Components at the pin | skills 7, agents 0, commands 0, hook events 0, MCP servers 0 (see K-01) |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Web developers who want Grok to open the page, reproduce the bug in a real browser and read the evidence (traces, network, console) instead of guessing.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install chrome-devtools@liquid-gold-grok
grok mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.10.1
```

The third line is the workaround for K-01: at this pin the plugin brings the skills but not the server.

## Why it is assayed

The gates pass and the server itself is well documented, but in Grok the plugin does not bring the thing it is named for. Grok reads the root `plugin.json` at this pin (it names the plugin `chrome-devtools`), and that manifest declares no MCP server; the server is declared only inline in `.claude-plugin/plugin.json` and in `mcp.json` without the leading dot. Grok looks for `.mcp.json`, so it installs seven skills that call Chrome DevTools MCP tools and no server to answer them. Six of the seven skill descriptions name Chrome DevTools MCP; only `chrome-devtools-cli` works through the command line instead. The fracture has a one-line workaround, and a seal draft is written; an outside contributor proposed the same fix upstream ([#2708](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/2708), [#2709](https://github.com/ChromeDevTools/chrome-devtools-mcp/pull/2709)) and closed both without a merge. When `.mcp.json` lands upstream, a re-assay can move this entry to gold.

## What it can execute

- **Hooks:** none.
- **Scripts:** none that the plugin runs. The repository holds the server's own source and build scripts, which Grok does not execute.
- **MCP servers:** declared for other agents as `npx --prefix ${PLUGIN_DATA} chrome-devtools-mcp@1.10.1` ([mcp.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/mcp.json)) and `npx chrome-devtools-mcp@1.10.1` ([.claude-plugin/plugin.json:5](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/.claude-plugin/plugin.json#L5)). Both pin the npm version. Grok registers neither (K-01). With the workaround, `npx` fetches `chrome-devtools-mcp@1.10.1` from npm and the server launches Chrome when a tool needs it.
- **Network:** the server sends usage statistics to Google by default, can send trace URLs to the Chrome UX Report API, and checks npm for updates. Each has an opt-out: `--no-usage-statistics` (or `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`), `--no-performance-crux`, and `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS`.
- **Disclosed in its README:** yes. Disclaimers, CrUX, usage statistics and update checks are documented ([README.md:24](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/README.md#L24) to line 60). The README also warns that the server exposes the browser's content to the agent.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `02c0112`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass, with a gap | `name: chrome-devtools`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)`; no `MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/ChromeDevTools/chrome-devtools-mcp.git@02c0112... --trust`: `Installed 1 plugin(s) ... chrome-devtools` |
| Gate: details | pass, with a gap | `chrome-devtools v1.10.1`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)`. In the same clean home, `cloudflare` (which ships `.mcp.json`) reports `... MCP servers` |
| Reading: promises against components | fracture | the manifest and README promise a DevTools MCP server; Grok registers skills only (K-01) |
| Reading: license | pass | Apache-2.0, `LICENSE` at the root, `"license": "Apache-2.0"` in the root `plugin.json` |
| Reading: what it can execute | pass | one pinned `npx` server (when registered); three disclosed network behaviors, each with an opt-out |
| Reading: maintenance | last push 2026-09-30, 108 open issues, 52,811 stars | GitHub API, 2026-09-30 |
| Workaround, at the pin | registers | in a clean home, `grok mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.10.1` wrote the server to the Grok config and `grok mcp list` shows `chrome-devtools: npx -y chrome-devtools-mcp@1.10.1`. The server was not started |
| Hands | not run | a Grok session costs model time, and starting the server fetches and runs npm code; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Grok installs the seven skills but registers no MCP server: the root `plugin.json` Grok reads has no `mcpServers`, and the server is declared only in `.claude-plugin/plugin.json` and `mcp.json`, not `.mcp.json`. | [plugin.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/plugin.json), [mcp.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/mcp.json); `grok plugin details chrome-devtools` lists no MCP servers | fracture | filed #2708 and PR #2709 by an outside contributor, both closed without a merge; not fixed at the pin | add `.mcp.json` with the server from `mcp.json`, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |
| K-02 | The Grok Build section of the client guide adds the server as a user MCP at `chrome-devtools-mcp@latest`, unpinned, and does not mention the plugin in xAI's marketplace. | [docs/client-configurations.md:295](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/docs/client-configurations.md#L295) | hairline | new | point Grok users at the plugin once K-01 is sealed, or pin the version, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |
| K-03 | The two manifests disagree on the name: `.claude-plugin/plugin.json` says `chrome-devtools-mcp`, the root `plugin.json` says `chrome-devtools`, and Grok uses the second, so `grok plugin details chrome-devtools-mcp` reports `Plugin "chrome-devtools-mcp" not found`. | [.claude-plugin/plugin.json:2](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/.claude-plugin/plugin.json#L2), [plugin.json:3](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/02c0112cd57e4fa4bac31a1e69d7507601773b14/plugin.json#L3) | hairline | new | one name in both manifests, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |

## Workarounds

K-01: after installing the plugin, register the server yourself at the same pinned version:

```bash
grok mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.10.1
```

Append `--no-usage-statistics` after the version to turn off Google's usage statistics. Use `--scope project` to write it to `./.grok/config.toml` instead of your user config. This assay checked that the command registers the server; it did not start it.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
