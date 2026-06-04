# Titan Validator Module Boundary

- Decision ID: AOA-EV-D-0141
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/titan.py`, `mechanics/titan/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: titan, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Titan route-token matrix:
parent route cards, direction boundary, parts lower index, seed-boundary route
cards, seed-boundary docs, stale route-phrase checks, seed-boundary decision
checks, and the Titan seed YAML shape validator.

Those checks are one seed-boundary route. They do not own Titan role classes,
bearer identity, summon boundary law, incarnation posture, memory sovereignty,
runtime activation, hidden arena behavior, mutation or judgment gate authority,
or executable proof scoring.

## Decision

Titan route and seed-canary validation lives in `scripts/validators/titan.py`.

`scripts/validate_repo.py` delegates Titan route checks through
`validate_titan_route_surfaces` and supplies a `TitanRouteContext` with the
root token lookup helper. The repo-wide `validate_titan_canary_surfaces`
entrypoint remains a thin wrapper around the Titan validator module.

The module owns Titan-specific route, seed-boundary, stale phrasing,
seed-canary shape, and decision expectations. Shared lookup posture remains
injected.

## Rationale

Titan is an owner-named proof-seed mechanic whose YAML canaries are easy to
overread as incarnation proof, summon authority, runtime cohort evidence, or
memory sovereignty. Keeping that route matrix and YAML shape validator inside
the root mechanics validator left Titan-specific agency boundaries in the
repo-wide entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded Titan seed
evidence while routing stronger Titan, memory, runtime, arena, gate, and proof
scoring truth to the owning surfaces.

## Consequences

- Positive: Titan route, seed-boundary docs, seed YAML shape, stale route
  phrasing, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Titan constants from the owner module directly.
- Follow-up: Agon can be split by the same owner-boundary rule when its route
  is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Titan route and seed-canary validation now lives in
  `scripts/validators/titan.py`.
- Superseded by: none.

## Boundaries

This decision does not make Titan the owner of Titan role classes, bearer
identity, summon boundary law, incarnation posture, memory sovereignty, runtime
activation, hidden arena behavior, mutation or judgment gate authority, or
executable proof scoring.

It does not move shared mechanic topology ledgers or route-token lookup helpers
into Titan.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/titan.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k titan`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
