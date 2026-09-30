# libre-geo

Generative engine optimization: twelve skills and five subagents that audit how AI search engines (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews, Bing Copilot) crawl, understand and cite a website, then write Markdown and PDF client reports.

| | |
|---|---|
| Level | **watch** |
| Domain | SEO and GEO |
| Author | [Diego Bodart](https://github.com/HermeticOrmus), building on [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) by [Zubair Trabzada](https://github.com/zubair-trabzada) (MIT; six skills and all five agents derive from it, see [NOTICE.md](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/NOTICE.md)) |
| License | [MIT](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/LICENSE), with both copyright lines |
| Source | [HermeticOrmus/LibreGEO-Claude-Code](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/tree/79e6aaac30f983c2f00caeec66cf1bf3b92ce756) |
| Pinned SHA | `79e6aaac30f983c2f00caeec66cf1bf3b92ce756` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 12, agents 5, commands 0, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Site owners, SEO consultants and agencies who want to know whether AI assistants can reach, parse and quote a site, and what to change first.

## Install

Not in the marketplace yet. The upstream install line is below, for reference only.

```bash
grok plugin install https://github.com/HermeticOrmus/LibreGEO-Claude-Code.git@79e6aaac30f983c2f00caeec66cf1bf3b92ce756 --trust
```

## Why it waits

It installs clean, and v1.0.0 already sealed four cracks. It waits on one break: the README promises "The skills make HTTP requests to your target site only. No data leaves your machine." ([README.md:210](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L210)), and the `geo-brand-mentions` skill, which every full audit runs, sends the brand and founder names to YouTube, Reddit, LinkedIn, Quora, Stack Overflow, Wikipedia and Wikidata searches (K-05). Scanning those platforms is the skill's job; the promise is what is broken, and a privacy promise that the code does not keep is a break under the [rubric](../RUBRIC.md). The seal is a one-paragraph README change, drafted. When it lands and the pin moves, this entry can be re-assayed for admission. Two fractures are drafted or held beside it.

## What it can execute

- **Hooks:** none.
- **Scripts:** five Python scripts in `skills/geo/scripts/`. The skills tell the agent to run `generate_pdf_report.py` (ReportLab) for PDF reports, and the `geo-schema` agent tells it to run `fetch_page.py`. `citability_scorer.py`, `llmstxt_generator.py` and `brand_scanner.py` ship but no skill or agent names them. Dependencies are in [`skills/geo/requirements.txt`](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo/requirements.txt). `setup.sh` at the root is the Claude Code installer; Grok never runs it.
- **MCP servers:** none.
- **Network:** the audited site (pages, `robots.txt`, `llms.txt`, sitemap), fetched by the scripts (which send a desktop Chrome user agent string) and by the agent's web tools; and, from `geo-brand-mentions`, searches on the platforms listed above plus the Wikipedia and Wikidata APIs ([SKILL.md:68](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo-brand-mentions/SKILL.md#L68), [:83](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo-brand-mentions/SKILL.md#L83)).
- **Disclosed in its README:** no. The README says the requests go to the target site only (K-05).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `79e6aaa`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 0 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreGEO-Claude-Code.git@79e6aaa... --trust`: `Installed 1 plugin(s) ... libre-geo` |
| Gate: details | pass | `libre-geo v1.0.0`, the install registry records commit `79e6aaa`; the installed folder holds 12 skills and 5 agents |
| Reading: promises against components | one fracture held, one hairline | the README's 12 skills all load ([README.md:69](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L69)); QUICK_START documents an option no skill reads (K-07); the README links a `demo/` folder that is not in the repository (K-08) |
| Reading: license | pass | MIT, `LICENSE` carries both the Diego Bodart and the Zubair Trabzada copyright lines; NOTICE.md reproduces the upstream license |
| Reading: what it can execute | break | the privacy promise at README.md:210 against the brand scan (K-05); a script path that exists only after the old copy install (K-06) |
| Reading: maintenance | last push 2026-09-30, 4 open issues and pull requests, 1 star | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time, and a real audit fetches a live site; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | `/geo report-pdf` and `geo-report-pdf` pointed at `~/.claude/skills/geo/scripts/generate_pdf_report.py`, which exists only after the old copy install, so PDF reports failed from a plugin install. | [CHANGELOG.md:22](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/CHANGELOG.md#L22); the seal is at [skills/geo-report-pdf/SKILL.md:18](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo-report-pdf/SKILL.md#L18) | fracture | release PR #2 | `${CLAUDE_SKILL_DIR}` paths, small | sealed #2 |
| K-02 | TROUBLESHOOTING suggested a `setup.sh --with-python-deps` flag that never existed. | [CHANGELOG.md:23](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/CHANGELOG.md#L23) | hairline | release PR #2 | `pip install -r skills/geo/requirements.txt`, small | sealed #2 |
| K-03 | The `geo` skill delegated full audits to five subagents the repository did not ship, so audits could not fan out. | [CHANGELOG.md:13](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/CHANGELOG.md#L13) | fracture | release PR #2 | the five agents added under `agents/`, credited, medium | sealed #2 |
| K-04 | The sample audits section read as if `demo/` shipped. | [CHANGELOG.md:19](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/CHANGELOG.md#L19); now [README.md:177](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L177) says it is not in this release | hairline | release PR #2 | say so plainly, small | sealed #2 |
| K-05 | The README promises requests to the target site only and that no data leaves your machine; `geo-brand-mentions` sends the brand and founder names to YouTube, Reddit, LinkedIn, Quora, Stack Overflow, Wikipedia and Wikidata. | [README.md:210](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L210) against [skills/geo-brand-mentions/SKILL.md:68](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo-brand-mentions/SKILL.md#L68) to :130 and [scripts/brand_scanner.py:121](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo/scripts/brand_scanner.py#L121) | break | new | say which sites the skills contact, small ([draft](../seals/libre-geo/K-05.md)) | drafted |
| K-06 | The `geo-schema` agent runs `python3 ~/.claude/skills/geo/scripts/fetch_page.py`, the K-01 cause left in an agent v1.0.0 took unchanged from upstream; from a plugin install the path does not exist, and the agent's own note says the WebFetch fallback loses JSON-LD. | [agents/geo-schema.md:17](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/agents/geo-schema.md#L17), [:19](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/agents/geo-schema.md#L19); the repo's own rule at [CONTRIBUTING.md:31](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/CONTRIBUTING.md#L31) | fracture | new | pass the script path from the delegating skill, `curl -sL` as fallback, small ([draft](../seals/libre-geo/K-06.md)) | drafted |
| K-07 | QUICK_START says the skills track score deltas between runs and shows `/geo-audit ... --compare-with <dir>`; no skill reads that option. | [QUICK_START.md:85](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/QUICK_START.md#L85), [:88](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/QUICK_START.md#L88) | fracture | held by HermeticOrmus ([#4](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/issues/4)) | a `geo-compare` skill, medium | open |
| K-08 | The README links two sample audits at `demo/`, a folder the repository does not have, so both links 404. | [README.md:179](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L179), [:180](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L180) | hairline | new | unlink until the folder exists, small | open |
| K-09 | The PDF steps rely on `${CLAUDE_SKILL_DIR}`; the grok 1.0.44 binary lists `${SKILL_DIR}` and `${CLAUDE_SKILL_DIR}` among its skill substitutions, but no Grok session confirmed the path resolves. | [skills/geo/SKILL.md:165](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/skills/geo/SKILL.md#L165); `strings grok` shows the tokens next to `$ARGUMENTS` | hairline | new | run one PDF report in a Grok session and record it, small | open |
| K-10 | The README and the manifest speak only to Claude Code: `/plugin` and `claude plugin` installs, and "GEO-first SEO for Claude Code", which Grok prints in `grok plugin details`. | [README.md:112](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/README.md#L112); [.claude-plugin/plugin.json:4](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/blob/79e6aaac30f983c2f00caeec66cf1bf3b92ce756/.claude-plugin/plugin.json#L4) | hairline | held by HermeticOrmus ([#6](https://github.com/HermeticOrmus/LibreGEO-Claude-Code/issues/6)) | add the Grok install, small | open |

## Workarounds

- K-05: if the brand or founder names must stay private, tell the audit to skip `geo-brand-mentions`. Everything else it does talks to the audited site.
- K-06: find the installed folder with `grok plugin details libre-geo` (the `path:` line), then run `python3 <path>/skills/geo/scripts/fetch_page.py <url> page` for the schema step, or give the agent that full path.
- K-07: keep each audit's output folder and compare two runs by hand; the option in QUICK_START does nothing.

None of these was run in a Grok session.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
