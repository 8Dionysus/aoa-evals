# Questbook / Part Index

## Role

`PARTS.md` lists the active parts inside `mechanics/questbook/`.

It is not the human quest index, generated quest reader, roadmap, or proof
bundle list. A questbook part is active only when it supports the recurring
quest obligation loop and keeps source quest records stronger than read models.

## Active Parts

### `source-record-contract`

Owned operation:

`proof obligation -> lane/state source quest record -> schema-backed lifecycle posture`

This part owns the source quest record contract:

- `mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json`
- `quests/<lane>/<state>/AOA-EV-Q-*.yaml`
- `quests/LIFECYCLE.md`

### `dispatch-reader`

Owned operation:

`source quest record -> generated catalog and dispatch reader -> deferred return route`

This part owns the dispatch projection contract:

- `mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`

The generated files stay in root `generated/` because they are repo-wide derived
readers, but their schema and route contract now live behind the questbook
mechanic.

## Part Contract

Inputs are unresolved proof obligations, lane/state source quest records, quest
lifecycle state, human open-obligation index entries, and generated reader
requirements.

Outputs are schema-backed source quest records, `QUESTBOOK.md`
open-obligation visibility, generated quest catalog and dispatch readers, and
deferred return routes for later reviewed promotion or closure.

Owner split stays explicit: `quests/<lane>/<state>/` owns source quest records;
`QUESTBOOK.md` owns human open-obligation visibility; generated quest readers
stay derived; eval bundles and sibling owners keep stronger proof or owner
truth.

Stop-lines forbid treating quests as eval bundles, verdicts, roadmap direction,
release items, generated authority, or owner acceptance.

Validation routes through [AGENTS](AGENTS.md#validation) and the affected part
route cards. Rebuild generated quest readers through the AGENTS route when
source quest records move.

## Stop-Lines

- Do not treat a quest as an eval bundle, verdict, release item, or roadmap
  direction.
- Do not list closed quests as open obligations in `QUESTBOOK.md`.
- Do not reintroduce old top-level quest source paths as aliases.
- Do not move generated quest readers into this package unless root generated
  topology changes for all repo-wide readers.
- Do not use post-session harvest output as source truth or owner acceptance.
- Do not promote one repeated pressure note into a proof surface without bundle
  or mechanic evidence.

## Validation

After changing these parts, use [AGENTS](AGENTS.md#validation) for executable
validation commands. If generated quest readers are stale, rebuild them through
the same route before rerunning checks.
