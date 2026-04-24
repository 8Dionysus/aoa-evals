# AGENTS.md

## Guidance for `examples/`

`examples/` demonstrates eval hooks, report shapes, artifact-to-verdict seams, and public-safe proof-adjacent objects.

Examples are illustrative. They should support schemas and docs without becoming the verdict or bundle-local claim.

Keep examples public-safe: no private benchmark payloads, hidden telemetry, secrets, or unreduced operator data.

When an example demonstrates an artifact-to-verdict bridge, preserve verdict ownership in `aoa-evals` and name what the example still does not prove.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
