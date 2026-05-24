# Agon Eval Recurrence Review Boundary

## Role

This guide routes mechanic-wide Agon recurrence review boundaries in
`aoa-evals`.

It sits between recurrence signals and Agon parts. Recurrence control-plane
contracts stay with recurrence owners, Agon payloads stay in owning Agon parts,
source proof meaning stays in eval bundles, and runtime activation stays with
runtime and Agon owners.

## Mechanic-wide Scope

Recurrence can surface repeated Agon proof pressure. `aoa-evals` may transform
that pressure into bounded review candidates only when the active Agon part,
source surface, and validation route are visible.

The recurrence-review shape is:

`recurrence signal -> Agon part route -> candidate-only eval support -> bundle-local review or owner handoff`

This applies across Agon parts because recurrence hooks and manifests can
observe pressure for many alignments, but none of those observations are live
Agon verdicts.

## Source Surfaces

- `mechanics/agon/README.md`
- `mechanics/agon/DIRECTION.md`
- `mechanics/agon/PARTS.md`
- `mechanics/agon/parts/`
- `mechanics/recurrence/README.md`
- `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`
- `mechanics/EVIDENCE_CLUSTERS.md`

## Stronger Owner Split

`aoa-evals` owns bounded proof interpretation and candidate-only review
support. Recurrence owners own recurrence law and control-plane truth.
`Agents-of-Abyss` owns Agon law, court, arena, rank, scar, and live judgment.
`aoa-memo`, KAG, and Tree of Sophia keep memory, knowledge, and canon truth.

## Stop-Lines

| Boundary pressure | Owner route |
| --- | --- |
| arena session from recurrence pressure | Agon owner and runtime owner route before any activation claim |
| memory, rank, scars, or Tree of Sophia promotion | `aoa-memo`, `aoa-stats`, `Agents-of-Abyss`, or `Tree-of-Sophia` as applicable |
| owner decision inferred from hook, manifest, beacon, or generated registry | accepting owner repository and source bundle review |
| new Agon parent or proof-suffix package pressure | active `PARTS.md`, existing part contract, and evidence-backed parent gate |

## Validation

Use `mechanics/agon/AGENTS.md#validation` for executable validation commands.
This mechanic-wide guide names recurrence review boundaries; the route card
owns command execution.
