# Recurrence / Memory Recall Validation

Executable validation commands for this part are kept in this on-demand route.

Use the `memory-recall` child validation block there. This file is the part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/recurrence/parts/memory-recall`.

## Commands

```bash
python scripts/validate_repo.py --eval aoa-memo-recall-integrity
python -m pytest -q mechanics/recurrence/parts/memory-recall/tests/test_memo_recall_phase_alpha_report.py
```

Shared checks live in [VALIDATION.md — Non-mutating checks](../../../../VALIDATION.md#non-mutating-checks).
