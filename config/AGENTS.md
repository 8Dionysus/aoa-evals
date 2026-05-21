# AGENTS.md

## Guidance for `config/`

`config/` is a compatibility route card, not an active config payload district.

No active root config payload should live here. Agon-owned seed/config payloads
live under `mechanics/agon/parts/*/config/`; latest-sibling canary config lives
under `mechanics/boundary-bridge/parts/latest-sibling-canary/config/`.

Config can influence which surfaces are built or selected, but it must not
silently upgrade a draft, bounded, or sidecar eval into canonical proof.

Keep status, baseline, comparison, and public-selection posture aligned with
bundle-local `EVAL.md`, `eval.yaml`, `EVAL_INDEX.md`, and `EVAL_SELECTION.md`.

No secrets, hidden datasets, private telemetry, or local-only absolute paths.

Verify with:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
