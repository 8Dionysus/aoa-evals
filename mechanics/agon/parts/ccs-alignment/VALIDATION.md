# Agon / CCS Alignment Validation

Executable validation commands for this part are kept in this on-demand route.

Use this local validation route so the README remains a contract map.


Source anchor: `mechanics/agon/parts/ccs-alignment`.

## Commands

```bash
python mechanics/agon/parts/ccs-alignment/scripts/build_agon_ccs_eval_alignment_registry.py --check
python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py
python -m pytest -q mechanics/agon/parts/ccs-alignment/tests/test_agon_ccs_eval_alignment.py
```
