# Antifragility Validator Layer Split

- Decision ID: AOA-EV-D-0234
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused Antifragility validator modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: antifragility, growth-cycle, comparison-spine, audit, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

AOA-EV-D-0136 correctly moved Antifragility route validation out of the root
mechanics validator. The resulting `scripts/validators/antifragility.py`
module still mixed route path constants, route token matrices, stale lower-index
scaffold tokens, injected route context, and the blocking Antifragility route
validator.

Tests imported path constants from that blocking validator.

## Decision

Remove `scripts/validators/antifragility.py`.

Split Antifragility validation into focused modules:

- `scripts/validators/antifragility_route_paths.py` owns Antifragility parent,
  lower-index, part, provenance, and decision path constants.
- `scripts/validators/antifragility_route_tokens.py` owns Antifragility route
  token sets and stale parts-index scaffold phrases.
- `scripts/validators/antifragility_routes.py` owns
  `AntifragilityRouteContext` and the blocking Antifragility route validator.

Mechanics route orchestration imports only `antifragility_routes.py`. Tests
import path constants from `antifragility_route_paths.py`.

## Rationale

Antifragility carries runtime repair, cleanup authority, permanent stability,
one-score stats, memory truth, generated-reader truth, and growth-cycle
completion pressure. `aoa-evals` validates bounded proof support and owner split;
stronger owners decide live repair, cleanup execution, stats meaning, memory
authority, generated-reader authority, and completion.

Separating path constants, token matrices, and route checks keeps that owner
split visible and prevents the blocking validator from becoming a generic
constants surface.

## Consequences

- Positive: the former broad Antifragility module is gone rather than preserved
  as a compatibility entrypoint.
- Positive: Antifragility route orchestration depends only on the route gate.
- Positive: tests no longer import constants from the blocking Antifragility
  validator.
- Tradeoff: Antifragility validation imports two focused helper modules.

## Boundaries

This split does not make Antifragility own runtime repair, cleanup authority,
permanent stability, one-score stats truth, memory truth, generated-reader
truth, source proof bundle meaning, or Growth Cycle completion.

It does not create a replacement Antifragility aggregate facade.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
