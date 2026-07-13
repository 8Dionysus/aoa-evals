# Experience Validator Layer Split

- Decision ID: AOA-EV-D-0232
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Experience validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: experience, distillation, proof-object, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

AOA-EV-D-0135 correctly moved Experience route validation out of the root
mechanics validator. The resulting `scripts/validators/experience.py` module
still mixed route path constants, route token matrices, injected route context,
and the blocking Experience route validator.

Tests imported constants from that blocking validator, leaving another
historical constants bucket.

## Decision

Remove `scripts/validators/experience.py`.

Split Experience validation into focused modules:

- `scripts/validators/experience_route_paths.py` owns Experience route, part,
  provenance, and decision path constants.
- `scripts/validators/experience_route_tokens.py` owns Experience route token
  sets.
- `scripts/validators/experience_routes.py` owns `ExperienceRouteContext` and
  the blocking Experience route validator.

Mechanics route orchestration imports only `experience_routes.py`. Tests import
path constants directly from `experience_route_paths.py`.

## Rationale

Experience carries strong live runtime, office, operator certification,
adoption, routing, memory, KAG, and Tree-of-Sophia pressure. `aoa-evals`
validates bounded proof-support routeability; stronger owners decide live
runtime behavior, operational authority, adoption, routing, memory, graph, and
authored-meaning truth.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Experience module is gone rather than preserved as
  a compatibility entrypoint.
- Positive: Experience route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Experience
  validator.
- Tradeoff: Experience validation imports two focused helper modules.

## Boundaries

This split does not make Experience own live runtime activation, office or
assistant authority, operator certification, owner-local adoption truth, routing
authorship, memory canon, KAG/ToS truth, broad Experience success, generated
projection truth, release publication, or runtime outcomes.

It does not create a replacement Experience aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
