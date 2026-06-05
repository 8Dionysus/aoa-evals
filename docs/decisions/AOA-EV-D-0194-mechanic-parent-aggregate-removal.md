# Mechanic Parent Aggregate Removal

- Decision ID: AOA-EV-D-0194
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic-parent validator modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, source/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0149 moved mechanic parent validation out of `scripts/validate_repo.py`,
and AOA-EV-D-0177 split current-direction checks into
`scripts/validators/mechanic_parent_direction.py`. The old
`scripts/validators/mechanic_parents.py` file still remained as an aggregate
container for allowlist, guidance-doc policy, index command hygiene, forbidden
legacy paths, and direction delegation.

That aggregate was no longer an owner boundary. It preserved the broad
historical shape that this refactor is removing.

## Decision

`scripts/validators/mechanic_parents.py` is removed.

Mechanic parent validation is split into focused modules:

- `mechanic_parent_allowlist.py` owns mechanics root allowlist, active parent
  route-card coverage, parent-class and legacy-skeleton handoffs, allowlist
  decision routing, and forbidden legacy active paths.
- `mechanic_parent_guidance.py` owns parent-level docs allowlists,
  mechanic-wide guidance content contracts, and guidance-boundary decision
  routing.
- `mechanic_parent_index.py` owns parent/lower index command ownership and
  lower parts index operating-card posture.
- `mechanic_parent_direction.py` continues to own current-direction contracts.

`mechanics_routes.py` orchestrates these focused modules directly.

## Rationale

Parent allowlist, guidance-doc admission, current direction, and index command
hygiene are all source/topology checks, but they protect different owner
surfaces. Keeping them behind an aggregate made the parent validator a place to
accumulate unrelated mechanic-parent rules.

Direct orchestration keeps each failure route close to the surface it protects.

## Consequences

- Positive: no mechanic-parent aggregate validator remains in source-fast
  topology.
- Positive: tests import allowlist, guidance, direction, and index validators
  directly.
- Positive: inventories and evidence ledger now name the focused mechanic
  parent boundaries.
- Tradeoff: `mechanics_routes.py` imports several mechanic-parent validators
  because it is the mechanic route-domain orchestrator.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanic parents must expose active route cards, current
  direction, allowlisted guidance, and lower parts indexes.
- Changed: `mechanic_parents.py` no longer exists.
- Supersedes: the aggregate parent-validator shape left by AOA-EV-D-0149 and
  AOA-EV-D-0177.

## Boundaries

This decision does not move mechanic payload meaning into root validators.

It does not let allowlist checks own direction contracts, guidance docs own
payload space, index hygiene own part validation command reachability, or
direction checks own parent admission.

It does not create a replacement aggregate mechanic-parent validator under
another name.

## Validation

- `python -m py_compile scripts/validators/mechanic_parent_allowlist.py scripts/validators/mechanic_parent_guidance.py scripts/validators/mechanic_parent_index.py scripts/validators/mechanic_parent_common.py scripts/validators/mechanic_parent_direction.py scripts/validators/mechanic_legacy_archive.py scripts/validators/mechanics_routes.py tests/test_mechanic_parent_topology.py tests/test_mechanic_parent_direction.py tests/test_mechanic_parts_index.py tests/test_mechanic_legacy_archive_routes.py`
- `python -m pytest -q tests/test_mechanic_parent_topology.py tests/test_mechanic_parent_direction.py tests/test_mechanic_parts_index.py tests/test_mechanic_legacy_archive_routes.py -k "mechanic_parent or mechanic_index or lower_parts_index or legacy_readmes"`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
