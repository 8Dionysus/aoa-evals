# Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Environment setup

```bash
python -m pip install -r requirements-dev.txt
```

## Non-mutating checks

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python -m pytest -q
```

## Intentional generated refresh

Run these only when the corresponding authored source changed and the task
explicitly includes regeneration:

```bash
python scripts/build_catalog.py
python scripts/generate_eval_report_index.py
```

Shared checks live in [mechanics/audit/parts/candidate-readers/VALIDATION.md — Commands](mechanics/audit/parts/candidate-readers/VALIDATION.md#commands).
Shared checks live in [mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/VALIDATION.md — Commands](mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/VALIDATION.md#commands).
