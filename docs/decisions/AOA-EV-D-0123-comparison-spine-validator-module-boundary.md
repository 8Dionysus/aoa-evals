# Comparison Spine Validator Module Boundary

- Decision ID: AOA-EV-D-0123
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused comparison-spine route validator modules, `mechanics/comparison-spine/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, comparison/readout, mechanics/topology
- Mechanic parents: comparison-spine, proof-object, proof-infra, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

Comparison-spine route-card and part-contract checks still lived in the broad
mechanics section of `scripts/validate_repo.py`.

Those checks protect one coherent owner surface: fixed-baseline, peer-compare,
longitudinal-window, fixture/readout placement, provenance, and anti-overread
boundaries. They do not own source bundle comparison meaning.

## Options Considered

- Keep comparison-spine checks in the broad mechanics pass.
- Merge them with generated comparison-spine parity.
- Move route, part, provenance, and anti-overread checks into
  `scripts/validators/comparison_spine.py` while keeping source bundle
  `comparison_surface` validation and generated parity in their current owner
  lanes.

## Decision

Comparison-spine route validation first lived in
`scripts/validators/comparison_spine.py`; AOA-EV-D-0220 later split that
aggregate into focused path, token, helper, and route validator modules.

`scripts/validate_repo.py` delegates the comparison-spine route-card,
part-contract, decision, provenance, and legacy fixture-placement checks to the
new module.

Source eval bundle `comparison_surface` validation remains with source-bundle
validation. Generated `generated/comparison_spine.json` parity remains in the
generated/catalog projection lane.

## Rationale

Comparison-spine is a support/readout organ. It preserves comparison posture
and anti-overread routes for fixed-baseline, peer-compare, and
longitudinal-window evidence.

It must not become stronger than `evals/**/EVAL.md`, `evals/**/eval.yaml`, or
bundle-local reports. It must also not become a second generated parity owner.
Splitting only the route/part surface keeps this boundary explicit.

## Consequences

- Positive: another mechanics owner surface leaves the root validator.
- Positive: comparison route and anti-overread checks are named without
  conflating them with generated parity.
- Tradeoff: source bundle comparison contract checks remain in the source
  validation lane until a separate source-bundle split.
- Follow-up: generated comparison-spine parity can move later as a projection
  validator if it stays below source bundle meaning.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: comparison-spine route and part checks now have a focused validator
  module.
- Changed: AOA-EV-D-0220 removes the original comparison-spine aggregate and
  keeps path constants, token matrices, route helpers, and route validation in
  separate modules.
- Superseded in part by: AOA-EV-D-0220 for comparison-spine validator splitting.

## Boundaries

This decision does not move source comparison meaning out of source eval
bundles.

It does not make a comparison readout a repo-global score, promotion decision,
runtime acceptance, or broad growth proof.

It does not make generated comparison readers source truth.

## Validation

- `python -m py_compile scripts/validators/comparison_spine_paths.py scripts/validators/comparison_spine_tokens.py scripts/validators/comparison_spine_route_helpers.py scripts/validators/comparison_spine_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_parts_index.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py tests/test_mechanic_parts_index.py -k comparison_spine`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
