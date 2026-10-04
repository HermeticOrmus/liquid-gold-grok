# Read the drift on a pin

A maintainer sees, for one entry or for every card, what changed upstream since the pinned
commit: the upstream head, the commits since the pin that touch the plugin folder, the files
changed, and a flag for any change to what the plugin can execute. A pin moves only through
a re-assay that starts from this report.

## Sub-features

- `drift-one` the report for one entry: pin, upstream head, commits, files, executable changes.
- `drift-all` one drift row per card, and exit `1` when an upstream cannot be read or no longer
  contains its pin.
- `drift-watch` a watch card's pin is read from the card, since it is not in the marketplace.

## How to get to it (user POV)

- Follow CONTRIBUTING.md "Re-assay a pinned entry", or read the latest dated drift report in
  `pantry/`.

## Driving it with scripts/repin.sh

Preconditions:

- The baseline in [README.md](./README.md) holds. Network access to each upstream is needed;
  no Grok CLI.

- **One entry.** Run `scripts/repin.sh <entry>`. Exit code `0`. The output names `entry:`,
  `source:`, `pinned:` and `upstream:`, then `Commits since the pin that touch <path>: <n>`, the
  changed files, and either `No changes to hooks, MCP config, manifests or scripts.` or the
  flagged files.
- **Every card.** Run `scripts/repin.sh --all`. One row per card in `entries/`. Exit `0` when
  every upstream was read and still holds its pin; exit `1` otherwise, with the failing rows
  marked.
- **Proof.** The command, its output and exit code, with the head SHA and the date run.
  Upstreams move, so a drift report is evidence for the moment it ran, not for the head.

## Gotchas

- Nothing is installed and nothing in the repo changes. A pin move is its own pull request.
- A pin that left the upstream default branch (a force-push or a deleted branch) fails `--all`
  even when the commit still exists by SHA.
- Upstream rate limits can make one row fail. Re-run that entry alone before calling it drift.
