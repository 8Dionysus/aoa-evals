# Proof Object Distillation Log

## Role

This log accounts for proof-object lineage distilled into active parts.

It is not a changelog, generated output, or source bundle list.

## Entries

### 2026-05-20 - Root template and eval schemas distilled into proof-object parts

Former root placement:

- `templates/EVAL.template.md`
- `schemas/eval-frontmatter.schema.json`
- `schemas/eval-manifest.schema.json`

Active parts:

- `mechanics/proof-object/parts/bundle-authoring/`
- `mechanics/proof-object/parts/bundle-contracts/`

Reason:

The template and schemas constrain source proof-object authoring and validation.
They are not generic root infrastructure and not separate parent mechanics.
Moving them behind `proof-object` keeps bundle contracts close to the operation
that owns proof-object completeness while source bundle meaning remains under
`bundles/`.

Validation route:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
