# Proof Object / Eval Contracts Part

## Role

This part owns the schema-backed source contracts for eval frontmatter and
manifests.

Eval registry meaning and generated reader authority route to their owning
source surfaces.

## Owned Operation

`EVAL.md frontmatter + eval.yaml manifest -> schema-backed proof-object contract -> validation`

## Source Surfaces

- `mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json`
- `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`
- `scripts/validate_repo.py`
- `evals/**/EVAL.md`
- `evals/**/eval.yaml`

## Inputs

- frontmatter metadata from `EVAL.md`;
- manifest metadata from `eval.yaml`, including separate skill and typed
  capability dependency refs;
- lifecycle status, category, claim type, baseline mode, evidence, and relation
  fields.

## Outputs

- schema validation errors when source eval contracts drift;
- bounded metadata accepted by generated catalog, capsule, section, and
  comparison readers.

## Stronger Owner Split

`evals/**/EVAL.md` and `evals/**/eval.yaml` own source proof meaning,
lifecycle status, bounded claim text, evidence posture, baseline mode,
dependencies, and report expectations.

This part owns schema-backed contract validation for frontmatter and manifests.
It can reject missing or malformed metadata while claim invention, maturity
movement, evidence acceptance, and verdict meaning stay with source eval
packages and bundle-local review.

Generated catalog, capsule, section, comparison, runtime candidate, quest,
receipt, and sibling-reference readers consume validated metadata as derived
navigation. They stay weaker than source eval packages and eval-local review.

`aoa-evals` owns the schema contract and validation route here. Approved proof
truth remains in source eval packages and their review evidence.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| schema loosening would make a weak eval package pass | route back to source package completeness |
| generated catalog convenience wants source meaning | keep generated convenience below source proof meaning |
| status movement reads stronger than eval evidence | route to eval evidence, lifecycle posture, and validation |
| source eval package movement appears | keep source eval packages under `evals/` |
| schema acceptance reads as eval-local review, evidence acceptance, publication, or release readiness | route those claims to bundle-local review, evidence review, publication, or release-support surfaces |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
