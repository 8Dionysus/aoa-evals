# Publication Receipts / Receipt Payload Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `receipt-payload` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/publication-receipts/parts/receipt-payload`.

## Commands

```bash
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
