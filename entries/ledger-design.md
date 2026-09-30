# ledger-design

Double-entry ledger design for financial systems: account taxonomy, immutable journal events, a balance invariant the database enforces, materialized balances, compensating corrections, multi-currency and rounding, and reconciliation against payment providers.

| | |
|---|---|
| Level | **gold** |
| Domain | Fintech |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/LICENSE) |
| Source | [HermeticOrmus/LibreFinTech-Claude-Code](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/tree/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design) (`plugins/ledger-design`) |
| Pinned SHA | `b49616e8c836a5bfe1cef51681fc5b9058bceab7` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Engineers building the system of record for money: a payments platform, a marketplace with payouts, a wallet, or anything that must answer "where did this dollar go" during an audit.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install ledger-design@liquid-gold-grok
```

## Why it is gold

This assay ran the plugin's SQL instead of trusting it, and found a real fracture: the agent's event table carries `CHECK (false)`, which PostgreSQL applies to inserts too, so the table rejects every event (K-04). The seal is in this card and was run at the pin: the `/ledger` command's own schema, plus one immutability trigger, accepts a balanced event, rejects an unbalanced one at commit, and refuses updates, on PostgreSQL 17.11. The upstream fix is drafted. The release gold is also in the vessel: before v1.0.0 none of the pack's plugins loaded, and this one carried two generations of every file; release [#2](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/pull/2) sealed both. The plugin executes nothing on its own.

## What it can execute

- **Hooks:** none. (The pack's optional `libre-fintech-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none. The SQL, TypeScript and Python in the files are reference code for your system.
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** nothing to disclose.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `b49616e`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreFinTech-Claude-Code.git@b49616e...#plugins/ledger-design --trust`: `Installed 1 plugin(s) ... ledger-design` |
| Gate: details | pass | `ledger-design v1.0.0 (subdir: plugins/ledger-design)`, the install registry records commit `b49616e`; the installed folder holds 1 skill, 1 agent, 1 command |
| Reading: promises against components | pass | the plugin README names the `ledger-architect` agent, the `/ledger` command and the `ledger-design` skill ([README.md:17](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/README.md#L17)); all load. The plugins it defers to (`pricing-engines`, `financial-reporting`) exist in the same marketplace |
| Reading: the SQL, run | one fracture, sealed in this card | the agent's schema ([agents/ledger-architect.md:32](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/agents/ledger-architect.md#L32) to :42) fails its first insert on PostgreSQL 17.11; the command's schema ([commands/ledger.md:112](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/commands/ledger.md#L112) to :172) works, see Workarounds |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 4 open issues and pull requests, 1 star | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay. The SQL was run in a throwaway PostgreSQL 17.11 container, which is evidence about the code, not about a Grok session |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | None of the pack's plugins loaded after `./setup.sh`: it copied folders into `~/.claude/plugins`, and the agents and commands sat in a nested layout the loader does not read. | [CHANGELOG.md:5](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/CHANGELOG.md#L5), [:24](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/CHANGELOG.md#L24) | break | release PR #2 | a marketplace, a `plugin.json` per plugin, the flat layout, large | sealed #2 |
| K-02 | ledger-design carried two generations of every file: a nested and a flat `ledger-architect`, two `/ledger` commands, and a `ledger-patterns` skill beside `ledger-design`. | [CHANGELOG.md:19](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/CHANGELOG.md#L19) | hairline | release PR #2 | merged into one file each, every section kept, medium | sealed #2 |
| K-03 | The agent was pinned to `sonnet` instead of the session's model. | [CHANGELOG.md:17](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/CHANGELOG.md#L17) | hairline | release PR #2 | `model: inherit`, small | sealed #2 |
| K-04 | The agent's `ledger_events` table declares `CHECK (false)`, meant to block updates; PostgreSQL applies check constraints to inserts too, so the table rejects every event. | [agents/ledger-architect.md:41](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/agents/ledger-architect.md#L41); on PostgreSQL 17.11: `ERROR: new row for relation "ledger_events" violates check constraint "events_immutable"` | fracture | new | a `BEFORE UPDATE OR DELETE` trigger instead, small ([draft](../seals/ledger-design/K-04.md)) | sealed (card, run at the pin); upstream drafted |
| K-05 | The agent defines `check_event_balanced()` but never attaches it, while its text says an unbalanced event rolls the transaction back. The command attaches it correctly. | [agents/ledger-architect.md:54](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/agents/ledger-architect.md#L54), [:69](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/agents/ledger-architect.md#L69); compare [commands/ledger.md:169](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/commands/ledger.md#L169) | hairline | new | add the deferred constraint trigger to the agent, small ([draft](../seals/ledger-design/K-04.md)) | drafted |
| K-06 | The plugin says "integer minor units always", but its skill and the command's Core Schema store `NUMERIC(38, 10)` amounts in major units, so it can hand you either convention. | [README.md:37](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/README.md#L37), [agents/ledger-architect.md:22](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/agents/ledger-architect.md#L22) against [skills/ledger-design/SKILL.md:248](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/skills/ledger-design/SKILL.md#L248) and [commands/ledger.md:332](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/commands/ledger.md#L332) | hairline | new | state one rule and name the other as the multi-currency option, small ([draft](../seals/ledger-design/K-04.md)) | drafted |
| K-07 | The repository README installs only through Claude Code; no Grok line. | [README.md:107](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/README.md#L107) (`/plugin marketplace add`, `claude plugin marketplace add`; the README never mentions Grok) | hairline | held by HermeticOrmus ([#6](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/issues/6), PR [#7](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/pull/7)) | add the Grok install, small | open |

## Workarounds

K-04, run at the pin on PostgreSQL 17.11: take the schema from the `/ledger` command (steps 4 and 5, [commands/ledger.md:112](https://github.com/HermeticOrmus/LibreFinTech-Claude-Code/blob/b49616e8c836a5bfe1cef51681fc5b9058bceab7/plugins/ledger-design/commands/ledger.md#L112) to :172), not the agent's inline block, and add an immutability trigger:

```sql
CREATE OR REPLACE FUNCTION forbid_change() RETURNS TRIGGER AS $$
BEGIN RAISE EXCEPTION 'ledger rows are immutable'; END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER trg_events_immutable BEFORE UPDATE OR DELETE ON ledger_events
FOR EACH ROW EXECUTE FUNCTION forbid_change();
```

Recorded result: a balanced two-line event committed; a one-line event failed at commit with `Event 2 is not balanced for currency USD (net: 10000)`; `UPDATE ledger_events` failed with `ledger rows are immutable`; the table held 1 event and 2 entries afterwards.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
