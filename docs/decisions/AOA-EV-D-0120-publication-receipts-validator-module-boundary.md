# Publication Receipts Validator Module Boundary

- Decision ID: AOA-EV-D-0120
- Status: Accepted
- Date: 2026-06-03
- Owner surface: `scripts/validators/publication_receipts.py`, `mechanics/publication-receipts/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, publication/receipt, boundary/runtime
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, report/release/receipt
- Posture: active rationale

## Context

Publication receipt validation remained inside `scripts/validate_repo.py` after
the first generated-reader and boundary-bridge validator splits.

The checks form one coherent owner surface: eval-result receipt payload shape,
local stats-envelope mirror posture, owner-local live receipt JSONL validation,
and receipt-intake dry-review posture.

## Options Considered

- Keep receipt validation inside `scripts/validate_repo.py` because it touches
  live JSONL and source bundle reports.
- Split payload schema, live log, and dry-review into three validator modules.
- Move the publication-receipts boundary into
  `scripts/validators/publication_receipts.py` while keeping `validate_repo.py`
  as the compatibility entrypoint.

## Decision

Publication receipt validation lives in
`scripts/validators/publication_receipts.py`.

`scripts/validate_repo.py` keeps compatibility aliases for receipt paths and
wrappers for `validate_eval_result_receipt_surfaces`,
`validate_live_receipt_log`, and
`validate_receipt_intake_dry_review_surface`.

The module validates receipt payload shape, stats-envelope mirror alignment,
append-only live-log entries, and dry-review non-publication posture.

## Rationale

Publication receipts are weaker than bundle-local reports and source bundles.
They record bounded publication facts; they do not own verdict meaning, proof
quality, runtime acceptance, or repo-global scoring.

Naming the module keeps receipt checks visible as a publication sidecar organ
instead of a generic report validator or runtime bucket. It also preserves the
local rule that dry-review payload previews are not publishable receipt
envelopes.

## Consequences

- Positive: publication-receipts validation leaves the root validator.
- Positive: live-log validation remains append-inspection only and does not
  publish or mutate receipt state.
- Tradeoff: compatibility wrappers remain because tests still import through
  `scripts/validate_repo.py`.
- Follow-up: release-support reports and runtime integrity review should remain
  separate owner surfaces.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: receipt payload, live-log, and dry-review checks now have a focused
  validator module.
- Superseded by: none.

## Boundaries

This decision does not make receipts stronger than reviewed reports.

It does not make dry-review output a live publication.

It does not change canonical `aoa-stats` ownership of the shared
stats-event-envelope vocabulary.

It does not append, rewrite, or publish `.aoa/live_receipts/` entries.

## Validation

- `python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
