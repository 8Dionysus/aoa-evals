# AGENTS.md

## Role

`examples/` is a route-card-only compatibility surface for root example paths.

Active example payloads route beside the source that owns their interpretation:

- bundle-local examples stay in `evals/**/examples/`;
- mechanic-owned examples stay under the owning
  `mechanics/*/parts/*/examples/`.

## Rules

Examples are illustrative support for schemas and docs. Verdict authority and
bundle-local claim meaning stay with the owning bundle or mechanic.

Keep examples public-safe: secrets, private benchmark payloads, hidden
telemetry, and unreduced operator data stay out of this route.

When an example demonstrates an artifact-to-verdict bridge, preserve verdict
ownership in `aoa-evals`, route it through `mechanics/audit/parts/`, and name
the proof limits it leaves outside the example.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
