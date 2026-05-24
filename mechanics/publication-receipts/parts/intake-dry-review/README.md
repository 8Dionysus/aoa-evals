# Publication Receipts / Intake Dry Review Part

## Role

This part owns the non-publishing receipt-intake review artifact.

It checks whether a reviewed bundle-local report can derive a valid
`eval_result_receipt` payload preview without crossing into envelope creation,
publisher execution, or live receipt append.

## Source Surfaces

- `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`
- `mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`

## Inputs

- `evals/workflow/aoa-verification-honesty/reports/aoa-evals-slice-19-lifecycle-contract.report.json`;
- `evals/workflow/aoa-verification-honesty/EVAL.md`;
- `evals/workflow/aoa-verification-honesty/eval.yaml`;
- `generated/eval_report_index.min.json`;
- receipt payload schema, stats envelope mirror, publisher path, and owner-local
  log path as referenced boundaries.

## Outputs

- one public-safe `receipt_intake_dry_review` JSON artifact;
- a schema-valid `candidate_payload_preview` derived from the reviewed report;
- `publication_boundary` fields proving `receipt_status` stays
  `not_published`;
- tests and validator checks that reject publishable envelope fields in the dry
  review shape.

## Stronger Owner Split

The source bundle and bundle-local report own verdict meaning, report format,
case count, and interpretation boundary.

This part owns only the dry derivation review. `receipt-payload` owns the
payload schema, `stats-envelope-mirror` owns local envelope validation support,
and `live-publisher` owns intentional append behavior.

## Boundary

The dry review may contain a schema-valid `candidate_payload_preview`.
It remains `not_published`: no receipt envelope, event id, publisher run, live
log append, runtime acceptance, bundle promotion, or goal completion follows
from it.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| top-level `event_kind`, `event_id`, `observed_at`, `object_ref`, `evidence_refs`, or `payload` appears | route to publishable envelope work instead of dry review |
| live publisher invocation appears | route to `live-publisher` only after a real receipt envelope exists |
| `.aoa/live_receipts/` append appears | keep dry review non-publishing and route append work to live publication |
| runtime evidence acceptance, quest closure, bundle promotion, GitHub release publication, or goal completion is inferred | route to runtime, quest, lifecycle, release, or goal closeout owners |
| payload derivability outranks the reviewed report or source bundle | return to the reviewed report and source bundle |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
