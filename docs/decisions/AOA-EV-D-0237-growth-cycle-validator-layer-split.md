# Growth-cycle Validator Layer Split

- Decision ID: AOA-EV-D-0237
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Growth-cycle validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: growth-cycle, antifragility, rpg, questbook, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

AOA-EV-D-0139 correctly moved Growth-cycle route validation out of the root
mechanics validator. The resulting `scripts/validators/growth_cycle.py` module
still mixed route path constants, route token matrices, repair-diagnosis
decision boundary constants, injected route context, and the blocking
Growth-cycle route validator.

Tests imported path constants from that blocking validator.

## Decision

Remove `scripts/validators/growth_cycle.py`.

Split Growth-cycle validation into focused modules:

- `scripts/validators/growth_cycle_route_paths.py` owns Growth-cycle parent,
  lower-index, diagnosis-gate, provenance, decision, and repair-diagnosis
  boundary path constants.
- `scripts/validators/growth_cycle_route_tokens.py` owns Growth-cycle route
  token sets and repair-diagnosis boundary token sets.
- `scripts/validators/growth_cycle_routes.py` owns `GrowthCycleRouteContext`
  and the blocking Growth-cycle route validator.

Mechanics route orchestration imports only `growth_cycle_routes.py`. Tests
import path constants from `growth_cycle_route_paths.py`.

## Rationale

Growth-cycle carries repair success, progression score, reviewed closeout
acceptance, donor harvest approval, quest promotion, memory canon, runtime
activation, hidden automation, and owner-local landing pressure. `aoa-evals`
validates bounded diagnosis support and repair-diagnosis route posture; stronger
owners decide repair, progression, closeout, harvest, quest, memory, runtime,
automation, and owner-local acceptance.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Growth-cycle module is gone rather than preserved
  as a compatibility entrypoint.
- Positive: Growth-cycle route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Growth-cycle
  validator.
- Tradeoff: Growth-cycle validation imports two focused helper modules.

## Boundaries

This split does not make Growth-cycle own repair success, progression score,
reviewed closeout acceptance, donor harvest approval, quest promotion, memory
canon, runtime activation, hidden automation, owner-local landing, or source
proof bundle meaning.

It does not create a replacement Growth-cycle aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
