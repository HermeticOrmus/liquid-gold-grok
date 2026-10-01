# sprites

Fly.io's Grok Build plugin for Sprites: isolated, persistent Linux machines for agent work, driven through Fly.io's hosted MCP server with OAuth. Three skills cover creating sprites, running commands and tests in them, services with URLs, checkpoints, network policy, a status check and a smoke test.

| | |
|---|---|
| Level | **assayed** |
| Domain | Remote compute |
| Author | [Fly.io](https://fly.io) |
| License | [MIT](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/LICENSE) |
| Source | [superfly/sprites-grok-plugin](https://github.com/superfly/sprites-grok-plugin/tree/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2) |
| Pinned SHA | `0b6adb56ce17d85e73dcdf67514e9046d79b6ac2` (committed 2026-08-05, version 0.2.0) |
| Components at the pin | skills 3, agents 0, commands 0, hook events 0, MCP servers 1 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Grok users who want risky or heavy work off their own machine: running generated code, long test suites, dependency installs, or a dev server with a URL, in a sandbox they can checkpoint and restore. It needs a Fly.io account with Sprites, and Fly.io bills sprite usage.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install sprites@liquid-gold-grok
```

Then say "List my sprites." and finish the browser sign-in. On the consent screen, keep a restricted name prefix (the default is `mcp-`) unless you mean to give the agent every sprite in the organization.

## Why it is assayed

Every gate passed at the pin, nothing runs on the local machine on its own, and the plugin was written for Grok: its README uses Grok's own commands (`grok mcp doctor`, `/mcps`, `/plugins`), and its skills name Grok's tool search and `run_terminal_command`. It installs, both slash skills and the main skill load, and the hosted server behaves the way the README says it will before sign-in: `grok mcp doctor sprites` reports `server started` and then an `Auth required` handshake, which the README's table lists as a good install waiting for browser sign-in ([README.md:46](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L46)). The server answers with a proper OAuth challenge and its metadata is live.

The safety work is the reason to admit it. The skills fail closed when the server is missing or not signed in, and forbid the shortcuts an agent reaches for: installing the CLI, raw calls to the API, a second MCP server, invented tokens ([SKILL.md:60](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/SKILL.md#L60)). Destroy, restore, network widening and public exposure each need the user's yes ([safety.md:3](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/safety.md#L3)). The README explains the OAuth trade-off plainly: a restricted prefix limits the agent to its own sprites, and "Full access" means every sprite in the organization. Even the two attribution headers the plugin sends are documented, with the reason for each value. The repository's own checks pass at the pin.

One fracture keeps it from gold. The skills tell the agent to prefer a sprite for heavy builds and tests, and to create one without asking, while neither the README nor the skills say that sprites cost money (K-02). Spending the user's money on the agent's own judgment is wrong behavior, so this is a fracture; Grok's default permission prompt is the guard at the pin, and the workaround below was not run in a session. One hairline is open: the README calls xAI's marketplace the canonical listing, but the listing is still a pull request there (K-01, held by Fly.io).

## What it can execute

- **Hooks:** none.
- **Scripts:** none for Grok. `scripts/check_repository.py` and `tests/` are the repository's CI checks; Grok does not load them. To put a file on a sprite, the skills have the agent base64-encode it with a local `python3 -c` and decode it on the sprite through `exec` ([files.md:40](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/files.md#L40)).
- **MCP servers:** `sprites`, type `http`, at `https://sprites.dev/mcp`, with OAuth, a 300-second tool timeout and two static headers, `Fly-Client-Agent: grok` and `Fly-Client-Interactive: false` ([.grok-plugin/mcp.json](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/.grok-plugin/mcp.json)). Whether Grok sends the headers was not observed.
- **Network:** the hosted server, which runs commands in the user's sprites on Fly.io. Whatever the agent copies or clones into a sprite leaves the machine, and sprite services can serve public URLs. Fly.io bills CPU, RAM and storage for active sprites ([sprites.dev](https://sprites.dev), pricing FAQ, read 2026-10-01).
- **Disclosed in its README:** yes for what runs: the hosted server and OAuth ([README.md:5](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L5)), the attribution headers ([README.md:133](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L133)), how files reach a sprite ([README.md:126](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L126)), public URLs and permanent destroy ([README.md:173](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L173)). Cost is not mentioned (K-02).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `0b6adb5`, clean `GROK_HOME` and `HOME` (`No plugins installed`, `No marketplace sources configured`) |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `Installed 1 plugin(s) from https://github.com/superfly/sprites-grok-plugin.git@0b6adb5...: sprites`; the registry records commit `0b6adb56ce17d85e73dcdf67514e9046d79b6ac2`. The README's `grok plugin install superfly/sprites-grok-plugin --trust` installs the same commit |
| Gate: details | pass | `sprites v0.2.0`, `components: 1 skill dir(s), 0 command dir(s), 0 agent dir(s), MCP servers` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 3 (`sprites`, `sprites-status`, `sprites-smoke`), MCP server `sprites` (http), the same as the files on disk; the plugin is `"enabled": true` right after install |
| MCP server under Grok | pass, as documented | `grok mcp doctor sprites`: `server started`, then `handshake failed (... Auth required, when send initialize request)`; the server answers `401` with `www-authenticate: Bearer resource_metadata="https://sprites.dev/.well-known/oauth-protected-resource", scope="sprites:read sprites:write"`, and that metadata URL answers 200 |
| Repository checks | pass | `python3 scripts/check_repository.py`: `Validated 21 repository files.`; `python3 -m unittest discover --start-directory tests`: `Ran 6 tests`, `OK` |
| Reading: promises against components | pass | the README names the hosted server, the main skill and two slash skills ([README.md:50](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L50)); all load |
| Reading: license | pass | MIT, `LICENSE` at the root (Copyright 2026 Fly.io, Inc.), `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | one hosted server with OAuth and documented static headers; no local code runs on its own |
| Reading: maintenance | last push 2026-08-05, 0 open issues, 0 open pull requests, 1 star | GitHub API, 2026-10-01 |
| Hands | not run | a Grok session costs model time, and a real run needs a Fly.io account that is billed for sprite usage |

Grok's behavior is cited from Grok's user guide (grok 1.0.44 writes it into every fresh `GROK_HOME`; the links go to the same text in xai-org/grok-build at `2bdd1d6`).

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The README says the canonical marketplace listing is maintained in `xai-org/plugin-marketplace`, but xAI's catalog has no `sprites` entry; Fly.io's pull request there is open, and it pins `a696ac3`, a commit from before the attribution headers. | [README.md:79](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/README.md#L79); [xAI catalog at b315f7d](https://github.com/xai-org/plugin-marketplace/blob/b315f7de89fd2215c1dd0dc8665bc84e55fa4611/.grok-plugin/marketplace.json) (30 plugins, no `sprites`); [xai-org/plugin-marketplace#120](https://github.com/xai-org/plugin-marketplace/pull/120), opened 2026-07-20 | hairline | held by Fly.io ([xai-org/plugin-marketplace#120](https://github.com/xai-org/plugin-marketplace/pull/120)) | #120 merged at this commit or a newer one, small | open (held in #120) |
| K-02 | The skills tell the agent to prefer a sprite on its own judgement when builds, tests or installs "would pollute or overload the local machine", and to create one without asking; destroy, restore, network and exposure need a yes, creating does not. Fly.io bills sprite CPU, RAM and storage, and neither the README nor the skills mention cost, apart from "Sprites can idle cheaply". Grok's default permission mode asks before tools that are not read-only, which is the guard at the pin. | [SKILL.md:25](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/SKILL.md#L25), [line 29](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/SKILL.md#L29), [compute.md:13](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/compute.md#L13), [compute.md:20](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/compute.md#L20), [compute.md:58](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/compute.md#L58), [safety.md:3](https://github.com/superfly/sprites-grok-plugin/blob/0b6adb56ce17d85e73dcdf67514e9046d79b6ac2/skills/sprites/references/safety.md#L3); pricing: [sprites.dev](https://sprites.dev) FAQ ("CPU, RAM, and hot storage, metered per hour of active use"); Grok: [22-permissions-and-safety.md:35](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md#L35) | fracture | new (the tracker holds only the two merged pull requests) | a cost line in the README, and ask before creating a sprite the user did not ask for, small | drafted ([seal](../seals/sprites/K-02.md)) |

## Workarounds

- **K-02:** keep Grok's default permission mode, which asks before tools that are not read-only, so creating a sprite waits for your yes ([22-permissions-and-safety.md:35](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/22-permissions-and-safety.md#L35)); do not run this plugin with an always-approve mode. To keep work local unless you ask, add to the project's `AGENTS.md`: "Use Sprites only when I ask for a sprite or a sandbox." Neither was tested in a Grok session, so K-02 stays drafted.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
