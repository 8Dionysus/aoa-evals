# Audit / Selected Evidence Packets Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `selected-evidence-packets` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/audit/parts/selected-evidence-packets`.

## Commands

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
```
