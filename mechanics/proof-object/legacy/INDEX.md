# Proof Object Legacy Index

## Role

This index maps old proof-object contract paths to the current active route.

It is not a bundle source list and not a compatibility alias set.

## Path Map

| Former path | Current active route | Posture |
| --- | --- | --- |
| `templates/EVAL.template.md` | `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md` | historical root template placement |
| `schemas/eval-frontmatter.schema.json` | `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json` | historical root schema placement |
| `schemas/eval-manifest.schema.json` | `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json` | historical root schema placement |

## Stop-Lines

- Do not recreate old root aliases.
- Do not treat old paths as active source truth.
- Do not use template lineage as proof bundle maturity.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
