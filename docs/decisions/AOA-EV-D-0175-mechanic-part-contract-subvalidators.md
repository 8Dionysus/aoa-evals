# Mechanic Part Contract Subvalidators

- Decision ID: AOA-EV-D-0175
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic part contract validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanic part, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After validation-command logic moved out of the aggregate part facade,
`mechanic_parts.py` still carried README contract checks, payload inventory,
source-surface refs, index/route heading roles, public aliases, and aggregate
validation in one module.

That kept part-local boundaries visible, but still bulky: README shape, payload
directory inventory, source refs, and executable validation routes answer
different questions.

## Decision

Mechanic part contract validation is split into focused modules:

- `mechanic_part_contract_index.py` owns parent `PARTS.md` contract tokens and
  README-contract decision routing.
- `mechanic_part_role_headings.py` owns part/index route heading roles.
- `mechanic_part_readme_contract.py` owns part README required-section checks,
  stale stop-line scaffold checks, and local traversal.
- `mechanic_part_contract_common.py` is helper-only shared constants and token
  lookup.
- `mechanic_part_payload_inventory.py` owns allowed payload classes, unexpected
  part-root entries, empty payload dirs, README payload routing, thin-part
  posture, and payload-inventory decision routing.
- `mechanic_part_source_surfaces.py` owns Source Surfaces path-like refs,
  repo-relative reachability, placeholder/nonlocal allowances, and source-surface
  decision routing.

## Rationale

Part README contracts describe the boundary. Payload inventory checks the file
shape under the part. Source-surface refs prove where the part takes authority
from. Validation commands prove there is reachable executable evidence.

Keeping those in one module recreated the historical gate pile at a smaller
scale. Splitting them keeps each validator aligned with the boundary it guards.

## Consequences

- Positive: no mechanic part validator module carries README, payload,
  source-ref, and validation-command behavior at once.
- Positive: validation-command checks no longer import through the aggregate
  facade for source regex and payload allowlist context.
- Positive: inventories and mechanics ledger rows name the actual part-local
  sub-boundaries.
- Tradeoff: `mechanic_part_readme_contract.py` still calls payload and
  source-surface subvalidators during README traversal because part-contract
  validation is incomplete without those local checks.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parts must expose README contract, payload inventory,
  source-surface refs, and validation-route evidence.
- Changed: README/index, payload inventory, and source-surface checks moved out
  of the aggregate `mechanic_parts.py` facade into focused modules. The
  aggregate facade is later removed; AOA-EV-D-0195 later removes the remaining
  part validation aggregate; AOA-EV-D-0204 later removes the remaining
  `mechanic_part_contracts.py` contract aggregate.
- Superseded by: AOA-EV-D-0188 for aggregate facade removal and AOA-EV-D-0195
  for validation aggregate removal; AOA-EV-D-0204 for contract aggregate
  removal.

## Boundaries

This decision does not let part validators define payload meaning, source eval
meaning, generated parity, release artifact freeze, runtime policy, or
trace/eval grading.

It no longer keeps `mechanic_parts.py` or `mechanic_part_contracts.py` as
compatibility or aggregate validation.

## Validation

- `python -m py_compile scripts/validators/mechanic_part_contract_common.py scripts/validators/mechanic_part_contract_index.py scripts/validators/mechanic_part_role_headings.py scripts/validators/mechanic_part_readme_contract.py scripts/validators/mechanic_part_payload_inventory.py scripts/validators/mechanic_part_source_surfaces.py scripts/validators/mechanic_parts_index_sync.py scripts/validators/mechanic_part_validation_commands.py scripts/validators/mechanic_part_validation_common.py scripts/validators/mechanics_routes.py`
- `python -m pytest -q tests/test_mechanic_part_contracts.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py tests/test_index_surface_roles.py`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
