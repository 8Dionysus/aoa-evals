# Recurrence / Stats Re-Grounding Boundary Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `stats-regrounding-boundary` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/recurrence/parts/stats-regrounding-boundary`.

## Commands

```bash
python scripts/validate_repo.py --eval aoa-stats-regrounding-boundary-integrity
python -m pytest -q mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py
python scripts/build_catalog.py --check
```
