# supabase

Supabase's skills for Grok: one for every Supabase product (Database, Auth, Edge Functions, Realtime, Storage, the CLI and the MCP server) with a security checklist for RLS, keys and privileged functions, and one with Postgres rules for schema, indexes, locking and RLS performance, plus Supabase's hosted MCP server for your projects.

| | |
|---|---|
| Level | **assayed** |
| Domain | Database |
| Author | [Supabase](https://supabase.com) |
| License | [MIT, stated in the manifest only](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/.grok-plugin/plugin.json#L10) (no license file at the pin) |
| Source | [supabase-community/supabase-plugin](https://github.com/supabase-community/supabase-plugin/tree/2c6d02d4565babe784103ee4d446a93ae9b24151) |
| Pinned SHA | `2c6d02d4565babe784103ee4d446a93ae9b24151` (committed 2026-09-28, version 0.1.16) |
| Components at the pin | skills 2, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers building on Supabase who want Grok to check current Supabase docs before it writes code, get RLS and auth right, and query or change their projects through the MCP server.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install supabase@liquid-gold-grok
```

The MCP server signs in with OAuth: open `/mcps`, select `supabase` and press `i`. To limit it to one project and read-only queries, see the workaround for K-03 below.

## Why it is assayed

Every gate passed at the pin and Grok loads both skills and the hosted MCP server, which answers an unauthenticated handshake with an OAuth challenge. The vessel already carries gold that matters to a Grok user: the server URL used to carry a `utm_source` query that made the OAuth resource check fail, and [#11](https://github.com/supabase-community/supabase-plugin/pull/11) moved that attribution into headers (K-01). The skill content is careful: it tells the agent to enable RLS in exposed schemas, never to add `SECURITY DEFINER` to get past a permission error, and to use scoped tokens.

One fracture is open: there is no license file at the pin. Six of its eight vendor manifests, the Grok one among them, say MIT, but the repository has no `LICENSE`, and the GitHub API reports no license for it (K-02). The rubric admits that as assayed, with a seal draft. The rest are hairlines. The README never names the hosted server, what it can change or how to scope it, and the Grok config connects unscoped and read-write; a user-level `config.toml` entry with `project_ref` and `read_only=true` replaced it at the pin (K-03). The feedback flow posts a public GitHub issue drafted from the conversation without showing the draft first (K-04), and one troubleshooting step writes a project `.mcp.json` that Grok ignores (K-05). OAuth sign-in was not run for this assay; two open issues report OAuth failures in Claude Code ([#50](https://github.com/supabase-community/supabase-plugin/issues/50), [#51](https://github.com/supabase-community/supabase-plugin/issues/51)), not checked in Grok. A license file would let a re-assay move this entry to gold.

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. The `supabase` skill tells the agent to use the Supabase CLI (discovering commands with `--help`), and for its troubleshooting step to run `curl` against the MCP server ([SKILL.md:104](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/SKILL.md#L104)). The feedback reference has the agent create a GitHub issue on `supabase/agent-skills` after asking permission (K-04).
- **MCP servers:** `supabase`, type `http`, at `https://mcp.supabase.com/mcp` with `X-Source-Name: grok-plugin` and `X-Source-Version: 0.1.16` headers ([agents/grok/mcp.json](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/agents/grok/mcp.json)). Nothing is installed locally. Supabase describes its tools as executing SQL, managing migrations, deploying functions and reading logs on hosted projects ([SUPABASE.md:7](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/SUPABASE.md#L7)).
- **Network:** the hosted MCP server; the skill has the agent fetch `https://supabase.com/changelog.md` before every Supabase task ([SKILL.md:16](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/SKILL.md#L16)) and docs pages as markdown, with its own web tools; open pull request [#62](https://github.com/supabase-community/supabase-plugin/pull/62), by an outside contributor, narrows that fetch to version-sensitive work. GitHub when a user agrees to send skill feedback.
- **Disclosed in its README:** partly. The manifest says "MCP access for project management, database work, auth, storage" ([.grok-plugin/plugin.json:4](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/.grok-plugin/plugin.json#L4)), and the README lists the two skills and "MCP adapters for each supported surface" ([README.md:7](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/README.md#L7)); neither names the server or what it can change (K-03).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `2c6d02d`, clean `GROK_HOME` and `HOME`: `No plugins installed`, `No marketplace sources configured` |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 0 command dir(s), 1 agent dir(s), MCP servers`; the "agent dir" is `agents/`, which holds each vendor's MCP config and no agents |
| Gate: install at the pin | pass | `grok plugin install https://github.com/supabase-community/supabase-plugin.git@2c6d02d... --trust`: `Installed 1 plugin(s) ... supabase` |
| Gate: details | pass | `supabase v0.1.16`, `components: 1 skill dir(s), 0 command dir(s), 1 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 2 (`supabase`, `supabase-postgres-best-practices`), agents 0, MCP server `supabase` (`http`, `https://mcp.supabase.com/mcp`), the same as the files on disk |
| MCP server under Grok | starts, sign-in needed | `grok mcp doctor`: `plugin: supabase 1 server`, `server started (0.2s)`, then `handshake failed (... Auth required, when send initialize request)` with the server's OAuth `resource_metadata` URL; expected without a sign-in |
| Reading: promises against components | pass | the README names both skills and the MCP adapters; all load, and the manifest's `mcpServers` points Grok at `agents/grok/mcp.json` |
| Reading: license | fracture | no license file in the [tree at the pin](https://github.com/supabase-community/supabase-plugin/tree/2c6d02d4565babe784103ee4d446a93ae9b24151); `gh api repos/supabase-community/supabase-plugin/license`: `Not Found (HTTP 404)`; `"license": "MIT"` in six of the eight vendor manifests (the Cursor and Gemini ones have no license field) and in `supabase-postgres-best-practices` (K-02) |
| Reading: what it can execute | partial | a read-write MCP server the README does not describe (K-03); a public issue posted from a draft the user does not see (K-04) |
| Reading: maintenance | last push 2026-09-28, 7 open (4 issues, 3 pull requests), 28 stars | GitHub API, 2026-10-01 |
| Scoping override, outside a session | pass | a `[mcp_servers.supabase]` entry in the clean home's `config.toml` with `?project_ref=abc123&read_only=true`: `grok inspect --json` lists `supabase` at that URL with source `configToml`, in place of the plugin's server |
| Hands | not run | a Grok session costs model time, and the server acts on a real Supabase account; not run for this assay |

The skills are synced from [supabase/agent-skills](https://github.com/supabase/agent-skills) releases ([README.md:33](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/README.md#L33)), so the seal drafts for skill text (K-04, K-05) are addressed there.

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The MCP URL carried `?utm_source=claude-code-plugin`; the server's OAuth resource is the bare URL, so sign-in was rejected. | [#9](https://github.com/supabase-community/supabase-plugin/pull/9) (closed, describes the failure), [#11](https://github.com/supabase-community/supabase-plugin/pull/11) (merged 2026-04-22), [agents/grok/mcp.json:5](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/agents/grok/mcp.json#L5) | break | merged upstream #11 | `X-Source-*` headers in place of the query, small | sealed |
| K-02 | There is no license file at the pin. Six of the eight vendor manifests say MIT, and the GitHub API reports no license for the repository. | [tree at the pin](https://github.com/supabase-community/supabase-plugin/tree/2c6d02d4565babe784103ee4d446a93ae9b24151), [.grok-plugin/plugin.json:10](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/.grok-plugin/plugin.json#L10); `gh api repos/supabase-community/supabase-plugin/license`: `Not Found (HTTP 404)` | fracture | new (no issue mentions a license) | add an MIT `LICENSE` at the root, small | drafted ([seal](../seals/supabase/K-02.md)) |
| K-03 | The README does not name the hosted server, say that its tools change hosted projects, or show how to scope it, and the Grok config connects without `project_ref` or `read_only`. Supabase's own MCP guide opens with a security caution and asks for project scoping and read-only mode before a production project is connected. | [agents/grok/mcp.json:5](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/agents/grok/mcp.json#L5), [README.md:9](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/README.md#L9); [Supabase MCP guide](https://supabase.com/docs/guides/getting-started/mcp) (configuration options and security risks) | hairline | new | a README section naming the server, its write tools and the scoping parameters, small | drafted ([seal](../seals/supabase/K-03.md)); the override below ran at the pin |
| K-04 | The skill-feedback flow asks permission, then drafts an issue from the conversation and creates it on the public `supabase/agent-skills` repository without showing the draft to the user first. | [skill-feedback.md:7](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/references/skill-feedback.md#L7), [line 9](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/references/skill-feedback.md#L9), [line 11](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/references/skill-feedback.md#L11) | hairline | new | show the title and body and wait for a yes before creating the issue, small | drafted ([seal](../seals/supabase/K-04.md)) |
| K-05 | MCP troubleshooting step 2 tells the agent to create a project `.mcp.json` pointing at the server when none exists. In Grok the plugin already provides a server named `supabase`, and Grok drops the project one: with that file in place, `grok mcp doctor` reports `.mcp.json 0 servers` and keeps `plugin: supabase`, while a project server under another name does load. | [SKILL.md:107](https://github.com/supabase-community/supabase-plugin/blob/2c6d02d4565babe784103ee4d446a93ae9b24151/skills/supabase/SKILL.md#L107); doctor output in a clean home | hairline | new | skip that step when the plugin provides the server, small | drafted ([seal](../seals/supabase/K-04.md), same draft) |

## Workarounds

- **K-02:** the MIT grant at this pin is the `license` field of the manifest Grok reads, linked in the table above. The skills come from `supabase/agent-skills`, which the GitHub API reports as MIT.
- **K-03:** to limit the server to one project and read-only SQL, add an entry with the same name to `~/.grok/config.toml`. Grok uses it in place of the plugin's server:

  ```toml
  [mcp_servers.supabase]
  url = "https://mcp.supabase.com/mcp?project_ref=<your project ref>&read_only=true"
  ```

  Run at the pin with a placeholder ref: `grok inspect --json` listed `supabase` at the scoped URL with source `configToml`. Sign in again from `/mcps` afterwards. Supabase documents a `features=` parameter for limiting tool groups as well.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
