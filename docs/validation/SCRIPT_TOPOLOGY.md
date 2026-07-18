# Script Topology

Scripts in `aoa-evals` are command-plane organs for the bounded proof canon.
They should name the boundary they protect, the source truth they read, the
projections or receipts they may write, and the validation lane that covers
them.

They are not a second command authority. Blocking lane sequences live in
[`validation_lanes.json`](validation_lanes.json).

## Inventory

Machine-readable script coverage lives in
[`script_inventory.json`](script_inventory.json). It includes every tracked
non-pyc file under `*/scripts/*`, including root scripts, mechanic part-local
scripts, and any future scripts under an owner-admitted repository skill home.

Each entry records:

- `path`
- `family`
- `organ_lane`
- `owner_surface`
- `source_truth`
- `reads`
- `writes`
- `side_effects`
- `validation_lane`
- `ci_inclusion`
- `test_target`
- `disposition`

`tests/test_script_topology.py` keeps the inventory synchronized with the
filesystem and rejects orphan scripts, hidden command gates, stale command
authority, and tracked Python cache residue.

## Script Families

| Family | Owns | Boundary |
| --- | --- | --- |
| `source_validator` | source/topology and route-card checks | may read source proof meaning; must not write generated projections |
| `projection_builder` | generated/read-model writes from source | may write tracked projections; must not define source meaning |
| `projection_contract_helper` | shared projection parsing and schema helpers | helper only; lane coverage comes through builders or validators |
| `validator_module` | focused root validator domains | owns one domain contract under root validator orchestration |
| `part_local_builder` | mechanic-owned generated or registry payloads | covered by mechanic part tests or part-local commands |
| `part_local_validator` | mechanic-owned payload validation | stays with the owning mechanic part |
| `owner_skill_resource` | read-only navigation packets for an admitted owner skill | invoked through that skill procedure, remains below source proof authority, and stays outside direct eval-apply and blocking command lanes |
| `lane_loader` / `lane_executor` | command manifest API and lane execution | reads command authority from `docs/validation/validation_lanes.json` |
| `release_entrypoint` | release stabilization and env routing | executes release lane from command authority |
| `script_route_card` | local script-district route law | guidance only, not executable command storage |

## Root Scripts

Root `scripts/*.py` own repo-wide builders, validators, lane execution, release
stabilization, and catalog/report helpers. `scripts/validate_repo.py` stays the
root compatibility CLI while rule ownership continues moving into
`scripts/validators/`.

## Non-Root Scripts

Mechanic scripts live beside the part that owns their payload. A future
repository-skill helper must live with an admitted top-level `skills/` source
and remains below proof authority unless a stronger owner contract says
otherwise.

## Promotion Rule

A script may move from advisory/local-only into a blocking lane only when a
current source owner and decision record prove that `aoa-evals` owns the
checked behavior. Until then, runtime policy, trace/eval verdicts, memory/RAG
authority, inter-agent execution, and security enforcement remain route-only or
sibling-owned.
