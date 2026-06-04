# Mechanic Parent Validator Boundary

- Decision ID: AOA-EV-D-0149
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanic_parents.py`, mechanic parent route/guidance guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

Mechanic parent validation protects parent route-card coverage, current
direction contracts, parent-level guidance doc allowlists, mechanics parent
allowlist shape, lower parts index operating-card shape, and old flat mechanic
path bans.

Before this split, `scripts/validate_repo.py` owned those parent-route checks
beside unrelated source eval topology, generated projection parity,
legacy/provenance bridge checks, route residue, and release-adjacent guards.
That kept root validation too close to mechanic parent law.

## Decision

Mechanic parent route/guidance validation lives in
`scripts/validators/mechanic_parents.py`.

The module owns:

- active parent route-card coverage for `AGENTS.md`, `README.md`,
  `DIRECTION.md`, and `PARTS.md`;
- mechanic parent allowlist checks;
- mechanic parent `DIRECTION.md`, README, and AGENTS direction contracts;
- parent-level guidance doc allowlists and content contract checks;
- lower parts index operating-card checks;
- mechanic index command ownership checks;
- forbidden old flat mechanic path checks.

`scripts/validate_repo.py` delegates to the module through
`validate_mechanic_parent_surfaces`. Tests for moved behavior import
`validators/mechanic_parents.py` directly instead of using root compatibility
wrappers.

## Rationale

Mechanic parent checks are source/topology boundaries. They decide whether a
mechanic parent exposes the route surfaces needed for current growth and keeps
part-owned payload below the part boundary.

They do not define mechanic payload meaning, generated read-model parity,
release artifact freeze, runtime policy, trace/eval grading, or sibling truth.
Keeping this boundary focused prevents `scripts/validate_repo.py` from becoming
the historical memory of every mechanic-parent wave.

## Consequences

- Positive: `validate_repo.py` no longer exports mechanic parent allowlist,
  direction, guidance, lower-index, or command-ownership wrappers.
- Positive: parent topology, parent direction, and lower parts index tests now
  call the owning module directly.
- Positive: script, validator, and evidence-cluster inventories name mechanic
  parent route/guidance as a distinct source-fast boundary.
- Follow-up: remaining root mechanics checks should split only when their
  boundary is not already covered by `mechanics.py`, `mechanic_parts.py`,
  `mechanic_legacy.py`, or this module.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parents must expose active route cards, current
  direction, allowlisted guidance, and lower parts indexes.
- Changed: mechanic parent checks moved from `scripts/validate_repo.py` to
  `scripts/validators/mechanic_parents.py`.
- Superseded by: none.

## Boundaries

This decision does not let parent validators define part payload meaning.
Payload meaning stays with the owning mechanic part and its source surfaces.

It does not turn parent-level guidance docs into payload space.

It does not make lower parts indexes command authority; executable validation
still routes through the nearest `AGENTS.md`.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanic_parents.py`
- `python -m pytest -q tests/test_mechanic_parent_topology.py tests/test_mechanic_parent_direction.py tests/test_mechanic_parts_index.py`
