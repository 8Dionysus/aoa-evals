# Distillation Validator Layer Split

- Decision ID: AOA-EV-D-0238
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Distillation validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: distillation, experience, recurrence, publication-receipts, cross-parent
- Guard families: source/topology, runtime-policy, observability/audit
- Posture: active rationale

## Context

AOA-EV-D-0140 correctly moved Distillation route validation out of the root
mechanics validator. The resulting `scripts/validators/distillation.py` module
still mixed route path constants, route token matrices, injected route context,
and the blocking Distillation route validator.

Tests imported path constants from that blocking validator.

## Decision

Remove `scripts/validators/distillation.py`.

Split Distillation validation into focused modules:

- `scripts/validators/distillation_route_paths.py` owns Distillation parent,
  part, provenance, and decision path constants.
- `scripts/validators/distillation_route_tokens.py` owns Distillation route
  token sets.
- `scripts/validators/distillation_routes.py` owns `DistillationRouteContext`
  and the blocking Distillation route validator.

Mechanics route orchestration imports only `distillation_routes.py`. Tests
import path constants from `distillation_route_paths.py`.

## Rationale

Distillation carries Tree-of-Sophia canon, memory canon, runtime promotion, live
receipt append behavior, KAG lift, owner-local adoption, and final owner
acceptance pressure. `aoa-evals` validates bounded compost and candidate-adoption
proof support; stronger owners decide canon, memory, runtime, receipt, KAG, and
owner acceptance truth.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Distillation module is gone rather than preserved
  as a compatibility entrypoint.
- Positive: Distillation route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Distillation
  validator.
- Tradeoff: Distillation validation imports two focused helper modules.

## Boundaries

This split does not make Distillation own Tree-of-Sophia canon, memory canon,
runtime promotion, live receipt append behavior, KAG lift, owner-local
adoption, final owner acceptance, legacy distillation logs, or source proof
bundle meaning.

It does not create a replacement Distillation aggregate facade.

## Validation

- `python -m py_compile scripts/validators/distillation_route_paths.py scripts/validators/distillation_route_tokens.py scripts/validators/distillation_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k distillation`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
