# Recurrence Validator Module Boundary

- Decision ID: AOA-EV-D-0133
- Status: Accepted
- Date: 2026-06-03
- Owner surface: Recurrence validator modules, `mechanics/recurrence/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: recurrence, proof-object, audit, rpg, cross-parent
- Guard families: source/topology, runtime-policy, projection/generated
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried a long recurrence parent block:
parent route cards, part READMEs, portable-proof-beacons AGENTS posture,
provenance, and recurrence decision-token checks.

Those checks are one mechanic route boundary. They do not own source proof
bundle meaning, runtime activation, audit packet curation, RPG progression
truth, or owner promotion.

## Decision

Recurrence route validation moved out of the root mechanics validator into a
Recurrence-specific validator boundary.

`scripts/validate_repo.py` delegates recurrence checks through
`validate_recurrence_route_surfaces` and supplies a `RecurrenceRouteContext`
with the root token lookup helper and shared provenance bridge tokens.

The root token lookup remains injected because it knows how to search companion
AGENTS validation cards for command tokens. The recurrence module owns the
recurrence-specific route and part-contract expectations.

## Rationale

Recurrence is an active mechanic parent with its own route cards and part
contracts. Leaving its route-token matrix inside the root mechanics validator
kept parent-specific history in the entrypoint after other mechanic parents had
already moved to focused modules.

The context boundary avoids copying shared provenance and command-token
fallback behavior while still removing recurrence-specific rules from the root
body.

## Consequences

- Positive: recurrence route, part-contract, beacon-posture, provenance, and
  decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates one more active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import recurrence constants from the owner boundary directly.
- Follow-up: Checkpoint, Experience, Antifragility, Method-growth, RPG,
  Growth-cycle, Distillation, Titan, and Agon can be split by the same
  owner-boundary rule when each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: AOA-EV-D-0227 split the former `scripts/validators/recurrence.py`
  boundary into focused route, path-helper, and token-helper modules.
- Superseded by: AOA-EV-D-0227 for module shape; still valid for why
  recurrence validation is not owned by the root mechanics validator.

## Boundaries

This decision does not make recurrence the owner of runtime activation,
runtime artifact acceptance, audit candidate packet curation, RPG progression,
or source proof bundle meaning.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into recurrence.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/recurrence_routes.py scripts/validators/recurrence_route_paths.py scripts/validators/recurrence_route_tokens.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k recurrence`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
