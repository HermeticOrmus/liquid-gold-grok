# The kintsugi rubric

Kintsugi mends broken pottery with gold, and the repair is the part people look at. This library applies that to Grok Build plugins. An entry earns its place because we traced its cracks with evidence, sealed what we could where everyone can see it, and pinned the commit that survived. Reputation, stars and vendor names do not admit anything.

Every entry card in [`entries/`](entries/) follows the five stages below, in order. Each stage ends on a check; the next stage starts only when the check holds.

## 1. Ready the vessel

- Pin a full 40-character commit SHA from the plugin's default branch. Tags and branch names move; a SHA does not.
- Install into a clean Grok home, never your own:

  ```bash
  export GROK_HOME="$(mktemp -d)"
  export HOME="$(mktemp -d)"   # Grok also reads Claude Code's marketplace list from HOME; an empty HOME keeps the run clean
  ```

- Record the Grok version (`grok --version`) and the date of the assay.

Check: the pin is a 40-character SHA that exists upstream, and the Grok home has no plugins or marketplaces before the install (`grok plugin list`, `grok plugin marketplace list`).

## 2. Trace the cracks

Three lights. The gates and the reading are required. The hands are optional.

### The gates

| Gate | Command | Passes when |
|------|---------|-------------|
| Validate | `grok plugin validate <plugin dir at the pin>` | exit 0, and the `components:` line names what the plugin claims |
| Install | `grok plugin install https://github.com/<owner>/<repo>.git@<sha>[#<path>] --trust` | exit 0 in the clean Grok home |
| Details | `grok plugin details <name>` | the plugin is listed at the pinned commit and version |
| Inspect | `grok inspect --json`, run from an empty folder | the skills, agents, commands, hook events and MCP servers Grok loaded for the plugin match the card's "Components at the pin" row |

The card records what Grok loads, not what the folder holds. When the folder holds more than `grok inspect` lists (an agent with frontmatter Grok cannot parse, an MCP config in a file Grok does not read), Grok skipped a component, and that is a crack. [`scripts/verify.sh`](scripts/verify.sh) prints both counts for every entry.

### The reading

Read the plugin at the pin, not its homepage.

- **Promises against components.** What the README and manifest say it does, against what Grok actually loads (skills, agents, commands, hooks, MCP servers). A promised MCP server that Grok does not register is a crack.
- **License.** A license file is present at the pin, and the manifest or README states it. The card links it at the pinned commit.
- **What it can execute.** Every hook and the event it runs on, every script it ships or tells the agent to run, every MCP server and how it starts (a pinned package, an unpinned `@latest`, a hosted URL), and every network call. Then: does the README say so?
- **Maintenance.** Last push, open issues and stars from the GitHub API on the day of the assay. These describe the vessel; they never admit it.

### What Grok reads, for the reading

A Claude Code plugin installs in Grok as it is, but Grok reads some parts differently. These are the differences the first stock turned up, each from Grok's own documentation or source at [xai-org/grok-build@2bdd1d6](https://github.com/xai-org/grok-build/tree/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8):

- **Manifest.** `plugin.json` at the plugin root wins, then `.grok-plugin/plugin.json`, then `.claude-plugin/plugin.json` ([manifest.rs:1](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-agent/src/plugins/manifest.rs#L1)). A root `plugin.json` without `mcpServers` hides the MCP server declared in `.claude-plugin/plugin.json`.
- **MCP config.** `.mcp.json` (with the dot) or the manifest's `mcpServers`. Inside it, `${CLAUDE_PLUGIN_ROOT}`, `${GROK_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}` and `${GROK_PLUGIN_DATA}` are substituted as text ([mcp_servers.rs:157](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-config/src/mcp_servers.rs#L157)). A server that reads them from its own environment instead found them empty in this stock's assay ([hindsight-memory K-02](entries/hindsight-memory.md)).
- **Hook output.** `SessionStart` output is ignored ([10-hooks.md:505](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L505)), and an allowing `UserPromptSubmit` hook's context is discarded ([10-hooks.md:481](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/10-hooks.md#L481)). `PreToolUse`, `PostToolUse` and `Stop` output is read.
- **Hook input.** camelCase keys, with snake_case aliases such as `tool_name` and `tool_input` ([event.rs:377](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-hooks/src/event.rs#L377)). The tool name is Grok's own (`run_terminal_command`, `search_replace`, `write`); Claude names are mapped only in `matcher` patterns ([claude_alias.rs:47](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-tools/src/types/claude_alias.rs#L47)). A hook script that compares the tool name to `Bash` or `Edit` in its own code does nothing in Grok.

### The hands

A real task in a Grok session with the plugin loaded. It costs model time, so it is optional. When the hands were not run, the card says so in the assay table. Hook scripts can be exercised without a session: run the script with the JSON a hook receives on stdin and `CLAUDE_PLUGIN_ROOT` and `GROK_PLUGIN_ROOT` set, and check the exit code and output. That is evidence about the script, not about Grok's hook runtime, and the card keeps the two apart.

Check: every gate ran, every reading question has an answer with evidence, and the hands are either recorded or marked not run.

## 3. Keep the ledger

One row per crack, in the entry card:

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | one plain sentence | file:line at the pin, a command and its output, or a link | hairline / fracture / break | new, filed #N, or held by owner | the fix in one line, and its size | open / drafted / sealed / hallmarked |

- **Grades.** `hairline`: copy or cosmetic. `fracture`: wrong behavior with a workaround. `break`: it does not work, loses data, or breaks a safety or privacy promise.
- **Promises.** A safety or privacy promise that the plugin breaks by default, and that its README never corrects, is a break. When the same README discloses the behavior elsewhere, with an opt-out, the contradiction is a fracture and the opt-out is its workaround.
- **Evidence.** A crack without evidence is marked *inferred* until it is proven.
- **IDs** are never reused, even when a crack is withdrawn.
- **Tracker.** Search the upstream issues first. A crack the owner is already holding is recorded as `held by <owner> (#N)` and left to them.
- **Root causes.** One cause with five symptoms is one crack with five evidence links.

Check: every crack is deduplicated against the upstream tracker and has evidence or the *inferred* mark.

## 4. Seal with gold

A seal is always visible. Three kinds:

1. **Our own repositories:** a pull request. The ledger links it (`sealed #N`).
2. **Someone else's repository:** a draft issue or pull request text in [`seals/<entry>/K-NN.md`](seals/), written for the owner in their own terms, with the evidence. Drafts are never posted from this library; the maintainer sends them. The ledger says `drafted`.
3. **A workaround in the entry card:** the exact steps a Grok user takes to get the promised behavior at the pinned commit. A workaround counts as a seal only when it was run at the pin and its result is recorded; otherwise it is documented help, and the crack stays `drafted` or `open`.

A crack the upstream project already fixed at the pinned commit (a CHANGELOG `Fixed` line, a merged pull request) is recorded as `sealed` with that link. That is the gold already in the vessel.

Check: every seal names its form and links its evidence.

## 5. Hallmark

The hallmark is what `scripts/verify.sh` proves on every change to this library, and what the card states:

- The pinned SHA installs clean through this marketplace, in a fresh Grok home, and the installed component counts match the card.
- Every `break` is sealed, or the entry is not admitted.
- Every `fracture` is sealed, or carries a workaround in the card.

## Levels

| Level | Admitted to the marketplace | What must hold |
|-------|-----------------------------|----------------|
| **gold** | yes | Hallmarked. The gates pass at the pin, a license file is present, everything it executes is disclosed, no break is open, and no fracture is open: each one is sealed at the pin, by a merged pull request, or by a workaround that was run at the pin. Open hairlines are allowed and listed. |
| **assayed** | yes | The gates pass at the pin, no break is open, and every open fracture carries a workaround in the card and a seal: a draft in `seals/`, a pull request, or an upstream issue or pull request that already holds it. A license stated only in the manifest, with no license file, is a fracture of this kind. |
| **watch** | no | Promising, not admitted. Any gate fails, there is no license at all, a break is open (an undisclosed network call or a broken safety promise is a break), or the assay is not finished. The card says which. |

Watch entries have cards and appear in [`CATALOG.md`](CATALOG.md) so the reason is public, but they are not in `.grok-plugin/marketplace.json`.

## Moving a pin

A pin moves only through a new assay. [`scripts/repin.sh <entry>`](scripts/repin.sh) shows the commits and files that changed upstream since the pinned SHA. Read that diff with the same five stages, add new cracks to the ledger with new IDs, then move the SHA in `.grok-plugin/marketplace.json` and in the card in one pull request.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
