# Growth-cycle / Parts Route

`mechanics/growth-cycle/parts/` is the lower index for active eval-side
Growth Cycle proof parts. Use it after the parent Growth Cycle route has
selected a part-level operation and the next agent needs the exact part,
source proof bundle, stronger-owner route, and validation lane.

## Operating Card

| Field | Route |
| --- | --- |
| role | lower index for active Growth Cycle proof parts |
| input | diagnosis pressure, cause-hypothesis evidence, repair eligibility pressure, broad growth pressure, closeout or quest pressure, or owner-local landing pressure |
| output | part README route, source bundle review, repair-proof route, progression route, owner handoff, or deferred part-family note |
| owner | `aoa-evals` owns diagnosis proof wording and verdict logic; AoA center, skills, agents, SDK, memo, runtime, playbook, and owner repositories keep their authority |
| next route | `mechanics/growth-cycle/PARTS.md`, selected part README, affected source bundle, deferred family note, and stronger-owner route |
| validation | `mechanics/growth-cycle/parts/AGENTS.md#validation` and `mechanics/growth-cycle/AGENTS.md#validation` |

## Active Parts

| Part | Operation | Start surface |
| --- | --- | --- |
| `diagnosis-gate/` | cause-hypothesis discipline before repair, progression, closeout, quest, memory, runtime, or owner acceptance claims | `diagnosis-gate/README.md` |

## Owner Pressure Routes

| Pressure | Route |
| --- | --- |
| cause certainty | source owner diagnosis review plus bundle-local proof evidence |
| repair success | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |
| owner-fit proof or final object quality | owner repository acceptance route |
| broad capability growth or universal progression score | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |
| reviewed-closeout acceptance, donor harvest approval, or quest promotion | closeout, donor, questbook, and target owner routes |
| memory canon | `aoa-memo` memory route |
| runtime activation or hidden automation | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |
| owner-local landing | owner repository acceptance route |

## Part Admission Route

| Source signal | Operation test | Next route |
| --- | --- | --- |
| diagnosis or self-diagnosis evidence needs cause-hypothesis discipline | source bundle and part contract already exist | `diagnosis-gate/README.md` |
| repair, progression, closeout, harvest, quest, memory, runtime, or owner-followthrough pressure | stronger owner route already owns current action or proof shape | route outward before adding a Growth Cycle part |
| future Growth Cycle part candidate | distinct eval-side source surface, payload home, owner split, and validator coverage | parent `PARTS.md` update plus decision review |
