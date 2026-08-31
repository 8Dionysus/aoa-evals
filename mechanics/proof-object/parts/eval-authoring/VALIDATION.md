# Proof Object / Eval Authoring Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `eval-authoring` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/proof-object/parts/eval-authoring`.

## Commands

```bash
python -m pytest -q mechanics/proof-object/parts/eval-authoring/tests
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
