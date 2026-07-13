# RPG Validator Module Boundary

- Decision ID: AOA-EV-D-0138
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused RPG validator modules, `mechanics/rpg/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: rpg, questbook, growth-cycle, comparison-spine, cross-parent
- Guard families: source/topology, projection/generated, runtime-policy
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the RPG route-token matrix: parent
route cards, progression-unlocks part contract, provenance, and RPG
decision-token checks.

Those checks are one mechanic route boundary. They do not own quest acceptance,
universal rank or score, runtime equip state, generated-card authority, reward
logic, or Growth Cycle movement.

## Decision

RPG route validation lives in focused RPG validator modules.

`scripts/validate_repo.py` delegates RPG checks through
`validate_rpg_route_surfaces` and supplies an `RpgRouteContext` with the root
token lookup helper and shared provenance bridge tokens.

The focused modules own RPG-specific route paths, token matrices, route checks,
progression-unlocks, provenance, and decision expectations. Shared lookup and
provenance posture remain injected.

## Rationale

RPG is an active mechanic parent whose proof support can be overread as broad
capability growth, universal score, unlock assignment, or runtime reward
authority. Keeping that token matrix inside the root mechanics validator left
progression-specific history in the repo-wide entrypoint.

The module boundary keeps `aoa-evals` responsible for bounded progression and
unlock proof support while routing quest acceptance, runtime equip/reward
logic, generated-card authority, and Growth Cycle movement to stronger owners.

## Consequences

- Positive: RPG route, progression-unlocks, provenance, and decision-token
  checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import RPG path constants from the path helper directly.
- Follow-up: Growth-cycle, Distillation, Titan, and Agon can be split by the
  same owner-boundary rule when each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: RPG route validation now lives in path, token, and route validator
  modules.
- Superseded by: AOA-EV-D-0236 removes the former aggregate module boundary.

## Boundaries

This decision does not make RPG the owner of quest acceptance, universal score
or rank, runtime equip state, generated-card authority, reward logic, or Growth
Cycle movement.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into RPG.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
