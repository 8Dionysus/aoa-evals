# Titan / Seed Boundary Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `seed-boundary` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/titan/parts/seed-boundary`.

## Commands

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_mechanic_surface_contracts.py -k titan
```
