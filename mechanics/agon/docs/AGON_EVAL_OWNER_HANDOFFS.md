# Agon Eval Owner Handoffs

## Role

This is mechanic-wide guidance for Agon proof-side owner handoffs in
`aoa-evals`.

It is not an Agon part payload, not a source proof bundle, not a decision
record, and not Agon law. Concrete alignment payloads stay under
`mechanics/agon/parts/`.

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

- Do not turn an Agon support part into live Agon judgment.
- Do not treat generated registries, recurrence hooks, or handoff notes as
  owner acceptance.
- Do not write memory, rank, scar, KAG canon, or ToS canon from this repo.
- Do not route new Agon work through legacy before checking `PARTS.md` and the
  owning part contract.

## Validation

Use `mechanics/agon/AGENTS.md#validation` for executable validation commands.
This mechanic-wide guide names owner handoff boundaries; the route card owns
command execution.
