# Mechanics Topology Validator Boundary

- Decision ID: AOA-EV-D-0146
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanics.py`, mechanics topology guard family

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

Mechanics topology validation lives in `scripts/validators/mechanics.py`.

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
  checks moved from `scripts/validate_repo.py` to
  `scripts/validators/mechanics.py`.
- Superseded by: none.

## Boundaries

This decision does not make mechanics topology own mechanic payload meaning.
Part payload contracts stay in the owning mechanic parent or part.

It does not promote advisory runtime, memory, handoff, observability, or
security routes into hard gates.

## Validation

- `python -m py_compile scripts/validate_repo.py scripts/validators/mechanics.py`
- `python -m pytest -q tests/test_mechanics_topology.py tests/test_mechanic_evidence_ledger.py tests/test_mechanic_root_district_recon.py`
