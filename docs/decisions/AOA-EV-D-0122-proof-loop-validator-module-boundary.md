# Proof Loop Validator Module Boundary

- Decision ID: AOA-EV-D-0122
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/proof_loop.py`, `mechanics/proof-loop/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, trace/eval, report/readout
- Mechanic parents: proof-loop, publication-receipts, proof-object, proof-infra, audit, boundary-bridge
- Guard families: source/topology, generated/report/receipt/runtime
- Posture: active rationale

## Context

Proof-loop validation still lived inside `scripts/validate_repo.py` after the
generated-reader, receipt, and release-support validator splits.

The checks form one coherent routeability surface: proof-loop parent and part
route cards, the route-smoke report, the first bundle-local proof-loop report,
and legacy placement bridges for the former root report path.

## Options Considered

- Keep proof-loop validation inside the broad mechanics pass.
- Fold proof-loop report checks into generated report-index or receipt
  validation.
- Move proof-loop route and report checks into
  `scripts/validators/proof_loop.py` while keeping `validate_repo.py` as the
  compatibility entrypoint.

## Decision

Proof-loop validation lives in `scripts/validators/proof_loop.py`.

`scripts/validate_repo.py` keeps compatibility wrappers for
`validate_proof_loop_smoke_report_surfaces` and
`validate_proof_loop_local_report_surfaces`.

The module owns proof-loop route-card, part-contract, provenance, legacy,
route-smoke, and bundle-local report token checks.

## Rationale

Proof-loop is a local routeability organ. It lets a reader follow one bounded
proof question through source selection, support contract, candidate evidence,
bundle-local review, bounded reporting, and optional receipt routing.

It does not make the route-smoke report a bundle promotion, runtime acceptance,
sibling-owner approval, or eval result receipt. Naming the module keeps those
authority limits explicit instead of hiding them in a generic mechanics block.

## Consequences

- Positive: proof-loop validation leaves the root validator.
- Positive: route-smoke and bundle-local report checks stay separate from
  publication receipt checks.
- Tradeoff: compatibility wrappers remain because tests still import through
  `scripts/validate_repo.py`.
- Follow-up: future trace/eval harness validators should remain separate from
  proof-loop routeability unless a bounded eval bundle promotes them.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: proof-loop route and report checks now have a focused validator
  module.
- Superseded by: none.

## Boundaries

This decision does not publish an eval result receipt.

It does not promote any bundle, accept runtime evidence, approve sibling truth,
or claim full proof-loop completeness.

It does not move bundle-local report authority out of `evals/**/reports/`.

## Validation

- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_loop`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
