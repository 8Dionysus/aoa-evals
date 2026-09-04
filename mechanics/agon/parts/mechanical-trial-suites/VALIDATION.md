# Agon / Mechanical Trial Suites Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `mechanical-trial-suites` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/agon/parts/mechanical-trial-suites`.

## Commands

```bash
python mechanics/agon/parts/mechanical-trial-suites/scripts/build_agon_mechanical_trial_eval_suites.py --check
python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py
python -m pytest -q mechanics/agon/parts/mechanical-trial-suites/tests/test_agon_mechanical_trial_eval_suites.py
```
