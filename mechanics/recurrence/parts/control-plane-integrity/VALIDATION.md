# Recurrence / Control Plane Integrity Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `control-plane-integrity` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/recurrence/parts/control-plane-integrity`.

## Commands

```bash
python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
