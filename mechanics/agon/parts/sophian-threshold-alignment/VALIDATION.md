# Agon / Sophian Threshold Alignment Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `sophian-threshold-alignment` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/sophian-threshold-alignment`.

## Commands

```bash
python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check
python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/sophian-threshold-alignment/tests/test_agon_sophian_eval_alignment_registry.py
```
