# Proof Object Direction

Proof Object in `aoa-evals` should keep source eval bundles complete, bounded,
and stronger than generated readers, reports, receipts, and release language.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source eval packages, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-object route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-object part map.
- `parts/`: eval-authoring and eval-contract support.
- `PROVENANCE.md`: controlled bridge from active route to old template and schema placement.
- `legacy/`: lineage only; not a template alias.
- `evals/`: source proof objects and stronger claim meaning.

## Current contour

- Keep `evals/**/EVAL.md` and `evals/**/eval.yaml` as source proof meaning.
- Keep authoring templates and schemas under parts as support, not source
  replacement.
- Keep generated catalogs derived from source eval packages.
- Keep reports and receipts subordinate to the concrete proof object.

## Growth rule

Add proof-object parts only when they improve source eval completeness,
contract validation, authoring discipline, or generated derivation without
moving proof meaning out of `evals/`.

## Stop-lines

- Do not move source eval packages into mechanics.
- Do not treat templates, schemas, generated readers, reports, receipts,
  runtime candidates, sibling refs, quests, or release readiness as stronger
  than source proof objects.

## Validation

Use the validation lane in [mechanics/proof-object/AGENTS.md](AGENTS.md#validation).
