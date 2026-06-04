# Proof Object Validator Module Boundary

- Decision ID: AOA-EV-D-0126
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/proof_object.py`, `mechanics/proof-object/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, source/topology, mechanics/topology
- Mechanic parents: proof-object, proof-infra, proof-loop, questbook, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

Proof-object route validation still lived in the broad
`validate_mechanics_surfaces` body of `scripts/validate_repo.py`.

Those checks covered proof-object parent route cards, the lower parts index,
eval-authoring and eval-contracts part contracts, provenance posture, and
decisions for proof-object package and part naming/owner split.

The checks protect source proof-object authority. They do not own generated
catalog parity, bundle-local report verdicts, receipts, runtime candidates,
sibling refs, or quest dispatch.

## Options Considered

- Keep proof-object checks inside `scripts/validate_repo.py`.
- Fold proof-object checks into generic mechanics validation.
- Move route, part, provenance, and decision checks into
  `scripts/validators/proof_object.py` while keeping `scripts/validate_repo.py`
  as the compatibility entrypoint.

## Decision

Proof-object route validation lives in `scripts/validators/proof_object.py`.

`scripts/validate_repo.py` delegates proof-object route-card, part-contract,
provenance, decision, and stale lower-index wording checks to the focused
module.

Compatibility constants and `validate_proof_object_parts_route_surface` remain
available through `scripts/validate_repo.py` for existing tests and imports.

## Rationale

Proof-object is the authored eval source authority surface. Its route cards and
part contracts explain how `evals/**/EVAL.md`, `evals/**/eval.yaml`, authoring
templates, and eval contract schemas relate.

Putting those checks in a focused module keeps source authority explicit and
prevents the root validator from becoming the long-lived owner of every
mechanic wave. Keeping generated catalog/capsule/section parity outside this
module preserves the rule that generated readers are derived projections, not
source meaning.

## Consequences

- Positive: another coherent owner surface leaves the root validator.
- Positive: proof-object source authority is named separately from proof-infra
  reusable support and proof-loop routeability.
- Positive: proof-object test fixtures now route to the focused module instead
  of preserving root compatibility aliases.
- Follow-up: source bundle contract parsing can move later only if it keeps
  source proof object meaning, generated projection parity, and report verdict
  surfaces distinct.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: proof-object route and part checks now have a focused validator
  module.
- Superseded by: none.

## Boundaries

This decision does not move generated catalog, capsule, section, or comparison
reader parity into proof-object.

It does not make eval-authoring templates or eval-contract schemas stronger
than the source eval bundle claim.

It does not move bundle-local reports, receipts, runtime candidates, sibling
truth, or quest dispatch into proof-object.

## Validation

- `python -m pytest -q tests/test_route_residue.py -k proof_object_parts_route`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_object`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
