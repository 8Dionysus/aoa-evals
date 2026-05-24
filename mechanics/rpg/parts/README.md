# RPG / Parts Route

`mechanics/rpg/parts/` is the lower index for active eval-side RPG proof
parts. Use it after the parent RPG route has selected a progression or unlock
operation and the next agent needs the exact part, payload home, owner route,
tool lane, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for RPG progression evidence and unlock proof parts |
| input | quest scope, route scope, campaign scope, artifact ref, evaluator ref, axis delta, confidence, caution, unlock candidate, condition, or source-owned playbook/quest/bundle/progression ref |
| output | progression evidence record route, unlock proof card route, condition route, caution route, owner handoff, or deferred part-family note |
| owner | `aoa-evals` owns proof wording, schemas, examples, unlock-card posture, and claim limits; stronger owners keep role, ability, feat, campaign, quest, runtime, and summary truth |
| next route | `mechanics/rpg/PARTS.md`, selected part README, source playbook/quest/bundle route, comparison/growth owner route, and parent validation lane |
| tools | generated quest projection checks, repo validator, semantic AGENTS validator, and RPG route checks through `mechanics/rpg/AGENTS.md#validation` |
| validation | `mechanics/rpg/parts/AGENTS.md#validation` and `mechanics/rpg/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `progression-unlocks/` | route-scoped progression evidence and unlock proof support | `progression-unlocks/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| universal score, automatic rank, or broad capability growth | bounded progression evidence plus comparison/growth owner review |
| quest acceptance or completion | quest source owner and questbook lifecycle route |
| role, skill, technique, playbook, party, or campaign authority | stronger owner repository route with eval evidence as support |
| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |
| generated-card authority | source support plus generated-reader route before citation |
| derived stats summary | `aoa-stats` derived route with proof refs |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| route-scoped progression or unlock proof needs local support | source scope, evidence records, part-local support paths, and validation lane exist | `progression-unlocks/README.md` |
| diagnosis, repair, harvest, closeout, or repeated-window movement pressure | current owner mechanic owns the proof route | route outward before adding an RPG part |
| future RPG operation | distinct source surface, payload home, owner split, and validation lane exist | parent `PARTS.md` update plus evidence-cluster review |
