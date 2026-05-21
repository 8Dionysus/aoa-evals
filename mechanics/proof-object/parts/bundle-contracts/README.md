# Proof Object / Bundle Contracts Part

## Role

This part owns the schema-backed source contracts for eval bundle frontmatter
and manifests.

It is not a bundle registry and not generated reader authority.

## Owned Operation

`EVAL.md frontmatter + eval.yaml manifest -> schema-backed proof-object contract -> validation`

## Source Surfaces

- `mechanics/proof-object/parts/bundle-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/bundle-contracts/schemas/eval-manifest.schema.json`
- `scripts/validate_repo.py`
- `evals/**/EVAL.md`
- `evals/**/eval.yaml`

## Inputs

- frontmatter metadata from `EVAL.md`;
- manifest metadata from `eval.yaml`;
- lifecycle status, category, claim type, baseline mode, evidence, and relation
  fields.

## Outputs

- schema validation errors when source bundle contracts drift;
- bounded metadata accepted by generated catalog, capsule, section, and
  comparison readers.

## Stronger Owner Split

`evals/**/EVAL.md` and `evals/**/eval.yaml` own source proof meaning,
lifecycle status, bounded claim text, evidence posture, baseline mode,
dependencies, and report expectations.

This part owns schema-backed contract validation for frontmatter and manifests.
It can reject missing or malformed metadata, but it does not invent bundle
claims, mature a bundle, accept evidence, or rewrite verdict meaning.

Generated catalog, capsule, section, comparison, runtime candidate, quest,
receipt, and sibling-reference readers consume validated metadata as derived
navigation. They stay weaker than source bundles and bundle-local review.

`aoa-evals` owns the schema contract and validation route here, not a registry
of approved proof truth.

## Stop-Lines

- Do not loosen schemas to make weak bundles pass.
- Do not encode generated catalog convenience as source proof meaning.
- Do not make status movement stronger than bundle evidence.
- Do not move source bundles into this part.
- Do not treat schema acceptance as bundle-local review, evidence acceptance,
  publication, or release readiness.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
