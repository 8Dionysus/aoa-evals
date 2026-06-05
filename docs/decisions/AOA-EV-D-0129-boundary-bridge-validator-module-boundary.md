# Boundary Bridge Validator Module Boundary

- Decision ID: AOA-EV-D-0129
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused boundary-bridge validators and `mechanics/boundary-bridge/`
- Refined by: AOA-EV-D-0206

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, inter-agent/handoff
- Mechanic parents: boundary-bridge, proof-object, proof-loop, cross-parent
- Guard families: source/topology, capability/permission, release/nightly
- Posture: active rationale

## Context

Boundary-bridge route checks still lived inside the broad
`validate_mechanics_surfaces` body.

That block checked one route organ: sibling proof refs, the parent route card,
`PARTS.md`, provenance, compatibility-map, latest-sibling-canary,
orchestrator-proof-anchors, legacy routing, and the boundary-bridge
part-contract decision.

The same area also contains repo-validation workflow-pin and sibling-canary
matrix shape checks. Workflow-pin hygiene protects sibling authority in the
public validation lane, while current canary execution remains a live drift
check.

## Options Considered

- Leave all boundary-bridge checks in `scripts/validate_repo.py`.
- Move route-card checks and matrix shape checks into one boundary-bridge
  module.
- Move route-card, provenance, legacy, sibling-ref, part-contract,
  repo-validation workflow-pin hygiene, and sibling-canary matrix shape checks
  into `scripts/validators/boundary_bridge.py`.

## Decision

Boundary-bridge route validation lives in
`scripts/validators/boundary_bridge.py`.

`scripts/validate_repo.py` delegates boundary-bridge route-card,
compatibility-map, handoff, provenance, legacy, active-part, decision,
repo-validation workflow-pin hygiene, and sibling-canary matrix shape checks to
the boundary-bridge module.

Tests import boundary-bridge constants from
`scripts/validators/boundary_bridge.py` directly. `scripts/validate_repo.py`
no longer re-exports boundary-bridge compatibility aliases.

## Rationale

Boundary-bridge is the inter-repo handoff organ. It can say which sibling ref
is current, legacy, rejected, or unresolved, and it can route authority-transfer
pressure to the sibling owner. It must not silently become permission to edit a
sibling repository or replace that sibling's own validation.

Keeping these route checks in the root validator made
`validate_mechanics_surfaces` carry historical sibling-handoff knowledge
directly. Moving them into a focused module makes the owner boundary visible
while preserving separate live gates for sibling canary execution and generated
phase-alpha matrix parity. Repo-validation workflow-pin hygiene and
sibling-canary matrix shape are now included in the boundary-bridge module
because they protect the same sibling authority-transfer boundary.

## Consequences

- Positive: another coherent route-card block leaves
  `validate_mechanics_surfaces`.
- Positive: boundary-bridge provenance, legacy routing, sibling-ref posture,
  active parts, part-contract checks, repo-validation workflow-pin hygiene, and
  sibling-canary matrix shape now have one validator owner.
- Positive: boundary-bridge test fixtures now route to the focused module
  instead of preserving root compatibility aliases.
- Follow-up: live sibling-canary execution remains an explicit advisory/latest
  sibling lane outside the source-fast route validator.

## Current Applicability

As of 2026-06-03:

- Still valid: live sibling-canary execution remains outside this source-fast
  module.
- Changed: boundary-bridge route-card and part-contract checks now have a
  focused validator module; repo-validation workflow-pin hygiene also moved to
  `scripts/validators/boundary_bridge.py`; sibling-canary matrix shape also
  moved to the same module.
- As of AOA-EV-D-0206: `scripts/validators/boundary_bridge.py` is removed;
  route cards and sibling-ref posture live in `boundary_bridge_routes.py`,
  workflow-pin hygiene lives in `boundary_bridge_workflow.py`, canary matrix
  shape lives in `boundary_bridge_canary.py`, and shared constants/token lookup
  live in `boundary_bridge_common.py`.
- Superseded by: AOA-EV-D-0206 for aggregate module shape.

## Boundaries

This decision does not authorize editing sibling repositories.

It does not make a pinned workflow ref or latest-sibling canary result a source
of truth for sibling repo meaning.

It does not move generated phase-alpha matrix parity or live sibling canary
execution into the route validator.

## Validation

- `python -m py_compile scripts/validators/boundary_bridge_common.py scripts/validators/boundary_bridge_routes.py scripts/validators/boundary_bridge_workflow.py scripts/validators/boundary_bridge_canary.py scripts/validators/mechanics_routes.py tests/test_mechanic_surface_contracts.py tests/test_mechanic_legacy_archive_routes.py tests/test_repo_validation_workflow.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k boundary_bridge`
- `python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k boundary_bridge`
- `python -m pytest -q tests/test_repo_validation_workflow.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
