# Agon Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check
python mechanics/agon/parts/ccs-alignment/scripts/build_agon_ccs_eval_alignment_registry.py --check
python mechanics/agon/parts/vds-alignment/scripts/build_agon_vds_eval_alignment_registry.py --check
python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python mechanics/agon/parts/mechanical-trial-suites/scripts/build_agon_mechanical_trial_eval_suites.py --check
python mechanics/agon/parts/epistemic-alignment/scripts/build_agon_epistemic_eval_alignment_registry.py --check
python mechanics/agon/parts/slc-alignment/scripts/build_agon_slc_eval_alignment_registry.py --check
python mechanics/agon/parts/kag-alignment/scripts/build_agon_kag_eval_alignment_registry.py --check
python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check
python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py
python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py
python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py
python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py
python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py
python mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py
python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py
python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py
python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/*/tests/test_agon*.py
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
