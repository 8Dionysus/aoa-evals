# Questbook Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/questbook/` routes the recurring operation that keeps proof
obligations visible, reviewable, and returnable across long `aoa-evals` work.

Source quest records stay in `quests/`, while roadmaps, playbooks, eval
bundles, and verdict owners keep their own roles. This package keeps quest
schema, lifecycle, dispatch-reader, and return-route support visible for
eval-side obligations.

## Owned Operation

The owned operation is:

`source quest record -> human open-obligation index -> generated quest reader -> deferred return or reviewed promotion`

This package keeps that operation coherent while quest source paths use the
lane/state layout.

## Source Surfaces

- `QUESTBOOK.md`
- `quests/README.md`
- `quests/AGENTS.md`
- `quests/LIFECYCLE.md`
- `mechanics/questbook/PARTS.md`
- `mechanics/questbook/PROVENANCE.md`
- `quests/<lane>/<state>/AOA-EV-Q-*.yaml`
- `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
- `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `.agents/skills/aoa-quest-harvest/SKILL.md`
- `docs/decisions/AOA-EV-D-0004-questbook-topology.md`

## Inputs

- unresolved proof obligations;
- regression or verdict-bridge gaps;
- repeated blind spots that should return later;
- proof-pressure harvest candidates;
- reviewed post-session promotion packets when the active route is closed.

## Outputs

- source quest records;
- human open-obligation index entries;
- generated quest catalog and dispatch readers;
- deferred return routes;
- reviewed promotion targets when repetition is isolated and owner-fit is clear.
- lifecycle state posture that keeps open obligations, closed provenance,
  proof-loop defer, and handoff routes distinct.

## Active Parts

- `source-record-contract`: source quest schema, lane/state source records, and
  lifecycle state posture.
- `dispatch-reader`: generated quest catalog and dispatch projection contract.

## Stronger Owner Split

`aoa-evals` owns proof obligations and proof-surface promotion targets.

`aoa-skills`, `aoa-playbooks`, `aoa-agents`, `aoa-memo`, and sibling owners keep
their own stronger meaning when a quest outcome points outside proof work.

The installed `aoa-quest-harvest` skill may support post-session promotion
triage. Quest source truth stays in reviewed source records, and active-route
promotion stays with the owning review path.

## Boundaries

| Pressure | Route |
| --- | --- |
| Quests route eval-bundle, verdict, or proof-promotion pressure | bundle-local proof surface or owning proof mechanic |
| `QUESTBOOK.md` used as roadmap direction | `ROADMAP.md` |
| generated quest reader used as live portable verdict authority | source quest record plus bundle/mechanic proof evidence |
| closed quest appearing as open obligation | closed-state route outside the open-obligation index |
| old top-level quest path used as active source | `PROVENANCE.md` and legacy path vocabulary |
| source path change | source record, validator, human index, and generated projection update in the same slice |
| promotion verdict used as owner acceptance | downstream owner evidence |

## Legacy Posture

Former Agon markdown quest notes are Agon lineage behind
`mechanics/agon/PROVENANCE.md`. Active quest lifecycle source records live under
`quests/<lane>/<state>/`.

Current IDs stay stable. Old top-level paths and former root schema placement
remain documented as historical accepted-input vocabulary, while generated
readers emit the current route.

Use `mechanics/questbook/PROVENANCE.md` for old questbook path lookup. Use
`mechanics/agon/PROVENANCE.md` for former Agon note lineage. Old root schema
aliases, old top-level quest source files, and markdown quest notes route
through provenance rather than active lifecycle directories.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

The next honest questbook movement is lifecycle tightening with:

- stable ID preservation;
- generated projection proof;
- validator proof;
- legacy path mapping review;
- preserved active/open quest visibility.

That lifecycle tightening now starts in `quests/LIFECYCLE.md`. Future state
movement should update the source record, path, human index, generated readers,
and lifecycle contract together.
