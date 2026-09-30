# figma

Figma's hosted MCP server plus fourteen skills for design-to-code work: read design context and variables, implement a frame in code, connect components through Code Connect, and write back to the canvas (new files, design system libraries, diagrams, FigJam, slides, motion).

| | |
|---|---|
| Level | **watch** |
| Domain | Design to code |
| Author | [Figma](https://www.figma.com) |
| License | none in the repository; the README places use under the [Figma Developer Terms](https://www.figma.com/legal/developer-terms/) |
| Source | [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide/tree/2c8af036a758af150ec0244489f6fb3d12e394db) |
| Pinned SHA | `2c8af036a758af150ec0244489f6fb3d12e394db` (committed 2026-09-30, version 2.2.124) |
| Components at the pin | skills 14, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Teams whose designs live in Figma and who want Grok to read the real frame, tokens and components instead of a screenshot, and to push changes back to the file.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/figma/mcp-server-guide.git@2c8af036a758af150ec0244489f6fb3d12e394db --trust
```

## Why it waits

The plugin itself is in good shape for Grok: the gates pass, and unlike some plugins in this catalog Grok registers its MCP server (`grok plugin details` ends in `MCP servers`). It waits on the license. There is no license file anywhere in the tree at the pin, the GitHub API reports no license for the repository, and the manifest has no license field. The README says that using the server and "the related resources (including these skills)" means agreeing to the Figma Developer Terms ([README.md:12](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L12)). This library links a license at the pinned commit for every admitted entry and cannot do that here, so the rubric holds it at watch. The repository has issues turned off, so the seal is a draft pull request. A license file, or a terms file in the repository that the card can link at a commit, would let a re-assay admit it.

## What it can execute

- **Hooks:** none.
- **Scripts:** `figma-generate-library` ships JavaScript helpers ([`skills/figma-generate-library/scripts/`](https://github.com/figma/mcp-server-guide/tree/2c8af036a758af150ec0244489f6fb3d12e394db/skills/figma-generate-library/scripts)) that the agent embeds in `use_figma` calls, so they run inside Figma through the MCP server, not on your machine.
- **MCP servers:** `figma`, type `http`, at `https://mcp.figma.com/mcp`, with an `X-Figma-Plugin-Bundle` header naming the plugin version ([.mcp.json](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/.mcp.json)). Nothing is installed locally.
- **Network:** the hosted MCP server, which reads from and writes to your Figma files once you authorize it.
- **Disclosed in its README:** yes. The server, its write-to-canvas ability and the terms are in the README ([README.md:12](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L12), [line 16](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L16)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `2c8af03`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/figma/mcp-server-guide.git@2c8af03... --trust`: `Installed 1 plugin(s) ... figma` |
| Gate: details | pass | `figma v2.2.124`, `components: ... MCP servers`; 14 skills in the installed folder |
| Reading: promises against components | pass | the server and skills the README describes load; the README says the `workflow-skills/` folder is not bundled with the plugin ([README.md:205](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L205)), and Grok does not load it |
| Reading: license | fail | no license file in the tree, `gh api repos/figma/mcp-server-guide/license` returns 404, no `license` in the manifest (K-01) |
| Reading: what it can execute | pass | one hosted MCP server; helper scripts run inside Figma |
| Reading: maintenance | last push 2026-09-30, 10 open (issues are turned off, so these are pull requests), 2,032 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time and a Figma account; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The repository has no license file; the README points to the Figma Developer Terms, which live off the repository and cannot be linked at a commit. | [tree at the pin](https://github.com/figma/mcp-server-guide/tree/2c8af036a758af150ec0244489f6fb3d12e394db), [README.md:12](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L12), [.claude-plugin/plugin.json](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/.claude-plugin/plugin.json) | fracture | new (issues are turned off) | add a LICENSE or TERMS file and a `license` field, small | drafted ([seal](../seals/figma/K-01.md)) |
| K-02 | The install guide covers VS Code, Cursor, Claude Code, Gemini CLI and a generic section for other editors, but not Grok Build, though xAI's marketplace lists the plugin and it installs cleanly. | [README.md:38](https://github.com/figma/mcp-server-guide/blob/2c8af036a758af150ec0244489f6fb3d12e394db/README.md#L38) | hairline | new | add a Grok Build install section, small | drafted ([seal](../seals/figma/K-01.md)) |

## Workarounds

None admits the entry: the license is the owner's to state. A Grok user who accepts the Figma Developer Terms can install at the pin with the line above.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
