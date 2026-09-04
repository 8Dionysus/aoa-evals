# Agon / VDS Alignment Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `vds-alignment` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/vds-alignment`.

## Commands

```bash
python mechanics/agon/parts/vds-alignment/scripts/build_agon_vds_eval_alignment_registry.py --check
python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py
python -m pytest -q mechanics/agon/parts/vds-alignment/tests/test_agon_vds_eval_alignment.py
```
