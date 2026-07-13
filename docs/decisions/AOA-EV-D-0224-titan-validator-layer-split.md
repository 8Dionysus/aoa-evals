# Titan Validator Layer Split

- Decision ID: AOA-EV-D-0224
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Titan validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: titan, cross-parent
- Guard families: source/topology, trace/eval
- Posture: active rationale

## Context

AOA-EV-D-0141 correctly moved Titan validation out of the root mechanics
validator, but the resulting `scripts/validators/titan.py` module still mixed
separate boundaries:

- Titan route path constants;
- route token matrices and stale route-phrase checks;
- blocking seed-boundary route validation; and
- Titan seed YAML shape validation.

That shape kept source/topology route law and seed canary shape in one large
module. It also forced tests and orchestration to import the route validator
when they only needed path constants, stale phrase tokens, or canary shape.

## Decision

Remove `scripts/validators/titan.py`.

Split the Titan validation surface into focused modules:

- `scripts/validators/titan_route_paths.py` owns Titan route path constants.
- `scripts/validators/titan_route_tokens.py` owns Titan route token sets and
  stale route-phrase denylist.
- `scripts/validators/titan_routes.py` owns the injected `TitanRouteContext`
  and the blocking Titan seed-boundary route validator.
- `scripts/validators/titan_canary.py` owns Titan seed YAML shape validation.

Mechanics route orchestration imports only `titan_routes.py`. Repo-wide readout
orchestration imports only `titan_canary.py`. Tests import path and token
helpers directly instead of using a broad Titan facade.

## Rationale

Route law and seed shape fail for different reasons. The route validator checks
authored source surfaces, owner split, stale route wording, and decision-token
coverage. The canary validator checks the concrete YAML seed payload shape.

Keeping both in a single module made it too easy for route meaning to bleed into
seed-shape checks or for seed-shape constants to become a convenience API for
route tests. The split keeps Titan seed canaries bounded as evidence while
routing stronger Titan role, bearer, summon, incarnation, memory, runtime, and
proof-scoring authority elsewhere.

## Consequences

- Positive: the former broad Titan module is gone rather than preserved as an
  aggregate compatibility entrypoint.
- Positive: route orchestration and readout orchestration depend on different
  Titan validator modules.
- Positive: path and token helper modules are visible support surfaces in the
  script inventory.
- Tradeoff: tests name the helper surface they actually use.

## Boundaries

This split does not make Titan validators own Titan role classes, bearer
identity, summon boundary law, incarnation posture, memory sovereignty, runtime
activation, hidden arena behavior, mutation or judgment gate authority, or
executable proof scoring.

It does not create a replacement Titan aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
