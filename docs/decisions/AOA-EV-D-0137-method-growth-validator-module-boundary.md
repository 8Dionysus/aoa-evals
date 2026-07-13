# Method-growth Validator Module Boundary

- Decision ID: AOA-EV-D-0137
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Method-growth validator modules, `mechanics/method-growth/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: method-growth, growth-cycle, antifragility, rpg, cross-parent
- Guard families: source/topology, trace/eval, projection/generated
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Method-growth route-token
matrix: parent route cards, candidate-lineage and owner-landing part contracts,
provenance, and Method-growth decision-token checks.

Those checks are one mechanic route boundary. They do not own final owner-object
truth, owner-local activation, derivative first-authoring, memory canon, seed
truth, stats truth, diagnosis-cause ownership, repair success, or universal
growth scoring.

## Decision

Method-growth route validation lives in focused Method-growth validator modules.

`scripts/validate_repo.py` delegates Method-growth checks through
`validate_method_growth_route_surfaces` and supplies a
`MethodGrowthRouteContext` with the root token lookup helper and shared
provenance bridge tokens.

The focused modules own Method-growth-specific route paths, token matrices,
route checks, part-contract, provenance, and decision expectations. Shared
lookup and provenance posture remain injected.

## Rationale

Method-growth is an active mechanic parent whose proof support can easily be
overread as final owner quality, permanent owner routing, derivative authority,
or growth score truth. Keeping that token matrix inside the root mechanics
validator left parent-specific growth-refinery history in the repo-wide
entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded lineage and
owner-fit proof support while routing final owner truth, derivative
first-authoring, memory, seed, stats, diagnosis, repair, and progression
meaning back to stronger owners.

## Consequences

- Positive: Method-growth route, candidate-lineage, owner-landing, provenance,
  and decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Method-growth path constants from the path helper
  directly.
- Follow-up: RPG, Growth-cycle, Distillation, Titan, and Agon can be split by
  the same owner-boundary rule when each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Method-growth route validation now lives in path, token, and route
  validator modules.
- Superseded by: AOA-EV-D-0235 removes the former aggregate module boundary.

## Boundaries

This decision does not make Method-growth the owner of final owner-object
truth, owner-local activation, derivative first-authoring, memory canon, seed
truth, stats truth, diagnosis-cause ownership, repair success, or universal
growth scoring.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into Method-growth.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
