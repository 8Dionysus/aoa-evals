# Proof Loop / Route Smoke Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `route-smoke` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/proof-loop/parts/route-smoke`.

## Commands

```bash
python -m pytest -q tests/test_validate_repo.py -k proof_loop
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
