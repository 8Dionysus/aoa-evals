# Audit / Integrity Review Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `integrity-review` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/audit/parts/integrity-review`.

## Commands

```bash
python scripts/validate_repo.py
python -m pytest -q tests/test_runtime_evidence_surfaces.py -k runtime_integrity_review
```
