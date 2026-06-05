# Comparison-spine Validator Layer Split

- Decision ID: AOA-EV-D-0220
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused comparison-spine route validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, comparison/readout, mechanics/topology
- Mechanic parents: comparison-spine, proof-object, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

AOA-EV-D-0123 correctly moved comparison-spine route and anti-overread checks
out of the root validator. The resulting module still carried four support
surfaces in one file:

- comparison-spine source, report, fixture, provenance, legacy, and decision
  path constants;
- route, part, report, fixture, provenance, and legacy token matrices;
- markdown and validation-route companion lookup helpers; and
- the actual comparison-spine route validator.

That was a smaller form of the broad historical validator shape.

## Decision

Remove `scripts/validators/comparison_spine.py`.

Comparison-spine validation is split into focused modules:

- `scripts/validators/comparison_spine_paths.py` owns path constants.
- `scripts/validators/comparison_spine_tokens.py` owns token sets.
- `scripts/validators/comparison_spine_route_helpers.py` owns route-token lookup
  helpers and validation-route companion text loading.
- `scripts/validators/comparison_spine_routes.py` owns route, part, provenance,
  legacy, and anti-overread validation.

`mechanics_routes.py` imports `comparison_spine_routes.py` directly. Tests
import path constants from `comparison_spine_paths.py`.

## Rationale

Path constants, token matrices, companion lookup, and route validation change
for different reasons. Keeping them in one module made comparison-spine look
like a general bucket for every fixture/readout concern.

The split keeps comparison-spine route validation below source-bundle meaning
and separate from generated `generated/comparison_spine.json` parity.

## Consequences

- Positive: the blocking validator now only orchestrates comparison-spine route
  checks.
- Positive: path constants and token sets are helper-only surfaces.
- Positive: route helper code no longer sits beside the full token matrix.
- Tradeoff: tests and mechanics route orchestration import more focused modules.

## Boundaries

This split does not move source comparison meaning out of source eval bundles.

It does not make comparison readouts repo-global scores, promotion decisions,
runtime acceptance, or broad growth proof.

It does not make generated comparison readers source truth.

## Validation

- `python -m py_compile scripts/validators/comparison_spine_paths.py scripts/validators/comparison_spine_tokens.py scripts/validators/comparison_spine_route_helpers.py scripts/validators/comparison_spine_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_parts_index.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py tests/test_mechanic_parts_index.py -k comparison_spine`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
