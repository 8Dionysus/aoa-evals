# Checkpoint Validator Module Boundary

- Decision ID: AOA-EV-D-0134
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused Checkpoint validator modules, `mechanics/checkpoint/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: checkpoint, proof-object, audit, cross-parent
- Guard families: source/topology, runtime-policy, trace/eval
- Posture: active rationale

## Context

`validate_mechanics_surfaces` still carried the checkpoint route-token matrix:
parent route cards, A2A summon-return and restartable-inquiry part contracts,
self-agent checkpoint posture, provenance, and checkpoint decision-token checks.

Those checks are one mechanic route boundary. They do not own runtime
activation, memory canon, autonomous self-repair acceptance, child-output
quality, or broad long-horizon competence claims.

## Decision

Checkpoint route validation lives in focused Checkpoint validator modules.

`scripts/validate_repo.py` delegates checkpoint checks through
`validate_checkpoint_route_surfaces` and supplies a `CheckpointRouteContext`
with the root token lookup helper and shared provenance bridge tokens.

The root token lookup remains injected because it knows how to search companion
AGENTS validation cards for command tokens. The focused Checkpoint modules own
checkpoint-specific paths, token matrices, route checks, posture-doc,
provenance, and decision expectations without treating the blocking route
validator as a constants bucket.

## Rationale

Checkpoint is an active mechanic parent with multiple support parts and strong
pressure toward runtime, memory, and self-agent interpretation. Keeping its
route-token matrix inside the root mechanics validator made the entrypoint look
like a historical gate pile instead of a repo-wide boundary organ.

The module boundary keeps checkpoint support posture explicit while preserving
the owner split: `aoa-evals` validates bounded proof support, and stronger
owners decide runtime activation, memory authority, self-agent behavior, and
final output acceptance.

## Consequences

- Positive: checkpoint route, part-contract, posture-doc, provenance, and
  decision-token checks have one focused owner.
- Positive: `validate_mechanics_surfaces` delegates another active mechanic
  parent instead of retaining parent-specific history.
- Positive: tests import checkpoint path constants from the path helper
  directly.
- Follow-up: Experience, Antifragility, Method-growth, RPG, Growth-cycle,
  Distillation, Titan, and Agon can be split by the same owner-boundary rule
  when each route is handled deliberately.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide command
  entrypoint.
- Changed: checkpoint route validation now lives in path, token, and route
  validator modules.
- Superseded by: AOA-EV-D-0231 removes the former aggregate module boundary.

## Boundaries

This decision does not make checkpoint the owner of runtime activation,
memory canon, autonomous self-repair acceptance, final child-output quality, or
broad long-horizon competence claims.

It does not move shared mechanic topology ledgers or shared provenance token
helpers into checkpoint.

## Validation

- `python -m py_compile scripts/validators/checkpoint_route_paths.py scripts/validators/checkpoint_route_tokens.py scripts/validators/checkpoint_routes.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k checkpoint`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python -m pytest -q`
- `python scripts/release_check.py`
