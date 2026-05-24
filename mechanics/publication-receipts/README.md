# Publication Receipts Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/publication-receipts/` routes the operation that turns one reviewed
bounded eval report into an optional machine-readable publication receipt.

Bundle reports, live receipt logs, stats envelopes, telemetry owners, and proof
bundles keep their meaning. This package keeps optional receipt payloads,
stats-envelope mirror checks, live-publisher posture, and intake dry-review
shape below reviewed reports.

## Owned Operation

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

This package routes publication receipt work. The bundle-local verdict meaning stays
in `evals/**/EVAL.md`, `evals/**/eval.yaml`, and the concrete report artifact
being published.

An optional receipt is valid only after that stronger report path exists.

## Part Topology

See `PARTS.md` for the package-local part map.

- `parts/receipt-payload/` owns the eval-result receipt guide, payload schema,
  and public example.
- `parts/stats-envelope-mirror/` owns the local validation mirror of the
  canonical `aoa-stats` event envelope.
- `parts/live-publisher/` owns the owner-local append tool.
- `parts/intake-dry-review/` owns the non-publishing receipt-intake dry review.

`.aoa/live_receipts/` remains the owner-local live receipt log path. It is
routed here while the log home stays outside `parts/`.

## Source Surfaces

- `mechanics/publication-receipts/PARTS.md`
- `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`
- `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`
- `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json`
- `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`
- `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
- `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py`
- `mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py`
- `mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- root route cards `reports/README.md` and `reports/AGENTS.md`
- `.aoa/live_receipts/AGENTS.md`
- `.aoa/live_receipts/eval-result-receipts.jsonl` as an owner-local append-only
  log path
- `docs/PROOF_TOPOLOGY.md`

## Inputs

- one reviewed bundle-local report artifact
- the source bundle `EVAL.md` and `eval.yaml`
- the emitted verdict string and claim scope from the report
- `object_ref` for the evaluated bundle or proof object
- `evidence_refs` that point back to the report and bundle contract
- optional `supersedes` link when a later receipt corrects an earlier one

## Outputs

- one schema-valid `eval_result_receipt` payload
- one `stats-event-envelope` sidecar around that payload
- optional append through `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py`
- downstream-readable publication facts that remain weaker than the report

Dry-review output is weaker: `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
may contain a schema-valid payload preview. It keeps `receipt_status` as `not_published`;
envelope creation, event id assignment, publisher runs, and live log appends
route to real publication work.

## Stronger Owner Split

`aoa-evals` owns eval verdict meaning, receipt payload semantics, and claim
limits for `eval_result_receipt`.

`aoa-stats` owns the canonical shared `stats-event-envelope` and active
cross-repo event-kind vocabulary. The local schema is a mirror for validation,
with canonical ownership routed to `aoa-stats`.

The bundle-local report is stronger than the receipt. The receipt records that
a bounded publication happened; evidence interpretation stays with the report
and source bundle.

The `.aoa/live_receipts/` log is owner-local publication memory. Bundle
acceptance, report meaning, and proof quality route back to the source bundle
and reviewed report.

## Boundaries

| Pressure | Publication-receipts route |
| --- | --- |
| receipt publication | start from a reviewed bounded report and keep the bundle-local report stronger than the receipt |
| receipt-intake dry review | keep it as non-published payload derivation evidence below the receipt envelope and live log |
| receipt volume or event count | treat it as publication count only; proof quality stays with bundle-local review |
| scoring pressure | route away from this mechanic to the owner that can justify a repo-global score |
| compact receipt payload | keep bundle-local report artifacts as the stronger source path |
| canonical envelope change | route canonical `aoa-stats` schema and event-kind ownership to `aoa-stats`; keep the local mirror for validation |
| raw live receipt logs | use route summaries for ordinary review and inspect raw JSONL only when the live publication route requires it |
| receipt correction | use `supersedes` and append a later receipt so publication history remains auditable |
| sensitive material | keep secrets, hidden telemetry, private logs, and unreduced operator traces out of examples and receipt payloads |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- changing `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`;
- changing `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`;
- refreshing the local `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json` mirror;
- changing `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`;
- changing `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py`;
- publishing or correcting owner-local eval result receipts.
- dry-reviewing receipt intake from a reviewed report without publication.
