# AGENTS.md

## Guidance for `tests/`

`tests/` protects eval contracts, catalogs, scorers, runners, report schemas, and anti-overread posture.

Tests should prove bounded behavior, not freeze incidental prose. Prefer cases around claim limits, fixture coverage, status drift, report validation, and comparison-spine integrity.

Do not update expected outputs without checking the owning bundle, schema, runner, or scorer.

Keep fixtures public-safe. No private benchmarks, hidden telemetry, secrets, or unreduced operator traces.

Verify with:

```bash
python -m pytest -q tests
python scripts/validate_semantic_agents.py
```
