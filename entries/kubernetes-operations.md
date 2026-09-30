# kubernetes-operations

Design, deploy and troubleshoot production Kubernetes workloads: resource sizing, probe semantics, rollouts, RBAC, default-deny NetworkPolicies, HPA and KEDA autoscaling, PodDisruptionBudgets, Helm charts, and the common pod failures, with kubectl and Helm operations for deploy, scale, debug and upgrade.

| | |
|---|---|
| Level | **assayed** |
| Domain | DevOps |
| Author | [Diego Bodart](https://github.com/HermeticOrmus) |
| License | [MIT](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/LICENSE) |
| Source | [HermeticOrmus/LibreDevOps-Claude-Code](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/tree/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations) (`plugins/kubernetes-operations`) |
| Pinned SHA | `a810d2fa0d4f1191a79246c0443f0166129d97dc` (committed 2026-09-30, release v1.0.1) |
| Components at the pin | skills 2, agents 1, commands 1, hook events 0, MCP servers 0 |
| Assayed | 2026-09-30 with grok 1.0.44 |

## Who it is for

Engineers who run workloads on EKS, GKE, AKS or on-prem clusters and want manifests with the safety controls already in them, or a straight answer to "why is this pod Pending, OOMKilled or in CrashLoopBackOff".

## Install

```bash
grok plugin marketplace add HermeticOrmus/liquid-gold-grok
grok plugin install kubernetes-operations@liquid-gold-grok
```

## Why it is assayed

The gates pass and the plugin executes nothing on its own. Release v1.0.0 sealed a pack that never loaded, a plugin that shipped two `k8s-engineer` agents and two `/k8s` commands, and an invalid `jq` expression in the debug snippets ([#2](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/pull/2)). This assay ran the remaining `jq` snippets and found one more of the same kind: the `scale` snippet pipes YAML into jq, which fails before the filter runs (K-05). The workaround is one flag and is below; the upstream fix is drafted. It stays assayed rather than gold because the workaround was checked on jq only: no cluster was available to run the `kubectl` half.

## What it can execute

- **Hooks:** none. (The pack's optional `libre-devops-hooks` plugin is separate and not part of this entry.)
- **Scripts:** none shipped. The `/k8s` command's operations reference is `kubectl` and `helm` commands for you, or the agent with your approval, to run against your cluster; several change cluster state (`kubectl apply`, `helm upgrade`, `kubectl drain`).
- **MCP servers:** none.
- **Network:** none from the plugin. The commands it suggests talk to your cluster and pull the images they name (`busybox`, `curlimages/curl`).
- **Disclosed in its README:** partly. The README describes the command's scope, not the individual cluster-changing commands; they are visible in [commands/k8s.md](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/commands/k8s.md#L80).

## Assay

| Check | Result | Evidence |
|-------|--------|----------|
| Ready the vessel | pass | pinned `a810d2f`, clean `GROK_HOME` and `HOME` |
| Gate: validate | pass | `components: 1 skill dir(s), 1 command dir(s), 1 agent dir(s)` |
| Gate: install at the pin | pass | `grok plugin install https://github.com/HermeticOrmus/LibreDevOps-Claude-Code.git@a810d2f...#plugins/kubernetes-operations --trust`: `Installed 1 plugin(s) ... kubernetes-operations` |
| Gate: details | pass | `kubernetes-operations v1.0.0 (subdir: plugins/kubernetes-operations)`, the install registry records commit `a810d2f`; the installed folder holds 2 skills, 1 agent, 1 command |
| Reading: promises against components | two hairlines | the plugin README names the `k8s-engineer` agent, the `/k8s` command and one skill; two skills load (K-08). Its operator and ingress bullets promise more than the files hold (K-07) |
| Reading: the snippets, run | one fracture | both `jq` filters in `/k8s` parse and run on JSON with jq 1.8.2; the `scale` snippet feeds them YAML (K-05) |
| Reading: license | pass | MIT, `LICENSE` at the repository root and `"license": "MIT"` in the manifest |
| Reading: what it can execute | pass | markdown only; the cluster commands are suggestions the user runs |
| Reading: maintenance | last push 2026-09-30, 3 open issues and pull requests, 0 stars | GitHub API, 2026-09-30 |
| Hands | not run | a Grok session costs model time, and no cluster was available; not run for this assay |

## Ledger

| ID | Crack | Evidence | Grade | Tracker | Seal | State |
|----|-------|----------|-------|---------|------|-------|
| K-01 | The pack never loaded: the old `setup.sh` copied plugin folders into `~/.claude/plugins`, which the loader does not read as plugins. | [CHANGELOG.md:12](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/CHANGELOG.md#L12), [:26](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/CHANGELOG.md#L26) | break | release PR #2 | a marketplace, a `plugin.json` per plugin, the flat layout, large | sealed #2 |
| K-02 | The plugin shipped two `k8s-engineer` agents and two `/k8s` commands. | [CHANGELOG.md:33](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/CHANGELOG.md#L33) | fracture | release PR #2 | one file each, every unique section kept, medium | sealed #2 |
| K-03 | An invalid `jq` expression in the `/k8s` debug snippets. | [CHANGELOG.md:35](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/CHANGELOG.md#L35); the debug filter at [commands/k8s.md:196](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/commands/k8s.md#L196) runs clean on JSON with jq 1.8.2 | fracture | release PR #2 | corrected expression, small | sealed #2 |
| K-04 | The README plugin tables did not name each plugin's agent and command, and their counts did not match the manifests. | [CHANGELOG.md:30](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/CHANGELOG.md#L30) | hairline | release PR #2 | tables rebuilt from the manifests, small | sealed #2 |
| K-05 | The `/k8s scale` snippet pipes `kubectl get vpa -o yaml` into `jq`, which parses JSON only, so the VPA recommendation check fails. | [commands/k8s.md:147](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/commands/k8s.md#L147); jq 1.8.2 on YAML input: `jq: parse error: Invalid numeric literal at line 1, column 11` | fracture | new | `-o json`, small ([draft](../seals/kubernetes-operations/K-05.md)) | drafted |
| K-06 | `kubectl drain ... --dry-run=true` uses the deprecated boolean form; kubectl warns and maps it to `client`. | [commands/k8s.md:151](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/commands/k8s.md#L151); [kubectl helpers.go](https://github.com/kubernetes/kubectl/blob/d1f17c3a0a590e70973faee0018fe73406605613/pkg/cmd/util/helpers.go), `GetDryRunStrategy` | hairline | new | `--dry-run=client`, small ([draft](../seals/kubernetes-operations/K-05.md)) | drafted |
| K-07 | The README promises operator patterns (controller loops, write versus use) and ingress coverage for Traefik, Gateway API and rate limiting; the files have one RBAC row about operators and nothing on the rest. | [README.md:17](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/README.md#L17), [:18](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/README.md#L18); a case-insensitive search of the agent, command and skills for Traefik, Gateway API, HTTPRoute and rate limiting finds nothing | hairline | new | add the material or trim the bullets, small ([draft](../seals/kubernetes-operations/K-05.md)) | drafted |
| K-08 | The README lists one skill; the plugin ships two (`kubernetes-operations` and `k8s-patterns`). | [README.md:9](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/plugins/kubernetes-operations/README.md#L9) | hairline | new | name both skills, small ([draft](../seals/kubernetes-operations/K-05.md)) | drafted |
| K-09 | The repository README installs only through Claude Code; no Grok line. | [README.md:109](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/blob/a810d2fa0d4f1191a79246c0443f0166129d97dc/README.md#L109) (the README never mentions Grok) | hairline | held by HermeticOrmus ([#7](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/issues/7), PR [#8](https://github.com/HermeticOrmus/LibreDevOps-Claude-Code/pull/8)) | add the Grok install, small | open |

## Workarounds

K-05: ask for JSON output before piping to jq:

```bash
kubectl get vpa -n production -o json | \
  jq '.items[].status.recommendation.containerRecommendations[]'
```

Checked at the pin with jq 1.8.2: the filter prints the container recommendations from JSON shaped like a VPA list. The `kubectl` half was not run, because no cluster was available.

<p align="center"><img src="https://brand.ormus.solutions/assets/marks/kintsugi-mark.svg" alt="Kintsugi mark" width="48" /></p>
