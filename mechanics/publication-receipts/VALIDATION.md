# Publication Receipts Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py
```
