# AGENTS.md

## Guidance for `reports/`

`reports/` contains eval readouts, summaries, and proof-adjacent result artifacts.

Reports are bounded outputs, not broad trust claims. They must name the object under evaluation, the fixture or case coverage, scoring posture, blind spots, and what was not measured.

Do not strengthen a verdict in a report beyond the bundle-local `EVAL.md`, `eval.yaml`, runner contract, and schema-backed output.

Keep reports public-safe. Do not include secrets, private datasets, hidden telemetry, or raw unreduced operator traces.

Verify with the touched runner or scorer plus:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
