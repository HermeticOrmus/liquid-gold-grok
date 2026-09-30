# handoff

Writes a HANDOFF.md at the end of a session: what is done, what is not, the context the diff does not show, a verify command for every "done" claim, open questions, and one specific next step. It indexes the handoff for the `pickup` plugin and puts a resume prompt on the clipboard.

| | |
|---|---|
| Level | **assayed** |
| Domain | Session workflow |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/LICENSE) |
| Source | [HermeticOrmus/LibreSessionFlow-Claude-Code](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/tree/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff) (`plugins/handoff`) |
| Pinned SHA | `c5822d81c207171f2831761e963729f3b59f3739` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone whose work outlives one session: before a context clear, a machine switch, a long break, or a handoff to a teammate, so the next session starts from a file instead of from memory.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install handoff@liquid-gold-grok
```

`/pickup`, the reading half of the contract, is a separate plugin in the same pack.

## Why it is assayed

The command itself is sound, and its one piece of shell was run: the index upsert that `/pickup` depends on keeps one row per handoff path, newest on top. Release [#2](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/pull/2) sealed the old cracks: the plugin never loaded, its skill shared a name with the command, the agent pinned a model, the docs named a `claude --clear` flag that does not exist, and nothing stopped a new handoff from replacing another task's file.

One fracture keeps it at assayed. The skill hands its procedure to the command file through `${CLAUDE_PLUGIN_ROOT}`, and grok 1.0.44 lists that variable for hooks, not among the placeholders it fills in skill text (K-07). The workaround is to run `/handoff` directly, which carries the whole procedure; it could not be checked without a Grok session, and the seal is drafted.

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. `/handoff` tells the agent to run a short shell block that creates or updates `<home>/handoffs/INDEX.md`, where `<home>` is `SESSIONFLOW_HOME`, else `~/.claude/sessionflow` ([commands/handoff.md:104](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/commands/handoff.md#L104) to :116); to rename an existing HANDOFF.md for another task to `HANDOFF.md.bak.<timestamp>` (:39); and to pipe the resume prompt to the first clipboard tool it finds: `wl-copy`, `xclip`, `xsel`, `pbcopy` or `clip.exe` (:122).
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** yes for the index and the clipboard ([README.md:11](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/README.md#L11)); the backup rename is in the command, not the README.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `c5822d8`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code.git@c5822d8...#plugins/handoff --trust`: `Installed 1 plugin(s) ... handoff` |
| Gate: details | pass | `handoff v1.0.0 (subdir: plugins/handoff)`, install registry commit `c5822d8` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 1, agents 1, commands 1 loaded, the same as the files on disk |
| Reading: promises against components | pass, one fracture | the `handoff-engineer` agent, `/handoff` command and `handoff-patterns` skill the README names all load ([README.md:7](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/README.md#L7) to :9); the skill's pointer to the command may not resolve under Grok (K-07) |
| Reading: the index shell block, run | pass | with `SESSIONFLOW_HOME` set to a temporary folder, three runs (path A, path B, path A again) left a header and two rows, the second A on top and the first A gone |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | agent-run shell for the index, the backup and the clipboard, disclosed except the backup |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 0 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay. It is the check K-07 needs |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | Plugins installed with the old `setup.sh` were never loaded: it copied folders that the loader does not read. | [CHANGELOG.md:5](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L5), [:35](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L35) | break | release PR #2 | a marketplace and a `plugin.json` per plugin, large | sealed #2 |
| K-02 | The handoff skill was a loose `skills/handoff.md` that shared its name with the `/handoff` command. | [CHANGELOG.md:28](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L28) | fracture | release PR #2 | moved to `skills/handoff-patterns/SKILL.md`, small | sealed #2 |
| K-03 | The `handoff-engineer` agent pinned a model instead of using the session's. | [CHANGELOG.md:29](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L29); now `model: inherit` ([agents/handoff-engineer.md:4](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/agents/handoff-engineer.md#L4)) | hairline | release PR #2 | `model: inherit`, small | sealed #2 |
| K-04 | The docs told you to run `claude --clear`, which is not a flag; the command is `/clear`. | [CHANGELOG.md:36](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L36) | hairline | release PR #2 | `/clear`, small | sealed #2 |
| K-05 | The handoff docs used one person's machines as examples. | [CHANGELOG.md:37](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L37) | hairline | release PR #2 | generic examples, small | sealed #2 |
| K-06 | A new handoff could replace another task's HANDOFF.md at the same path: the v0.1 command had no check for an existing file. | the v0.1 command (commit `8bd24cf`) has no existing-file step; [CHANGELOG.md:20](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/CHANGELOG.md#L20); now [commands/handoff.md:39](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/commands/handoff.md#L39) renames it to `HANDOFF.md.bak.<timestamp>` first | fracture | release PR #2 | back up, never overwrite silently, small | sealed #2 |
| K-07 | *Inferred*: the skill says to follow `${CLAUDE_PLUGIN_ROOT}/commands/handoff.md`, and grok 1.0.44 lists `$ARGUMENTS`, `${SKILL_DIR}`, `${CLAUDE_SKILL_DIR}`, `${SESSION_ID}` and `${CLAUDE_SESSION_ID}` as skill placeholders and `CLAUDE_PLUGIN_ROOT` only for hooks, so under Grok the model may get a path it cannot open and lose the index and clipboard steps. | [skills/handoff-patterns/SKILL.md:11](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/skills/handoff-patterns/SKILL.md#L11); the placeholder list is in the grok 1.0.44 binary's skill tool | fracture | new; the same root cause is open for the pack's other commands in [PR #6](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/pull/6) (its ledger K-12, which leaves `handoff` out) | point the skill at `${CLAUDE_SKILL_DIR}/../../commands/handoff.md`, small ([draft](../seals/handoff/K-07.md)) | drafted |
| K-08 | The default index lives under `~/.claude/sessionflow`, a Claude Code folder, for Grok users too. | [commands/handoff.md:36](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/commands/handoff.md#L36), [:109](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/commands/handoff.md#L109), [README.md:11](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/README.md#L11) | hairline | new | name `SESSIONFLOW_HOME` in the README as the way to move it, small ([draft](../seals/handoff/K-07.md)) | drafted |
| K-09 | The repository README installs only through Claude Code; no Grok line. | [README.md:84](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/README.md#L84) (`/plugin marketplace add`; the README never mentions Grok) | hairline | held by HermeticOrmus ([#5](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/issues/5), PR [#6](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/pull/6)) | add the Grok install, small | open |

## Workarounds

K-07: run `/handoff` yourself rather than relying on the skill to find it. The command file carries the whole procedure inline: the gap, the location, the template, the draft review, the save, the index and the clipboard. Not yet checked in a Grok session.

K-08: set `SESSIONFLOW_HOME` to the folder you want. Run at the pin: with it set to a temporary folder, the index block wrote `handoffs/INDEX.md` there; the block reads `~/.claude/sessionflow` only when `SESSIONFLOW_HOME` is unset ([commands/handoff.md:109](https://github.com/HermeticOrmus/LibreSessionFlow-Claude-Code/blob/c5822d81c207171f2831761e963729f3b59f3739/plugins/handoff/commands/handoff.md#L109)).

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
