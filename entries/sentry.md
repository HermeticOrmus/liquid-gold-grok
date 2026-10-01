# sentry

Sentry's own skills for working with Sentry from Grok: getting started and SDK instrumentation for any platform, debugging a production issue through to a fix, readable stack traces (source maps and debug files), releases and suspect commits, alerts, OpenTelemetry Collector routing and Apple snapshot testing, plus Sentry's hosted MCP server.

| | |
|---|---|
| Level | **assayed** |
| Domain | Error monitoring |
| Author | [Sentry](https://sentry.io) |
| License | [MIT](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/LICENSE) |
| Source | [getsentry/plugin-grok](https://github.com/getsentry/plugin-grok/tree/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67) |
| Pinned SHA | `3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67` (committed 2026-09-30, version 1.4.1) |
| Components at the pin | skills 8, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers who run Sentry and want Grok to set up the SDK, pull an issue's stack trace, breadcrumbs and trace through the MCP server, fix it with a test, and close it with a `Fixes PROJECT-NAME-12A` commit.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install sentry@liquid-gold-grok
```

The MCP server signs in with OAuth: open `/mcps`, select `sentry` and press `i` (Grok's MCP guide documents `i` for OAuth servers).

## Why it is assayed

Every gate passed at the pin and Grok loads everything the plugin ships: 8 skills and the hosted MCP server, which answers an unauthenticated handshake with an OAuth challenge. The repository is generated from [getsentry/sentry-for-ai](https://github.com/getsentry/sentry-for-ai), and all 8 skills match that source at [`9813087`](https://github.com/getsentry/sentry-for-ai/tree/98130873715020f94a48236637f2ef305aba4c68/src/skills) byte for byte.

One fracture is open, and Sentry already holds it. `sentry-create-alert` lists the auth token as a detail to ask the user for and writes it into `curl` commands as `Authorization: Bearer {token}`, so a token with `alerts:write` goes into the conversation, the model's context and the process list (K-01). The plugin's own token reference says every tool reads `SENTRY_AUTH_TOKEN` and the value is never printed. Open pull request [#338](https://github.com/getsentry/sentry-for-ai/pull/338), by a Sentry maintainer, replaces the skill with `sentry-create-monitor`, which reads the token from the environment. The workaround below keeps the token out of the chat at this pin. The other four cracks are hairlines: the README describes code-review and router skills that upstream removed (K-02), every skill says Apache-2.0 while the license file says MIT (K-03), the getting-started skill makes onboarding progress calls without narrating them (K-04), and setup steps fetch installers at `@latest` (K-05). When #338 merges, a re-assay at the new pin can move this entry to gold.

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. The skills tell the agent to run Sentry's tools on request: `npx @sentry/wizard@latest -i <platform>` for SDK and source-map setup ([debug-artifacts/javascript.md:71](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-instrument/references/debug-artifacts/javascript.md#L71)), `sentry-cli` for uploads and releases, `curl` against the Sentry API in `sentry-create-alert` to look up members, teams and integrations and to create, update and delete alert workflows ([SKILL.md:46](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-create-alert/SKILL.md#L46)), `pip install` and `npm install` for OpenTelemetry, and a `curl` download of the OpenTelemetry Collector from GitHub releases ([sentry-otel-exporter-setup/SKILL.md:95](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-otel-exporter-setup/SKILL.md#L95)). The Apple snapshot CI templates it writes install `sentry-cli` with `curl -sL https://sentry.io/get-cli/ | bash` inside GitHub Actions ([github-actions-simple.md:86](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-snapshots-cocoa/references/github-actions-simple.md#L86)). `sentry-debug-issue` resolves issues through commits and says not to push or open a PR unless the user asked ([SKILL.md:147](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-debug-issue/SKILL.md#L147)).
- **MCP servers:** `sentry`, type `http`, at `https://mcp.sentry.dev/mcp?utm_source=plugin` ([.mcp.json](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/.mcp.json)). Nothing is installed locally. Its OAuth resource metadata lists the scopes `org:read`, `project:write`, `team:write`, `event:write` and `alerts:write`.
- **Network:** the hosted MCP server; the `utm_source=plugin` tag attributes that traffic to the plugin, as sentry-for-ai's [TELEMETRY.md](https://github.com/getsentry/sentry-for-ai/blob/98130873715020f94a48236637f2ef305aba4c68/TELEMETRY.md) explains. The Sentry API with the user's token; npm, PyPI and GitHub downloads during setup; onboarding progress calls through the MCP server when the first prompt carries a Sentry onboarding code (K-04).
- **Disclosed in its README:** partly. The README names the setup wizards and the hosted MCP server ([README.md:25](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/README.md#L25)); it does not mention the token step, the onboarding calls or the attribution tag.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `3d0347f`, clean `GROK_HOME` and `HOME`: `No plugins installed`, `No marketplace sources configured` |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/getsentry/plugin-grok.git@3d0347f... --trust`: `Installed 1 plugin(s) ... sentry` |
| Gate: details | pass | `sentry v1.4.1`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 8 and MCP server `sentry` (`http`, `https://mcp.sentry.dev/mcp?utm_source=plugin`), the same as the files on disk |
| MCP server under Grok | starts, sign-in needed | `grok mcp doctor`: `plugin: sentry 1 server`, `server started (0.2s)`, then `handshake failed (... Auth required, when send initialize request)` with the server's OAuth `resource_metadata` URL; expected without a sign-in |
| Reading: promises against components | pass, with a copy crack | the 8 skills in [SKILL_TREE.md](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/SKILL_TREE.md) all load, with the server; the README's code-review and router claims are out of date (K-02) |
| Reading: license | pass, with a copy crack | MIT `LICENSE` at the root (Copyright 2025 Sentry), `"license": "MIT"` in the manifest; skill frontmatter says Apache-2.0 (K-03) |
| Reading: what it can execute | partial | token into the chat (K-01), unnarrated onboarding calls (K-04), unpinned installers (K-05) |
| Reading: maintenance | last push 2026-09-30, 0 open issues, 1 star (the source repository sentry-for-ai: 48 open issues, 269 stars) | GitHub API, 2026-10-01 |
| Hands | not run | a Grok session costs model time, and the skills need a Sentry organization; not run for this assay |

`SKILL_TREE.md` at the root is a router written for agents ("Start Here"). Grok does not load it, because it is not a skill; the 8 skills reach the model through their own descriptions.

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `sentry-create-alert` asks the user for the auth token as a detail and writes it into `curl` command lines, so a token with `alerts:write` lands in the conversation, the model's context and the process list. The plugin's own token reference says every tool reads `SENTRY_AUTH_TOKEN` and never prints it. | [sentry-create-alert/SKILL.md:33](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-create-alert/SKILL.md#L33), [line 47](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-create-alert/SKILL.md#L47), [line 170](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-create-alert/SKILL.md#L170); [auth-token.md:24](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-get-started/references/auth-token.md#L24), [line 38](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-get-started/references/auth-token.md#L38) | fracture | held by getsentry ([#338](https://github.com/getsentry/sentry-for-ai/pull/338), open) | `sentry-create-monitor` reads `$SENTRY_USER_TOKEN` from the environment, medium | open |
| K-02 | The README promises "code review with Sentry context" and router skills that hide the rest behind `disable-model-invocation`. Upstream removed the code-review skills ([#283](https://github.com/getsentry/sentry-for-ai/pull/283), merged 2026-07-13) and the routers ([#311](https://github.com/getsentry/sentry-for-ai/pull/311), merged 2026-08-04). At the pin no skill reviews code, none sets `disable-model-invocation`, and all 8 load for the model; `SKILL_TREE.md` offers a "Review code" path with no skill behind it. | [README.md:5](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/README.md#L5), [line 23](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/README.md#L23), [line 28](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/README.md#L28), [SKILL_TREE.md:13](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/SKILL_TREE.md#L13); source: [src/plugins/grok/README.md:4](https://github.com/getsentry/sentry-for-ai/blob/98130873715020f94a48236637f2ef305aba4c68/src/plugins/grok/README.md#L4) | hairline | new | describe the current 8 skills in `src/plugins/grok/README.md`, drop the review option from `SKILL_TREE.md`, small | drafted ([seal](../seals/sentry/K-02.md)) |
| K-03 | Every skill's frontmatter says `license: Apache-2.0`; the repository `LICENSE`, the manifest and sentry-for-ai itself are MIT. | [sentry-create-alert/SKILL.md:4](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-create-alert/SKILL.md#L4) (line 4 in all 8 skills), [LICENSE](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/LICENSE), [.grok-plugin/plugin.json:10](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/.grok-plugin/plugin.json#L10) | hairline | new | one license in both places, small | drafted ([seal](../seals/sentry/K-03.md)) |
| K-04 | `sentry-get-started` tells the agent to make onboarding progress calls through the MCP server silently, "with no narration", when the first prompt carries a Sentry onboarding code. The calls carry stage statuses and a short note, and the skill forbids source, paths, terminal output, secrets and personal data in them. The README does not mention them. | [sentry-get-started/SKILL.md:23](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-get-started/SKILL.md#L23), [line 38](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-get-started/SKILL.md#L38), [line 52](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-get-started/SKILL.md#L52) | hairline | new | one README line naming the onboarding updates, small | drafted ([seal](../seals/sentry/K-02.md), same draft) |
| K-05 | Setup steps fetch installers at use, unpinned: `npx @sentry/wizard@latest` in the setup references, and `curl -sL https://sentry.io/get-cli/ \| bash` in the Apple snapshot CI templates. | [debug-artifacts/javascript.md:71](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-instrument/references/debug-artifacts/javascript.md#L71), [github-actions-simple.md:86](https://github.com/getsentry/plugin-grok/blob/3d0347fbc4f2bfd39a30c9a2107f52f3efc54d67/skills/sentry-snapshots-cocoa/references/github-actions-simple.md#L86) | hairline | new | pin the wizard and CLI versions in the templates, small | open |

## Workarounds

- **K-01:** keep the token out of the conversation. Put an organization token with `alerts:write` in the environment of the shell that starts Grok, from your secret store, under the name the plugin's other skills use (`SENTRY_AUTH_TOKEN`). Then, when you ask for an alert, tell Grok: "use `$SENTRY_AUTH_TOKEN` in the Authorization header and do not ask me for the token." The token does appear in `curl`'s argument list while each call runs. Not run for this assay: it needs a Sentry organization and a Grok session.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
