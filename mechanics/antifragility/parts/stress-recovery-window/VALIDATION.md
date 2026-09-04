# Antifragility / Stress Recovery Window Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `stress-recovery-window` child validation block there; its focused
part-local proof runs first when the input manifest or example report refs
change. This file is the part-local validation route marker so the README can
remain a contract map.


Source anchor: `mechanics/antifragility/parts/stress-recovery-window`.

## Commands

```bash
python -m pytest -q mechanics/antifragility/parts/stress-recovery-window/tests
python scripts/validate_repo.py --eval aoa-stress-recovery-window
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
