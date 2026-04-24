# AGENTS.md

## Guidance for `docs/`

`docs/` explains eval philosophy, comparison posture, trace seams, repeated-window discipline, and shared proof infrastructure.

Documentation may clarify proof meaning, but it must not outrank bundle-local `EVAL.md` and `eval.yaml` for a specific eval claim.

Keep anti-overread language sharp: bounded evals are not total intelligence scores, general safety claims, or universal readiness proofs.

When docs touch comparison, trace, or shared infrastructure semantics, re-read `EVAL_INDEX.md`, `EVAL_SELECTION.md`, and the affected bundle before reporting the change.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
