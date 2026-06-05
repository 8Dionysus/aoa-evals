# Growth-cycle Validator Module Boundary

- Decision ID: AOA-EV-D-0139
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Growth-cycle validator modules, `mechanics/growth-cycle/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: growth-cycle, antifragility, rpg, questbook, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Growth-cycle route-token matrix:
parent route cards, parts lower index, diagnosis-gate part contract,
provenance, Growth-cycle decision-token checks, and the repair-diagnosis route
boundary decision.

Those checks are one diagnosis route boundary. They do not own repair success,
progression score, reviewed closeout acceptance, donor harvest approval, quest
promotion, memory canon, runtime activation, hidden automation, or owner-local
landing.

## Decision

Growth-cycle route validation lives in focused Growth-cycle validator modules.

`scripts/validate_repo.py` delegates Growth-cycle checks through
`validate_growth_cycle_route_surfaces` and supplies a
`GrowthCycleRouteContext` with the root token lookup helper and shared
provenance bridge tokens.

The focused modules own Growth-cycle-specific route paths, token matrices,
route checks, diagnosis-gate, lower parts index, repair-diagnosis boundary,
provenance, and decision expectations. Shared lookup and provenance posture
remain injected.

## Rationale

Growth-cycle is an active mechanic parent whose first proven operation is
diagnosis-cause discipline. Keeping the diagnosis and repair-boundary token
matrix inside the root mechanics validator left cause/repair/progression
history in the repo-wide entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded diagnosis support
while routing repair success, progression, closeout, donor harvest, quest,
memory, runtime, hidden automation, and owner-local landing to stronger owners.

## Consequences

- Positive: Growth-cycle route, parts-index, diagnosis-gate, provenance,
  repair-diagnosis boundary, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Growth-cycle path constants from the path helper
  directly.
- Follow-up: Distillation, Titan, and Agon can be split by the same
  owner-boundary rule when each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Growth-cycle route validation now lives in path, token, and route
  validator modules.
- Superseded by: AOA-EV-D-0237 removes the former aggregate module boundary.

## Boundaries

This decision does not make Growth-cycle the owner of repair success,
progression score, reviewed closeout acceptance, donor harvest approval, quest
promotion, memory canon, runtime activation, hidden automation, or owner-local
landing.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into Growth-cycle.

## Validation

- `python -m py_compile scripts/validators/growth_cycle_route_paths.py scripts/validators/growth_cycle_route_tokens.py scripts/validators/growth_cycle_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k "growth_cycle or repair_diagnosis_route_boundary"`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
