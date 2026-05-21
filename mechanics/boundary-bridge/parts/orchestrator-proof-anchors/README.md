# Boundary Bridge / Orchestrator Proof Anchors Part

## Role

This part owns the proof-anchor alignment surface for orchestrator-facing quest
families.

It is not an `orchestrator` parent mechanic, not role policy, not playbook
authority, and not memory truth.

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

Stop-lines forbid creating an `orchestrator` mechanic, treating proof anchors
as class identity, using quests as verdict authority, or turning local
capability targets into sibling-owner acceptance.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
