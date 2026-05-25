# Titan Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/titan/` routes the operation that keeps Titan seed canary
surfaces shaped, bounded, and visibly weaker than full incarnation proof.

`aoa-agents`, `aoa-memo`, and runtime owners keep Titan law, memory, roster,
summon, activation, and incarnation truth. This package keeps public-safe seed
canary shape, validation visibility, and future scorer routes below those
owners.

## Owned Operation

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

This package routes Titan proof-seed boundary work. Current source canary seeds
stay under `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`.

## Source Surfaces

- `mechanics/titan/parts/seed-boundary/docs/TITAN_INCARNATION_CANARIES.md`
- `mechanics/titan/parts/seed-boundary/docs/TITAN_SUMMON_DISCIPLINE_CANARIES.md`
- `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`
- `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`
- `docs/architecture/LEGACY_NAMING.md`
- `docs/architecture/PROOF_TOPOLOGY.md`
- `scripts/validate_repo.py` function `validate_titan_canary_surfaces`
- `tests/test_validate_repo.py`

## Inputs

- one Titan boundary pressure such as named identity, summon discipline, gate
  payload, memory provenance, lineage non-erasure, runtime roster, closeout
  receipt, or hidden-arena prevention
- one public-safe seed YAML file under
  `mechanics/titan/parts/seed-boundary/seeds/`
- an `id` or `eval_id` that matches the filename stem
- a `purpose`, `claim`, `kind`, `description`, or `objective`
- `checks`, `required_fields`, `expected_failure`, `expected_result`,
  `expected`, `forbidden`, or failure examples that make the seed falsifiable

## Outputs

- seed-defined Titan boundary canary
- validator-visible canary shape
- route to a future executable scorer only when scorer contracts exist
- bounded proof or owner handoff only after review accepts the canary result

## Stronger Owner Split

`aoa-evals` owns the canary seed shape and bounded proof posture.

`aoa-agents` owns Titan role classes, bearer identity, summon boundary law, and
incarnation posture. `aoa-memo` keeps memory authority. Runtime owners keep
activation, roster, and service truth. A canary can point at a boundary
pressure; it cannot grant runtime authority, activate a Titan cohort, or
certify incarnation by itself.

When a canary depends on external Titan law, the source owner keeps the stronger
meaning and `aoa-evals` keeps only the bounded check surface.

## Boundary Pressure Routes

| Pressure | Route |
| --- | --- |
| seed canary reads like full incarnation proof | keep it as seed-boundary evidence until stronger-owner review accepts a broader claim |
| YAML seed implies runtime activation, hidden arena, hidden background arena, or live summon authority | route to runtime or Titan summon owners before proof wording changes |
| memory canary implies memory sovereignty | route to `aoa-memo` and keep the canary source-ref oriented |
| mutation gate or judgment gate pressure appears | keep the gate explicit in seed-boundary docs and canary validation |
| executable scorer claim appears | wait for scorer contracts, fixtures, and review evidence |
| historical Titan canary vocabulary appears | route through `PROVENANCE.md`, legacy indexes, and validator-backed replacement paths |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- adding or changing `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`;
- changing `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md` or
  `mechanics/titan/parts/seed-boundary/seeds/README.md`;
- changing Titan canary guide wording;
- changing `validate_titan_canary_surfaces`;
- deciding whether a Titan seed canary can become an executable scorer-backed
  eval;
- routing Titan canary legacy vocabulary into active topology.
