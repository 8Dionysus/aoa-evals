# Questbook / Quest Source Record Contract Part

## Role

This part owns the schema-backed source contract for quest records in
`aoa-evals`.

It routes quest record source shape. Human open-obligation visibility routes to
`QUESTBOOK.md`, generated dispatch routes to the dispatch-reader part, roadmap
direction routes to `ROADMAP.md`, and proof bundle meaning routes to
bundle-local proof surfaces.

## Owned Operation

`proof obligation -> lane/state quest source record -> lifecycle-aware return route`

## Source Surfaces

- `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
- `quests/<lane>/<state>/AOA-EV-Q-*.yaml`
- `quests/LIFECYCLE.md`
- `quests/README.md`
- `quests/AGENTS.md`

## Inputs

- missing proof or regression pressure;
- verdict-bridge debt;
- repeated blind spots;
- owner handoff pressure;
- reviewed post-session harvest candidates.

## Outputs

- one stable quest `id`;
- lane/state source placement;
- lifecycle state that matches the directory;
- `QUESTBOOK.md` visibility when the state is open;
- generated projection input for quest catalog and dispatch readers.

## Stronger Owner Split

`quests/<lane>/<state>/AOA-EV-Q-*.yaml` owns source quest record identity,
lane, state, public-safe obligation text, refs, and return posture.
`quests/LIFECYCLE.md` owns the lifecycle vocabulary and allowed state meaning.

`QUESTBOOK.md` owns human open-obligation visibility. Generated quest catalog
and dispatch readers own derived navigation only. Eval bundles and mechanic
parts own proof verdicts when a quest pressure becomes a source proof object.

Sibling repositories own downstream owner acceptance when a quest points
outside `aoa-evals`. The shared `aoa-session-harvest` `classify` mode may
support session-local triage when explicitly supplied; its source stays with
`aoa-skills`, and source quest truth stays in reviewed quest records.

`aoa-evals` owns the quest schema contract, lane/state consistency checks, and
claim limits for source quest records.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| quest record used as proof verdict | bundle-local proof surface or owning mechanic evidence |
| quest state movement | matching source path, schema, human index, generated reader, and validation updates |
| old top-level quest path revived as active source | `PROVENANCE.md` and legacy path vocabulary |
| `aoa-session-harvest` classify output used as source truth or direct promotion | reviewed source quest record and target-owner acceptance |
| quest source record used as roadmap direction, release readiness, owner acceptance, or live promotion authority | `ROADMAP.md`, release-support route, sibling-owner evidence, or reviewed promotion route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
