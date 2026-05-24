# Publication Receipts Legacy Index

| Former or overloaded source | Current active route | Posture |
| --- | --- | --- |
| `docs/EVAL_RESULT_RECEIPT_GUIDE.md` | `mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md` | former docs-root receipt guide path |
| `schemas/eval-result-receipt.schema.json` | `mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json` | former root schema path |
| `examples/eval_result_receipt.example.json` | `mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json` | former root example path |
| `schemas/stats-event-envelope.schema.json` | `mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json` | former root mirror schema path |
| `scripts/publish_live_receipts.py` | `mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py` | former root publisher path |
| `tests/test_publish_live_receipts.py` | `mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py` | former root publisher test path |
| `tests/test_live_receipt_log.py` | `mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py` | former root live log test path |
| `reports/eval-result-receipt-intake-dry-review-v1.json` | `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` | former root dry-review report path |
| `tests/test_receipt_intake_dry_review.py` | `mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py` | former root dry-review test path |
| `.aoa/live_receipts/eval-result-receipts.jsonl` | `.aoa/live_receipts/eval-result-receipts.jsonl` | owner-local live log remains in place under routed local memory |

## Boundary

Former root receipt paths are provenance context. Current receipt contracts
cite the active part-local paths. The owner-local live receipt log remains
append-only local memory below authored mechanic source and proof authority.
