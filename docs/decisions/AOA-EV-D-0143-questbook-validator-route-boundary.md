# Questbook Validator Route Boundary

- Decision ID: AOA-EV-D-0143
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/questbook.py`, `mechanics/questbook/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology, generated/read-model
- Mechanic parents: questbook, rpg, agon, cross-parent
- Guard families: source/topology, projection/generated, trace/eval
- Posture: active rationale

## Context

`scripts/validators/questbook.py` already owned quest source records,
generated quest dispatch readers, quest schemas, and RPG unlock bridge checks.
`scripts/validate_repo.py` still carried the adjacent Questbook route surfaces:
`quests/` route cards, lifecycle route residue, Agon quest-note provenance
decision checks, Questbook parent route cards, part owner-split contracts,
provenance bridge posture, and Questbook decision-token checks.

Those checks are one Questbook boundary. They do not own live task assignment,
proof-surface promotion, owner acceptance, runtime dispatch, or final quest
state movement.

## Decision

Quest route and Questbook mechanic route validation live in
`scripts/validators/questbook.py`.

`scripts/validate_repo.py` calls the Questbook validator module directly,
supplying a `QuestbookRouteContext` with the root token lookup helper and
shared provenance bridge tokens for route-token checks.

The module owns Questbook-specific source, projection, route, part-contract,
lifecycle residue, and decision expectations. Shared lookup and provenance
posture remain injected.

## Rationale

Keeping source/projection truth in `scripts/validators/questbook.py` while
leaving route and part-contract truth in the root validator split one owner
surface across two modules. That made the repo-wide entrypoint remember
Questbook history and Agon quest-note routing.

The module boundary keeps `aoa-evals` responsible for source quest records,
generated dispatch parity, route cards, and part owner-split posture while
routing live assignment, proof promotion, owner acceptance, and runtime dispatch
to stronger owners.

## Consequences

- Positive: Quest source/projection, route residue, parent route, part
  owner-split, provenance, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` no longer retains
  Questbook-specific token matrices, and root no longer re-exports Questbook
  source/projection helper APIs.
- Positive: tests import Questbook route constants from the owner module
  directly.
- Follow-up: remaining root constants should be reduced only when the owning
  module can carry the full boundary without compatibility aliases.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Quest route and Questbook mechanic route validation now lives in
  `scripts/validators/questbook.py`; tests import Questbook helpers and schema
  constants from the owning module.
- Superseded by: none.

## Boundaries

This decision does not make Questbook the owner of live task assignment,
proof-surface promotion, owner acceptance, runtime dispatch, or final quest
state movement.

It does not move shared mechanic topology ledgers or route-token lookup helpers
into Questbook.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/questbook.py tests/test_mechanic_surface_contracts.py tests/test_quest_and_reader_surfaces.py tests/validate_repo_fixtures.py`
- `python -m pytest -q tests/test_quest_and_reader_surfaces.py -k quest_route`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k questbook`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
