# Checkpoint / A2A Summon Return Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `a2a-summon-return` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/checkpoint/parts/a2a-summon-return`.

## Commands

```bash
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
