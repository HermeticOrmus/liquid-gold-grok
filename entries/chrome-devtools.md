# chrome-devtools

Google Chrome's DevTools server for coding agents: drive a live Chrome, record performance traces, read network requests and console messages, audit accessibility, cookies, LCP and memory leaks. The plugin carries seven skills that teach the agent to use those tools.

| | |
|---|---|
| Level | **assayed** |
| Domain | Browser debugging |
| Author | [Google Chrome](https://developer.chrome.com/) (ChromeDevTools) |
| License | [Apache-2.0](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/LICENSE) |
| Source | [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp/tree/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78) |
| Pinned SHA | `b2f522c8ba0fd2e00a679159b4aa5243de5f1b78` (committed 2026-10-02, version 1.10.1) |
| Components at the pin | skills 7, agents 0, commands 0, hook events 0, MCP servers 0 (see K-01) |
| Assayed | 2026-10-04 with grok 1.0.46 (2765805b9442); first assay 2026-09-30 at `02c0112` with grok 1.0.44 |

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

The pin moved from `02c0112` (2026-09-30) to `b2f522c` (2026-10-02), sixteen commits later. The gates pass, and the server itself is still well documented, but Grok still does not load the thing the plugin is named for. Grok reads the root `plugin.json` (it names the plugin `chrome-devtools`), and that manifest declares no MCP server. There is still no `.mcp.json`. The server is declared only inline in `.claude-plugin/plugin.json` and in `mcp.json` without the leading dot. `grok inspect --json` lists seven skills and no plugin MCP server. Six of the seven skill descriptions name Chrome DevTools MCP; only `chrome-devtools-cli` works through the command line instead. The fracture has a one-line workaround, re-run at this pin, and the seal draft is updated for the new SHA. An outside contributor proposed the same file upstream ([#2708](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/2708), [#2709](https://github.com/ChromeDevTools/chrome-devtools-mcp/pull/2709)) and closed both without a merge. [#2095](https://github.com/ChromeDevTools/chrome-devtools-mcp/pull/2095) had removed a duplicate `.mcp.json` on 2026-05-21, and it was not added back. When a file Grok reads declares the server, a re-assay can seal K-01 and move this entry to gold.

The sixteen commits change the server source in the git tree. Grok does not run that source. The manifests still start `npx chrome-devtools-mcp@1.10.1`, the npm release published 2026-09-23, which does not contain those commits. One new line in the CLI skill describes a flag that package does not have (K-04). No break is open.

## What it can execute

- **Hooks:** none.
- **Scripts:** none that the plugin runs. The repository holds the server's own source and build scripts, which Grok does not execute.
- **MCP servers:** declared for other agents as `npx --prefix ${PLUGIN_DATA} chrome-devtools-mcp@1.10.1` ([mcp.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/mcp.json)) and `npx chrome-devtools-mcp@1.10.1` ([.claude-plugin/plugin.json:5](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/.claude-plugin/plugin.json#L5)). Both pin the npm version. Grok registers neither (K-01). With the workaround, `npx` fetches `chrome-devtools-mcp@1.10.1` from npm and the server launches Chrome when a tool needs it. `npm view chrome-devtools-mcp@1.10.1 time` reports that version published `2026-09-23T10:42:53.202Z`. `git grep` for `sourcePath` and `fileNavigations` at tag `chrome-devtools-mcp-v1.10.1` exits 1.
- **Server source at this pin, not executed by Grok:** `--file-navigations` defaults to true ([src/config/mcp-options.ts:134](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/src/config/mcp-options.ts#L134), [docs/configuration.md:212](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/docs/configuration.md#L212)); `evaluate_script` can read a local script through `loadResource`, which checks the path ([src/tools/script.ts:207](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/src/tools/script.ts#L207), [src/McpContext.ts:925](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/src/McpContext.ts#L925)); named groups in URL patterns are rejected ([src/utils/url.ts:120](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/src/utils/url.ts#L120), [#2857](https://github.com/ChromeDevTools/chrome-devtools-mcp/pull/2857)). None of that is in the npm package the manifests start.
- **Network:** the server sends usage statistics to Google by default, can send trace URLs to the Chrome UX Report API, and checks npm for updates. Each has an opt-out: `--no-usage-statistics` (or `CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`), `--no-performance-crux`, and `CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS`. The telemetry tables at this pin add metric names for `file_navigations` and `source_path`; they use the same usage-statistics channel.
- **Disclosed in its README:** yes, for those three behaviors. Disclaimers, CrUX, usage statistics and update checks are documented ([README.md:24](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/README.md#L24) to line 60). The README also warns that the server exposes the browser's content to the agent. `--file-navigations` is disclosed in the configuration guide, which the README links, and is not in the npm package above.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `b2f522c`, which `git merge-base --is-ancestor` accepts from `origin/main`. Clean `GROK_HOME` and `HOME`: `grok plugin list` printed `No plugins installed`, `grok plugin marketplace list` printed `No marketplace sources configured`. grok 1.0.46 |
| Gate: validate | pass, with a gap | exit 0. `name: chrome-devtools`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)`; no `MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/ChromeDevTools/chrome-devtools-mcp.git@b2f522c8ba0fd2e00a679159b4aa5243de5f1b78 --trust` printed `Installed 1 plugin(s) from ...: chrome-devtools`. The installed registry commit is `b2f522c8ba0fd2e00a679159b4aa5243de5f1b78` |
| Gate: details | pass, with a gap | `chrome-devtools v1.10.1`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s)` |
| Gate: inspect | pass, with a gap | `grok inspect --json` from an empty folder loaded 7 skills, 0 agents, 0 commands, 0 hook events, and 0 plugin MCP servers. `scripts/count_components.py` on the pin agrees: `skills=7 agents=0 commands=0 hooks=0 mcp=0` |
| Reading: promises against components | fracture | the manifest and README promise a DevTools MCP server; Grok registers skills only (K-01) |
| Reading: license | pass | Apache-2.0, `LICENSE` at the root, `"license": "Apache-2.0"` in the root `plugin.json` |
| Reading: what it can execute | pass, with a hairline | the declared server is still one pinned `npx` package; three disclosed network behaviors, each with an opt-out. The CLI skill describes a flag that package does not have (K-04) |
| Reading: maintenance | last push 2026-10-04, 78 open issues, 52,921 stars | GitHub API, 2026-10-04. Open issues are the search `is:issue is:open` (78). `pushed_at` is 2026-10-04; the default-branch commit is 2026-10-02 |
| Workaround, at the pin | registers | in the same clean home, `grok mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.10.1` printed `Added stdio MCP server 'chrome-devtools' with command: npx -y chrome-devtools-mcp@1.10.1` and `grok mcp list` shows that line. The server was not started. Inspect lists that server with no plugin name |
| Hands | not run | a Grok session costs model time, and starting the server fetches and runs npm code; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Grok installs the seven skills but registers no MCP server: the root `plugin.json` Grok reads has no `mcpServers`, and the server is declared only in `.claude-plugin/plugin.json` and `mcp.json`, not `.mcp.json`. | [plugin.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/plugin.json), [mcp.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/mcp.json); `grok plugin details chrome-devtools` lists no MCP servers; `grok inspect --json` loads 0 plugin MCP servers | fracture | filed #2708 and PR #2709 by an outside contributor, both closed without a merge; #2095 removed a `.mcp.json` on 2026-05-21; not fixed at the pin | add `.mcp.json` with the server from `mcp.json`, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |
| K-02 | The Grok Build section of the client guide adds the server as a user MCP at `chrome-devtools-mcp@latest`, unpinned, and does not mention the plugin in xAI's marketplace. | [docs/client-configurations.md:295](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/docs/client-configurations.md#L295). On grok 1.0.46 that line registers: `Added stdio MCP server 'chrome-devtools' with command: npx chrome-devtools-mcp@latest` | hairline | new | point Grok users at the plugin once K-01 is sealed, or pin the version, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |
| K-03 | The two manifests disagree on the name: `.claude-plugin/plugin.json` says `chrome-devtools-mcp`, the root `plugin.json` says `chrome-devtools`, and Grok uses the second, so `grok plugin details chrome-devtools-mcp` reports `Plugin "chrome-devtools-mcp" not found`. | [.claude-plugin/plugin.json:2](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/.claude-plugin/plugin.json#L2), [plugin.json:3](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/plugin.json#L3). Re-run at this pin: `Error: Plugin "chrome-devtools-mcp" not found.` | hairline | new | one name in both manifests, small | drafted ([seal](../seals/chrome-devtools/K-01.md)) |
| K-04 | The CLI skill's new example evaluates a local file with `--sourcePath` and `--format script`, and the configuration guide documents `--file-navigations`, but the manifests still start `chrome-devtools-mcp@1.10.1` (npm, published 2026-09-23), which has neither flag. | [skills/chrome-devtools-cli/SKILL.md:137](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/skills/chrome-devtools-cli/SKILL.md#L137), [docs/configuration.md:212](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/docs/configuration.md#L212); `git grep -e sourcePath -e fileNavigations chrome-devtools-mcp-v1.10.1` exits 1; [mcp.json](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/b2f522c8ba0fd2e00a679159b4aa5243de5f1b78/mcp.json) pins `@1.10.1` | hairline | new | drop the example until the npm pin includes commit 9cf47a4, or bump the pin, small | drafted ([seal](../seals/chrome-devtools/K-04.md)) |

## Workarounds

K-01: after installing the plugin, register the server yourself at the same pinned version:

```bash
grok mcp add chrome-devtools -- npx -y chrome-devtools-mcp@1.10.1
```

Append `--no-usage-statistics` after the version to turn off Google's usage statistics. Use `--scope project` to write it to `./.grok/config.toml` instead of your user config. This assay checked that the command registers the server on grok 1.0.46 at `b2f522c`; it did not start it.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
