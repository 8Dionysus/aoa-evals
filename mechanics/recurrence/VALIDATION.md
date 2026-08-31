# Recurrence Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py --case mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/cases/RCPI-001.registry-mixed-manifests.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py
python mechanics/recurrence/parts/recursor-boundary/scripts/run_recursor_readiness_boundary_eval.py --case mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/cases/RRB-001.no-spawn-readiness.json --check-expected --json
python -m pytest -q mechanics/recurrence/parts/recursor-boundary/tests/test_recursor_readiness_boundary_eval_seed.py mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py
python scripts/validate_repo.py
```
