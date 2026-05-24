# Boundary Bridge / Orchestrator Proof Anchors Part

## Role

This part owns the proof-anchor alignment surface for orchestrator-facing quest
families.

Orchestrator parent topology, role policy, playbook authority, and memory truth
route to their owning surfaces.

## Source Surfaces

- `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`
- `quests/orchestrator/captured/AOA-EV-Q-0006.yaml`
- `quests/orchestrator/captured/AOA-EV-Q-0007.yaml`
- `quests/orchestrator/captured/AOA-EV-Q-0008.yaml`
- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `scripts/validate_repo.py`

## Inputs

Inputs are orchestrator-facing quest records, `aoa-agents:*` class refs,
capability targets, playbook family refs, memo surface refs, and local proof
surface refs.

## Outputs

Outputs are the authored proof-anchor alignment note, quest owner-surface
bindings, generated quest reader projections, and validator coverage for the
three supported orchestrator proof classes.

## Stronger Owner Split

Owner split stays explicit: `aoa-agents` owns orchestrator class identity,
`aoa-playbooks` owns playbook family meaning, `aoa-memo` owns memory surface
meaning, and `aoa-evals` owns only the bounded proof-anchor posture and quest
obligation route.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| creating an `orchestrator` mechanic becomes the apparent next step | route topology pressure through `boundary-bridge` parent review and stronger owner lanes |
| proof anchors read as class identity | route identity meaning to `aoa-agents` |
| quests read as verdict authority | route verdict meaning to bundle-local proof review |
| local capability targets read as sibling-owner acceptance | route acceptance to the referenced sibling owner |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
