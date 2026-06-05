# Mechanics Root-district Subvalidators

- Decision ID: AOA-EV-D-0185
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/mechanics_root_districts.py`, focused `scripts/validators/root_authored_surface_*` validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale, superseded in part by AOA-EV-D-0215

## Context

AOA-EV-D-0164 moved mechanics root-surface checks out of
`scripts/validators/mechanics.py`, but
`scripts/validators/mechanics_root_surfaces.py` still mixed two boundaries:

- root-district reconnaissance: district posture, required district rows,
  route-card-only status, and root-district decision routing; and
- residual root-authored surface classification: docs/scripts/tests allowlists,
  file inventory drift, ledger rows, and root-authored classification decision
  routing.

Those checks both protect mechanics/root topology, but they fail for different
owners and should not share one growing validator.

## Decision

Mechanics root-surface validation is split into focused modules:

- `scripts/validators/mechanics_root_districts.py` owns root-district
  reconnaissance.
- Residual root-authored surface classification first moved to
  `scripts/validators/root_authored_surface_classification.py`; AOA-EV-D-0215
  later split that layer across focused `root_authored_surface_*` validators.
- `scripts/validators/mechanics_common.py` owns only shared mechanics route
  constants, markdown parsing helpers, decision-token lookup, and shared
  roadmap direction tokens.

`scripts/validators/mechanics_root_surfaces.py` is removed after direct imports
move to the focused modules. AOA-EV-D-0215 later removes the residual
classification aggregate as well.

## Rationale

Root-district reconnaissance is about posture: which root districts remain
source, generated, route-card-only, repo-wide, or mechanic-adjacent.

Residual root-authored classification is about inventory: which root docs,
scripts, and tests may remain in root districts, and how each row states the
mechanic-owned payload boundary.

Keeping those together would recreate a broad root mechanics bucket and force
one validator to remember both district posture and every root-authored file.

## Consequences

- Positive: root-district posture and root-authored file inventory drift now
  have distinct failure routes.
- Positive: `mechanics_root_surfaces.py` is removed instead of preserved as a
  compatibility facade.
- Positive: `mechanics.py` still preserves the public mechanics compatibility
  API while delegating to focused owners.
- Tradeoff: the root-authored classification layer carries the explicit
  docs/scripts/tests allowlist because that is the boundary it owns.

## Current Applicability

As of 2026-06-04:

- Still valid: mechanics topology remains responsible for ensuring root
  districts do not silently become mechanic payload homes.
- Changed: root-district reconnaissance moved into
  `mechanics_root_districts.py`; residual root-authored file classification
  first moved into `root_authored_surface_classification.py`; AOA-EV-D-0215
  later split that residual classification layer into
  `root_authored_surface_common.py`,
  `root_authored_surface_inventory.py`,
  `root_authored_surface_ledger.py`, and
  `root_authored_surface_decision.py`. Shared roadmap
  mechanics-evidence direction tokens moved into `mechanics_common.py`.
- Supersedes: the single-module owner shape described by AOA-EV-D-0164.
- Superseded in part by: AOA-EV-D-0215 for residual root-authored
  classification subvalidators.

## Boundaries

This decision does not make either validator own mechanic payload meaning,
parent evidence semantics, part contracts, runtime evidence, generated
projection parity, release packaging, or proof verdict meaning.

It does not remove `scripts/validators/mechanics.py`; that module remains a
compatibility and root-route surface until its public imports can be narrowed
without churn.

## Validation

- `python -m py_compile scripts/validators/mechanics.py scripts/validators/mechanics_common.py scripts/validators/mechanic_parent_registry.py scripts/validators/mechanic_evidence_dimensions.py scripts/validators/mechanic_evidence_route_refs.py scripts/validators/mechanics_root_districts.py scripts/validators/root_authored_surface_common.py scripts/validators/root_authored_surface_inventory.py scripts/validators/root_authored_surface_ledger.py scripts/validators/root_authored_surface_decision.py scripts/validators/mechanics_routes.py`
- `python -m pytest -q tests/test_mechanics_topology.py tests/test_mechanic_root_district_recon.py tests/test_mechanic_evidence_ledger.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
