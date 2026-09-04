# Generated Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Regenerate after source changes

```bash
python scripts/build_catalog.py
python scripts/generate_eval_report_index.py
python scripts/build_eval_readiness_dashboard.py --write-generated
python scripts/build_eval_readiness_dashboard.py --no-live-checks --write-generated
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py
```

Use the readiness-dashboard variant that matches the intended snapshot
posture; do not run both by habit.

## Non-mutating freshness checks

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/build_eval_readiness_dashboard.py --check
python scripts/check_eval_support_registry.py --json
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_repo.py
```
