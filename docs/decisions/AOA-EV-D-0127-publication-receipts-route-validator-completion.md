# Publication Receipts Route Validator Completion

- Decision ID: AOA-EV-D-0127
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/publication_receipts.py`, `mechanics/publication-receipts/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, publication/receipt, mechanics/topology
- Mechanic parents: publication-receipts, proof-loop, proof-object, cross-parent
- Guard families: source/topology, generated/report/receipt/runtime
- Posture: active rationale

## Context

Decision AOA-EV-D-0120 moved publication receipt payload, live-log, and
dry-review validation into `scripts/validators/publication_receipts.py`.

The publication-receipts route-card and part-contract checks still remained in
the broad `validate_mechanics_surfaces` body. That left one owner organ split
across two validator places: route meaning in root, receipt payload behavior in
the module.

## Options Considered

- Leave route-card checks in `scripts/validate_repo.py` as generic mechanics
  validation.
- Create a second publication-receipts route module.
- Move publication-receipts route, part, provenance, legacy, and decision token
  checks into the existing `scripts/validators/publication_receipts.py` module.

## Decision

Publication-receipts route validation also lives in
`scripts/validators/publication_receipts.py`.

`scripts/validate_repo.py` delegates publication-receipts route-card,
part-contract, provenance, legacy, and decision checks to
`validate_publication_receipts_route_surfaces`.

Tests import publication-receipts constants from
`scripts/validators/publication_receipts.py` directly. `scripts/validate_repo.py`
no longer re-exports publication-receipts compatibility aliases.

## Rationale

Publication receipts are one owner organ: route cards explain the same receipt
sidecar boundary that payload, stats-envelope mirror, live publisher, live log,
and dry-review checks enforce.

Keeping route checks in root made the root validator preserve historical
receipt knowledge after the focused module already existed. Moving the route
checks into the module makes the boundary complete while preserving the rule
that receipts stay weaker than reviewed bundle-local reports.

## Consequences

- Positive: another long route-card block leaves `validate_mechanics_surfaces`.
- Positive: publication-receipts route, payload, live-log, and dry-review checks
  now have one validator owner.
- Positive: publication-receipts test fixtures now route to the focused module
  instead of preserving root compatibility aliases.
- Follow-up: audit and boundary-bridge route blocks can receive the same
  treatment when their focused module boundary is ready.

## Current Applicability

As of 2026-06-03:

- Still valid: AOA-EV-D-0120 remains the publication-receipts module boundary.
- Changed: route-card and part-contract checks now live in that module too.
- Superseded by: none.

## Boundaries

This decision does not make receipts stronger than reviewed reports.

It does not publish, append, rewrite, or accept live receipt entries.

It does not move release-support, runtime integrity review, generated report
index parity, or bundle-local verdict meaning into publication-receipts.

## Validation

- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k publication_receipts`
- `python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k publication_receipts`
- `python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
