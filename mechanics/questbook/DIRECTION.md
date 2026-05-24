# Questbook Direction

Questbook in `aoa-evals` keeps proof obligations visible and returnable while
roadmap direction, playbook scenarios, and bundle meaning stay with their owner
surfaces.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest questbook route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active questbook part map.
- `parts/`: source-record contract and dispatch-reader support.
- `PROVENANCE.md`: controlled bridge from active route to old quest schema placement.
- `legacy/`: archive-local route for old quest schema placement after
  `PROVENANCE.md`.
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

| Pressure | Route |
| --- | --- |
| quest used as eval bundle, roadmap authority, playbook, live task assignment, proof verdict, or owner acceptance | bundle-local proof surface, `ROADMAP.md`, playbook owner, live owner route, proof mechanic, or sibling-owner evidence |
| duplicate top-level quest source file | lane/state source record under `quests/<lane>/<state>/` and provenance for old paths |

## Validation

Use the validation lane in [mechanics/questbook/AGENTS.md](AGENTS.md#validation).
