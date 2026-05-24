# Eval Result Receipt Guide

## Purpose

This guide defines the bounded machine-readable publication seam for
`aoa-evals`.

An `eval_result_receipt` records that one bounded eval publication happened.
It keeps the publication legible for later derived read models while verdict
meaning stays with bundle-local review.

## Core Rule

An `eval_result_receipt` is a publication sidecar.
Proof-canon pressure routes to the bundle-local report and source bundle.

It is subordinate to:

- the owning bundle `EVAL.md`
- the bundle-local report schema
- the concrete report artifact being published
- the bundle-local interpretation boundary

Bundle-local verdict meaning stays with the reviewed report and source bundle.

## Shared receipt surfaces

The shared schema-backed surfaces for this seam are:

- canonical shared envelope:
  `repo:aoa-stats/schemas/stats-event-envelope.schema.json`
- `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`
- owner-local append-only log:
  `.aoa/live_receipts/eval-result-receipts.jsonl`

Use the shared `stats-event-envelope` for event facts.
Treat the local `aoa-evals` copy as a mirror of the canonical `aoa-stats`
schema rather than as a competing source of ownership.
Use `eval-result-receipt.schema.json` only for the bounded proof payload that
travels inside that envelope.
Use `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py` to append validated owner-local receipts
to the live JSONL log.

## Dry review boundary

`mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` is the first
report-to-receipt intake dry review. It may show a schema-valid
`candidate_payload_preview`.

Publication pressure routes to the receipt envelope and live-publisher lane.
Envelope pressure routes to the `stats-event-envelope` mirror and canonical
`aoa-stats` owner. Live-log pressure routes to `.aoa/live_receipts/` through
the live publisher.

Use the dry review when checking whether a reviewed report can derive the
payload fields. Use the publisher only when a later slice intentionally emits a
receipt.

## What the receipt may say

An `eval_result_receipt` may name:

- which eval bundle published the result
- which report artifact carries the bounded readout
- the emitted verdict string
- the bounded claim scope used for this publication
- case count or score when the owning bundle already exposes them
- an explicit interpretation bound

It stays evidence-linked and points back to the report artifact and bundle
contract instead of duplicating the whole proof surface.

## Receipt Pressure Routes

| Pressure | Route |
| --- | --- |
| repo-global score | scoring owner and explicit score contract |
| bundle-local report replacement | reviewed report and source bundle |
| blind spots hidden behind counters | report limitations and interpretation boundary |
| comparative or repeated-window read becomes universal ranking | comparison owner and bounded ranking contract |
| derived summary claims verdict ownership | `aoa-evals` verdict owner and bundle-local review |

## Correction posture

Receipts should stay append-only.

When a published receipt needs correction, emit a later receipt and link it
through `supersedes`.
Correction pressure routes through a later receipt so publication history stays
auditable.

## Boundary to preserve

- `aoa-stats` owns the shared cross-repo receipt envelope and active event-kind
  vocabulary used for downstream derivation
- `aoa-evals` owns verdict meaning, report interpretation, and claim limits
- bundle-local report schemas remain the stronger machine-readable proof
  contract
- shared receipts remain weaker than bundle-local interpretation guidance
- later derived stats or observatory layers may read receipts; proof-authority
  pressure routes back to bundle-local review
