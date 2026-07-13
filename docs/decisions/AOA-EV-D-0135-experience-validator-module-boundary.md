# Experience Validator Module Boundary

- Decision ID: AOA-EV-D-0135
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Experience validator modules, `mechanics/experience/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: experience, distillation, proof-object, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the Experience route-token matrix:
parent route cards, protocol/certification/adoption/governance/office part
contracts, provenance, and Experience decision-token checks.

Those checks are one mechanic route boundary. They do not own live runtime
activation, office or assistant authority, operator certification, owner-local
adoption truth, routing authorship, memory canon, KAG/ToS truth, or broad
Experience success claims.

## Decision

Experience route validation lives in focused Experience validator modules.

`scripts/validate_repo.py` delegates Experience checks through
`validate_experience_route_surfaces` and supplies an `ExperienceRouteContext`
with the root token lookup helper and shared provenance bridge tokens.

The root token lookup remains injected because it knows how to search companion
AGENTS validation cards for command tokens. The focused Experience modules own
Experience-specific paths, token matrices, route checks, provenance, and
decision expectations without treating the blocking route validator as a
constants bucket.

## Rationale

Experience is an active mechanic parent with strong pressure toward runtime,
office, operator, routing, KAG, Tree-of-Sophia, and adoption interpretation.
Keeping its route-token matrix inside the root mechanics validator made the
entrypoint carry parent-specific history after focused validator modules became
the active route.

The module boundary preserves the bounded proof role: `aoa-evals` validates
Experience support posture and owner split, while stronger owners decide live
runtime behavior, operational authority, adoption, routing, memory, graph, and
authored-meaning truth.

## Consequences

- Positive: Experience route, part-contract, provenance, and decision-token
  checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific token matrices.
- Positive: tests import Experience path constants from the path helper
  directly.
- Follow-up: Antifragility, Method-growth, RPG, Growth-cycle, Distillation,
  Titan, and Agon can be split by the same owner-boundary rule when each route
  is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: Experience route validation now lives in path, token, and route
  validator modules.
- Superseded by: AOA-EV-D-0232 removes the former aggregate module boundary.

## Boundaries

This decision does not make Experience the owner of live runtime activation,
office or assistant authority, operator certification, owner-local adoption
truth, routing authorship, memory canon, KAG/ToS truth, or broad Experience
success claims.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into Experience.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
