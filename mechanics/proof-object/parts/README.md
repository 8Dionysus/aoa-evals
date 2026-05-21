# Proof Object Parts

## Role

`mechanics/proof-object/parts/` holds support parts for source proof-object
authoring and validation.

Parts support `bundles/*/EVAL.md` and `bundles/*/eval.yaml`. They do not own
bundle meaning and do not replace generated readers.

## Active Parts

- `bundle-authoring/`: starter template for bounded eval bundle authoring.
- `bundle-contracts/`: schema-backed frontmatter and manifest contracts.

## Validation

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
