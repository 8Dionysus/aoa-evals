# Release Support / Readiness Audit Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `readiness-audit` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/release-support/parts/readiness-audit`.

## Commands

```bash
python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py
python scripts/validate_repo.py
python scripts/release_check.py
```
