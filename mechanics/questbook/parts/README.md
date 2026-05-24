# Questbook / Parts Route

`mechanics/questbook/parts/` is the lower index for quest obligation loop
support parts. Use it after the parent Questbook route has selected a source
record or generated-reader operation and the next agent needs the exact part,
payload home, owner route, tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for quest source-record and dispatch-reader support parts |
| input | unresolved proof obligation, lane/state source quest record, lifecycle state, human open-obligation index entry, generated-reader requirement, or deferred return route |
| output | source quest record route, lifecycle contract route, generated catalog route, dispatch reader route, open-obligation visibility route, or owner handoff |
| owner | `quests/<lane>/<state>/` owns source records; `QUESTBOOK.md` owns human open-obligation visibility; generated readers stay derived |
| next route | `mechanics/questbook/PARTS.md`, selected part README, source quest record, generated reader, `QUESTBOOK.md`, and parent validation lane |
| tools | quest reader builders, generated-surface checks, repo validator, and focused quest tests through `mechanics/questbook/AGENTS.md#validation` |
| validation | `mechanics/questbook/parts/AGENTS.md#validation` and `mechanics/questbook/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `source-record-contract/` | schema-backed source quest record and lifecycle contract | `source-record-contract/README.md` |
| `dispatch-reader/` | generated quest catalog and dispatch projection contract | `dispatch-reader/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| quest treated as eval bundle, verdict, release item, or roadmap direction | bundle-local proof surface, release-support route, or `ROADMAP.md` |
| closed quest listed as open obligation | closed-state route and `QUESTBOOK.md` open-obligation index |
| old top-level quest source path revived as alias | `PROVENANCE.md` and legacy path vocabulary |
| generated quest reader moved into this package | root generated topology review for repo-wide readers |
| post-session harvest output as source truth or owner acceptance | source quest record review or owner route |
| repeated pressure note promoted into proof surface | bundle or mechanic evidence review |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| source quest record or lifecycle contract changes | schema-backed source record route owns the source shape | `source-record-contract/README.md` |
| generated catalog or dispatch reader changes | source quest records feed deterministic reader outputs | `dispatch-reader/README.md` |
| roadmap, release, verdict, generated authority, or owner acceptance pressure | stronger owner route already exists | route outward before adding a Questbook part |
| future questbook operation | distinct source surface, payload home, owner split, and validation lane exist | parent `PARTS.md` update plus decision review |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
parts index names the active parts and their roles; the parts route card owns
the command lane.
