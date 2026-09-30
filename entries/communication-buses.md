# communication-buses

Driver design and debugging for I2C, SPI, UART, CAN and USB: init sequences, DMA strategy, error recovery, bit timing and baud math, and the peripheral quirks of STM32, NXP, Nordic and ESP32, with STM32 HAL and LL code.

| | |
|---|---|
| Level | **gold** |
| Domain | Embedded |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/LICENSE) |
| Source | [HermeticOrmus/LibreEmbed-Claude-Code](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/tree/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses) (`plugins/communication-buses`) |
| Pinned SHA | `87880829cd3dbd5667c9e678b76b7024566666f8` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Firmware engineers writing or porting a bus driver, or chasing a bus that reads 0xFF, hangs, or drops bytes under load.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install communication-buses@liquid-gold-grok
```

## Why it is gold

In firmware a wrong number is a wrong bus, so the numbers are where this assay looked hardest. Before v1.0.0 the plugin could not load at all, and its code would have misconfigured hardware in three places: a CAN setup that ran at 560 kbit/s instead of 500, a wrong UART baud register value, and a DMA callback that misread its own argument. Release [#2](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/pull/2) sealed all four, and this assay recomputed the sealed figures at the pin: 42 MHz / 6 / 14 time quanta = 500 kbit/s, and 42,000,000 / (16 x 22.8125) = 115,068 baud for BRR 0x16D. The plugin executes nothing. What stays open is hairline: README copy.

## What it can execute

- **Hooks:** none.
- **Scripts:** none. The C code in the agent, command and skill is reference code for your firmware; nothing runs it.
- **MCP servers:** none.
- **Network:** none.
- **Disclosed in its README:** nothing to disclose.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `8788082`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreEmbed-Claude-Code.git@8788082...#plugins/communication-buses --trust`: `Installed 1 plugin(s) ... communication-buses` |
| Gate: details | pass | `communication-buses v1.0.0 (subdir: plugins/communication-buses)`, the install registry records commit `8788082`; the installed folder holds 1 skill, 1 agent, 1 command |
| Reading: promises against components | pass, one hairline | the plugin README names the `bus-driver-engineer` agent, the `/comm-bus` command and the `communication-buses` skill ([README.md:11](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/README.md#L11)); all load. The skill has reference sections for all five buses. See K-06 for the one promise without material |
| Reading: the sealed figures | pass | CAN: 42 MHz / 6 = 7 MHz, 1 + 11 + 2 = 14 quanta, 7 MHz / 14 = 500 kbit/s ([agents/bus-driver-engineer.md:327](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/agents/bus-driver-engineer.md#L327)). UART: 42,000,000 / (16 x 115200) = 22.786, mantissa 22, fraction 13, BRR 0x16D ([commands/comm-bus.md:306](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/commands/comm-bus.md#L306)) |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 6 open issues and pull requests, 49 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The pack could not load: no plugin manifests, agents and commands in nested folders the loader does not read, and a `setup.sh` that copied into an ignored directory. The bus code lived in those unread copies. | [CHANGELOG.md:7](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L7), [:13](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L13), [:22](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L22) | break | release PR #2 | a `plugin.json` per plugin and the flat layout, with the old code merged in, large | sealed #2 |
| K-02 | CAN at 500 kbit/s from a 42 MHz clock used prescaler 5 with 15 time quanta, which runs the bus at 560 kbit/s. | [CHANGELOG.md:30](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L30); the seal is at [agents/bus-driver-engineer.md:332](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/agents/bus-driver-engineer.md#L332) and [commands/comm-bus.md:320](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/commands/comm-bus.md#L320) | fracture | release PR #2 | prescaler 6 with 1 + 11 + 2 quanta, small | sealed #2 |
| K-03 | The UART BRR value for 115200 baud at 42 MHz was wrong. | [CHANGELOG.md:31](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L31); the seal is at [agents/bus-driver-engineer.md:308](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/agents/bus-driver-engineer.md#L308) and [commands/comm-bus.md:314](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/commands/comm-bus.md#L314) | fracture | release PR #2 | BRR 0x16D, 115,068 baud actual, small | sealed #2 |
| K-04 | The UART DMA pattern treated the `size` passed to `HAL_UARTEx_RxEventCallback` as a count since the last call; it is the write position in the buffer. | [CHANGELOG.md:32](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/CHANGELOG.md#L32); the seal is at [skills/communication-buses/SKILL.md:384](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/skills/communication-buses/SKILL.md#L384) | fracture | release PR #2 | track the position modulo the buffer size, small | sealed #2 |
| K-05 | The plugin README shows only the Claude Code install (`/plugin marketplace add`, `/plugin install`). | [plugins/communication-buses/README.md:55](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/README.md#L55) | hairline | held by HermeticOrmus ([#8](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/issues/8), PR [#9](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/pull/9)) | add the Grok install line, small | open |
| K-06 | The README promises "multi-interface composite devices" for USB; the agent, command and skill cover CDC and HID classes but have no composite-device material (`grep -i composite` finds only the README). | [plugins/communication-buses/README.md:31](https://github.com/HermeticOrmus/LibreEmbed-Claude-Code/blob/87880829cd3dbd5667c9e678b76b7024566666f8/plugins/communication-buses/README.md#L31) | hairline | new | add a composite descriptor example to the skill, or drop the phrase, small | open |

## Workarounds

None needed. No fracture is open.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
