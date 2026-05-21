# AGENTS.md

## Guidance for `examples/`

`examples/` is a compatibility route card, not an active root examples payload
district.

No active root examples payload should live here. Bundle-local examples stay in
`evals/**/examples/`; mechanic-owned examples stay under the owning
`mechanics/*/parts/*/examples/`.

Examples are illustrative. They should support schemas and docs without becoming the verdict or bundle-local claim.

Keep examples public-safe: no private benchmark payloads, hidden telemetry, secrets, or unreduced operator data.

When an example demonstrates an artifact-to-verdict bridge, preserve verdict
ownership in `aoa-evals`, route it through `mechanics/audit/parts/`, and name
what the example still does not prove.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
