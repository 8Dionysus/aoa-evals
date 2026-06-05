# Mechanics Topology Validator Boundary

- Decision ID: AOA-EV-D-0146
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanics.py`, focused mechanics topology validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

The mechanics topology guard family protects the mechanics root route surfaces,
parent evidence map, parent class split, root-district reconnaissance ledger,
and residual root-authored surface classification.

Before this split, `scripts/validate_repo.py` still held the mechanics root
token contract, active parent class map validator, and the root-district
reconnaissance validator, even though their source truth is
`mechanics/README.md`, `mechanics/AGENTS.md`,
`mechanics/EVIDENCE_CLUSTERS.md`, and the related mechanics decisions.

That kept root validation larger than the owner boundary. The root entrypoint
was remembering mechanics evidence details instead of delegating to the
mechanics topology organ.

## Decision

Mechanics topology validation routes through `scripts/validators/mechanics.py`.

The module owns:

- mechanics root route-token checks;
- active parent class map checks;
- active parent evidence dimension ledger checks;
- active parent evidence route refs checks;
- root-district reconnaissance ledger checks;
- residual root-authored surface classification checks.

`scripts/validate_repo.py` delegates to this module and keeps only repo-wide
orchestration. Tests for the moved behavior import `validators/mechanics.py`
directly instead of using root compatibility wrappers.

Follow-up decisions split root-district and parent-class behavior into focused
modules while preserving the `mechanics.py` import surface.

## Rationale

Parent evidence and root-district posture are mechanics topology boundaries.
They decide whether an active mechanic parent has enough local evidence and
whether root districts are still route cards, generated readers, source proof
trees, or mechanic-owned payload routes.

They do not define eval source meaning, generated projection parity, release
artifact freeze, runtime policy, trace/eval grading, or sibling truth. Keeping
them in the mechanics validator makes the owner visible and prevents another
historical gate pile from forming in `scripts/validate_repo.py`.

## Consequences

- Positive: `validate_repo.py` no longer carries mechanics root token lists or
  exports parent-class, root-district, or residual root-authored classification
  validator wrappers.
- Positive: mechanics evidence tests now call the owning module directly.
- Positive: `mechanics/EVIDENCE_CLUSTERS.md`, validator inventories, and the
  mechanics module describe the same owner boundary.
- Follow-up: the remaining overloaded mechanics allowlist path should be split
  after legacy raw accounting, parent guidance, and archive-route checks get
  their own coherent owner route.

## Current Applicability

As of 2026-06-04:

- Still valid: active mechanic parents must stay evidence-backed and
  allowlisted.
- Changed: mechanics root route-token checks, parent evidence ledger,
  root-district reconnaissance, and residual root-authored classification
  checks moved from `scripts/validate_repo.py` to the mechanics validator
  family. Root-district reconnaissance now delegates to
  `scripts/validators/mechanics_root_districts.py`; residual root-authored
  classification now delegates to focused
  `scripts/validators/root_authored_surface_*` validators.
  Parent-class and evidence-ledger checks now delegate to
  `scripts/validators/mechanic_parent_registry.py`,
  `scripts/validators/mechanic_evidence_dimensions.py`, and
  `scripts/validators/mechanic_evidence_route_refs.py`.
- Superseded in part by: AOA-EV-D-0164 for the root-surface validator split;
  AOA-EV-D-0181 for the parent-class/evidence-ledger validator split;
  AOA-EV-D-0215 for the residual root-authored classification split.

## Review Log

### 2026-06-04 - Mechanics root-surface split

- Previous assumption: `mechanics.py` should carry parent evidence and
- Previous assumption: `mechanics.py` should carry parent evidence and
  root-surface classification as one mechanics topology validator.
- New reality: parent evidence remains in `mechanics.py`; root-district
  reconnaissance and residual root-authored classification first moved to
  `scripts/validators/mechanics_root_surfaces.py`; AOA-EV-D-0185 later split
  those into `scripts/validators/mechanics_root_districts.py` and the residual
  root-authored classification layer; AOA-EV-D-0215 later split that layer
  across focused `scripts/validators/root_authored_surface_*` validators.
  Shared parsing helpers live in `scripts/validators/mechanics_common.py`.
- Reason: root file classification is a distinct topology boundary and should
  not keep growing the parent-evidence validator.
- Source surfaces updated: `scripts/validators/mechanics.py`,
  `scripts/validators/mechanics_common.py`,
  `scripts/validators/mechanics_root_districts.py`,
  focused `scripts/validators/root_authored_surface_*` validators, validation
  inventories, and mechanics residual classification.
- Validation: see AOA-EV-D-0164.

### 2026-06-04 - Parent-class and evidence-ledger split

- Previous assumption: after the root-surface split, parent evidence could
  remain in `mechanics.py`.
- New reality: active parent allowlists, class split, former wrong-parent
  routes, evidence dimension ledger, and evidence route-ref ledger now live in
  `scripts/validators/mechanic_parent_registry.py`,
  `scripts/validators/mechanic_evidence_dimensions.py`, and
  `scripts/validators/mechanic_evidence_route_refs.py`.
- Reason: parent-class law is a different boundary from mechanics root
  route-token checks and part-local test placement.
- Source surfaces updated: `scripts/validators/mechanics.py`,
  `scripts/validators/mechanic_parent_registry.py`,
  `scripts/validators/mechanic_evidence_dimensions.py`,
  `scripts/validators/mechanic_evidence_route_refs.py`, validation
  inventories, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: see AOA-EV-D-0181.

### 2026-06-04 - Parent-class aggregate removal

- Previous assumption: a single parent-class validator could own registry,
  evidence dimensions, and evidence route refs together.
- New reality: registry/class-map checks route to
  `scripts/validators/mechanic_parent_registry.py`, evidence dimension checks
  route to `scripts/validators/mechanic_evidence_dimensions.py`, and evidence
  route-ref checks route to
  `scripts/validators/mechanic_evidence_route_refs.py`.
- Reason: active parent identity, evidence dimensions, and concrete route refs
  are separate mechanics topology boundaries.
- Source surfaces updated: focused parent/evidence validators, validation
  inventories, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: see AOA-EV-D-0198.

## Boundaries

This decision does not make mechanics topology own mechanic payload meaning.
Part payload contracts stay in the owning mechanic parent or part.

The root-district and residual root-authored classification checks now route
through `scripts/validators/mechanics_root_districts.py` and
focused `scripts/validators/root_authored_surface_*` validators; parent-class and
evidence-ledger checks now route through
`scripts/validators/mechanic_parent_registry.py`,
`scripts/validators/mechanic_evidence_dimensions.py`, and
`scripts/validators/mechanic_evidence_route_refs.py`; generated/read-model,
release, runtime, and parent payload meanings remain outside that authority.

It does not promote advisory runtime, memory, handoff, observability, or
security routes into hard gates.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanics.py scripts/validators/mechanic_parent_registry.py scripts/validators/mechanic_evidence_dimensions.py scripts/validators/mechanic_evidence_route_refs.py scripts/validators/mechanics_root_districts.py scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py`
- `python -m pytest -q tests/test_mechanics_topology.py tests/test_mechanic_evidence_ledger.py tests/test_mechanic_root_district_recon.py`
