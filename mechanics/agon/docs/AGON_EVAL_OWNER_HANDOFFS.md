# Agon Eval Owner Handoffs

## Role

This guide routes mechanic-wide Agon proof-side owner handoffs in `aoa-evals`.

It sits above the parts as the shared handoff map. Concrete alignment payloads
stay under `mechanics/agon/parts/`, source proof meaning stays in eval bundles,
decision rationale stays in `docs/decisions/`, and Agon law stays with
`Agents-of-Abyss`.

## Mechanic-wide Scope

Use this guide when an Agon proof-alignment part reaches the boundary where
`aoa-evals` can no longer interpret the next step locally.

The handoff shape is:

`Agon proof pressure -> part-local support artifact -> bounded eval-side review -> stronger owner handoff`

This guide applies across Agon parts because every part shares the same
stronger-owner split: evals can shape candidate proof alignment, but it cannot
grant court, arena, rank, scar, memory, KAG, or ToS authority.

## Source Surfaces

- `mechanics/agon/README.md`
- `mechanics/agon/DIRECTION.md`
- `mechanics/agon/PARTS.md`
- `mechanics/agon/parts/`
- `mechanics/agon/docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`
- `mechanics/EVIDENCE_CLUSTERS.md`

## Stronger Owner Split

Input owners:

- `Agents-of-Abyss` for Agon move law, court posture, arena limits, scar/rank
  meaning, and center mechanic authority.
- `aoa-routing` for gate hints and route compatibility pressure.
- `aoa-playbooks` for trial choreography and scenario composition.
- `aoa-sdk` and recurrence owners for review queues or typed recurrence
  support surfaces.

Output owners:

- `Agents-of-Abyss` for any future verdict bridge or center-law change.
- `aoa-memo` for reviewed memory candidates.
- `aoa-stats` for derived movement summaries.
- Source bundle owners in `aoa-evals` for bounded eval interpretation.

## Stop-Lines

| Boundary pressure | Owner route |
| --- | --- |
| live Agon judgment | `Agents-of-Abyss` Agon owner route before eval-side wording changes |
| owner acceptance from generated registries, recurrence hooks, or handoff notes | accepting owner repository and source bundle review |
| memory, rank, scar, KAG canon, or ToS canon | `aoa-memo`, `aoa-stats`, `Agents-of-Abyss`, `aoa-kag`, or `Tree-of-Sophia` as applicable |
| new or legacy Agon work | `PARTS.md` and the owning part contract first; `PROVENANCE.md` opens legacy after the owner route is known |

## Validation

Use `mechanics/agon/AGENTS.md#validation` for executable validation commands.
This mechanic-wide guide names owner handoff boundaries; the route card owns
command execution.
