# Root Route-card Validator Module Boundary

- Decision ID: AOA-EV-D-0144
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/root_route_cards.py`, root route-card-only districts

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, root/topology, source/topology
- Mechanic parents: none
- Guard families: source/topology
- Posture: active rationale

## Context

Root compatibility districts such as `fixtures/`, `schemas/`, `reports/`,
`examples/`, and `config/` are route-card-only surfaces. They exist to point
agents back to owning eval bundles or mechanic parts, not to become active
payload homes again.

`scripts/validate_repo.py` still carried the district allowlist, route-card
token matrix, root route-card guard decision checks, and stray-payload scan.
That made the repo-wide entrypoint look like the owner of these root districts.

## Decision

Root route-card-only district validation lives in
`scripts/validators/root_route_cards.py`.

`scripts/validate_repo.py` keeps only the repo-wide orchestration path and
injects the shared token lookup context. Tests import route-card constants and
the validator from the owner module.

## Rationale

The route-card guard is a source/topology boundary, not release packaging,
generated parity, runtime smoke, or historical cleanup. Keeping it in the root
validator made the root file hold a permanent topology ledger for a bounded
surface that can be named and tested directly.

The focused module keeps the rule visible without making root a second source
of active payload meaning.

## Consequences

- Positive: route-card-only district rules are owned by a focused validator
  module.
- Positive: `validate_repo.py` no longer exports root route-card constants or
  wrapper functions.
- Positive: route-residue validators import the root district contract from the
  route-card module instead of duplicating it.
- Follow-up: remaining root topology guards should be split only when their
  owner surface is equally clear.

## Current Applicability

As of 2026-06-04:

- Still valid: root compatibility districts remain route-card-only.
- Changed: route-card district validation moved from `scripts/validate_repo.py`
  to `scripts/validators/root_route_cards.py`.
- Superseded by: none.

## Boundaries

This decision does not authorize active payloads in root compatibility
districts.

It does not make the route-card validator own eval bundle meaning, mechanic
payload meaning, generated projection parity, or release packaging.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/root_route_cards.py tests/test_route_residue.py`
- `python -m pytest -q tests/test_route_residue.py`
