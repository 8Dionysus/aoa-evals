# Experience / Protocol Integrity Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `protocol-integrity` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/experience/parts/protocol-integrity`.

## Commands

```bash
python -m pytest -q mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
