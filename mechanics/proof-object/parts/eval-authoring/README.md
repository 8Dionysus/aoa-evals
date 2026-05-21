# Proof Object / Eval Authoring Part

## Role

This part owns the starter authoring scaffold for source eval packages.

It is not a proof bundle, doctrine essay, generated reader, or example report.

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

`docs/ARCHITECTURE.md`, `docs/EVAL_PHILOSOPHY.md`, review guides, comparison
guides, score guides, and verdict guides own repo-level proof vocabulary. The
template borrows that vocabulary for a starter shape; it does not become
doctrine or accepted proof meaning.

`mechanics/proof-object/parts/eval-contracts/` owns schema-backed contract
checks. Generated catalogs, capsules, sections, reports, receipts, runtime
candidates, and sibling refs stay weaker than source eval packages.

`aoa-evals` owns only the bounded authoring scaffold in this part: a starter
form that helps a future eval package expose source truth without hiding
limits.

## Stop-Lines

- Do not turn the template into active proof meaning.
- Do not use placeholder text as evidence.
- Do not hide comparison posture in prose when frontmatter or `eval.yaml`
  must carry it.
- Do not move source eval packages into this part.
- Do not let generated readers, reports, receipts, runtime candidates, or
  sibling refs outrank source eval packages.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
