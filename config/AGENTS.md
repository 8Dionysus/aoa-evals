# AGENTS.md

## Guidance for `config/`

`config/` holds eval publication, selection, and validation-support inputs.

Config can influence which surfaces are built or selected, but it must not silently upgrade a draft, bounded, or sidecar eval into canonical proof.

Keep status, baseline, comparison, and public-selection posture aligned with bundle-local `EVAL.md`, `eval.yaml`, `EVAL_INDEX.md`, and `EVAL_SELECTION.md`.

No secrets, hidden datasets, private telemetry, or local-only absolute paths.

Verify with:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
