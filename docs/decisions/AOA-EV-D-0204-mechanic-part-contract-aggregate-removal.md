# Mechanic Part Contract Aggregate Removal

- Decision ID: AOA-EV-D-0204
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

AOA-EV-D-0175 split mechanic part validation out of the old
`mechanic_parts.py` facade, but left `scripts/validators/mechanic_part_contracts.py`
as the remaining contract aggregate. It still mixed:

- shared mechanic part constants and token lookup;
- parent `PARTS.md` contract-token checks;
- mechanic route H1 role-heading checks; and
- part README traversal that delegates payload inventory and source refs.

Those checks are adjacent, but they repair through different owner surfaces.
Keeping them in one module made the last contract aggregate look like the
natural landing place for every future part-local rule.

## Decision

`scripts/validators/mechanic_part_contracts.py` is removed.

Mechanic part contract validation now routes through focused modules:

- `mechanic_part_contract_common.py` is helper-only shared constants and token
  lookup.
- `mechanic_part_contract_index.py` owns parent `PARTS.md` contract tokens and
  README-contract decision routing.
- `mechanic_part_role_headings.py` owns mechanic route H1 role naming for
  parent indexes, lower parts routes, part READMEs, and part VALIDATION files.
- `mechanic_part_readme_contract.py` owns part README section requirements,
  orphan route coverage, stale stop-line scaffold checks, and local traversal.
- `mechanic_part_payload_inventory.py` and `mechanic_part_source_surfaces.py`
  remain focused delegated validators for their own part-local boundaries.

`mechanics_routes.py`, `root_topology.py`, and tests import the focused modules
directly.

## Rationale

Part-local contract validation should expose the exact boundary that failed.
Parent `PARTS.md` contract tokens, route role naming, README section shape,
payload inventory, source refs, and validation-command reachability are not one
rule family just because they all touch mechanic parts.

Removing the aggregate keeps future rules from drifting into a historical
bucket and makes the validation inventory match the actual repair route.

## Consequences

- Positive: no mechanic part contract aggregate module remains.
- Positive: root and mechanics orchestrators name the focused validator they
  call.
- Positive: inventories and mechanics evidence ledger no longer present README,
  index, heading, payload, and source-ref checks as one owner surface.
- Tradeoff: there is one small helper module for shared constants and token
  lookup; it is helper-only and does not own gate meaning.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic part source-fast validation remains blocking.
- Changed: mechanic part contract behavior no longer lives in
  `mechanic_part_contracts.py`; it is split across focused contract-index,
  role-heading, README-contract, payload-inventory, source-surface, index-sync,
  and validation-command validators.
- Supersedes: the remaining contract aggregate shape left by AOA-EV-D-0175,
  AOA-EV-D-0188, and AOA-EV-D-0195.

## Boundaries

This decision does not let part validators define mechanic payload meaning,
source eval meaning, generated parity, release artifact freeze, runtime policy,
or trace/eval grading.

It does not create a replacement mechanic part contract aggregate under another
name.

## Validation

- `python -m py_compile scripts/validators/mechanic_part_contract_common.py scripts/validators/mechanic_part_contract_index.py scripts/validators/mechanic_part_role_headings.py scripts/validators/mechanic_part_readme_contract.py scripts/validators/mechanic_part_payload_inventory.py scripts/validators/mechanic_part_source_surfaces.py scripts/validators/mechanic_parts_index_sync.py scripts/validators/mechanic_part_validation_commands.py scripts/validators/mechanic_part_validation_common.py scripts/validators/mechanics_routes.py scripts/validators/root_topology.py`
- `python -m pytest -q tests/test_mechanic_part_contracts.py tests/test_index_surface_roles.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py tests/test_mechanic_parent_topology.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
