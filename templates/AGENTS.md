# AGENTS.md

## Role

The active eval authoring template now lives at
`mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`.

`templates/` is a route-card-only compatibility surface for historical template
paths. Active template payloads route to proof-object eval authoring.

## Rules

Preserve the required headings, frontmatter keys, and placeholders unless the repository-wide eval contract changes.
Keep `comparison_surface`, `shared_family_path`, `paired_readout_path`, and `integrity_sidecar` explicit in the template where comparison applies.
Keep `comparison_mode` guidance aligned with the report-schema contract for comparative evals.
Doctrine essays and repo-specific example evals route to their owning docs or
bundle surfaces.
Keep placeholders neutral, bounded, and public-safe.
Historical root template lineage routes through the proof-object part.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
