# Recurrence / Recursor Boundary Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `recursor-boundary` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/recurrence/parts/recursor-boundary`.

## Commands

```bash
python mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py --case mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/cases/RRB-001.no-spawn-readiness.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py
```
