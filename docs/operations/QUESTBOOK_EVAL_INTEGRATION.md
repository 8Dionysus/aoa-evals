# Questbook Eval Integration

## Purpose

This guide shows how `QUESTBOOK.md` fits into `aoa-evals` as the public tracked
surface for deferred proof obligations.

## Operating Card

| Field | Route |
| --- | --- |
| role | quest/eval integration guide for deferred proof obligations |
| input | missing proof surface, regression seam, verdict-bridge debt, repeated caution pattern, post-session harvest pressure, or generated quest reader pressure |
| output | quest anchor route, deferred obligation route, reviewed promotion route, generated reader route, or owner handoff route |
| owner | this guide owns docs-level quest/eval integration; quest source records, `QUESTBOOK.md`, mechanics/questbook parts, and bundle-local proof surfaces own concrete state and evidence |
| next route | `QUESTBOOK.md`, `quests/AGENTS.md`, `quests/LIFECYCLE.md`, `mechanics/questbook/`, affected source quest record, or affected proof bundle |
| validation | `docs/AGENTS.md#validation` and `mechanics/questbook/AGENTS.md#validation` |

## Role split

| Surface | Role |
| --- | --- |
| eval bundles | source of eval meaning |
| indexes and selection docs | public navigation and proof surfaces |
| `QUESTBOOK.md` | public human obligation index for deferred proof work |
| source quest records | lifecycle state, owner route, and durable obligation metadata |
| generated quest readers | repo-local review projection and dispatch reader over source quest records |
| proof/regression/verdict-bridge boundaries | reviewable boundaries that route stronger proof claims to their owner |
| repeated caution patterns | candidates for reusable proof shape after enough recurrence to deserve stable IDs |

## Anchor Routes

| Pressure | Anchor route |
| --- | --- |
| public proof navigation | `EVAL_INDEX.md` |
| comparison or regression seam | `docs/guides/COMPARISON_SPINE_GUIDE.md` |
| verdict-bridge debt | `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md` |
| artifact/process confusion | `docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` |
| repeated-window caution | `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md` |

## Initial posture

A good eval quest points to one of these durable pressures:

| Pressure | Quest route |
| --- | --- |
| missing proof surface | source quest record plus affected bundle or mechanic owner |
| regression or comparison seam | comparison-spine or regression proof route |
| trace-to-verdict bridge debt | verdict-bridge owner route |
| repeated caution pattern | recurring proof-pattern candidate until stable ID review |

## Installed quest-harvest posture

`aoa-quest-harvest` may assist this repo only as a post-session installed skill after a reviewed run, closure, or pause.

| Pressure | Route |
| --- | --- |
| active-route execution | current owner route and nearest `AGENTS.md` |
| orchestrator identity | orchestrator owner surface |
| eval bundle meaning | bundle-local `EVAL.md`, `eval.yaml`, reports, and review notes |
| playbook route canon | `aoa-playbooks` owner route |
| memo ownership | `aoa-memo` owner route |
| one anecdotal repeat | keep as harvest evidence until recurrence and owner-fit justify promotion |

Its allowed outcomes are:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

## Generated quest surfaces

The live generated quest catalog and dispatch surfaces are repo-local review
projection and validation projection over source quest records.
The matching example files remain versioned example-only surfaces and example
mirrors.
Portable verdict authority stays with eval bundle evidence, mechanic proof
evidence, and owner review.

Example-only progression surfaces may cite upstream read-only refs such as `AOA-SK-Q-0003`.
Those references stay source-owned upstream while this rollout stays in the
`aoa-evals` proof route.

## Manual-first pilot lane

- `AOA-EV-Q-0002` closed one source/proof review lane by anchoring the surviving proof question in `EVAL_INDEX.md` and `docs/guides/COMPARISON_SPINE_GUIDE.md`.
- This pass stayed manual-first: source/proof alignment landed without adding a live routing consumer, dispatch input, or quest builder.
- The result is bounded proof alignment; verdict authority remains with bundle and mechanic evidence.
