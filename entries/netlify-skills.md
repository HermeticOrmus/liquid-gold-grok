# netlify-skills

Netlify's own reference skills for building on Netlify (Functions, Edge Functions, Blobs, managed Postgres, Image CDN, Forms, Identity, caching, AI Gateway, framework adapters, deploys, access control, Agent Runners, MCP servers hosted on Netlify) plus Netlify's hosted MCP server for projects, deploys and environment variables.

| | |
|---|---|
| Level | **gold** |
| Domain | Cloud platform |
| Author | [Netlify](https://www.netlify.com) |
| License | [MIT](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/LICENSE) |
| Source | [netlify/context-and-tools](https://github.com/netlify/context-and-tools/tree/47d1f147cc134043593574b69e6483e1f6ae16ad) |
| Pinned SHA | `47d1f147cc134043593574b69e6483e1f6ae16ad` (committed 2026-10-01, version 1.6.0) |
| Components at the pin | skills 15, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Anyone shipping a site or an API to Netlify from Grok: writing Functions or Edge Functions, storing files in Blobs, adding a database, a form or a login, tuning the CDN cache, or wiring a framework adapter and a deploy.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install netlify-skills@liquid-gold-grok
```

The plugin names itself `netlify-skills`. xAI's catalog lists the same repository as `netlify` (K-02), so after an install from either place, `grok plugin details netlify-skills` is the line that finds it.

## Why it is gold

Every gate passed at the pin, the plugin runs nothing on its own (no hooks, no scripts; every skill is reference text), and Grok loads the 15 skills the README lists plus the hosted MCP server the README discloses with its URL and its OAuth sign-in. The vessel already carries gold: the MCP server used to start as `npx -y @netlify/mcp`, an unpinned npm package fetched at session start that also needed Node 22, and [#51](https://github.com/netlify/context-and-tools/pull/51) replaced it with Netlify's hosted HTTP endpoint. The skills carry habits worth copying. `netlify-agent-runner` treats a remote agent run as billable and makes it wait for "explicit permission before running any `netlify agents:create` command", taken as "its own turn, separate from the user's original request" ([SKILL.md:138](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/skills/netlify-agent-runner/SKILL.md#L138)). The access-control and Identity skills tell the agent to "Never curl `api.netlify.com` or read local auth tokens" and to hand the user the dashboard path instead ([netlify-access-control/SKILL.md:8](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/skills/netlify-access-control/SKILL.md#L8), [netlify-identity/SKILL.md:18](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/skills/netlify-identity/SKILL.md#L18)). What is left open are three hairlines: the catalog name and the plugin name differ, the license is in the file but in neither manifest nor the README, and one skill claims every MCP request.

## What it can execute

- **Hooks:** none.
- **Scripts:** none in the plugin's skills. The repository's `scripts/` and `bin/` are build, release and install tools for other channels; Grok does not run them.
- **MCP servers:** `netlify`, type `http`, at `https://netlify-mcp.netlify.app/mcp` ([.mcp.json](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/.mcp.json)). `.grok-plugin/plugin.json` declares no `mcpServers`, so Grok finds the server through the `.mcp.json` convention. It authorizes through OAuth on first connection; nothing is installed locally.
- **Network:** the hosted MCP server, once you authorize it. The skills ask the agent to use the Netlify CLI, to run `npm view <pkg> version` before pinning a framework version, and to run `netlify agents:create` (which consumes plan credits) only after a separate yes.
- **Disclosed in its README:** yes. The skills are listed at [README.md:7](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/README.md#L7) and the MCP server, its URL and its OAuth flow at [README.md:162](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/README.md#L162).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `47d1f14`, the head of `main`; clean `GROK_HOME` and `HOME`. xAI's catalog pins `c840ee7` (1.5.2), three commits behind |
| Gate: validate | pass | `name: netlify-skills`, `version: 1.6.0`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/netlify/context-and-tools.git@47d1f14... --trust`: `Installed 1 plugin(s) from ...: netlify-skills` |
| Gate: details | pass | `grok plugin details netlify-skills`: `netlify-skills v1.6.0`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers`. `grok plugin details netlify` exits 1 with `Plugin "netlify" not found` (K-02) |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: 15 skills from `netlify-skills`, MCP server `netlify` (`http`, `https://netlify-mcp.netlify.app/mcp`), no hook file, no agents; the folder holds the same counts |
| Reading: promises against components | pass | the README Skills table lists 15 skills and the MCP server section names one server; all load |
| Reading: license | pass, with a hairline | MIT, `LICENSE` at the root (Copyright (c) 2025 Netlify); `package.json` says MIT; neither plugin manifest nor the README states it (K-03) |
| Reading: what it can execute | pass | one hosted MCP server, disclosed; no hooks, no scripts |
| Reading: maintenance | last push 2026-10-01, 2 open issues and 5 open pull requests, 38 stars | GitHub API, 2026-10-01 |
| xAI catalog install | installs, under another name | clean home, `grok plugin marketplace add xai-org/plugin-marketplace`, then `grok plugin install netlify@xai-official --trust`: `Installed 1 plugin(s) from xAI Official: netlify-skills`, at `c840ee7` |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The bundled MCP server started as `npx -y @netlify/mcp`, an unpinned npm package fetched on every session start that also needed Node 22 or later. | [#51](https://github.com/netlify/context-and-tools/pull/51) (merged 2026-06-11), [.mcp.json at the pin](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/.mcp.json) | fracture | merged upstream #51 | hosted `type: http` server, small | sealed |
| K-02 | xAI's catalog lists the plugin as `netlify` and the README tells Grok users to install **netlify**, but the plugin names itself `netlify-skills`; after the install, `grok plugin details netlify` fails and `grok plugin list` shows `netlify-skills`. | [README.md:156](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/README.md#L156), [.grok-plugin/plugin.json:2](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/.grok-plugin/plugin.json#L2); the clean-home outputs in the assay table | hairline | new | say in the Grok section which name the plugin installs under, or align the two names with xAI, small | drafted ([seal](../seals/netlify-skills/K-02.md)) |
| K-03 | The license is stated only in `LICENSE` and `package.json`: neither `.grok-plugin/plugin.json` nor `.claude-plugin/plugin.json` has a `license` field, and the README has no license section. | [.grok-plugin/plugin.json](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/.grok-plugin/plugin.json), [.claude-plugin/plugin.json](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/.claude-plugin/plugin.json), [package.json:5](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/package.json#L5) | hairline | new | add `"license": "MIT"` to both manifests, small | drafted ([seal](../seals/netlify-skills/K-02.md), same draft) |
| K-04 | `netlify-mcp-servers` claims every MCP-server request, "Use even when the user just says \"MCP\"", so in a project with no Netlify site it steers the agent toward Netlify Functions. The skill is reference text; nothing runs. | [skills/netlify-mcp-servers/SKILL.md:3](https://github.com/netlify/context-and-tools/blob/47d1f147cc134043593574b69e6483e1f6ae16ad/skills/netlify-mcp-servers/SKILL.md#L3) | hairline | new | scope the trigger to MCP servers on Netlify, small | open |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
