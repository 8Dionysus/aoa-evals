# AGENTS.md

## Applies to

`mechanics/proof-object/legacy/`.

## Role

This legacy bridge preserves old proof-object template and schema placement
behind the active proof-object mechanic.

## Read before editing

1. root `AGENTS.md`
2. `mechanics/proof-object/README.md`
3. `mechanics/proof-object/PARTS.md`
4. `mechanics/proof-object/PROVENANCE.md`
5. `mechanics/proof-object/legacy/INDEX.md`

## Boundaries

- Do not start new bundle authoring here.
- Do not recreate old root template or eval schema aliases.
- Do not use legacy path vocabulary as source proof meaning.
- Keep source bundle meaning in `evals/**/EVAL.md` and `eval.yaml`.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
