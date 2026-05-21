# AGENTS.md

## Role

`reports/` is a route-card-only compatibility surface for former root report
payloads.

Active report payloads route to the owning bundle or mechanic part unless an
explicit topology decision and validator allowlist update establishes a new
root route.

## Rules

Active reports are bounded outputs. They must name the
object under evaluation, the fixture or case coverage, blind spots, scoring
posture, and measured boundary.

Verdict strength stays within the bundle-local `EVAL.md`, `eval.yaml`, runner
contract, and schema-backed output.

Keep reports public-safe: secrets, private datasets, hidden telemetry, and raw
unreduced operator traces stay out of this route.
Top-level report artifacts may return to `reports/` only through an explicit
topology decision and validator allowlist update.

## Current Routes

Current owner routes:

- bundle-local reports: `evals/<family>/<eval>/reports/`
- proof-loop reports: `mechanics/proof-loop/parts/*/reports/`
- comparison-spine reports: `mechanics/comparison-spine/parts/*/reports/`
- release-support reports: `mechanics/release-support/parts/*/reports/`
- receipt dry-review reports: `mechanics/publication-receipts/parts/*/reports/`

When a comparison-spine paired readout uses shared dossiers, keep the primary
bundle-local dossier path in `paired_readout_path`, record additional shared
dossiers in `additional_paired_readout_paths`, and keep top-level dossiers
weaker than bundle-local interpretation guidance.

## Validation

Use the touched runner or scorer route plus:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
