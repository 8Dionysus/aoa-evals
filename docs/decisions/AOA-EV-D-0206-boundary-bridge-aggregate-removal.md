# Boundary Bridge Aggregate Removal

- Decision ID: AOA-EV-D-0206
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused boundary-bridge validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, inter-agent/handoff
- Mechanic parents: boundary-bridge, proof-object, proof-loop, cross-parent
- Guard families: source/topology, capability/permission, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0129 moved boundary-bridge checks out of root validation and into
`scripts/validators/boundary_bridge.py`.

That module still mixed:

- boundary-bridge route cards, sibling refs, part contracts, provenance, and
  legacy bridge checks;
- repo-validation workflow-pin hygiene; and
- latest-sibling canary matrix JSON shape.

These all protect sibling authority, but they repair through different owner
surfaces and should not become one historical boundary bucket.

## Decision

`scripts/validators/boundary_bridge.py` is removed.

Boundary-bridge validation now routes through focused modules:

- `boundary_bridge_routes.py` owns route cards, sibling-ref handoff posture,
  part contracts, provenance, legacy bridge, and decision routing.
- `boundary_bridge_workflow.py` owns `.github/workflows/repo-validation.yml`
  release-audit execution and sibling checkout/pin residue checks.
- `boundary_bridge_canary.py` owns sibling canary matrix JSON shape, expected
  repo coverage, and `abyss-stack` resolver posture.
- `boundary_bridge_common.py` is helper-only shared constants and token lookup.

`mechanics_routes.py` calls each focused validator directly.

## Rationale

Boundary-bridge is the inter-repo handoff organ, but not every handoff-adjacent
check has the same repair route. A route-card failure is fixed in the
boundary-bridge mechanic. A workflow-pin failure is fixed in the GitHub
workflow or pin-refresh decision. A matrix-shape failure is fixed in the
latest-sibling canary config.

Splitting those surfaces prevents future sibling-authority, workflow, and
matrix rules from accumulating in one broad module.

## Consequences

- Positive: no boundary-bridge aggregate validator remains.
- Positive: workflow-pin and canary-matrix failures now name their exact owner
  surfaces.
- Positive: inventories and mechanics evidence ledger no longer merge route
  handoff, workflow hygiene, and matrix shape into one owner.
- Tradeoff: `mechanics_routes.py` imports three focused boundary-bridge
  validators because it orchestrates mechanics route-domain validation.

## Current Applicability

As of 2026-06-04:

- Still valid: live sibling-canary execution remains outside source-fast
  validation.
- Changed: boundary-bridge behavior no longer lives in
  `boundary_bridge.py`; it is split across route, workflow-pin, canary-matrix,
  and helper-only modules.
- Supersedes: the aggregate module shape left by AOA-EV-D-0129.

## Boundaries

This decision does not authorize editing sibling repositories.

It does not make a pinned workflow ref or latest-sibling canary result a source
of truth for sibling repo meaning.

It does not move generated phase-alpha matrix parity or live sibling canary
execution into source-fast route validation.

It does not create a replacement boundary-bridge aggregate under another name.

## Validation

- `python -m py_compile scripts/validators/boundary_bridge_common.py scripts/validators/boundary_bridge_routes.py scripts/validators/boundary_bridge_workflow.py scripts/validators/boundary_bridge_canary.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py tests/test_repo_validation_workflow.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k boundary_bridge`
- `python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k boundary_bridge`
- `python -m pytest -q tests/test_repo_validation_workflow.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
