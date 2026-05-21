# 0024 Receipt Intake Dry Review

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/publication-receipts/`

## Context

The proof loop now has a first schema-backed bundle-local report at
`bundles/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`
and a generated report reader at `generated/eval_report_index.min.json`.

The next pressure is receipt intake: can a reviewed report yield the bounded
`eval_result_receipt` payload fields without accidentally publishing a receipt,
creating a `stats-event-envelope`, appending `.aoa/live_receipts/`, or promoting
the bundle?

## Options Considered

- Publish a real receipt immediately: rejected because the current proof-loop
  needs one dry route review before owner-local live receipt memory is touched.
- Add another report only: rejected because it would not exercise the receipt
  payload seam.
- Add `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`: accepted because
  it tests the derivation path while keeping the artifact visibly outside the
  receipt, envelope, and live-log classes.

## Decision

`aoa-evals` keeps a public-safe receipt-intake dry review at
`mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`.

The artifact may contain a schema-valid `candidate_payload_preview` derived from
the reviewed bundle-local report. It must not contain a publishable receipt
envelope, `event_kind`, `event_id`, `observed_at`, live log line, or publisher
execution claim.

## Rationale

This route makes the next proof-loop step concrete without crossing the
publication boundary. It gives validators and reviewers a real artifact to
inspect, while preserving the stronger owner split:

- the bundle-local report keeps verdict meaning;
- the dry review checks payload derivability;
- the receipt guide and schemas define the publication seam;
- the owner-local live log remains untouched;
- `aoa-stats` keeps ownership of the shared envelope vocabulary.

## Consequences

- Positive: future agents can inspect the first report-to-receipt intake route
  without reading private logs or publishing receipt data.
- Tradeoff: a dry review is weaker than a receipt; it proves routeability, not
  publication.
- Follow-up: only a later reviewed publication slice should create an envelope,
  event id, stats sidecar, or live JSONL append.

## Boundaries

Do not infer that an eval result receipt was published.
Do not infer that `.aoa/live_receipts/` was appended.
Do not infer runtime evidence acceptance, bundle promotion, quest closure, or
completion of the whole strategic refactor.

## Validation

The route is protected by `scripts/validate_repo.py`, targeted tests for the
dry-review artifact, publisher rejection of the dry-review shape, and the normal
receipt tests when receipt publication behavior changes.
