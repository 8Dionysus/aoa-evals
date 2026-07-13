# Validation Topology Layer Split

- Decision ID: AOA-EV-D-0216
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused `scripts/validators/validation_*` topology validators

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/validation_topology.py` checked six different validation
authority surfaces in one module: validation docs, lane manifest, validator
inventory, script inventory, test inventory, and shared discovery helpers.

That worked as a growth gate, but it recreated the shape this refactor is
removing: one root validator that knows every lane/inventory/test topology
detail and accumulates unrelated failure routes.

## Decision

Remove `scripts/validators/validation_topology.py`.

Validation topology checks now route through focused modules:

- `scripts/validators/validation_topology_common.py` owns only constants, JSON
  loading, command parsing, and script/test discovery helpers.
- `scripts/validators/validation_topology_docs.py` owns
  `VALIDATOR_TOPOLOGY.md` and `COMMAND_AUTHORITY.md` required-token checks.
- `scripts/validators/validation_lane_manifest.py` owns
  `docs/validation/validation_lanes.json` lane ids, posture, command sequences,
  generated command grouping, and owner-surface reachability.
- `scripts/validators/validation_validator_inventory.py` owns
  `docs/validation/validator_inventory.json` fields, owner surfaces, lane/mode
  shape, and validator module discovery drift.
- `scripts/validators/validation_script_inventory.py` owns
  `docs/validation/script_inventory.json` fields, active script discovery drift,
  and lane command script classification.
- `scripts/validators/validation_test_inventory.py` owns
  `docs/testing/test_inventory.json` fields and root/part-local test discovery
  drift.

`scripts/validators/root_topology.py` calls those focused validators directly.

## Rationale

Docs authority, lane command authority, validator inventory, script inventory,
and test inventory fail for different owners. A single validator made every
change look like generic validation-topology work instead of pointing to the
surface that actually drifted.

The split keeps the same hard gate behavior while giving each source surface a
clearer boundary and smaller module.

## Consequences

- Positive: lane manifest drift fails through a lane-manifest validator.
- Positive: validator/script/test inventory drift no longer shares one broad
  code path.
- Positive: docs-token checks no longer live beside JSON inventory discovery.
- Positive: the former aggregate file is removed instead of kept as a
  compatibility facade.
- Tradeoff: `tests/test_validation_topology.py` still assembles the focused
  checks in one local helper because it tests the combined topology contract.

## Boundaries

This split does not make validation topology validators own mechanic payload
meaning, generated projection parity, runtime behavior, release packaging, or
test semantics.

Lane command execution remains owned by `scripts/ci_gate.py`,
`scripts/release_check.py`, and `scripts/validation_lanes.py`; this split only
checks the authored topology surfaces.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
