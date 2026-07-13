# Method-growth Validator Layer Split

- Decision ID: AOA-EV-D-0235
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Method-growth validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: method-growth, growth-cycle, antifragility, rpg, cross-parent
- Guard families: source/topology, trace/eval, projection/generated
- Posture: active rationale

## Context

AOA-EV-D-0137 correctly moved Method-growth route validation out of the root
mechanics validator. The resulting `scripts/validators/method_growth.py` module
still mixed route path constants, route token matrices, injected route context,
and the blocking Method-growth route validator.

Tests imported path constants from that blocking validator.

## Decision

Remove `scripts/validators/method_growth.py`.

Split Method-growth validation into focused modules:

- `scripts/validators/method_growth_route_paths.py` owns Method-growth parent,
  part, provenance, and decision path constants.
- `scripts/validators/method_growth_route_tokens.py` owns Method-growth route
  token sets.
- `scripts/validators/method_growth_routes.py` owns `MethodGrowthRouteContext`
  and the blocking Method-growth route validator.

Mechanics route orchestration imports only `method_growth_routes.py`. Tests
import path constants from `method_growth_route_paths.py`.

## Rationale

Method-growth carries final owner truth, owner-local activation, derivative
first-authoring, memory canon, seed truth, stats truth, diagnosis-cause
ownership, repair success, and universal growth score pressure. `aoa-evals`
validates bounded lineage and owner-fit proof support; stronger owners decide
final acceptance, derivative authorship, memory, seed, stats, diagnosis, repair,
and progression meaning.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Method-growth module is gone rather than preserved
  as a compatibility entrypoint.
- Positive: Method-growth route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Method-growth
  validator.
- Tradeoff: Method-growth validation imports two focused helper modules.

## Boundaries

This split does not make Method-growth own final owner truth, owner-local
activation, derivative first-authoring, memory canon, seed truth, stats truth,
diagnosis-cause ownership, repair success, universal growth scoring, or source
proof bundle meaning.

It does not create a replacement Method-growth aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
