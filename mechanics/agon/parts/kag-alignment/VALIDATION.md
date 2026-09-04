# Agon / KAG Alignment Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `kag-alignment` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/kag-alignment`.

## Commands

```bash
python mechanics/agon/parts/kag-alignment/scripts/build_agon_kag_eval_alignment_registry.py --check
python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/kag-alignment/tests/test_agon_kag_eval_alignment_registry.py
```
