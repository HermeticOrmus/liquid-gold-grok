# pr-review-toolkit

Six review agents for a pull request or a working diff, each with one job: comments, tests, error handling (silent failures), type design, general code review, and simplification. A `/review-pr` command picks the ones that fit the change and aggregates their findings into critical, important and suggested fixes.

| | |
|---|---|
| Level | **assayed** |
| Domain | Code review |
| Author | [Anthropic](https://github.com/anthropics) (README credits Daisy) |
| License | [Apache-2.0](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/LICENSE) |
| Source | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit) |
| Pinned SHA | `ab024cdcfa7ca80be204acd4907656ba5a968589` (committed 2026-09-30) |
| Components at the pin | skills 0, agents 5 (6 in the folder; one does not load, see K-01), commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Anyone who wants a structured second look at a change before opening or merging a pull request, split into focused passes instead of one long review.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install pr-review-toolkit@liquid-gold-grok
```

## Why it is assayed

It installs clean, runs nothing on its own, and posts nothing anywhere: `/review-pr` reads `git diff` and `gh pr view` and reports in the session. But Grok loads five of its six agents. `grok inspect` in a clean Grok home lists `type-design-analyzer`, `pr-test-analyzer`, `comment-analyzer`, `code-simplifier` and `code-reviewer`, and not `silent-failure-hunter`, whose frontmatter is not valid YAML. Upstream already holds that crack ([#4726](https://github.com/anthropics/claude-plugins-official/issues/4726), [#6261](https://github.com/anthropics/claude-plugins-official/issues/6261)), so it is recorded and left to them; the workaround below was run at the pin and brings the sixth agent back.

## What it can execute

- **Hooks:** none.
- **Scripts:** none.
- **MCP servers:** none.
- **Network:** none of its own. `/review-pr` runs `git diff --name-only` and `gh pr view` ([commands/review-pr.md:31](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/commands/review-pr.md#L31)), which read from your GitHub account; nothing is written back.
- **Disclosed in its README:** nothing it runs needs disclosure beyond the command text.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `ab024cd`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `grok plugin validate`: `components: 0 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/anthropics/claude-plugins-official.git@ab024cd...#plugins/pr-review-toolkit --trust`: `Installed 1 plugin(s) ... pr-review-toolkit` |
| Gate: details | partial | `pr-review-toolkit (subdir: plugins/pr-review-toolkit)` at commit `ab024cd`; 6 agents and 1 command in the installed folder, but `grok inspect` lists skill `review-pr` and 5 agents (K-01) |
| Reading: promises against components | fail on one agent | the README promises "6 expert review agents" ([README.md:7](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/README.md#L7)); five load |
| Reading: license | pass, with a copy crack | Apache-2.0 [LICENSE](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/LICENSE) in the plugin folder; the README says MIT (K-04) |
| Reading: what it can execute | pass | Markdown only; read-only `git` and `gh` commands |
| Reading: maintenance | last push 2026-09-30, 1,044 open issues, 37,242 stars (whole marketplace repository) | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `silent-failure-hunter` does not load in Grok. Its `description` is an unquoted YAML scalar containing `: `, which a strict parser rejects (PyYAML: "mapping values are not allowed here"), and `grok inspect` lists the other five agents only. | [agents/silent-failure-hunter.md:3](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/agents/silent-failure-hunter.md#L3); `grok inspect` in a clean Grok home | fracture | held by anthropics ([#4726](https://github.com/anthropics/claude-plugins-official/issues/4726), [#6261](https://github.com/anthropics/claude-plugins-official/issues/6261)) | quote the description or use a block scalar, small | open (workaround run at the pin) |
| K-02 | The agents tell the model to "use the Task tool" to launch specialists, a Claude Code tool name; the Grok name for subagent dispatch is not mapped here. | [agents/code-simplifier.md:14](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/agents/code-simplifier.md#L14), [commands/review-pr.md:4](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/commands/review-pr.md#L4) | hairline (*inferred*) | held by anthropics ([#1900](https://github.com/anthropics/claude-plugins-official/issues/1900)) | name the action, not the tool, small | open |
| K-03 | Four agents and the command read project rules from `CLAUDE.md` only; a Grok project usually keeps them in `AGENTS.md`. | [agents/code-simplifier.md:49](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/agents/code-simplifier.md#L49), [agents/pr-test-analyzer.md:71](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/agents/pr-test-analyzer.md#L71), [commands/review-pr.md:138](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/commands/review-pr.md#L138) | hairline | held by anthropics ([#6307](https://github.com/anthropics/claude-plugins-official/issues/6307)) | name `AGENTS.md` next to `CLAUDE.md`, small | open |
| K-04 | The README's License section says MIT; the license file in the plugin folder is Apache-2.0. | [README.md:305](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/README.md#L305), [LICENSE](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/LICENSE) | hairline | new | README says Apache-2.0, small | drafted ([seal](../seals/pr-review-toolkit/K-04.md)) |
| K-05 | The README's install and contributing notes point at Claude Code's `/plugins` menu and at `.claude/agents/` in `claude-cli-internal`, a repository readers cannot open; the manifest has no `version`. | [README.md:183](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/README.md#L183), [README.md:301](https://github.com/anthropics/claude-plugins-official/blob/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/README.md#L301) | hairline | the missing version is held by anthropics ([#1758](https://github.com/anthropics/claude-plugins-official/issues/1758)) | point contributors at this repository, small | drafted ([seal](../seals/pr-review-toolkit/K-04.md), same draft) |

## Workarounds

- **K-01:** add a project copy of the agent with its description quoted. From the root of your project:

  ```bash
  mkdir -p .grok/agents
  python3 - <<'EOF'
  import json, pathlib, urllib.request
  url = "https://raw.githubusercontent.com/anthropics/claude-plugins-official/ab024cdcfa7ca80be204acd4907656ba5a968589/plugins/pr-review-toolkit/agents/silent-failure-hunter.md"
  text = urllib.request.urlopen(url).read().decode()
  head, body = text.split("\n---\n", 1)
  lines = []
  for line in head.lstrip("-\n").split("\n"):
      if line.startswith("description: "):
          line = "description: " + json.dumps(line[len("description: "):].replace("\\n", "\n"))
      lines.append(line)
  pathlib.Path(".grok/agents/silent-failure-hunter.md").write_text("---\n" + "\n".join(lines) + "\n---\n" + body)
  EOF
  grok inspect | grep silent-failure-hunter
  ```

  Run at the pin in a clean Grok home: `grok inspect` then lists `silent-failure-hunter` as a project agent next to the five plugin agents.
- **K-03:** if your project keeps its rules in `AGENTS.md`, say so: `/review-pr all. Project rules are in AGENTS.md.`

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
