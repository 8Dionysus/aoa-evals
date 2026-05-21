# AGENTS.md

Local guidance for contributors working under `evals/`.

## Purpose

`evals/<claim-family>/<eval-name>/` is the source-owned eval bundle surface.
The authoritative objects remain each bundle's `EVAL.md` and `eval.yaml`.

Use [README.md](README.md) as the bundle source index before treating short
`notes/`, `checks/`, or `examples/` artifacts as debris.

## Owns

This layer owns:
- bundle-local claim wording
- bundle-local verdict and scoring boundary wording
- bundle-local dependency fields such as `technique_dependencies` and `skill_dependencies`
- bundle-local evidence references, including `support_note` when a comparative bundle requires it

## Does not own

Do not treat this layer as the place to redefine:
- shared fixture families owned by mechanic-local proof-infra or narrower
  mechanic parts
- shared scorer helpers owned by
  `mechanics/proof-infra/parts/reportable-contracts/`
- shared runner contracts owned by
  `mechanics/proof-infra/parts/reportable-contracts/`
- generated catalogs and capsules in `generated/`
- repository doctrine in `docs/`

## Editing rules

When editing a bundle:
- keep `EVAL.md` and `eval.yaml` semantically aligned
- keep the bundle under the claim family implied by `eval.yaml`: category for
  non-comparison evals and `comparison/<baseline_mode>` for comparison evals
- keep the bounded claim narrow and reviewable
- keep `comparison_surface` mirrored across frontmatter and `eval.yaml` when `baseline_mode` is not `none`
- preserve `technique_dependencies` and `skill_dependencies` unless the task explicitly changes dependency meaning
- treat evidence entries as part of claim hygiene, not decoration

Do not add bundle-local AGENTS.md by default. Use a deeper override only when one bundle genuinely needs stronger local rules than the repository and `evals/` layer already provide.

## Validation

For one touched bundle:

```bash
python scripts/validate_repo.py --eval <bundle-name>
```

For bundle index, generated reader, or cross-bundle wording changes:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
```

Run the full test suite when bundle changes also touch validators, generated
contracts, report schemas, or shared proof infrastructure.
