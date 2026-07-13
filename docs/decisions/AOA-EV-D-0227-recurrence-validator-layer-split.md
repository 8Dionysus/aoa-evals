# Recurrence Validator Layer Split

- Decision ID: AOA-EV-D-0227
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Recurrence validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: recurrence, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0133 correctly moved Recurrence route validation out of the root
mechanics validator. The resulting `scripts/validators/recurrence.py` module
still mixed separate layers:

- Recurrence route, part, provenance, and decision path constants;
- route, part, portable-proof-beacon, stale-phrase, and decision token sets;
  and
- the blocking Recurrence route validator with injected provenance tokens.

The module was focused on Recurrence, but it had become a path/token bucket for
tests and route orchestration.

## Decision

Remove `scripts/validators/recurrence.py`.

Split the Recurrence validation surface into focused modules:

- `scripts/validators/recurrence_route_paths.py` owns Recurrence route path
  constants.
- `scripts/validators/recurrence_route_tokens.py` owns Recurrence route token
  sets and the portable-proof-beacons stale phrase denylist.
- `scripts/validators/recurrence_routes.py` owns the injected
  `RecurrenceRouteContext` and the blocking Recurrence route validator.

Mechanics route orchestration imports only `recurrence_routes.py`. Tests import
path and token helpers directly. No replacement aggregate facade is added.

## Rationale

Recurrence carries heavy route pressure: continuity anchors, memory recall,
recursor boundaries, stats regrounding, portable proof beacons, and runtime
activation temptation. Path constants, token matrices, and route validation
change for different reasons.

The split keeps Recurrence validation bounded to source/topology route checks
while routing stronger recurrence doctrine, hidden continuity, runtime
activation, owner promotion, source bundle proof meaning, memory canon,
recursor authority, and stats truth to their owning surfaces.

## Consequences

- Positive: the former broad Recurrence module is gone rather than preserved as
  a compatibility entrypoint.
- Positive: route orchestration depends on the route validator only.
- Positive: tests no longer import path or stale phrase constants from a
  blocking validator.
- Tradeoff: Recurrence callers import more precise helper modules.

## Boundaries

This split does not make Recurrence validators own recurrence doctrine, hidden
continuity, runtime activation, owner promotion, source bundle proof meaning,
memory canon, recursor authority, stats truth, generated projection truth, or
runtime outcomes.

It does not create a replacement Recurrence aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
