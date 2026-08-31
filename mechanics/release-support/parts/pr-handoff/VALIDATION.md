# Release Support / PR Handoff Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `pr-handoff` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/release-support/parts/pr-handoff`.

## Commands

```bash
python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py
python scripts/validate_repo.py
python scripts/release_check.py
```
