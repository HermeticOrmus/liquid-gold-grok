# mattpocock-skills

Matt Pocock's skills for engineering with an agent: grilling sessions that pin down what you mean, specs and tracer-bullet tickets, test-driven development, bug diagnosis loops, code review against standards and spec, deep-module design, handoffs and teaching.

| | |
|---|---|
| Level | **gold** |
| Domain | Engineering workflow |
| Author | [Matt Pocock](https://www.aihero.dev) |
| License | [MIT](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/LICENSE) |
| Source | [mattpocock/skills](https://github.com/mattpocock/skills/tree/d81f3a183412e71a5b1e84ca21bc1a35eea03a60) |
| Pinned SHA | `d81f3a183412e71a5b1e84ca21bc1a35eea03a60` (committed 2026-09-29, version 1.2.3) |
| Components at the pin | skills 27, agents 0, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Developers who lose time to an agent that built the wrong thing: these skills make it ask first, share your vocabulary, work in vertical slices, and review its own diff before it commits.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install mattpocock-skills@liquid-gold-grok
```

Then run `/setup-matt-pocock-skills` once per repository, as the README says.

## Why it is gold

Every gate passed at the pin, the plugin executes nothing on its own, and the 27 skills the README lists are exactly the 27 the manifest declares and Grok loads. The vessel already carries gold, and two of its seals matter to a Grok user. The subagent steps in `code-review`, `codebase-design` and `improve-codebase-architecture` used to name Claude Code's own tools and agent types, which other agents cannot follow; [#781](https://github.com/mattpocock/skills/pull/781) made them harness-neutral. `diagnosing-bugs` had the agent paste commands and captured output with secrets in them; [#779](https://github.com/mattpocock/skills/pull/779) added a Redact step. The one skill that writes Claude Code settings, `git-guardrails-claude-code`, lives in `skills/misc/`, outside the manifest, so Grok does not load it. What is left open is a hairline: the README names Claude Code and skills.sh and not Grok.

## What it can execute

- **Hooks:** none.
- **Scripts:** none that run on their own. Two skills ship templates the agent copies and adapts: `diagnosing-bugs/scripts/hitl-loop.template.sh` (a human-in-the-loop repro loop) and `wizard/template.sh` (a bash wizard for steps only you can do). `setup-matt-pocock-skills` edits `AGENTS.md` or `CLAUDE.md`, whichever the repository already has ([SKILL.md:76](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/setup-matt-pocock-skills/SKILL.md#L76)).
- **MCP servers:** none.
- **Network:** none from the plugin. `research` asks the agent to read primary sources with its own web tools.
- **Disclosed in its README:** yes. Each skill is listed with what it does ([README.md:184](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/README.md#L184)). The README describes the setup step by its questions; the skill itself shows a draft of every file it will write and lets you edit it first ([SKILL.md:63](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/setup-matt-pocock-skills/SKILL.md#L63)).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `d81f3a1`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 27 skill dir(s), 0 command dir(s), 0 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/mattpocock/skills.git@d81f3a1... --trust`: `Installed 1 plugin(s) ... mattpocock-skills` |
| Gate: details | pass | `mattpocock-skills v1.2.3`, `components: 27 skill dir(s), 0 command dir(s), 0 agent dir(s)` |
| Reading: promises against components | pass | the README Reference lists 27 skills ([README.md:184](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/README.md#L184)); the manifest declares the same 27 ([.claude-plugin/plugin.json](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/.claude-plugin/plugin.json)) and all load |
| Reading: license | pass | MIT, `LICENSE` at the root (Copyright 2026 Matt Pocock), `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | templates only; one setup skill edits your agent instruction file, as documented |
| Reading: maintenance | last push 2026-09-29, 539 open issues, 272,891 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The subagent-dispatch steps in `code-review`, `codebase-design` and `improve-codebase-architecture` named Claude Code's tools and agent types, so other agents could not follow them. | [#781](https://github.com/mattpocock/skills/pull/781) (merged 2026-08-06), [CHANGELOG.md:13](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/CHANGELOG.md#L13) | fracture | merged upstream #781 | harness-neutral wording, small | sealed |
| K-02 | `diagnosing-bugs` had the agent show commands, output and captured artifacts without redacting secrets. | [#779](https://github.com/mattpocock/skills/pull/779) (merged 2026-08-06), [diagnosing-bugs/SKILL.md:12](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/skills/engineering/diagnosing-bugs/SKILL.md#L12) | fracture | merged upstream #779 | a Redact section, small | sealed |
| K-03 | The installation section covers the Claude Code plugin and `npx skills`; there is no Grok Build line, though the plugin installs and loads all 27 skills in Grok. | [README.md:25](https://github.com/mattpocock/skills/blob/d81f3a183412e71a5b1e84ca21bc1a35eea03a60/README.md#L25) | hairline | new (no issue asks for Grok install docs) | add a Grok Build install line, small | drafted ([seal](../seals/mattpocock-skills/K-03.md)) |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
