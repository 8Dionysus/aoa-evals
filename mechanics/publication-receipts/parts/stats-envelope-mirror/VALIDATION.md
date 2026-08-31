# Publication Receipts / Stats Envelope Mirror Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `stats-envelope-mirror` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/publication-receipts/parts/stats-envelope-mirror`.

## Commands

```bash
python scripts/validate_repo.py
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py
```
