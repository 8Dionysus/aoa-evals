# RPG Validator Layer Split

- Decision ID: AOA-EV-D-0236
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused RPG validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: rpg, questbook, growth-cycle, comparison-spine, cross-parent
- Guard families: source/topology, projection/generated, runtime-policy
- Posture: active rationale

## Context

AOA-EV-D-0138 correctly moved RPG route validation out of the root mechanics
validator. The resulting `scripts/validators/rpg.py` module still mixed route
path constants, route token matrices, injected route context, and the blocking
RPG route validator.

Tests imported path constants from that blocking validator.

## Decision

Remove `scripts/validators/rpg.py`.

Split RPG validation into focused modules:

- `scripts/validators/rpg_route_paths.py` owns RPG parent, progression-unlocks,
  provenance, and decision path constants.
- `scripts/validators/rpg_route_tokens.py` owns RPG route token sets.
- `scripts/validators/rpg_routes.py` owns `RpgRouteContext` and the blocking
  RPG route validator.

Mechanics route orchestration imports only `rpg_routes.py`. Tests import path
constants from `rpg_route_paths.py`.

## Rationale

RPG carries quest acceptance, universal score, rank assignment, runtime equip
state, reward logic, generated-card authority, and Growth Cycle movement
pressure. `aoa-evals` validates bounded progression and unlock proof support;
stronger owners decide quest acceptance, runtime activation/rewards, generated
reader authority, and growth movement.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad RPG module is gone rather than preserved as a
  compatibility entrypoint.
- Positive: RPG route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking RPG validator.
- Tradeoff: RPG validation imports two focused helper modules.

## Boundaries

This split does not make RPG own quest acceptance, universal score or rank,
runtime equip state, reward logic, generated-card authority, Growth Cycle
movement, or source proof bundle meaning.

It does not create a replacement RPG aggregate facade.

## Validation

- `python -m py_compile scripts/validators/rpg_route_paths.py scripts/validators/rpg_route_tokens.py scripts/validators/rpg_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k rpg`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
