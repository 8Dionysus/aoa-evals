# AGENTS.md

Local guidance for contributors working under `bundles/`.

## Purpose

`bundles/*` is the source-owned eval bundle surface. The authoritative objects remain each bundle's `EVAL.md` and `eval.yaml`.

## Owns

This layer owns:
- bundle-local claim wording
- bundle-local verdict and scoring boundary wording
- bundle-local dependency fields such as `technique_dependencies` and `skill_dependencies`
- bundle-local evidence references, including `support_note` when a comparative bundle requires it

## Does not own

Do not treat this layer as the place to redefine:
- top-level shared fixture families in `fixtures/`
- shared scorer helpers in `scorers/`
- top-level runner contracts in `runners/`
- generated catalogs and capsules in `generated/`
- repository doctrine in `docs/`

## Editing rules

When editing a bundle:
- keep `EVAL.md` and `eval.yaml` semantically aligned
- keep the bounded claim narrow and reviewable
- keep `comparison_surface` mirrored across frontmatter and `eval.yaml` when `baseline_mode` is not `none`
- preserve `technique_dependencies` and `skill_dependencies` unless the task explicitly changes dependency meaning
- treat evidence entries as part of claim hygiene, not decoration

Do not add bundle-local AGENTS.md by default. Use a deeper override only when one bundle genuinely needs stronger local rules than the repository and `bundles/` layer already provide.

## Validation

Run:
- `python scripts/validate_repo.py`
- `python scripts/validate_repo.py --eval <bundle-name>` when a targeted bundle check is useful
