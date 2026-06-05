# Route Residue Facade Removal

- Decision ID: AOA-EV-D-0192
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused `scripts/validators/route_residue_*.py` domain modules

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, generated/read-model, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology, projection/generated
- Posture: active rationale

## Context

AOA-EV-D-0167 split route residue validation into focused domain modules, but
`scripts/validators/route_residue.py` remained as a compatibility and aggregate
facade. After `root_topology.py`, `mechanics_routes.py`, and tests can import
the focused domain modules directly, the aggregate file has no owner meaning
left.

## Decision

`scripts/validators/route_residue.py` is removed.

Root topology orchestration imports the root-authored, decision, repo-config,
source-bundle, and generated/readout route-residue validators directly.

Mechanics route orchestration imports active-mechanic and mechanic-payload
route-residue validators directly.

Tests import the focused route-residue module for the domain under test.

## Rationale

Route residue remains one guard family, but generated/readout references,
active mechanic route cards, root-authored docs, decision records, repo config,
source bundles, and mechanic payload files are different owner surfaces.

Keeping an aggregate facade after the split would make stale route cleanup
look like one validator again, which is the historical shape this refactor is
removing.

## Consequences

- Positive: no route-residue aggregate facade remains in source-fast topology.
- Positive: failure routes now name the focused residue domain directly.
- Positive: tests name the residue domain they exercise.
- Tradeoff: `root_topology.py` and `mechanics_routes.py` import several focused
  route-residue modules because they are orchestration surfaces.

## Current Applicability

As of 2026-06-04:

- Still valid: route-card-only districts and legacy mechanic parent paths must
  not become current authority.
- Changed: `route_residue.py` no longer exists.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0145 and
  AOA-EV-D-0167.

## Boundaries

This decision does not let generated/readout validators define source meaning,
does not let mechanic-payload residue checks define mechanic payload meaning,
and does not let route-card residue checks define runtime policy or release
artifact truth.

It does not add a replacement aggregate route-residue facade under another
name.

## Validation

- `python -m py_compile scripts/validators/root_topology.py scripts/validators/mechanics_routes.py scripts/validators/route_residue_common.py scripts/validators/route_residue_active_mechanics.py scripts/validators/route_residue_root_authored.py scripts/validators/route_residue_decisions.py scripts/validators/route_residue_repo_config.py scripts/validators/route_residue_source_bundle.py scripts/validators/route_residue_generated.py scripts/validators/route_residue_mechanic_payload.py`
- `python -m pytest -q tests/test_route_residue.py tests/test_generated_route_residue.py tests/test_mechanic_manifest_routes.py tests/test_root_surface_roles.py tests/test_mechanics_topology.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
