# Boundary Bridge / Parts Route

`mechanics/boundary-bridge/parts/` is the lower index for package-local
sibling-reference compatibility and proof-anchor parts. Use it after the
parent Boundary Bridge route has selected a reference boundary operation and
the next agent needs the exact part, payload home, owner route, tool lane, and
validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for sibling-reference compatibility and proof-anchor boundary parts |
| input | repo-qualified ref, sibling route hint, compatibility posture, orchestrator class ref, quest owner-surface binding, Phase Alpha run record, or local checkout path |
| output | compatibility map route, canary matrix route, proof-anchor map route, Phase Alpha eval matrix route, generated reader route, or sibling-owner handoff |
| owner | `aoa-evals` owns local reference compatibility and proof-review routing; sibling repositories own source truth |
| next route | `mechanics/boundary-bridge/PARTS.md`, selected part README, sibling owner route, generated matrix route, and parent validation lane |
| tools | latest-sibling canary runner, Phase Alpha matrix generator, repo validator, and semantic AGENTS validator through `mechanics/boundary-bridge/AGENTS.md#validation` |
| validation | `mechanics/boundary-bridge/parts/AGENTS.md#validation` and `mechanics/boundary-bridge/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `compatibility-map/` | authored compatibility map and posture vocabulary for sibling proof refs | `compatibility-map/README.md` |
| `latest-sibling-canary/` | current-sibling matrix and runner for local compatibility checks | `latest-sibling-canary/README.md` |
| `orchestrator-proof-anchors/` | orchestrator-facing proof-anchor map and quest owner-surface binding | `orchestrator-proof-anchors/README.md` |
| `phase-alpha-eval-matrix/` | bridge from sibling-owned Phase Alpha playbook runs to local eval anchors and support refs | `phase-alpha-eval-matrix/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| sibling source truth or sibling edit pressure | sibling owner repository route |
| compatibility posture vocabulary | `compatibility-map/README.md` plus parent `PARTS.md` |
| current checkout or canary freshness | `latest-sibling-canary/README.md` and canary runner route |
| orchestrator identity or class authority | `aoa-agents` owner route plus local proof-anchor map |
| Phase Alpha run truth | `aoa-playbooks` owner route plus local eval matrix route |
| generated matrix or reader drift | owning generator, generated output, and repo validation route |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| sibling ref needs posture before supporting local proof | compatibility map owns the posture vocabulary | `compatibility-map/README.md` |
| sibling checkout freshness needs a local canary | matrix and runner can check current sibling state without editing sibling truth | `latest-sibling-canary/README.md` |
| orchestrator-facing proof anchor needs local eval routing | source class remains owner-routed while eval anchor is local | `orchestrator-proof-anchors/README.md` |
| Phase Alpha playbook run needs eval-anchor support refs | sibling run truth remains in playbooks while local anchors are generated | `phase-alpha-eval-matrix/README.md` |
| new boundary bridge pressure | distinct source surface, owner split, payload home, and validation lane exist | parent `PARTS.md` update plus decision review |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
