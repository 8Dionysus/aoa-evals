# Antifragility Validator Module Boundary

- Decision ID: AOA-EV-D-0136
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Antifragility validator modules, `mechanics/antifragility/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: antifragility, growth-cycle, comparison-spine, audit, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Antifragility route-token
matrix: parent route cards, parts lower index, posture/stress/repair part
contracts, stress-window posture doc, provenance, stale parts-index scaffold
guard, and Antifragility decision-token checks.

Those checks are one mechanic route boundary. They do not own live runtime
repair, cleanup authority, permanent stability, one-score stats truth, memory
truth, generated-reader truth, or Growth Cycle completion.

## Decision

Antifragility route validation lives in focused Antifragility validator
modules.

`scripts/validate_repo.py` delegates Antifragility checks through
`validate_antifragility_route_surfaces` and supplies an
`AntifragilityRouteContext` with the root token lookup helper and shared
provenance bridge tokens.

The focused modules own Antifragility-specific route paths, token matrices,
route checks, part-contract, stress-window, stale-scaffold, provenance, and
decision expectations. Shared lookup and provenance posture remain injected.

## Rationale

Antifragility is an active mechanic parent with strong pressure toward runtime
repair, cleanup, stats, memo, growth-cycle, and owner-local stability claims.
Keeping its route-token matrix in the root mechanics validator left
parent-specific stress/repair history inside the repo-wide entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded proof support
and stop-line posture while routing live repair authority, cleanup execution,
stats interpretation, memory truth, and growth-cycle completion back to their
stronger owners.

## Consequences

- Positive: Antifragility route, parts-index, part-contract, stress-window,
  provenance, stale-scaffold, and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Antifragility path constants from the path helper
  directly.
- Follow-up: Method-growth, RPG, Growth-cycle, Distillation, Titan, and Agon
  can be split by the same owner-boundary rule when each route is handled
  deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Antifragility route validation now lives in path, token, and route
  validator modules.
- Superseded by: AOA-EV-D-0234 removes the former aggregate module boundary.

## Boundaries

This decision does not make Antifragility the owner of runtime repair, cleanup
authority, permanent stability, one-score stats truth, memory truth,
generated-reader truth, or Growth Cycle completion.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into Antifragility.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
