# Publication Receipts Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/publication-receipts/` routes the operation that turns one reviewed
bounded eval report into an optional machine-readable publication receipt.

It is not the reports directory, live receipt log, shared stats envelope owner,
telemetry dashboard, proof bundle source, or repo-global score.

## Owned Operation

`reviewed bounded report -> eval-result receipt payload -> stats-event-envelope sidecar -> owner-local live receipt log -> downstream derived reader`

This package routes publication receipt work. The bundle-local verdict meaning stays
in `bundles/*/EVAL.md`, `bundles/*/eval.yaml`, and the concrete report artifact
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
routed here but not moved into `parts/`.

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
may contain a schema-valid payload preview, but it must keep
`receipt_status` as `not_published` and must not create an envelope, event id,
publisher run, or live log append.

## Stronger Owner Split

`aoa-evals` owns eval verdict meaning, receipt payload semantics, and claim
limits for `eval_result_receipt`.

`aoa-stats` owns the canonical shared `stats-event-envelope` and active
cross-repo event-kind vocabulary. The local schema is a mirror for validation,
not a competing source of ownership.

The bundle-local report is stronger than the receipt. The receipt records that
a bounded publication happened; it does not reinterpret the evidence.

The `.aoa/live_receipts/` log is owner-local publication memory. It is not the
source of truth for bundle acceptance, report meaning, or proof quality.

## Boundaries

- Do not publish a receipt without a reviewed bounded report.
- Do not treat a receipt-intake dry review as a published receipt.
- Do not treat receipt volume as proof quality.
- Do not create a repo-global score.
- Do not replace bundle-local report artifacts with one receipt payload.
- Do not hand-edit the canonical `aoa-stats` envelope from this repo.
- Do not read, paste, or publish raw live receipt logs when a route summary is
  enough.
- Do not silently rewrite old receipts; use `supersedes` and append a later
  receipt.
- Do not put secrets, hidden telemetry, private logs, or unreduced operator
  traces into examples or receipt payloads.

## Validation

After changing publication receipt route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If schemas, examples, or publisher behavior change, also run:

```bash
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py tests/test_validate_repo.py
```

If generated readers or catalogs change, run their owning builders in `--check`
mode rather than hand-editing generated output.

## Next Route

Use this package before:

- changing `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md`;
- changing `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json`;
- refreshing the local `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json` mirror;
- changing `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json`;
- changing `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py`;
- publishing or correcting owner-local eval result receipts.
- dry-reviewing receipt intake from a reviewed report without publication.
