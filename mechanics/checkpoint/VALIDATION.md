# Checkpoint Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
