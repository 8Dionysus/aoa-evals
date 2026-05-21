# Publication Receipts / Live Publisher Part

## Role

This part owns the owner-local append tool for already reviewed,
schema-valid eval-result receipt envelopes.

It performs the optional publication append after a receipt envelope already
exists. It does not derive verdict meaning, decide proof acceptance, or publish
dry-review previews.

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
when explicitly invoked with receipt input. It does not publish dry reviews,
promote bundles, create verdict authority, or read private log content for
docs-only changes.

## Stop-Lines

- Do not run the publisher for a dry-review payload preview.
- Do not silently rewrite old log entries; use a later receipt and
  `supersedes` when correction is needed.
- Do not let duplicate skipping imply proof review or receipt acceptance.
- Do not append secrets, private telemetry, hidden benchmark payloads, local
  credentials, or unreduced operator traces.
- Do not treat an owner-local append as GitHub release, runtime acceptance,
  quest closure, bundle promotion, or goal completion.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
