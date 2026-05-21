# AGENTS.md

## Role

`config/` is a route-card-only compatibility route card for root config paths.

Active root config payloads route to the operation that owns them:

- Agon-owned seed/config payloads live under `mechanics/agon/parts/*/config/`.
- Latest-sibling canary config lives under
  `mechanics/boundary-bridge/parts/latest-sibling-canary/config/`.

## Rules

Config can influence which surfaces are built or selected. draft, bounded, and
sidecar evals keep their bundle-local proof posture during config selection.

Keep status, baseline, comparison, and public-selection posture aligned with
bundle-local `EVAL.md`, `eval.yaml`, `EVAL_INDEX.md`, and `EVAL_SELECTION.md`.

Secrets, hidden datasets, private telemetry, and local-only absolute paths stay
out of this public route.

## Validation

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
