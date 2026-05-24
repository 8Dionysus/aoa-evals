# Progression Evidence Model

## Purpose

This note defines the first portable proof surface for RPG-style advancement in `aoa-evals`.

It exists so that agent progression can be updated through bounded, reviewable evidence rather than through vague reputation or one universal score.

## Core route

Progression evidence is quest-scoped or route-scoped proof.

Supported readings:

- award axis deltas
- hold advancement with no delta
- reanchor advancement after drift
- record a downgrade or caution

Pressure routes:

| Pressure | Route |
| --- | --- |
| one universal score or broad capability growth | keep multi-axis deltas here; route broad comparison through comparison/growth owner review |
| eval bundle meaning | bundle-local `EVAL.md`, `eval.yaml`, and verdict logic |
| quest acceptance or state-transition pressure | quest owner route plus cited evidence |
| rank, role, or unlock doctrine | `aoa-agents` role route and unlock proof bridge route |

## Verdict posture

Recommended first-wave verdicts:

- `advance`
- `hold`
- `reanchor`
- `downgrade`

A verdict is a progression interpretation of reviewed evidence. Quest state
transitions route to the quest owner.

## Review scope

Use small scopes first:

- `quest_scoped`
- `route_scoped`
- `campaign_scoped`

The wider the scope, the higher the burden of evidence.

## Axis deltas

Axis deltas should stay small and interpretable.

Good first-wave posture:
- allow zero deltas
- allow negative deltas when the evidence really warrants caution
- prefer several small reviewed deltas over one giant award
- cite the artifacts that justify the interpretation

## Cautions

cautions are first-class proof.

Use them for:
- unresolved tradeoffs
- success with sharp boundary warnings
- partial correctness
- proof that informs progression while the clean unlock stays gated

## Upstream refs

Example progression evidence may cite upstream read-only refs such as `AOA-SK-Q-0003`.
Those refs stay source-owned in their home repos; this rollout remains inside
`aoa-evals`.

## Route Checks

| Pressure | Route |
| --- | --- |
| universal intelligence score or automatic rank assignment from one event | multi-axis evidence plus owner review |
| progression evidence without quest or artifact refs | add cited source refs before review |
| routing hint as proof | bundle-local proof review |
| memo witness as progression authority | `aoa-memo` witness route plus proof evidence |
