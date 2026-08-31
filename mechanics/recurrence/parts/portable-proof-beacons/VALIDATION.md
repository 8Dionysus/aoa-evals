# Recurrence / Portable Proof Beacons Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `portable-proof-beacons` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/recurrence/parts/portable-proof-beacons`.

## Commands

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
```
