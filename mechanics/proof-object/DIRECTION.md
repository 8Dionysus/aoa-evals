# Proof Object Direction

Proof Object in `aoa-evals` should keep source eval bundles complete, bounded,
and stronger than generated readers, reports, receipts, and release language.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-object route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-object part map.
- `parts/`: bundle-authoring and bundle-contract support.
- `PROVENANCE.md`: controlled bridge from active route to old template and schema placement.
- `legacy/`: lineage only; not a template alias.
- `bundles/`: source proof objects and stronger claim meaning.

## Current contour

- Keep `bundles/*/EVAL.md` and `bundles/*/eval.yaml` as bundle meaning.
- Keep authoring templates and schemas under parts as support, not source
  replacement.
- Keep generated catalogs derived from source bundles.
- Keep reports and receipts subordinate to the concrete proof object.

## Growth rule

Add proof-object parts only when they improve source bundle completeness,
contract validation, authoring discipline, or generated derivation without
moving bundle meaning out of `bundles/`.

## Stop-lines

- Do not move source bundles into mechanics.
- Do not treat templates, schemas, generated readers, reports, receipts,
  runtime candidates, sibling refs, quests, or release readiness as stronger
  than source proof objects.

## Validation

Use the validation lane in [mechanics/proof-object/AGENTS.md](AGENTS.md#validation).
