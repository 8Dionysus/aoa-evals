# Agon Validator Layer Split

- Decision ID: AOA-EV-D-0233
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Agon validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: agon, recurrence, questbook, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

AOA-EV-D-0142 correctly moved Agon route validation out of the root mechanics
validator. The resulting `scripts/validators/agon.py` module still mixed route
path constants, route token matrices, the part README contract matrix, stale
stop-line phrases, injected route context, and the blocking Agon route
validator.

Tests imported both path and stale-phrase constants from that blocking
validator.

## Decision

Remove `scripts/validators/agon.py`.

Split Agon validation into focused modules:

- `scripts/validators/agon_route_paths.py` owns Agon parent, part README, and
  decision path constants.
- `scripts/validators/agon_route_tokens.py` owns Agon route token sets, the part
  README contract matrix, and stale stop-line phrases.
- `scripts/validators/agon_routes.py` owns `AgonRouteContext` and the blocking
  Agon route validator.

Mechanics route orchestration imports only `agon_routes.py`. Tests import path
constants from `agon_route_paths.py` and stale phrase constants from
`agon_route_tokens.py`.

## Rationale

Agon carries live-verdict, center-law, rank/trust, arena, KAG, Tree-of-Sophia,
recurrence-hook, and generated-registry pressure. `aoa-evals` validates bounded
part-contract routeability; stronger owners decide law, verdicts, canon writes,
rank/trust mutation, arena execution, promotion, and generated registry parity.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Agon module is gone rather than preserved as a
  compatibility entrypoint.
- Positive: Agon route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Agon validator.
- Tradeoff: Agon validation imports two focused helper modules.

## Boundaries

This split does not make Agon own live verdicts, center law, rank or trust
mutation, arena execution, KAG promotion, Tree-of-Sophia canon writes,
recurrence hook execution, part-local generated registry parity, generated
projection truth, release publication, or runtime outcomes.

It does not create a replacement Agon aggregate facade.

## Validation

- `python -m py_compile scripts/validators/agon_route_paths.py scripts/validators/agon_route_tokens.py scripts/validators/agon_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_parent_direction.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py tests/test_mechanic_parent_direction.py -k agon`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
