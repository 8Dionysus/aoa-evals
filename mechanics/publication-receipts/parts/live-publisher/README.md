# Publication Receipts / Live Publisher Part

## Role

This part owns the owner-local append tool for already reviewed,
schema-valid eval-result receipt envelopes.

It performs the optional publication append after a receipt envelope already
exists. Verdict meaning, proof acceptance, and dry-review previews route to the
reviewed report, bundle-local review, and intake dry-review surfaces.

## Source Surfaces

- `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py`

## Inputs

- one or more JSON or JSONL receipt envelopes with `event_kind` set to
  `eval_result_receipt`;
- a payload that validates against `receipt-payload` schema;
- a stats event envelope that validates against the local `stats-envelope-mirror`
  schema;
- explicit operator intent to append to the owner-local live receipt log path.

## Outputs

- append-only JSONL writes to `.aoa/live_receipts/eval-result-receipts.jsonl`
  when the publisher is intentionally invoked;
- duplicate `event_id` skips instead of silent rewrites;
- validation errors for malformed JSON, unsupported event kinds, invalid
  datetime values, missing fields, or schema drift;
- local tests proving dry-review artifacts are rejected as publishable receipts.

## Stronger Owner Split

`aoa-evals` owns the local append tool, duplicate handling, and schema-backed
publication boundary for eval-result receipts.

The reviewed report and source bundle own proof meaning. `.aoa/live_receipts/`
is owner-local publication memory, not verdict authority. `aoa-stats` owns the
canonical shared envelope vocabulary.

## Boundary

The publisher appends to `.aoa/live_receipts/eval-result-receipts.jsonl` only
when explicitly invoked with receipt input. Dry reviews, bundle promotion,
verdict authority, and private log content route to intake review,
bundle-local review, proof owners, and private evidence owners.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| dry-review payload preview looks publishable | route to intake dry review until an actual receipt envelope exists |
| old log entry needs correction | append a later receipt with `supersedes` |
| duplicate skipping reads as proof review or receipt acceptance | return to reviewed report, receipt validation, and bundle-local review |
| secret, private telemetry, hidden benchmark payload, local credential, or unreduced operator trace appears | keep it outside owner-local publication |
| owner-local append reads as GitHub release, runtime acceptance, quest closure, bundle promotion, or goal completion | route to release, runtime, quest, lifecycle, or goal closeout owner |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
