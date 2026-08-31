# Checkpoint / Restartable Inquiry Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `restartable-inquiry` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/checkpoint/parts/restartable-inquiry`.

## Commands

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
