# Questbook Direction

Questbook in `aoa-evals` should keep proof obligations visible and returnable
without replacing roadmap direction, playbook scenarios, or bundle meaning.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest questbook route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active questbook part map.
- `parts/`: source-record contract and dispatch-reader support.
- `PROVENANCE.md`: controlled bridge from active route to old quest schema placement.
- `legacy/`: lineage only; not an open-task queue.
- `quests/`: active source quest records by lane and state.

## Current contour

- Keep source quest records stable and lane/state-routed.
- Keep human `QUESTBOOK.md` visibility separate from generated readers.
- Keep generated quest catalogs subordinate to source records.
- Keep deferred pressure from becoming proof verdict or owner acceptance.

## Growth rule

Add questbook parts only when the quest obligation loop needs a recurring
source-record, dispatch, harvest, promotion, or validation operation.

## Stop-lines

- Do not use quests as eval bundles, roadmap authority, playbooks, live task
  assignment, proof verdicts, or owner acceptance.
- Do not recreate duplicate top-level quest source files.

## Validation

Use the validation lane in [mechanics/questbook/AGENTS.md](AGENTS.md#validation).
