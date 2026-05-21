# Bundle Authoring

## Role

This part owns the starter authoring scaffold for source proof bundles.

It is not a proof bundle, doctrine essay, generated reader, or example report.

## Owned Operation

`origin proof pressure -> starter scaffold -> bounded source proof object`

## Source Surfaces

- `mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md`
- `bundles/*/EVAL.md`
- `bundles/*/eval.yaml`
- `mechanics/proof-object/parts/bundle-contracts/`

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

`bundles/*/EVAL.md` and `bundles/*/eval.yaml` own the actual source proof
claim, object under evaluation, status, evidence posture, verdict logic,
blind spots, and manifest metadata.

`docs/ARCHITECTURE.md`, `docs/EVAL_PHILOSOPHY.md`, review guides, comparison
guides, score guides, and verdict guides own repo-level proof vocabulary. The
template borrows that vocabulary for a starter shape; it does not become
doctrine or accepted proof meaning.

`mechanics/proof-object/parts/bundle-contracts/` owns schema-backed contract
checks. Generated catalogs, capsules, sections, reports, receipts, runtime
candidates, and sibling refs stay weaker than source bundles.

`aoa-evals` owns only the bounded authoring scaffold in this part: a starter
form that helps a future bundle expose source truth without hiding limits.

## Stop-Lines

- Do not turn the template into active proof meaning.
- Do not use placeholder text as evidence.
- Do not hide comparison posture in prose when frontmatter or `eval.yaml`
  must carry it.
- Do not move source bundles into this part.
- Do not let generated readers, reports, receipts, runtime candidates, or
  sibling refs outrank source bundles.

## Validation

Payload coverage anchor: `mechanics/proof-object/parts/bundle-authoring/`.

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
