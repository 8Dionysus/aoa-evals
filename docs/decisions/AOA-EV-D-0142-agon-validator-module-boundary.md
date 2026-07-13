# Agon Validator Module Boundary

- Decision ID: AOA-EV-D-0142
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Agon validator modules, `mechanics/agon/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: agon, recurrence, questbook, cross-parent
- Guard families: source/topology, trace/eval, runtime-policy
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Agon route-token matrix:
parent route cards, Agon package decision checks, nine part README contracts,
stale imperative stop-line phrase checks, and the Agon part-contract guard
decision.

Those checks are one bounded part-contract route. They do not own live
verdicts, center law, rank or trust mutation, arena execution, KAG promotion,
Tree of Sophia canon writes, recurrence hook execution, or part-local generated
registry parity.

## Decision

Agon route validation lives in focused Agon validator modules.

`scripts/validate_repo.py` delegates Agon checks through
`validate_agon_route_surfaces` and supplies an `AgonRouteContext` with the root
token lookup helper.

The focused Agon modules own Agon-specific paths, token matrices, route checks,
part README contracts, stale stop-line phrasing, and decision expectations.
Shared lookup posture remains injected without treating the blocking route
validator as a constants bucket.

## Rationale

Agon is a parent mechanic with many part-local builders, validators, generated
registries, and observe-only recurrence hooks. Keeping all part README contract
tokens in the repo-wide validator made the root entrypoint carry Agon history
and live-verdict/canon boundary pressure directly.

The module boundary keeps `aoa-evals` responsible for bounded Agon alignment
support while routing law, verdict, arena, rank, KAG, Tree of Sophia, hook
execution, and generated registry parity truth to the owning surfaces.

## Consequences

- Positive: Agon parent route, part README contracts, stale stop-line phrasing,
  and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Agon path constants and stale phrase constants from
  focused helpers directly.
- Follow-up: remaining root mechanics checks should be split only when they
  represent coherent owner boundaries, not historical aliases.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Agon route and part-contract validation now lives in path, token,
  and route validator modules.
- Superseded by: AOA-EV-D-0233 removes the former aggregate module boundary.

## Boundaries

This decision does not make Agon the owner of live verdicts, center law, rank
or trust mutation, arena execution, KAG promotion, Tree of Sophia canon writes,
recurrence hook execution, or part-local generated registry parity.

It does not move Agon part-local builders, validators, generated registries,
shared mechanic topology ledgers, or route-token lookup helpers into the root
entrypoint.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
