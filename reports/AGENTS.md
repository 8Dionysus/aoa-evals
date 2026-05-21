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

Current owner routes:

- bundle-local reports: `bundles/<name>/reports/`
- proof-loop reports: `mechanics/proof-loop/parts/*/reports/`
- comparison-spine reports: `mechanics/comparison-spine/parts/*/reports/`
- release-support reports: `mechanics/release-support/parts/*/reports/`
- receipt dry-review reports: `mechanics/publication-receipts/parts/*/reports/`

Verify with the touched runner or scorer plus:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
