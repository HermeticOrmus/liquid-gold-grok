# exa

Exa's Grok Build plugin: one research skill, a `/tutorial` command, and Exa's hosted MCP server for semantic web search and reading a page as markdown. Search and fetch both require an Exa sign-in.

| | |
|---|---|
| Level | **assayed** |
| Domain | Web search |
| Author | [Exa](https://github.com/exa-labs) |
| License | [MIT, stated in the manifest only](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/.grok-plugin/plugin.json#L11) (no license file at the pin; GitHub reports none) |
| Source | [exa-labs/exa-grok-plugin](https://github.com/exa-labs/exa-grok-plugin/tree/879fae0c814765c43f39ea8f56aae1d44e9d9bc8) |
| Pinned SHA | `879fae0c814765c43f39ea8f56aae1d44e9d9bc8` (committed 2026-07-27, version 1.1.0) |
| Components at the pin | skills 1, agents 0, commands 1, hook events 0, MCP servers 1 |
| Assayed | 2026-10-04 with grok 1.0.46 |

## Who it is for

Grok users who want live web search, a page read as markdown, or a cited research pass (companies, people, papers, news, code docs) through Exa's index. An Exa account is required; new accounts get free credits at signup.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install exa@liquid-gold-grok
```

Then open `/mcps`, select `exa` and press `i`. The browser opens Exa's sign-in. The server does not answer until that sign-in succeeds.

## Why it is assayed

Every gate passed at the pin. Grok loads the one skill (`exa-search`), the one command (`tutorial`) and the hosted server `exa` at `https://mcp.exa.ai/mcp/oauth`. In a clean home the server starts and then refuses the handshake until OAuth: the `www-authenticate` header names `https://mcp.exa.ai/.well-known/oauth-protected-resource/mcp/oauth`, which answers with resource `https://mcp.exa.ai/mcp/oauth` and authorization server `https://auth.exa.ai`. That matches the README and the skill. xAI's catalog pins this same commit.

There is no license file. The repository has never had one. GitHub's license API returns 404, and the repository metadata has `license: null`. The only statement left at the pin is `"license": "MIT"` in `.grok-plugin/plugin.json`. The README used to end with a License section whose whole text was the word MIT; [6860457](https://github.com/exa-labs/exa-grok-plugin/commit/6860457f6fc8d210a71c8d7bdc215fb487683214) (2026-07-21, "drop license section") removed it, so the README at the pin states no license. The rubric treats a license stated only in the manifest, with no license file, as a fracture (K-01). Gold requires a license file, so the level stops at assayed. It is not "no license at all": the manifest still names MIT, which is why the entry is admitted rather than left on watch. A `LICENSE` file at the pin would let a re-assay consider gold.

The other open fracture is the security rule. `rules/security.md` says fetched pages are untrusted, tells the agent not to follow instructions found in them, and says not to put credentials in queries. Grok does not load a plugin `rules/` directory. `grok inspect` lists the skill, the command and the server, and does not list `exa-security` (K-03). Copying that file into the Grok home's `rules/` directory makes inspect list it; that workaround ran at the pin. The rest are hairlines: the README and the tutorial say `/mcp`, and the name alone does not install in a clean home (K-02); the skill writes `./exa-results/` and may fall back to another fetch tool, which the README does not say (K-04).

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. `exa-search` tells the agent to dispatch subagents that call `web_search_exa` and `web_fetch_exa`, and, when the answer is longer than one screen, to write `./exa-results/<topic>-<YYYY-MM-DD>` ([SKILL.md:165](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/SKILL.md#L165)). `references/searching.md` says not to use Bash, Grep, Read or Write to process results, and, if `web_fetch_exa` fails, to fetch with any other fetch tool ([searching.md:7](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/references/searching.md#L7), [line 82](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/references/searching.md#L82)). `/tutorial` tells the agent to run a live search for "latest news about xAI" and to fetch `https://exa.ai` ([tutorial.md:17](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/commands/tutorial.md#L17), [line 25](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/commands/tutorial.md#L25)).
- **MCP servers:** `exa`, type `http`, at `https://mcp.exa.ai/mcp/oauth`, with header `x-exa-source: grok-build` ([.mcp.json:5](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/.mcp.json#L5)). Nothing is installed locally. The note on that server names two tools, `web_search_exa` and `web_fetch_exa`. Which tools the signed-in server lists was not assessed: the handshake stops at OAuth.
- **Network:** the hosted MCP server receives search queries and URLs. Sign-in is OAuth against `https://auth.exa.ai` (issuer, authorization and token endpoints in its metadata; PKCE `S256`; scope `mcp:tools`). The skill's fallback can send a URL to whatever other fetch tool the session has (K-04). The source header is sent on the MCP connection.
- **Disclosed in its README:** partly. The README names Exa's hosted server, the two tools, the `exa-search` skill and browser sign-in ([README.md:5](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/README.md#L5), [line 37](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/README.md#L37)). It does not name the server URL, the source header, the `./exa-results/` write, the fallback fetch, or `rules/security.md`.

## Assay

Grok's slash-command names are from the user guide grok 1.0.46 writes into a fresh `GROK_HOME` (`docs/user-guide/04-slash-commands.md`). OAuth metadata was read with plain HTTPS GET on 2026-10-04.

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `879fae0`, clean `GROK_HOME` and `HOME`: `No plugins installed`, `No marketplace sources configured` |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 1 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/exa-labs/exa-grok-plugin.git@879fae0c814765c43f39ea8f56aae1d44e9d9bc8 --trust`: `Installed 1 plugin(s) ... exa`; the registry records commit `879fae0c814765c43f39ea8f56aae1d44e9d9bc8` |
| Gate: details | pass | `exa v1.1.0`, `components: 1 skill dir(s), 1 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skill `exa-search`, command `tutorial`, MCP server `exa` (`http`, `https://mcp.exa.ai/mcp/oauth`); same counts as the files on disk. `rules/security.md` is not listed (K-03) |
| MCP server under Grok | starts, sign-in needed | from an empty folder, `grok mcp doctor exa`: `plugin: exa 1 server`, `server started (0.3s)`, then `handshake failed (... Auth required ...)`. The header is `Bearer resource_metadata="https://mcp.exa.ai/.well-known/oauth-protected-resource/mcp/oauth"`. That URL answers 200 with `authorization_servers: ["https://auth.exa.ai"]` and `scopes_supported: ["mcp:tools"]`. `https://auth.exa.ai/.well-known/oauth-authorization-server` answers 200 with issuer `https://auth.exa.ai` and `code_challenge_methods_supported: ["S256"]` |
| xAI catalog pin | same commit | [xai-org/plugin-marketplace@77a16ec](https://github.com/xai-org/plugin-marketplace/blob/77a16ec85ded1c3b133f686bd2e1bea36090e124/.grok-plugin/marketplace.json#L196) pins `879fae0c814765c43f39ea8f56aae1d44e9d9bc8`, which is also `main` HEAD of exa-labs/exa-grok-plugin on the assay date. This card pins that same SHA |
| Reading: promises against components | pass | the README's one skill, two tools and hosted server are what Grok loads; the sign-in command name is wrong (K-02) |
| Reading: license | fracture | no license file in the [tree at the pin](https://github.com/exa-labs/exa-grok-plugin/tree/879fae0c814765c43f39ea8f56aae1d44e9d9bc8), and `git log --all --diff-filter=A` shows none was ever added; `gh api repos/exa-labs/exa-grok-plugin/license` returns `Not Found (HTTP 404)` and the repo object's `license` is null; `"license": "MIT"` is only in the manifest ([plugin.json:11](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/.grok-plugin/plugin.json#L11)); the README License section was removed in [6860457](https://github.com/exa-labs/exa-grok-plugin/commit/6860457f6fc8d210a71c8d7bdc215fb487683214) (K-01) |
| Reading: what it can execute | partial | results files and a fallback fetch are not in the README (K-04); the security rule is not loaded (K-03) |
| Reading: maintenance | last push 2026-07-27, 0 open issues, 0 open pull requests, 2 stars | GitHub API, 2026-10-04. The tracker holds two merged pull requests ([#1](https://github.com/exa-labs/exa-grok-plugin/pull/1), [#2](https://github.com/exa-labs/exa-grok-plugin/pull/2)) and no issues |
| README install line | fails in a clean home | `grok plugin install exa --trust`: `No marketplace plugin named "exa" in any registered marketplace` (K-02). The pinned URL install above passes |
| Hands | not run | a Grok session costs model time, and the server needs an Exa account; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | There is no license file at the pin, and there has never been one. GitHub reports no license. The manifest says MIT, and the README no longer says anything: its License section, whose entire text was the word MIT, was removed. | [tree at the pin](https://github.com/exa-labs/exa-grok-plugin/tree/879fae0c814765c43f39ea8f56aae1d44e9d9bc8), [.grok-plugin/plugin.json:11](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/.grok-plugin/plugin.json#L11), [6860457](https://github.com/exa-labs/exa-grok-plugin/commit/6860457f6fc8d210a71c8d7bdc215fb487683214); `gh api repos/exa-labs/exa-grok-plugin/license`: `Not Found (HTTP 404)`; repo `license` is null | fracture | new (the tracker holds only the two merged pull requests) | add an MIT `LICENSE` at the root if MIT is the grant, and point the README at it, small | drafted ([seal](../seals/exa/K-01.md)) |
| K-02 | The README and `/tutorial` tell the user to open `/mcp` and press `i`. Grok's command is `/mcps`. The README's install is "find exa in the marketplace"; in a clean home with no marketplace registered, `grok plugin install exa --trust` fails. The command file is `commands/tutorial.md`, so Grok loads it as `/tutorial`. | [README.md:24](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/README.md#L24), [line 29](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/README.md#L29), [tutorial.md:11](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/commands/tutorial.md#L11); grok 1.0.46 user guide `04-slash-commands.md` headings `/marketplace` (line 232) and `/mcps` (line 359), no `/mcp` heading; `grok inspect` names the command `tutorial`; name-only install: `No marketplace plugin named "exa" in any registered marketplace` | hairline | new (the tracker holds only the two merged pull requests) | say `/mcps`, give the pinned install line, and name the command `exa-tutorial`, small | drafted ([seal](../seals/exa/K-02.md)) |
| K-03 | The prompt-injection and credential rules live in `rules/security.md`. Grok does not load a plugin `rules/` directory (it scans project `.grok/rules/`, `.claude/rules/`, `.cursor/rules/`, and `$GROK_HOME/rules/`), so those rules are not in the session. | [rules/security.md:10](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/rules/security.md#L10); `grok inspect --json` lists `exa-search`, `tutorial` and server `exa`, and does not list `exa-security`; grok 1.0.46 user guide `12-project-rules.md` line 30 | fracture | new (the tracker holds only the two merged pull requests) | put the rules in the skill Grok loads, small | drafted ([seal](../seals/exa/K-03.md)); workaround run at the pin |
| K-04 | The README does not say that a long answer is written under `./exa-results/`, that a failed `web_fetch_exa` falls back to any other fetch tool, or that the MCP connection sends `x-exa-source: grok-build`. `searching.md` forbids Claude's Bash, Grep, Read and Write, while `SKILL.md` tells the agent to write that results file. `/tutorial` lists GitHub as a category; the skill's category list is company, research paper, news, personal site and people. | [SKILL.md:165](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/SKILL.md#L165), [searching.md:7](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/references/searching.md#L7), [line 35](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/references/searching.md#L35), [line 82](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/skills/exa-search/references/searching.md#L82), [.mcp.json:7](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/.mcp.json#L7), [tutorial.md:19](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/commands/tutorial.md#L19), [README.md:33](https://github.com/exa-labs/exa-grok-plugin/blob/879fae0c814765c43f39ea8f56aae1d44e9d9bc8/README.md#L33) | hairline | new (the tracker holds only the two merged pull requests) | name the write, the fallback and the header in the README, and use one tool list and one category list, small | drafted ([seal](../seals/exa/K-03.md), same draft) |

## Workarounds

- **K-01:** the only license statement at this pin is `"license": "MIT"` in the manifest linked above. The repository does not contain the MIT text. Until a `LICENSE` file lands, read the grant the manifest names at [opensource.org/license/mit](https://opensource.org/license/mit). That page is not a file in this repository, and this workaround was not a substitute for one.
- **K-03:** copy the plugin's `rules/security.md` into the Grok home so Grok loads it as a global rule. After installing the pin, the plugin directory is under the Grok home's `installed-plugins/`:

  ```bash
  mkdir -p "${GROK_HOME:-$HOME/.grok}/rules"
  cp /path/to/exa-grok-plugin/rules/security.md "${GROK_HOME:-$HOME/.grok}/rules/exa-security.md"
  ```

  Run at the pin, in the clean home: `grok inspect --json` then listed that file as a global rules instruction (`fileType: rules`, 773 bytes). It did not list the copy inside the plugin. A session was not run, so this shows that the text is loaded, not that the model follows it. Delete the file to undo it.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
