# Checkpoint Validator Layer Split

- Decision ID: AOA-EV-D-0231
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Checkpoint validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: checkpoint, proof-object, audit, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

AOA-EV-D-0134 correctly moved Checkpoint route validation out of the root
mechanics validator. The resulting `scripts/validators/checkpoint.py` module
still mixed route path constants, route token matrices, injected route context,
and the blocking Checkpoint route validator.

Tests imported constants from that blocking validator, which made the gate act
as another historical constants bucket.

## Decision

Remove `scripts/validators/checkpoint.py`.

Split Checkpoint validation into focused modules:

- `scripts/validators/checkpoint_route_paths.py` owns Checkpoint route,
  part, posture-doc, provenance, and decision path constants.
- `scripts/validators/checkpoint_route_tokens.py` owns Checkpoint route token
  sets.
- `scripts/validators/checkpoint_routes.py` owns `CheckpointRouteContext` and
  the blocking Checkpoint route validator.

Mechanics route orchestration imports only `checkpoint_routes.py`. Tests import
path constants directly from `checkpoint_route_paths.py`.

## Rationale

Checkpoint carries high runtime, memory, self-agent, and child-output quality
pressure. `aoa-evals` validates bounded proof-support routeability; stronger
owners decide runtime activation, memory canon, autonomous self-repair
acceptance, and final output acceptance.

Separating path constants, token matrices, and route checks keeps that boundary
visible and prevents the blocking validator from becoming a generic constants
surface.

## Consequences

- Positive: the former broad Checkpoint module is gone rather than preserved as
  a compatibility entrypoint.
- Positive: Checkpoint route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Checkpoint
  validator.
- Tradeoff: Checkpoint validation imports two focused helper modules.

## Boundaries

This split does not make Checkpoint own runtime activation, memory canon,
autonomous self-repair acceptance, final child-output quality, broad
long-horizon competence, generated projection truth, or release/runtime
outcomes.

It does not create a replacement Checkpoint aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
