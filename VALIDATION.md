#  Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q
python scripts/build_catalog.py
python scripts/generate_eval_report_index.py
```
