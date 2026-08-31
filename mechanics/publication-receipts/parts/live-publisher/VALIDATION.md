# Publication Receipts / Live Publisher Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `live-publisher` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/publication-receipts/parts/live-publisher`.

## Commands

```bash
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py
python scripts/validate_repo.py
```
