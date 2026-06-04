# Mechanics Routes Validator Boundary

- Decision ID: AOA-EV-D-0155
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanics_routes.py`, mechanics route-domain validation orchestration

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

After the focused mechanic validators moved out of `scripts/validate_repo.py`,
the root CLI still carried `validate_mechanics_surfaces()` and the private
route-context factories for recurrence, checkpoint, experience, antifragility,
method-growth, RPG, growth-cycle, distillation, Titan, Agon, route residue, and
Questbook.

That left the command entrypoint as the place where mechanic route-domain
behavior was assembled. Tests still called the root CLI module for mechanic
route validation, so the old mega-validator dependency survived even after the
individual checks had focused owners.

## Decision

Mechanics route-domain orchestration lives in
`scripts/validators/mechanics_routes.py`.

The module owns:

- aggregation order for focused mechanic route validators;
- route-residue context wiring for active mechanic and mechanic-payload
  residue checks;
- route-token lookup context injection for mechanic parent route validators;
- mechanic provenance bridge token injection for route validators that depend on
  active-to-archive posture;
- conversion of focused validator issue objects into the root
  `ValidationIssue` shape.

`scripts/validate_repo.py` remains the CLI entrypoint and calls
`mechanics_routes.validate_mechanics_surfaces(repo_root)` from the root topology
domain.

## Rationale

Mechanic route aggregation is not source eval meaning, generated parity, runtime
acceptance, release evidence, or the payload truth of any mechanic. It is a
cross-parent source/topology boundary that decides which focused validators run
together and how shared route context is injected.

Moving it out of `validate_repo.py` keeps the root command from becoming the
historical owner of every mechanic route rule, while avoiding a new
`validate_everything.py`: the focused modules still own the actual checks.

## Consequences

- Positive: `scripts/validate_repo.py` no longer carries
  `validate_mechanics_surfaces()` or mechanic-only route-context factories.
- Positive: mechanic route tests import the mechanic route-domain owner instead
  of the root CLI module.
- Positive: route-token and provenance context remain explicit inputs to focused
  validators rather than hidden root globals.
- Tradeoff: `mechanics_routes.py` is a deliberate orchestrator; future changes
  must keep new rule meaning in focused validators or owning mechanic surfaces.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  command.
- Changed: mechanic route-domain aggregation and mechanic route context factories
  moved to `scripts/validators/mechanics_routes.py`.
- Superseded by: none.

## Boundaries

This decision does not let `mechanics_routes.py` define mechanic payload meaning,
source eval contracts, generated projection freshness, runtime policy
acceptance, trace/eval grading, live receipt publication, release artifact
identity, or sibling compatibility truth.

It is an orchestration boundary for focused mechanic validators, not a second
root validator.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py tests/test_mechanics_topology.py`
