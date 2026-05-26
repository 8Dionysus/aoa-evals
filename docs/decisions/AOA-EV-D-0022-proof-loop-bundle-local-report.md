# Proof Loop Bundle-Local Report

- Decision ID: AOA-EV-D-0022

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-20
- Surface classes: report/release/receipt
- Mechanic parents: proof-loop
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

`mechanics/proof-loop/` now has a local route and
`mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md` proves that the route can be
followed without importing runtime, sibling, generated, or receipt authority.

That smoke report is intentionally weaker than a real bundle-local eval result.
After the quest lifecycle contract, the next missing Phase 8 object was one
schema-backed report under the selected source proof object.

## Decision

Add the first real proof-loop bundle-local report at
`evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`.

The report evaluates the verification-truthfulness closeout for the slice 19
quest lifecycle contract. It is an actual `aoa-verification-honesty` report
validated against the bundle-local
`evals/workflow/aoa-verification-honesty/reports/summary.schema.json`.

Also validate every bundle-local `*.report.json` file against its local
`evals/<family>/<eval>/reports/summary.schema.json`, not only
`evals/<family>/<eval>/reports/example-report.json`.

## Non-Goals

- no eval result receipt is published;
- no bundle status is promoted;
- no quest state changes;
- no runtime candidate is accepted;
- no sibling-owner approval is inferred;
- no global proof-loop template or hidden dispatch is created.

## Consequences

The active proof loop now has a second materialized rung:

1. route-smoke report in `mechanics/proof-loop/parts/route-smoke/reports/`;
2. schema-backed bundle-local report under the selected bundle.

This makes `pick -> inspect -> expand -> review -> bounded report` more real
without crossing into optional receipt publication. Receipt work remains under
`mechanics/publication-receipts/` and still requires a reviewed bounded report
as input.

Future proof-loop reports should stay bundle-local unless they are truly shared
cross-bundle dossiers. Future checklists or generated proof-loop surfaces should
wait until more than one reviewed local run reveals a repeated operation.

## Validation

Expected checks:

- `python scripts/validate_repo.py --eval aoa-verification-honesty`
- `python -m pytest -q tests/test_validate_repo.py -k "actual_report or proof_loop"`
- `python scripts/validate_repo.py`
- broad repository checks before closeout.
