# Questbook Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/questbook/` routes the recurring operation that keeps proof
obligations visible, reviewable, and returnable across long `aoa-evals` work.

It is not an eval bundle home, not the roadmap, not a playbook, and not a live
verdict authority.

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
- `docs/decisions/0004-questbook-topology.md`

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
triage. It does not become quest source truth and it does not authorize
promotion during an active route.

## Boundaries

- Quests are not eval bundles.
- `QUESTBOOK.md` is not roadmap direction.
- Generated quest readers are not live portable verdict authority.
- Closed quests stay out of the open-obligation index.
- Old top-level quest paths are legacy path vocabulary, not active source
  files.
- Source path changes must update validators and generated projections in the
  same slice.
- A promotion verdict is smaller than downstream owner acceptance.

## Legacy Posture

Former Agon markdown quest notes are no longer active quest lifecycle source
records. They are preserved as Agon lineage behind `mechanics/agon/PROVENANCE.md`.

Current IDs stay stable. Old top-level paths and former root schema placement
remain documented as historical accepted-input vocabulary, while generated
readers emit the current route.

Use `mechanics/questbook/PROVENANCE.md` for old questbook path lookup. Use
`mechanics/agon/PROVENANCE.md` for former Agon note lineage. Do not recreate
old root schema aliases, old top-level quest source files, or markdown quest
notes under active lifecycle directories.

## Validation

After changing quest source records, quest route docs, or this mechanic, run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If generated quest readers are stale, rebuild them with:

```bash
python scripts/build_catalog.py
```

Then rerun the checks.

## Next Route

The next honest questbook movement is lifecycle tightening with:

- stable ID preservation;
- generated projection proof;
- validator proof;
- legacy path mapping review;
- no loss of active/open quest visibility.

That lifecycle tightening now starts in `quests/LIFECYCLE.md`. Future state
movement should update the source record, path, human index, generated readers,
and lifecycle contract together.
