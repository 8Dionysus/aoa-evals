# Questbook / Quest Source Record Contract Part

## Role

This part owns the schema-backed source contract for quest records in
`aoa-evals`.

It is not the human open-obligation index, generated dispatch reader, roadmap,
or proof bundle source.

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
outside `aoa-evals`. The installed `aoa-quest-harvest` skill may support
triage, but it does not become source quest truth.

`aoa-evals` owns the quest schema contract, lane/state consistency checks, and
claim limits for source quest records.

## Stop-Lines

- Do not make quest records proof verdicts.
- Do not move quest state without matching source path, schema, human index,
  generated reader, and validation updates.
- Do not reintroduce old top-level quest paths as active source files.
- Do not treat `aoa-quest-harvest` output as source truth.
- Do not use a quest source record as roadmap direction, release readiness,
  owner acceptance, or live promotion authority.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
