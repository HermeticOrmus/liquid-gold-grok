# rag-architecture

Retrieval-augmented generation, layer by layer: chunking by document type, embedding and vector store choice, hybrid retrieval with reciprocal rank fusion, cross-encoder reranking, grounded generation prompts, and an evaluation harness (RAGAS or LLM-as-judge on a golden set) that is built before anything is tuned.

| | |
|---|---|
| Level | **gold** |
| Domain | ML and LLM ops |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/LICENSE) |
| Source | [HermeticOrmus/LibreMLOps-Claude-Code](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/tree/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture) (`plugins/rag-architecture`) |
| Pinned SHA | `d129beed47bbb52bd166a5c1589ee17031478617` (committed 2026-09-30, release v1.0.0) |
| Components at the pin | skills 1, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Engineers building or rescuing a RAG system: the one that works in the demo and hallucinates in production, the team choosing a vector store or embedding model, and anyone who wants the eval harness before the first tuning pass.

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install rag-architecture@liquid-gold-grok
```

## Why it is gold

This assay ran the plugin's code instead of trusting it. The release notes call its LangChain and RAGAS code "working" ([CHANGELOG.md:11](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/CHANGELOG.md#L11)), but every LangChain import in the skill and the `/rag` command fails on LangChain 1.4.3, the version PyPI served for this assay (K-04). The seal is in this card and was run at the pin: with `langchain<1` and `langchain-community<1` all eight distinct import lines and the RAGAS imports resolve. The port to current LangChain is drafted. The release gold is also in the vessel: before v1.0.0 the plugin never loaded, carried two overlapping generations of its agent, command and skill, and pinned a model by name; release [#2](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/pull/2) sealed all three. The plugin executes nothing on its own.

## What it can execute

- **Hooks:** none. (The pack's optional `libre-mlops-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none. The Python in the skill and command is reference code for your system.
- **MCP servers:** none.
- **Network:** none from the plugin. The reference code calls embedding and chat APIs (OpenAI, Anthropic, Cohere) when you run it.
- **Disclosed in its README:** nothing the plugin runs needs disclosing.

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `d129bee`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreMLOps-Claude-Code.git@d129bee...#plugins/rag-architecture --trust`: `Installed 1 plugin(s) ... rag-architecture` |
| Gate: details | pass | `rag-architecture v1.0.0 (subdir: plugins/rag-architecture)`, install registry commit `d129bee` |
| Gate: inspect | pass | `grok inspect --json` from an empty folder: skills 1, agents 1, commands 1 loaded, the same as the files on disk |
| Reading: promises against components | pass, one hairline | the `rag-engineer` agent, `/rag` command and `rag-architecture` skill the README names all load ([README.md:7](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/README.md#L7)); the multilingual and code RAG line promises more than the files hold (K-05) |
| Reading: the Python, run | one fracture, sealed in this card | on a fresh Python 3.12 environment with `langchain` 1.4.3 and `langchain-core` 1.6.6, all eight distinct LangChain import lines fail with `ModuleNotFoundError` or `ImportError`; see K-04 and Workarounds |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 0 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time; not run for this assay. The imports were run in throwaway virtual environments, which is evidence about the code, not about a Grok session; the patterns themselves need API keys and a Postgres database and were not run end to end |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | None of the pack's plugins loaded: the old `setup.sh` copied folders into `~/.claude/plugins`, where plugins are not loaded from. | [CHANGELOG.md:5](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/CHANGELOG.md#L5) | break | release PR #2 | a marketplace and a `plugin.json` per plugin, large | sealed #2 |
| K-02 | rag-architecture carried two generations of its parts: an older `rag-architect` agent, a nested `/rag` command and a `rag-patterns` skill beside the newer `rag-engineer`, `/rag` and `rag-architecture`. | [CHANGELOG.md:18](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/CHANGELOG.md#L18) | hairline | release PR #2 | merged into the newer files, unique material kept, medium | sealed #2 |
| K-03 | The agent was pinned to Sonnet instead of the session's model, a name that means nothing to Grok. | [CHANGELOG.md:19](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/CHANGELOG.md#L19); now `model: inherit` ([agents/rag-engineer.md:4](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/agents/rag-engineer.md#L4)) | hairline | release PR #2 | `model: inherit`, small | sealed #2 |
| K-04 | The LangChain code does not import on current LangChain: `langchain.text_splitter`, `langchain.document_loaders`, `langchain.vectorstores`, `langchain.schema`, `langchain.retrievers` and `langchain.chains` are gone in LangChain 1.x, and `langchain.embeddings` and `langchain.chat_models` no longer export `OpenAIEmbeddings` and `ChatAnthropic`. No version is stated. | [skills/rag-architecture/SKILL.md:145](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/skills/rag-architecture/SKILL.md#L145), [:196](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/skills/rag-architecture/SKILL.md#L196), [:236](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/skills/rag-architecture/SKILL.md#L236), [:325](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/skills/rag-architecture/SKILL.md#L325); [commands/rag.md:99](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/commands/rag.md#L99), [:129](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/commands/rag.md#L129); on `langchain` 1.4.3: `ModuleNotFoundError: No module named 'langchain.text_splitter'`, five more `ModuleNotFoundError`s and two `ImportError`s | fracture | new | port the imports to the split packages (each new path checked on LangChain 1.4.3), then check the call sites, small ([draft](../seals/rag-architecture/K-04.md)) | sealed (card, run at the pin); upstream drafted |
| K-05 | The README promises "special-case patterns for non-English + code corpora"; the files hold one chunking line for code, one embedding table row and one failure-mode line for multilingual, and no pattern for either. | [README.md:20](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/README.md#L20) against [SKILL.md:22](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/skills/rag-architecture/SKILL.md#L22), [agents/rag-engineer.md:59](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/agents/rag-engineer.md#L59), [commands/rag.md:86](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/plugins/rag-architecture/commands/rag.md#L86) | hairline | new | trim the README line, or add a multilingual and code RAG section, small ([draft](../seals/rag-architecture/K-04.md)) | drafted |
| K-06 | The repository README installs only through Claude Code; no Grok line. | [README.md:81](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/blob/d129beed47bbb52bd166a5c1589ee17031478617/README.md#L81) (`/plugin marketplace add`; the README never mentions Grok) | hairline | held by HermeticOrmus ([#5](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/issues/5), PR [#6](https://github.com/HermeticOrmus/LibreMLOps-Claude-Code/pull/6)) | add the Grok install, small | open |

## Workarounds

K-04, run at the pin on Python 3.12: install LangChain below 1.0 next to the code.

```bash
pip install "langchain<1" "langchain-community<1" ragas datasets
```

Recorded result (`langchain` 0.3.30, `langchain-community` 0.3.31, `ragas` 0.4.3): all eight distinct LangChain import lines from the skill and the command exit 0, with deprecation warnings, and `from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision` exits 0. On `langchain` 1.4.3 the same RAGAS import also fails inside `ragas` itself (`No module named 'langchain_community.chat_models.vertexai'`), so pinning below 1.0 is the path that worked in this assay. Only the imports were run; the patterns need your own API keys and services.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
