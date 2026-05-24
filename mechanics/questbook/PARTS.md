# Questbook / Part Index

## Role

`PARTS.md` lists the active parts inside `mechanics/questbook/`.

Use it as the part map for the recurring quest obligation loop. Human
open-obligation visibility routes to `QUESTBOOK.md`, generated quest readers
route to root `generated/`, roadmap direction routes to `ROADMAP.md`, and proof
bundle meaning routes to bundle-local proof surfaces.

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

| Field | Route |
| --- | --- |
| Inputs | unresolved proof obligations, lane/state source quest records, lifecycle state, human open-obligation index entries, and generated reader requirements |
| Outputs | schema-backed source quest records, `QUESTBOOK.md` open-obligation visibility, generated catalog/dispatch readers, and deferred return routes for later reviewed promotion or closure |
| Owner split | `quests/<lane>/<state>/` owns source records; `QUESTBOOK.md` owns human open-obligation visibility; generated readers stay derived; eval bundles and sibling owners keep stronger proof or owner truth |
| Stop-lines | route eval-bundle, verdict, roadmap, release, generated-authority, and owner-acceptance pressure to the stronger owner surface |
| Validation | parent `AGENTS.md`, affected part route cards, and generated-reader checks when source records move |

Validation routes through [AGENTS](AGENTS.md#validation) and the affected part
route cards. Rebuild generated quest readers through the AGENTS route when
source quest records move.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| quest treated as eval bundle, verdict, release item, or roadmap direction | bundle-local proof surface, release-support route, or `ROADMAP.md` |
| closed quest listed as open obligation | closed-state route and `QUESTBOOK.md` open-obligation index |
| old top-level quest source path revived as alias | `PROVENANCE.md` and legacy path vocabulary |
| generated quest reader moved into this package | root generated topology review for all repo-wide readers |
| post-session harvest output as source truth or owner acceptance | source quest record review or owner route |
| repeated pressure note promoted into proof surface | bundle or mechanic evidence review |

## Validation

After changing these parts, use [AGENTS](AGENTS.md#validation) for executable
validation commands. If generated quest readers are stale, rebuild them through
the same route before rerunning checks.
