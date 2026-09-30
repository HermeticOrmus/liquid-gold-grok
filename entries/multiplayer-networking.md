# multiplayer-networking

Multiplayer netcode for games: picking rollback, lockstep or an authoritative server by genre and player count, client prediction with server reconciliation, lag compensation for hit detection, bandwidth budgets with delta encoding and quantization, NAT traversal, and Godot and Unity networking APIs.

| | |
|---|---|
| Level | **gold** |
| Domain | Game development |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/LICENSE) |
| Source | [HermeticOrmus/claude-code-game-development](https://github.com/HermeticOrmus/claude-code-game-development/tree/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking) (`plugins/multiplayer-networking`) |
| Pinned SHA | `6959bed6b74ac0e2436089ca1748f78632938bf7` (committed 2026-09-30, release v2.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Game developers adding multiplayer, or chasing rubber-banding, desync and "I shot them and missed", who want the netcode model chosen for their genre and the reasons written down.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install multiplayer-networking@liquid-gold-grok
```

## Why it is gold

This assay ran the plugin's Godot code on Godot 4.7 instead of trusting it, and found two real fractures in the examples people copy. The prediction example stamps every input with `multiplayer.get_remote_sender_id()`, which returns 0 outside an RPC, so reconciliation can never match a server correction to its input (K-02). The attack example guards server work with `is_multiplayer_authority()`, which is false on the server once a player owns its character, so the damage check runs on the attacker's own machine, the exact anti-pattern the skill warns about (K-03). Both seals are in this card and were run at the pin on Godot 4.7; the upstream fixes are drafted. The vessel's older gold came from release [#2](https://github.com/HermeticOrmus/claude-code-game-development/pull/2), which renamed a marketplace that collided with another project's. The plugin executes nothing on its own.

## What it can execute

- **Hooks:** none. (The repository's optional `libre-gamedev-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none. The GDScript and C# in the files are reference code for your game.
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** nothing the plugin runs needs disclosing.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `6959bed`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/claude-code-game-development.git@6959bed...#plugins/multiplayer-networking --trust`: `Installed 1 plugin(s) ... multiplayer-networking` |
| Gate: details | pass | `multiplayer-networking v2.0.0 (subdir: plugins/multiplayer-networking)`, install registry commit `6959bed` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 1, agents 1, commands 1 loaded, the same as the files on disk |
| Reading: promises against components | pass, two hairlines | the `network-engineer` agent, `/multiplayer` command and `multiplayer-networking` skill the README names all load ([README.md:13](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/README.md#L13) to :21); matchmaking and Unreal coverage are thinner than promised (K-05), and the docs pointers miss (K-06) |
| Reading: the GDScript, run | two fractures, sealed in this card | Godot 4.7.stable, headless: `get_remote_sender_id()` outside an RPC returned `[0, 0, 0]`; a server and a client over ENet in one process, with the character's authority on the client, reproduced the attack guard failing and the fix working (K-03) |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 4 open issues and pull requests, 65 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay. The GDScript checks ran in a throwaway headless Godot, which is evidence about the code, not about a Grok session |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The repository's marketplace was named `claude-code-workflows`, the same name as wshobson/agents, so the two could not both be added. | [CHANGELOG.md:7](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/CHANGELOG.md#L7), [:21](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/CHANGELOG.md#L21) | fracture | release PR #2 | renamed to `claude-code-game-development`, small | sealed #2 |
| K-02 | The client prediction example stamps each input with `multiplayer.get_remote_sender_id()`, commented "Use tick counter". Outside an RPC that call returns 0, so every input carries tick 0 and a server correction cannot be matched to the input it confirms. | [skills/multiplayer-networking/SKILL.md:246](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/skills/multiplayer-networking/SKILL.md#L246); Godot 4.7 headless: three calls returned `[0, 0, 0]`, and 0 again after `create_server` | fracture | new | stamp inputs with `Engine.get_physics_frames()`, small ([draft](../seals/multiplayer-networking/K-02.md)) | sealed (card, run at the pin); upstream drafted |
| K-03 | The authoritative character example uses `is_multiplayer_authority()` for two different roles. `_ready` gives the character's physics to its authority ("Only process input for our own character"), which makes the owning client the authority; `request_attack` then returns early unless `is_multiplayer_authority()` ("Only server processes this"). So the server skips the check, the attacker's own machine validates the hit, and because `_apply_damage` is an `"authority"` RPC (line 214) the owning client is the one peer allowed to send it, with any amount: the client-trusted damage the skill's own anti-pattern forbids. | [SKILL.md:192](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/skills/multiplayer-networking/SKILL.md#L192) to :193, [:206](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/skills/multiplayer-networking/SKILL.md#L206) to :217, against [:405](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/skills/multiplayer-networking/SKILL.md#L405); two peers over ENet in one headless Godot 4.7 process, character authority on the client: the server printed "returned early (not authority)", the client passed the guard, and an `"authority"` damage RPC the client sent with an amount of its choosing (25) was applied on the server | fracture | new | guard with `multiplayer.is_server()` and let the damage RPC come only from the server, small ([draft](../seals/multiplayer-networking/K-02.md)) | sealed (card, run at the pin); upstream drafted |
| K-04 | The RPC reference says `unreliable_ordered` means "Latest delivery guaranteed, older dropped". Godot's class reference says packets in that mode "are not acknowledged, no resend attempts are made for lost packets". | [commands/multiplayer.md:300](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/commands/multiplayer.md#L300); [MultiplayerPeer, TRANSFER_MODE_UNRELIABLE_ORDERED](https://docs.godotengine.org/en/stable/classes/class_multiplayerpeer.html) | hairline | new | "Not acknowledged, no resend; packets arrive in the order they were sent", the class reference's own terms, small ([draft](../seals/multiplayer-networking/K-02.md)) | drafted |
| K-05 | The README lists "Matchmaking + lobbies: skill-based, latency-based, party-based matching algorithms" and Unreal replication graph among what the plugin covers; the agent, command and skill carry no matching algorithm and one line on Unreal, and the README's own limits say the agent does not write the matchmaking backend. | [README.md:32](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/README.md#L32), [:46](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/README.md#L46), [:53](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/README.md#L53); [agents/network-engineer.md:243](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/agents/network-engineer.md#L243) | hairline | new | point the README at the repository's `docs/06-networking-multiplayer/matchmaking-systems.md`, or trim the lines, small ([draft](../seals/multiplayer-networking/K-02.md)) | drafted |
| K-06 | The skill's cross-references miss: `docs/09-advanced-patterns/` has no replication graph page (no file under `docs/` mentions it), matchmaking lives in `docs/06-networking-multiplayer/matchmaking-systems.md` rather than `docs/12-deployment-distribution/`, and all three paths are relative to the repository root, not to the installed plugin. | [SKILL.md:409](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/plugins/multiplayer-networking/skills/multiplayer-networking/SKILL.md#L409) to :411; [docs/09-advanced-patterns](https://github.com/HermeticOrmus/claude-code-game-development/tree/6959bed6b74ac0e2436089ca1748f78632938bf7/docs/09-advanced-patterns), [docs/06-networking-multiplayer/matchmaking-systems.md](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/docs/06-networking-multiplayer/matchmaking-systems.md) | hairline | new | link the pages by their GitHub URLs and fix the two folders, small ([draft](../seals/multiplayer-networking/K-02.md)) | drafted |
| K-07 | The repository README installs only through Claude Code; no Grok line. | [README.md:209](https://github.com/HermeticOrmus/claude-code-game-development/blob/6959bed6b74ac0e2436089ca1748f78632938bf7/README.md#L209) (`/plugin marketplace add`; the README never mentions Grok) | hairline | held by HermeticOrmus ([#6](https://github.com/HermeticOrmus/claude-code-game-development/issues/6)) | add the Grok install, small | open |

## Workarounds

Both run at the pin on Godot 4.7.stable, headless.

K-02: stamp inputs with the physics frame counter instead of the RPC sender.

```gdscript
input.tick = Engine.get_physics_frames()
```

Recorded result: over four physics frames it returned `[1, 2, 3, 4]`, one distinct tick per input, which is what the reconciliation loop matches on.

K-03: validate on the server, and accept damage only from the server. Two changes, because once the client owns the character, an `"authority"` RPC from the server is refused (`RPC '_apply_damage' is not allowed on node ... from: 1. Mode is "authority"`).

```gdscript
@rpc("any_peer", "call_local", "reliable")
func request_attack(target_id: int) -> void:
    if not multiplayer.is_server():
        return  # Only the server validates and applies damage
    var target := get_node_or_null("/root/Game/Players/%d" % target_id)
    if target and _is_valid_target(target):
        _apply_damage.rpc(target_id, 10.0)

@rpc("any_peer", "call_local", "reliable")
func _apply_damage(target_id: int, amount: float) -> void:
    if multiplayer.get_remote_sender_id() != 1 and not multiplayer.is_server():
        return  # Ignore damage that did not come from the server
    if multiplayer.get_unique_id() == target_id:
        health -= amount
```

Call it from the client with `request_attack.rpc_id(1, target_id)`. Recorded result, same two-peer test: the server ran the check (`is_server()` true while `is_multiplayer_authority()` was false), the server's damage RPC arrived on the client from sender 1, and the `"authority"` version of the same RPC was refused with the error above.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
