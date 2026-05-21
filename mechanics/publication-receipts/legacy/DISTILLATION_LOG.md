# Publication Receipts Legacy Distillation Log

## 2026-05-20 Mechanics Refactor

Publication receipt work moved from root guide, schema, example, publisher,
test, and dry-review paths into the active `mechanics/publication-receipts/`
parent.

Distilled into active route:

- receipt payload guide, schema, and example live under
  `mechanics/publication-receipts/parts/receipt-payload/`;
- local stats envelope mirror lives under
  `mechanics/publication-receipts/parts/stats-envelope-mirror/`;
- live publisher script and tests live under
  `mechanics/publication-receipts/parts/live-publisher/`;
- receipt-intake dry review report and test live under
  `mechanics/publication-receipts/parts/intake-dry-review/`;
- `.aoa/live_receipts/` remains the owner-local live log route, not package
  source.

Still historical:

- root receipt docs, schemas, examples, scripts, tests, and dry-review report
  placement;
- any reading where a receipt, dry review, or live log outranks a bundle-local
  reviewed report.

Do not create new publication receipt work in legacy. Distill into the owning
active part first.
