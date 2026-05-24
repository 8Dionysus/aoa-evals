# Titan Canary Seeds

## Role

`mechanics/titan/parts/seed-boundary/seeds/` owns the source YAML seed family
for the Titan mechanic.

These files are seed-defined boundary checks. Full eval bundles, executable
scorer suites, runtime activation receipts, summon authority, memory authority,
and Titan incarnation proof route to later scorer or stronger-owner surfaces.

## Source Shape

Current seed files match `titan*.yaml`.

Each seed must keep:

- an `id` or `eval_id` matching the filename stem;
- public-safe boundary pressure;
- a non-empty `purpose`, `claim`, `kind`, `description`, or `objective`;
- falsifiability through `checks`, `required_fields`, `expected_failure`,
  `expected_result`, `expected`, `forbidden`, `description`, or failure
  examples.

## Boundaries

- Keep seed files package-local under
  `mechanics/titan/parts/seed-boundary/seeds/`.
- Keep seed-defined status unless scorer contracts, fixtures, and reports are
  added.

| Pressure | Route |
| --- | --- |
| full incarnation proof, runtime activation, hidden arena, live summon authority, memory sovereignty, mutation-gate bypass, or judgment-gate bypass | route to stronger Titan, runtime, memory, or later scorer-owner surfaces |
| stronger Titan owner law appears in a seed change | keep `aoa-evals` on the public-safe seed shape and route law changes to the owner repository |

## Validation

Use [AGENTS.md](AGENTS.md#validation) for the seed-local validation route.
Executable validation commands are centralized in the parent `mechanics/titan/parts/AGENTS.md` lane.
