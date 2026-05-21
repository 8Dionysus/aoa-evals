# Titan / Part Index

`mechanics/titan/parts/` contains the active parts of the Titan
proof-seed operation.

The mechanic owns the route:

`Titan boundary pressure -> seed canary YAML -> shape validation -> future executable scorer route -> bounded proof or owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `seed-boundary` | Maintains seed-defined Titan boundary canary YAML files and seed-local route law. | `mechanics/titan/parts/seed-boundary/seeds/titan*.yaml`, `mechanics/titan/parts/seed-boundary/seeds/AGENTS.md`, `mechanics/titan/parts/seed-boundary/seeds/README.md` |

## Boundary

Parts are not standalone mechanics. The `seed-boundary` part owns the current
seed-defined canary family because all current Titan canaries share one source
shape and one validation route. It does not split canaries by topic until a
topic gains a different scorer, fixture, report, or validator contract.

The part remains seed-defined. It does not create full incarnation proof,
runtime activation, summon authority, memory sovereignty, mutation-gate bypass,
judgment-gate bypass, or executable scorer-backed proof.

## Part Contract

Inputs are Titan boundary pressure, seed YAML files, seed-local route law, and
the incarnation or summon-discipline guide surfaces.

Outputs are validated seed canary shapes and a future executable scorer route,
not full proof by themselves.

Owner split stays explicit: `aoa-evals` owns seed-boundary proof shape;
`aoa-agents`, `aoa-memo`, and runtime owners keep Titan role, memory, and
activation truth.

Stop-lines forbid treating canary presence as incarnation, summon authority,
runtime cohort proof, memory sovereignty, mutation-gate bypass, or
judgment-gate bypass.

Validation routes through [AGENTS](AGENTS.md#validation), including the
`validate_titan_canary_surfaces` repo validation lane.
