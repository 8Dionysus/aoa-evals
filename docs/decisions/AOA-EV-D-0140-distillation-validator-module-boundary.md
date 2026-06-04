# Distillation Validator Module Boundary

- Decision ID: AOA-EV-D-0140
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/distillation.py`, `mechanics/distillation/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: distillation, experience, recurrence, publication-receipts, cross-parent
- Guard families: source/topology, runtime-policy, observability/audit
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Distillation route-token
matrix: parent route cards, compost-provenance and runtime-candidate-adoption
part contracts, provenance, and Distillation decision-token checks.

Those checks are one mechanic route boundary. They do not own Tree-of-Sophia
canon, memory canon, runtime promotion, live receipt append behavior, KAG lift,
owner-local adoption, or final owner acceptance.

## Decision

Distillation route validation lives in `scripts/validators/distillation.py`.

`scripts/validate_repo.py` delegates Distillation checks through
`validate_distillation_route_surfaces` and supplies a
`DistillationRouteContext` with the root token lookup helper and shared
provenance bridge tokens.

The module owns Distillation-specific route, part-contract, provenance, and
decision expectations. Shared lookup and provenance posture remain injected.

## Rationale

Distillation is an active mechanic parent whose proof support can be overread
as canon transfer, memory acceptance, runtime promotion, receipt publication,
or owner-local adoption. Keeping that route-token matrix inside the root
mechanics validator left parent-specific adoption and compost history in the
repo-wide entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded distillation
proof support while routing canon, memory, runtime, receipt, KAG, and owner
acceptance truth to stronger owners.

## Consequences

- Positive: Distillation route, compost-provenance, runtime-candidate-adoption,
  provenance, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Distillation constants from the owner module directly.
- Follow-up: Titan and Agon can be split by the same owner-boundary rule when
  each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Distillation route validation now lives in
  `scripts/validators/distillation.py`.
- Superseded by: none.

## Boundaries

This decision does not make Distillation the owner of Tree-of-Sophia canon,
memory canon, runtime promotion, live receipt append behavior, KAG lift,
owner-local adoption, or final owner acceptance.

It does not move legacy distillation logs, shared mechanic topology ledgers, or
shared provenance token helpers into Distillation.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/distillation.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k distillation`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
