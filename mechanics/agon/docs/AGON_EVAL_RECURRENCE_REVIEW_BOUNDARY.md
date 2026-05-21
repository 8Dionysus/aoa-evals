# Agon Eval Recurrence Review Boundary

## Role

This is mechanic-wide guidance for Agon recurrence review boundaries in
`aoa-evals`.

It is not a recurrence control-plane contract, not an Agon part payload, not a
source proof bundle, and not permission to activate Agon runtime machinery.

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

- Do not open an arena session from recurrence pressure.
- Do not write memory, mutate rank, create scars, or promote to Tree of Sophia.
- Do not read a recurrence hook, manifest, beacon, or generated registry as an
  owner decision.
- Do not let recurrence pressure create a new Agon parent or proof-suffix
  package.

## Validation

Use `mechanics/agon/AGENTS.md#validation` for executable validation commands.
This mechanic-wide guide names recurrence review boundaries; the route card
owns command execution.
