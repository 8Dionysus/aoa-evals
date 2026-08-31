# Agon / Court Prebinding Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `court-prebinding` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/court-prebinding`.

## Commands

```bash
python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check
python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py
python -m pytest -q mechanics/agon/parts/court-prebinding/tests/test_agon_eval_prebindings.py
```
