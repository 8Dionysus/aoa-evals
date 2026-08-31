# Proof Infra Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py
```
