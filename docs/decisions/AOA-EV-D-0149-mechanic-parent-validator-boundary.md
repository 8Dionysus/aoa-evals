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
  focused mechanic legacy/provenance validators, or this module.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parents must expose active route cards, current
  direction, allowlisted guidance, and lower parts indexes.
- Changed: mechanic parent checks moved from `scripts/validate_repo.py` to
  `scripts/validators/mechanic_parents.py`; current-direction checks later
  moved into `scripts/validators/mechanic_parent_direction.py`; the remaining
  aggregate was removed under AOA-EV-D-0194.
- Superseded by: AOA-EV-D-0177 for mechanic parent current-direction checks
  and AOA-EV-D-0194 for the current focused allowlist, guidance, and index
  boundaries.

## Review Log

### 2026-06-04 - Current-direction split

- Previous assumption: `mechanic_parents.py` owned parent direction contracts
  inline alongside allowlist, guidance docs, lower-index command hygiene, and
  legacy path bans.
- New reality: `mechanic_parents.py` delegates parent `DIRECTION.md`,
  README/AGENTS direction-entry routes, stale route wording, and direction
  decision checks to `scripts/validators/mechanic_parent_direction.py`.
- Reason: current direction is a distinct source/topology boundary and should
  not remain hidden inside the aggregate parent validator.
- Source surfaces updated: `scripts/validators/mechanic_parents.py`,
  `scripts/validators/mechanic_parent_common.py`,
  `scripts/validators/mechanic_parent_direction.py`, validation inventories,
  and mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Aggregate removal

- Previous assumption: `mechanic_parents.py` could remain as an aggregate
  validator after direction moved out.
- New reality: `mechanic_parents.py` no longer exists; allowlist, guidance,
  index hygiene, and direction checks live in focused modules.
- Reason: the aggregate was no longer an owner boundary and kept unlike parent
  concerns behind one historical import path.
- Source surfaces updated: `scripts/validators/mechanic_parent_allowlist.py`,
  `scripts/validators/mechanic_parent_guidance.py`,
  `scripts/validators/mechanic_parent_index.py`,
  `scripts/validators/mechanic_parent_direction.py`,
  `scripts/validators/mechanics_routes.py`, validation inventories, and
  mechanics residual classification.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not let parent validators define part payload meaning.
Payload meaning stays with the owning mechanic part and its source surfaces.

It does not turn parent-level guidance docs into payload space.

It does not make lower parts indexes command authority; executable validation
still routes through the nearest `AGENTS.md`.

Current-direction route checks live in
`scripts/validators/mechanic_parent_direction.py`; allowlist checks live in
`scripts/validators/mechanic_parent_allowlist.py`; guidance checks live in
`scripts/validators/mechanic_parent_guidance.py`; index command-hygiene checks
live in `scripts/validators/mechanic_parent_index.py`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
