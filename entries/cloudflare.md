# cloudflare

Cloudflare's own skills for building on its developer platform (Workers, Durable Objects, the Agents SDK, Wrangler, Sandbox, Turnstile, Cloudflare One, web performance) plus Cloudflare's hosted MCP server for the Cloudflare API and current docs.

| | |
|---|---|
| Level | **gold** |
| Domain | Cloud platform |
| Author | [Cloudflare](https://www.cloudflare.com/) |
| License | [Apache-2.0](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/LICENSE) |
| Source | [cloudflare/skills](https://github.com/cloudflare/skills/tree/626547c06881a20b3322bdc2ed6e6451b33a4fb6) |
| Pinned SHA | `626547c06881a20b3322bdc2ed6e6451b33a4fb6` (committed 2026-09-26) |
| Components at the pin | skills 14, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone deploying to Cloudflare from Grok: Workers and Wrangler, Durable Objects, agents on the Agents SDK, Sandbox, Turnstile on a form, or a Cloudflare One rollout.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install cloudflare@liquid-gold-grok
```

## Why it is gold

Every gate passed at the pin, and Grok registers the MCP server the README promises (`grok plugin details` ends in `MCP servers`, which is not true of every plugin in this domain; see [chrome-devtools](chrome-devtools.md)). The vessel already carries gold: its MCP servers used to start through `npx mcp-remote`, an unpinned npm package fetched on every session, and [#16](https://github.com/cloudflare/skills/pull/16) replaced that with direct HTTP connections. The one script-heavy skill, turnstile-spin, calls the Cloudflare API only with a token you provide, and says so in its own README and in each step. What is left open is a hairline: the install docs name six agents and not Grok.

## What it can execute

- **Hooks:** none.
- **Scripts:** the turnstile-spin skill ships four bash scripts ([`skills/turnstile-spin/scripts/`](https://github.com/cloudflare/skills/tree/626547c06881a20b3322bdc2ed6e6451b33a4fb6/skills/turnstile-spin/scripts)): `auth-probe.sh` checks your API token's Turnstile scope with a deliberately invalid request (and deletes a widget if one is ever created by mistake), `widget-create.sh` creates the widget, `validate.sh` runs a siteverify check, and `persist-skill.sh` clones this repo into your project on request. They need `curl`, `python3` and (for validate) `jq`.
- **MCP servers:** `cloudflare`, type `http`, at `https://mcp.cloudflare.com/mcp` ([.mcp.json](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/.mcp.json)). Nothing is installed locally.
- **Network:** the hosted MCP server; the turnstile scripts call `api.cloudflare.com` and `challenges.cloudflare.com` with your token; `persist-skill.sh` clones from GitHub.
- **Disclosed in its README:** yes. The MCP server is in the MCP Servers section ([README.md:84](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/README.md#L84)); the scripts are listed in the skill's README ([skills/turnstile-spin/README.md:12](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/skills/turnstile-spin/README.md#L12)) and the skill tells the agent to confirm before every irreversible step ([SKILL.md:44](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/skills/turnstile-spin/SKILL.md#L44)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `626547c`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/cloudflare/skills.git@626547c... --trust`: `Installed 1 plugin(s) ... cloudflare` |
| Gate: details | pass | `cloudflare v1.0.1`, `components: ... MCP servers`; 14 skills in the installed folder |
| Reading: promises against components | pass | the README Skills table lists 14 skills and one MCP server ([README.md:63](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/README.md#L63)); all 14 skills and the server load |
| Reading: license | pass | Apache-2.0, `LICENSE` at the root, `"license": "Apache-2.0"` in both manifests |
| Reading: what it can execute | pass | one hosted MCP server; four disclosed turnstile scripts that act only with your token |
| Reading: maintenance | last push 2026-09-26, 27 open issues, 2,952 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

Grok reads the root `plugin.json` (agent-plugins schema) at this pin, not `.claude-plugin/plugin.json`, and finds the server through the conventional `.mcp.json`. Both manifests carry the same name, version and license, so nothing differs for a Grok user.

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The bundled MCP servers started through `npx mcp-remote`, an unpinned npm package fetched on every session. | [#16](https://github.com/cloudflare/skills/pull/16) (merged 2026-02-08), [.mcp.json at the pin](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/.mcp.json) | fracture | merged upstream #16 | direct `type: http` servers, small | sealed |
| K-02 | The install docs cover Codex, Claude Code, VS Code, Cursor, `npx skills` and a manual copy, and the turnstile-spin README links only into `~/.claude/skills`; there is no Grok Build path, though the plugin installs cleanly in Grok. | [README.md:5](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/README.md#L5), [skills/turnstile-spin/README.md:29](https://github.com/cloudflare/skills/blob/626547c06881a20b3322bdc2ed6e6451b33a4fb6/skills/turnstile-spin/README.md#L29) | hairline | new (no issue mentions Grok) | add a Grok Build install section, small | drafted ([seal](../seals/cloudflare/K-02.md)) |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
