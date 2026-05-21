# AGENTS.md

## Guidance for `reports/`

`reports/` is a route-card-only compatibility surface for former root report
payloads. Do not add active report files here without an explicit topology
decision and validator allowlist update.

Active reports are bounded outputs, not broad trust claims. They must name the
object under evaluation, the fixture or case coverage, blind spots, scoring
posture, and what was not measured.

Do not strengthen a verdict in a report beyond the bundle-local `EVAL.md`, `eval.yaml`, runner contract, and schema-backed output.

Keep reports public-safe. Do not include secrets, private datasets, hidden telemetry, or raw unreduced operator traces.
Top-level report artifacts may return to `reports/` only through an explicit
topology decision and validator allowlist update.

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

Verify with the touched runner or scorer plus:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
