# ponytail

Six skills that push the agent toward the smallest change that works: ask whether the code needs to exist at all, use the standard library and platform features before custom code or new dependencies, mark deliberate shortcuts with a `ponytail:` comment, and review a diff or a whole repo for what to delete.

| | |
|---|---|
| Level | **gold** |
| Domain | Code minimalism |
| Author | [Dietrich Gebert](https://github.com/DietrichGebert) |
| License | [MIT](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/LICENSE) |
| Source | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail/tree/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156) |
| Pinned SHA | `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` (committed 2026-09-14, version 4.10.0 in `.claude-plugin/plugin.json`; the root manifest Grok reads declares no version, K-02) |
| Components at the pin | skills 6, agents 0, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-10-01 with grok 1.0.44 |

## Who it is for

Developers whose agent writes a class where a function would do, adds a dependency for three lines of code, or builds configuration nobody sets. Ponytail keeps the guardrails it names: validation at trust boundaries, error handling that prevents data loss, security, accessibility, anything you asked for explicitly, and one runnable check for non-trivial logic ([SKILL.md:92](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail/SKILL.md#L92)).

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install ponytail@liquid-gold-grok
```

Grok can invoke `ponytail` on its own for coding tasks from the skill description. Type `/ponytail` (or `/ponytail lite`, `/ponytail ultra`) to load it on purpose, and say "stop ponytail" to drop it. Install only from `DietrichGebert/ponytail`: the owner's tracker warns about a trojanized clone that shipped malware ([#735](https://github.com/DietrichGebert/ponytail/issues/735)).

## Why it is gold

Every gate passed at the pin, Grok loads exactly the six skills the README's Grok section names, and in Grok the plugin executes nothing on its own.

The owner already did the Grok reading this library asks for. Ponytail's Claude Code and Codex editions activate through hooks, and before [#661](https://github.com/DietrichGebert/ponytail/pull/661) Grok loaded that hook map too: installed at the parent commit `a2712bc`, `grok inspect` lists `hooks/claude-codex-hooks.json` for ponytail (`SessionStart`, `SubagentStart`, `UserPromptSubmit`), and Grok passes none of those events' output to the model ([10-hooks.md:481](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L481), [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505)). #661 shipped a root `plugin.json` that holds only the name, which Grok reads before `.claude-plugin/plugin.json` ([manifest.rs:1](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/plugins/manifest.rs#L1)), and a test that keeps hooks and MCP servers out of it ([tests/grok-plugin.test.js:12](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/tests/grok-plugin.test.js#L12)). At the pin `grok inspect` lists six skills and no hook file, and the README says why: "Grok lifecycle hooks are not used because their SessionStart output cannot inject instructions" ([README.md:278](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L278)).

One fracture found in this assay, sealed in this card: the repo's Grok marketplace file lists the plugin with `"source": "./"`, which Grok's scanner rejects, so the marketplace route installs nothing (K-03). The README's direct install works at the pin, and a drafted fix with a tested `url` source is ready for the owner. The rest is copy: the README asks Grok users to enable a plugin that `grok plugin install` already enabled (K-04), the portability doc lists a `commands/` folder Grok does not load (K-05), the help card describes hook-host settings that do nothing in Grok (K-06), and the root manifest carries no version, which an open pull request would fix (K-02).

## What it can execute

- **Hooks:** none in Grok. The repo ships hook scripts for Claude Code, Codex, Cursor, Copilot and Qoder under `hooks/`; at the pin Grok does not load them.
- **Scripts:** none that run on their own. `ponytail-debt` tells the agent to run `grep -rnE '(#|//) ?ponytail:' .` and, if you want an owner per row, `git blame` ([SKILL.md:20](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail-debt/SKILL.md#L20)); it writes a `PONYTAIL-DEBT.md` only when you ask. `ponytail-review` and `ponytail-audit` list findings and apply nothing.
- **MCP servers:** none in Grok. The `ponytail-mcp/` server serves other hosts and is not declared to Grok.
- **Network:** none from the plugin.
- **Disclosed in its README:** yes. The Grok Build section states what loads and that hooks are not used ([README.md:265](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L265)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `e3ba2aa`, clean `GROK_HOME` and `HOME`: `No plugins installed.`, `No marketplace sources configured.` |
| Gate: validate | pass | `Plugin manifest is valid.`, `components: 1 skill dir(s), 1 command dir(s), 0 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/DietrichGebert/ponytail.git@e3ba2aa... --trust`: `Installed 1 plugin(s) from https://github.com/DietrichGebert/ponytail.git@e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156: ponytail` |
| Gate: details | pass | `plugins (1): ponytail`, `components: 1 skill dir(s), 1 command dir(s), 0 agent dir(s)`; the registry records commit `e3ba2aa`. No version line, because the root manifest declares none (K-02) |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: 6 skills from `ponytail`, `provides: {skills: 6, agents: 0, hooks: false, mcpServers: 0}` |
| Reading: promises against components | pass | the Grok section names six skills ([README.md:278](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L278)) and all six load. The `commands/` folder holds Gemini CLI `.toml` files that Grok does not load; the same six slash names come from the skills (K-05) |
| Reading: license | pass | MIT, `LICENSE` at the root (Copyright 2026 DietrichGebert), a License section in the README ([README.md:383](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L383)), `"license": "MIT"` in `package.json` |
| Reading: what it can execute | pass | nothing runs on its own in Grok |
| Reading: maintenance | last push 2026-09-14, 112 open issues and 217 open pull requests, 150,211 stars | GitHub API, 2026-10-01 |
| README install line | pass | `grok plugin install DietrichGebert/ponytail --trust` in a clean home: `Installed 1 plugin(s) from DietrichGebert/ponytail: ponytail`; `config.toml` then holds `enabled = ["ponytail"]` |
| Repo marketplace file | fail | `grok plugin marketplace add DietrichGebert/ponytail`, then `grok plugin install ponytail@ponytail --trust`: `Error: No marketplace plugin named "ponytail" in "ponytail".`; with `--debug`: `marketplace index entry 'ponytail' has invalid source path: marketplace path is empty` (K-03) |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Grok loaded the Claude Code hook map from `.claude-plugin/plugin.json` (`SessionStart`, `SubagentStart`, `UserPromptSubmit`) and passes none of those events' output to the model, so the hooks ran on every session and prompt and delivered nothing; the skills still loaded. | [#661](https://github.com/DietrichGebert/ponytail/pull/661) (merged 2026-08-07); installed at parent `a2712bc`, `grok inspect` lists `hooks/claude-codex-hooks.json` for ponytail; at the pin [plugin.json:1](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/plugin.json#L1) and [tests/grok-plugin.test.js:12](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/tests/grok-plugin.test.js#L12); Grok: [10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505) | fracture | merged upstream #661 | a skills-only root manifest that Grok reads first, small | sealed |
| K-02 | The root `plugin.json`, the manifest Grok reads first, holds only `"name"`, so Grok shows no version, description, author or license for ponytail, and `scripts/check-versions.js` does not check that file against the 4.10.0 the other manifests carry. | [plugin.json:1](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/plugin.json#L1), [scripts/check-versions.js:21](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/scripts/check-versions.js#L21); `grok plugin details ponytail` lists `ponytail` with no version | hairline | held upstream: open [#911](https://github.com/DietrichGebert/ponytail/pull/911) (by erwinkramer) fills the root manifest with version, description, author and license | fill the root manifest and add it to `VERSION_FILES`, small | open |
| K-03 | `.grok-plugin/marketplace.json` lists the plugin with `"source": "./"`, which Grok's marketplace scanner rejects as an empty path, so `grok plugin marketplace add DietrichGebert/ponytail` adds a marketplace with nothing to install. | [.grok-plugin/marketplace.json:12](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/.grok-plugin/marketplace.json#L12); `Error: No marketplace plugin named "ponytail" in "ponytail".` and `invalid source path: marketplace path is empty`. On a local copy at the pin, `"."` fails (`must not contain current-directory components`), a `github` source fails ([xai-org/plugin-marketplace#123](https://github.com/xai-org/plugin-marketplace/issues/123)), and `{"source": "url", "url": "https://github.com/DietrichGebert/ponytail.git"}` installs (`Installed 1 plugin(s) from mk: ponytail`) | fracture | new on this tracker; the owner noted the scanner rejection in the #661 commit message ([2ed6c52](https://github.com/DietrichGebert/ponytail/commit/2ed6c52c9d7e5e56942508591085fd45dea277d3)) | a `url` source, small | sealed (card): the README's direct install ran at the pin; fix drafted ([seal](../seals/ponytail/K-03.md)) |
| K-04 | The README tells Grok users the plugin is "off by default" and to enable it in `/plugins` or `config.toml`, but `grok plugin install DietrichGebert/ponytail --trust` wrote `enabled = ["ponytail"]` itself and `grok inspect` lists it as enabled. | [README.md:271](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L271); the clean-home run in the Assay table | hairline | new | say that install enables it, small | drafted ([seal](../seals/ponytail/K-04.md)) |
| K-05 | `docs/agent-portability.md` lists `commands/` among the Grok adapter's files, and `grok plugin validate` counts `1 command dir(s)`, but the folder holds Gemini CLI `.toml` files that Grok does not load (`grok inspect`: 0 commands from ponytail). | [docs/agent-portability.md:13](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/docs/agent-portability.md#L13), [commands/ponytail.toml:1](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/commands/ponytail.toml#L1) | hairline | new | drop `commands/` from the Grok row, small | drafted (same draft as K-04) |
| K-06 | The `ponytail-help` card, which Grok loads, says the default mode is "auto-active every session", that `PONYTAIL_DEFAULT_MODE` or `~/.config/ponytail/config.json` sets it, that `"off"` disables auto-activation on session start, and that updates go through Claude Code's `/plugin`. In Grok nothing loaded reads those settings: only the hook scripts and the root `__init__.py` plugin for another agent host do, and Grok loads neither. The README's general configuration paragraph says the same without naming hosts. | [skills/ponytail-help/SKILL.md:46](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail-help/SKILL.md#L46), [:58](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail-help/SKILL.md#L58), [:65](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/skills/ponytail-help/SKILL.md#L65); readers: [hooks/ponytail-config.js:78](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/hooks/ponytail-config.js#L78), [__init__.py:53](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/__init__.py#L53); [README.md:295](https://github.com/DietrichGebert/ponytail/blob/e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156/README.md#L295) | hairline | new (the open help-card issues, #949 and #648, concern Codex and Claude Code) | a Grok line on the help card, small | drafted (same draft as K-04) |

## Workarounds

- **K-03:** install directly, as the README says: `grok plugin install DietrichGebert/ponytail --trust` (ran at the pin in a clean Grok home). Through this library's marketplace the entry installs at the pinned SHA.
- **K-06:** in Grok, the default-mode settings do nothing. To keep ponytail off in a session, say "stop ponytail"; to keep it off everywhere, run `grok plugin disable ponytail` or turn it off in `/plugins`.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
