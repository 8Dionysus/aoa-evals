# Mechanics Root-surface Validator Boundary

- Decision ID: AOA-EV-D-0164
- Status: Accepted
- Date: 2026-06-04
- Historical owner surface: `scripts/validators/mechanics_root_surfaces.py`, `mechanics/EVIDENCE_CLUSTERS.md`
- Refined by: AOA-EV-D-0185

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

`scripts/validators/mechanics.py` carried both parent-evidence checks and
root-surface classification checks:

- mechanics root route-token checks;
- active parent class, evidence dimension, and evidence route-ref checks;
- root-district reconnaissance ledger checks; and
- residual root-authored surface classification checks.

Those are adjacent, but not the same boundary. Parent evidence asks whether
mechanic parents are allowlisted, evidence-backed, and routed. Root-surface
classification asks whether root districts remain source, route-card, generated,
or mechanic-owned payload surfaces.

## Decision

At this decision point, root-district reconnaissance and residual
root-authored surface classification validation moved to
`scripts/validators/mechanics_root_surfaces.py`.

Shared mechanics markdown/table/token helpers live in
`scripts/validators/mechanics_common.py`.

`scripts/validators/mechanics.py` remains the mechanics root route and parent
evidence validator. It imports the root-surface validator to preserve the public
API used by tests and the mechanics route orchestrator.

## Rationale

Root-district classification is a topology boundary over root-authored files and
route-card-only districts. It should not be mixed with parent evidence semantics,
and it should not make `mechanics.py` remember every root file allowlist forever.

Separating the root-surface checks keeps the question precise:

- `mechanics.py`: are mechanic parents evidence-backed and routed?
- `mechanics_root_surfaces.py` at this decision point: are root-authored
  surfaces classified and bounded below mechanic payload ownership?
- `mechanics_common.py`: are shared parsing/token helpers kept meaning-free?

## Consequences

- Positive: `mechanics.py` drops from a broad mixed topology validator to a
  parent-evidence/root-route validator.
- Positive: root-district and residual root-authored classification checks have
  their own module, inventory entries, mechanics ledger rows, and decision
  rationale.
- Positive: helper code is isolated from topology meaning.
- Tradeoff: public imports remain available through `mechanics.py` because tests
  and route orchestration already depend on that module path.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanics topology remains the owner of parent evidence and
  root-district classification.
- Changed at this decision point: root-surface classification moved out of
  `mechanics.py` and into `mechanics_root_surfaces.py`; shared helpers moved
  into `mechanics_common.py`.
- Refined on 2026-06-04: AOA-EV-D-0185 removed
  `scripts/validators/mechanics_root_surfaces.py` after moving root-district
  reconnaissance to `scripts/validators/mechanics_root_districts.py` and
  residual root-authored surface classification to the
  `scripts/validators/root_authored_surface_*` validator family after
  AOA-EV-D-0215.
- Superseded by: AOA-EV-D-0185 for the single-module owner shape.
- Superseded in part by: AOA-EV-D-0215 for residual root-authored
  classification subvalidators.

## Boundaries

This decision does not make root-surface classification own mechanic payload
meaning, part contracts, runtime evidence, generated projection parity, release
packaging, or parent evidence semantics.

It also does not move focused mechanic route-domain validation out of
`scripts/validators/mechanics_routes.py`.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
