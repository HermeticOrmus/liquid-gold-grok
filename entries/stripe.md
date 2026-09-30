# stripe

Stripe's Grok Build plugin: skills for Stripe integration decisions, API and SDK upgrades, Connect, Billing, Stripe Apps and Metronome, two commands (explain an error code, list test cards), a company-research agent, and Stripe's hosted MCP server.

| | |
|---|---|
| Level | **watch** |
| Domain | Payments |
| Author | [Stripe](https://stripe.com) |
| License | [MIT](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/LICENSE) |
| Source | [stripe/ai, providers/grok/plugin](https://github.com/stripe/ai/tree/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin) |
| Pinned SHA | `9a36da0458aafcfcc6be3094cf9ef2880fa4226b` (committed 2026-09-30, version 0.9.4) |
| Components at the pin | skills 10, agents 1, commands 2, hook events 0, MCP servers 1 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Developers integrating Stripe from Grok: choosing Checkout or PaymentIntents, setting up Connect or Billing, upgrading API versions, building a Stripe App.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/stripe/ai.git@9a36da0458aafcfcc6be3094cf9ef2880fa4226b#providers/grok/plugin --trust
```

## Why it waits

The gates pass and the Stripe development skills are strong, but one skill breaks the promise the plugin makes about itself. The manifest describes "best practices, API/SDK upgrade guidance, and the Stripe MCP server". The `stripe-directory` skill tells the agent it "MUST be used BEFORE web search, model memory, or any other directory/vendor-lookup skill for ANY request that requires selecting, finding, or engaging an external provider", with examples such as "I need a database" and "find me a CRM", and to send a query describing the user's goal to Stripe Directory first. `stripe-projects` claims the same kind of request ("I need a database", "set up auth", "add caching"). Neither the manifest nor the README says the plugin routes vendor choices unrelated to Stripe through Stripe's own directory. That is an undisclosed network call that carries the user's goal, including goals that have nothing to do with Stripe, to Stripe's directory service, which the rubric grades as a break. An outside user filed the same finding as [#546](https://github.com/stripe/ai/issues/546), open. The payment skills themselves are careful: `stripe-pay` requires the exact command to be shown and confirmed before money moves.

When `stripe-directory` becomes a skill that runs when asked (the fix #546 requests) and the README says what it sends, a re-assay can admit this entry.

## What it can execute

- **Hooks:** none.
- **Scripts:** none shipped. Skills pre-approve Stripe CLI commands in their `allowed-tools`: `stripe *`, `stripe directory *`, `stripe pay *`, `stripe docs *`, and `brew install stripe/stripe-cli/stripe` ([stripe-directory/SKILL.md:17](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-directory/SKILL.md#L17)). The directory setup step installs the CLI and a CLI plugin: `brew install stripe/stripe-cli/stripe && stripe plugin install directory` ([line 54](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-directory/SKILL.md#L54)).
- **MCP servers:** `stripe`, type `http`, at `https://mcp.stripe.com` ([.mcp.json](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/.mcp.json)); the README says it uses OAuth.
- **Network:** the hosted MCP server; `stripe directory search "<query>"` with a query built from the user's goal ([stripe-directory/SKILL.md:73](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-directory/SKILL.md#L73)); `stripe projects` provisioning and `stripe pay` transfers, both behind explicit user approval.
- **Disclosed in its README:** partly. The README documents the MCP server and the Grok install ([README.md:12](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/README.md#L12), [line 50](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/README.md#L50)); it does not mention Directory, Projects or Pay. The plugin folder has no README of its own.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `9a36da0`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `.grok-plugin/plugin.json`, `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s), MCP servers` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/stripe/ai.git@9a36da0...#providers/grok/plugin --trust`: `Installed 1 plugin(s) ... stripe` |
| Gate: details | pass | `stripe v0.9.4 (subdir: providers/grok/plugin)`; the installed folder holds 10 skills, 1 agent, 2 commands and `.mcp.json` |
| Reading: promises against components | break | the manifest's description leaves out the Directory, Projects and Pay skills, and Directory claims requests unrelated to Stripe (K-01) |
| Reading: license | pass | MIT, `LICENSE` at the repository root, `"license": "MIT"` in the Grok manifest |
| Reading: what it can execute | break | an undisclosed query to Stripe Directory on unrelated vendor requests (K-01) |
| Reading: maintenance | last push 2026-09-30, 93 open issues, 1,850 stars | GitHub API, 2026-09-30 |
| README install line | fails in a clean home | `grok plugin install stripe --trust` with no marketplace registered: `No marketplace plugin named "stripe" in any registered marketplace` (K-02) |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `stripe-directory` (and `stripe-projects`) claim every vendor-selection request, including ones unrelated to Stripe, and send a query describing the user's goal to Stripe Directory before web search or the model's own knowledge; the manifest and README do not say so. | [stripe-directory/SKILL.md:3](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-directory/SKILL.md#L3), [line 34](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-directory/SKILL.md#L34), [stripe-projects/SKILL.md:3](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/skills/stripe-projects/SKILL.md#L3), [.grok-plugin/plugin.json:3](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/providers/grok/plugin/.grok-plugin/plugin.json#L3) | break | filed #546 by an outside user, open | make Directory run when asked, scope Projects to Stripe requests, disclose both in the README, small | drafted ([seal](../seals/stripe/K-01.md)) |
| K-02 | The README's Grok line `grok plugin install stripe --trust` fails in a Grok home without the xAI marketplace registered. | [README.md:55](https://github.com/stripe/ai/blob/9a36da0458aafcfcc6be3094cf9ef2880fa4226b/README.md#L55); clean-home output in the assay table | hairline | new | give the qualified or direct form, small | drafted ([seal](../seals/stripe/K-02.md)) |

## Workarounds

None admits the entry. A Grok user who wants the Stripe development skills anyway can install at the pin and tell Grok, in the project's `AGENTS.md`, to use `stripe-directory` and `stripe-projects` only when asked by name. That instruction was not tested in a Grok session for this assay.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
