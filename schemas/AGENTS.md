# AGENTS.md

## Guidance for `schemas/`

`schemas/` holds contracts for reports, runners, fixtures, live receipts, and eval-adjacent public artifacts.

Schema edits are proof contract edits. Preserve `$schema`, stable identifier posture, required fields, enums, and descriptions that keep verdict interpretation bounded.

Do not make schemas more permissive to pass a weak report. Fix the report, scorer, runner, or bundle-local contract.

Pair schema changes with examples, validator updates, and docs that explain interpretation limits.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
