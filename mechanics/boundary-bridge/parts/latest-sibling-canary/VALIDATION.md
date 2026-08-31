# Boundary Bridge / Latest Sibling Canary Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `latest-sibling-canary` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/boundary-bridge/parts/latest-sibling-canary`.

## Commands

```bash
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python -m pytest -q mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py
python scripts/validate_repo.py
```
