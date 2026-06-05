# Mechanics Parent Class Aggregate Removal

- Decision ID: AOA-EV-D-0198
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused mechanic parent registry and evidence validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0181 moved parent-class and evidence-ledger checks out of the broad
`mechanics.py` facade. The resulting `scripts/validators/mechanics_parent_class.py`
module still mixed three boundaries:

- active parent registry, AoA-aligned/evals-native class sets, and former
  wrong-parent route mappings;
- active parent evidence dimension ledger checks; and
- active parent evidence route-ref checks, including stale/generic/rationale-only
  route refs.

Those checks cooperate, but a class registry is not the same authority as a
dimension ledger or a concrete route-ref ledger.

## Decision

`scripts/validators/mechanics_parent_class.py` is removed.

Mechanic parent evidence validation now routes through focused modules:

- `mechanic_parent_registry.py` owns active parent names, class sets, former
  wrong-parent mappings, and parent-class decision/doc route tokens.
- `mechanic_evidence_dimensions.py` owns the active parent evidence dimension
  ledger and its decision/doc route tokens.
- `mechanic_evidence_route_refs.py` owns concrete parent evidence route refs,
  stale/generic/rationale-only ref checks, and its decision/doc route tokens.

`mechanics_routes.py` calls these validators directly. `mechanics.py` remains a
compatibility adapter for public constants and mechanics root-route checks, but
it no longer exposes an aggregate parent-class validation function.

## Rationale

The registry answers "which parents exist and how are they classed." The
dimension ledger answers "what kinds of evidence each parent must carry." The
route-ref ledger answers "which concrete local surfaces prove that evidence."

Keeping all three behind one module made any parent-evidence pressure look like
one historical gate. Focused modules keep failures close to the owner surface
and prevent `mechanics.py` or a parent-class aggregate from becoming the next
catch-all.

## Consequences

- Positive: no mechanic parent-class aggregate validator remains.
- Positive: parent registry, dimension ledger, and route-ref ledger now have
  separate inventory rows, mechanics ledger rows, and import paths.
- Positive: `mechanics_routes.py` orchestrates the focused validators directly.
- Tradeoff: `mechanics.py` still re-exports constants as a compatibility
  surface for dependent validators and tests.

## Current Applicability

As of 2026-06-04:

- Still valid: active mechanic parents must stay evidence-backed, classed, and
  free of stale/generic/rationale-only route refs.
- Changed: parent-class/evidence behavior no longer lives in
  `mechanics_parent_class.py`; it is split across
  `mechanic_parent_registry.py`, `mechanic_evidence_dimensions.py`, and
  `mechanic_evidence_route_refs.py`.
- Supersedes: the remaining aggregate shape left by AOA-EV-D-0181.

## Boundaries

This decision does not make parent registry or evidence validators own mechanic
payload meaning, part contracts, runtime activation, generated projections,
release evidence, root-district classification, or root route-token presence.

It does not create a replacement parent-class aggregate under another name.

## Validation

- `python -m py_compile scripts/validators/mechanic_parent_registry.py scripts/validators/mechanic_evidence_dimensions.py scripts/validators/mechanic_evidence_route_refs.py scripts/validators/mechanics.py scripts/validators/mechanics_routes.py tests/test_mechanic_evidence_ledger.py`
- `python -m pytest -q tests/test_mechanic_evidence_ledger.py tests/test_mechanic_parent_topology.py tests/test_mechanics_topology.py tests/test_mechanic_parent_direction.py tests/test_mechanic_root_district_recon.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
