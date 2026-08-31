# Agon / Retention Rank Alignment Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `retention-rank-alignment` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/retention-rank-alignment`.

## Commands

```bash
python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py
python -m pytest -q mechanics/agon/parts/retention-rank-alignment/tests/test_agon_retention_rank_eval_alignment.py
```
