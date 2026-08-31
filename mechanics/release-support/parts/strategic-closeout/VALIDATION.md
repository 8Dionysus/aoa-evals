# Release Support / Strategic Closeout Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `strategic-closeout` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/release-support/parts/strategic-closeout`.

## Commands

```bash
python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py
python scripts/validate_repo.py
python scripts/release_check.py
```
