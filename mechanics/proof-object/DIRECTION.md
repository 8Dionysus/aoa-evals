# Proof Object Direction

Proof Object in `aoa-evals` should keep source eval bundles complete, bounded,
and stronger than generated readers, reports, receipts, and release language.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source eval packages,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-object route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active proof-object part map.
- `parts/`: eval-authoring and eval-contract support.
- `PROVENANCE.md`: controlled bridge from active route to old template and schema placement.
- `legacy/`: archive-local route for old template and schema placement after
  `PROVENANCE.md`; active template and schema routes stay in parts.
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

| Pressure | Route |
| --- | --- |
| source eval package movement appears | keep source eval packages under `evals/`; route support through mechanics |
| template, schema, generated reader, report, receipt, runtime candidate, sibling ref, quest, or release-readiness surface reads as stronger truth | return to the source proof object and its bundle-local review |

## Validation

Use the validation lane in [mechanics/proof-object/AGENTS.md](AGENTS.md#validation).
