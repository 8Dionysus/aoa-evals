# Mechanic Part Facade Removal

- Decision ID: AOA-EV-D-0188
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic-part validator modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanic part, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0165 and AOA-EV-D-0175 split mechanic part validation into focused
validators, but `scripts/validators/mechanic_parts.py` still existed as a
compatibility facade. It re-exported constants and helper functions, then
called the focused README/index and validation-command validators.

After direct callers moved to the focused modules, the facade had no owner
meaning left.

## Decision

`scripts/validators/mechanic_parts.py` is removed.

Mechanics route orchestration now calls:

- `mechanic_part_contract_index.validate_mechanic_part_contract_index_surfaces`;
- `mechanic_part_readme_contract.validate_mechanic_part_readme_contract_surfaces`;
- `mechanic_parts_index_sync.validate_mechanic_parts_index_sync_surfaces`; and
- `mechanic_part_validation_commands.validate_mechanic_part_validation_command_surfaces`.

Root topology and tests import the focused module that owns the checked
surface.

## Rationale

The focused part validators already express the real boundaries: README/index
contracts, payload inventory, source-surface refs, PARTS synchronization, and
validation-command reachability.

Keeping a facade would invite future rules to land in a broad mechanic part
bucket instead of the owning boundary.

## Consequences

- Positive: mechanic part checks no longer route through compatibility aliases.
- Positive: tests name the focused part owner they exercise.
- Positive: validation inventories and mechanics evidence ledger no longer list
  a facade as a blocking source-fast validator.
- Tradeoff: `mechanics_routes.py` has explicit calls to the focused part
  validators, because it is the route-domain orchestrator.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic part source-fast validation remains blocking.
- Changed: aggregate part validation moved from `mechanic_parts.py` into direct
  calls from `mechanics_routes.py`; the later `mechanic_part_validation.py`
  aggregate is also removed by AOA-EV-D-0195, and the remaining
  `mechanic_part_contracts.py` aggregate is removed by AOA-EV-D-0204.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0147 and
  AOA-EV-D-0175.
- Superseded by: AOA-EV-D-0195 for the remaining validation aggregate and
  AOA-EV-D-0204 for the remaining contract aggregate.

## Boundaries

This decision does not let part validators define mechanic payload meaning,
source eval meaning, generated parity, release artifact freeze, runtime policy,
or trace/eval grading.

It does not add a new aggregate part facade under another name.

## Validation

- `python -m py_compile scripts/validators/mechanics_routes.py scripts/validators/root_topology.py scripts/validators/mechanic_part_contract_common.py scripts/validators/mechanic_part_contract_index.py scripts/validators/mechanic_part_readme_contract.py scripts/validators/mechanic_part_role_headings.py scripts/validators/mechanic_part_payload_inventory.py scripts/validators/mechanic_part_source_surfaces.py scripts/validators/mechanic_parts_index_sync.py scripts/validators/mechanic_part_validation_commands.py scripts/validators/mechanic_part_validation_common.py`
- `python -m pytest -q tests/test_index_surface_roles.py tests/test_mechanic_part_contracts.py tests/test_mechanic_parts_index.py tests/test_mechanic_part_validation_commands.py tests/test_mechanic_parent_topology.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
