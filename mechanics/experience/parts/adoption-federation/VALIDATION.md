# Experience / Adoption Federation Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `adoption-federation` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/experience/parts/adoption-federation`.

## Commands

```bash
python -m pytest -q mechanics/experience/parts/adoption-federation/tests
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
