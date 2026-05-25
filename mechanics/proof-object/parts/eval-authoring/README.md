# Proof Object / Eval Authoring Part

## Role

This part owns the starter authoring scaffold for source eval packages.

Proof bundle, doctrine essay, generated reader, and example report meaning
route to their owning source surfaces.

## Owned Operation

`origin proof pressure -> starter scaffold -> bounded source proof object`

## Source Surfaces

- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `mechanics/proof-object/parts/eval-contracts/`

## Inputs

- a bounded proof question;
- object under evaluation;
- claim type and baseline posture;
- expected evidence, fixtures, runners, reports, and blind spots.

## Outputs

- a new or reshaped `EVAL.md` scaffold;
- frontmatter aligned with the eval source contract;
- explicit comparison and report contract placeholders when applicable.

## Stronger Owner Split

`evals/**/EVAL.md` and `evals/**/eval.yaml` own the actual source proof
claim, object under evaluation, status, evidence posture, verdict logic,
blind spots, and manifest metadata.

`docs/architecture/ARCHITECTURE.md`, `docs/guides/EVAL_PHILOSOPHY.md`, review guides, comparison
guides, score guides, and verdict guides own repo-level proof vocabulary.
The template borrows that vocabulary for a starter shape. When it reads as
doctrine or accepted proof meaning, route back to the source package and proof
guides.

`mechanics/proof-object/parts/eval-contracts/` owns schema-backed contract
checks. Generated catalogs, capsules, sections, reports, receipts, runtime
candidates, and sibling refs stay weaker than source eval packages.

`aoa-evals` owns only the bounded authoring scaffold in this part: a starter
form that helps a future eval package expose source truth without hiding
limits.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| template reads as active proof meaning | route proof meaning to `evals/**/EVAL.md`, `evals/**/eval.yaml`, and repo proof guides |
| placeholder text reads as evidence | route to real evidence entries, fixtures, reports, or examples |
| comparison posture hides in prose | carry it in frontmatter, `eval.yaml`, and comparison guidance |
| source eval package movement appears | keep source eval packages under `evals/` |
| generated readers, reports, receipts, runtime candidates, or sibling refs outrank source eval packages | return to source eval packages and bundle-local review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
