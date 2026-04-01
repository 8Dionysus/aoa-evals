# Progression Evidence Model

## Purpose

This note defines the first portable proof surface for RPG-style advancement in `aoa-evals`.

It exists so that agent progression can be updated through bounded, reviewable evidence rather than through vague reputation or one universal score.

## Core rule

Progression evidence is quest-scoped or route-scoped proof.

It may:
- award axis deltas
- hold advancement with no delta
- reanchor advancement after drift
- record a downgrade or caution

It must not:
- pretend one number explains all capability
- replace the underlying eval bundle meaning
- replace repo-owned quest acceptance
- invent rank or unlock doctrine by itself

## Verdict posture

Recommended first-wave verdicts:

- `advance`
- `hold`
- `reanchor`
- `downgrade`

A verdict is not the same thing as a quest state transition. It is a progression interpretation of reviewed evidence.

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

Cautions are first-class proof.

Use them for:
- unresolved tradeoffs
- success with sharp boundary warnings
- partial correctness
- proof that is strong enough to inform progression but not strong enough to justify a clean unlock

## Upstream refs

Example progression evidence may cite upstream read-only refs such as `AOA-SK-Q-0003`.
Those refs stay source-owned in their home repos and do not widen this rollout into `aoa-skills`.

## Anti-patterns

- a universal intelligence score
- automatic rank assignment from one event
- progression evidence with no quest or artifact refs
- treating a routing hint as proof
- treating memo witness alone as progression authority
