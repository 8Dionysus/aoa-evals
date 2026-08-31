# Boundary Bridge Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_semantic_agents.py
```
