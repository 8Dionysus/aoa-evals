# RPG / Progression Unlocks Part

## Role

This part owns the support route for bounded progression evidence and unlock
proof through the RPG mechanic.

It keeps multi-axis progression and unlock cards under `rpg` because AoA RPG
routes progression and unlock readings to `aoa-evals` for proof, while
stronger owner repositories keep role, skill, technique, campaign, quest,
runtime, and stats truth.

## Source Surfaces

- `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`
- `mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md`
- `mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json`
- `mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json`
- `mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json`
- `mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json`
- `quests/proof/captured/AOA-EV-Q-0005.yaml`
- `quests/unlock/triaged/AOA-EV-Q-0009.yaml`

## Inputs

- one quest, route, or campaign scope;
- reviewed artifact refs;
- multi-axis deltas or explicit hold/reanchor/downgrade evidence;
- unlock candidates, dispositions, conditions, and cautions;
- evaluator refs and public-safe review dates.

## Outputs

- progression evidence examples and schemas;
- unlock proof examples and schemas;
- proof cards that can justify, gate, hold, or revoke an unlock candidate;
- owner handoff route when an unlock candidate requires role, skill,
  technique, playbook, quest, runtime, or stats authority.

## Stronger Owner Split

`Agents-of-Abyss` owns RPG reflection grammar, progression-reading vocabulary,
and the boundary that keeps RPG language adjunct. `aoa-agents` owns roles,
ranks, personas, actor contracts, and role truth. `aoa-skills` owns
skill-shaped ability truth. `aoa-techniques` owns feat-like reusable practice
truth. `aoa-playbooks` owns campaign choreography and party-template truth.
Quest source owners own quest acceptance and completion. `abyss-stack` owns
runtime state and equip behavior. `aoa-stats` owns derived summaries.

`aoa-evals` owns only bounded progression/unlock proof wording, schemas,
example posture, unlock-card interpretation, cautions, and claim limits.

## Stop-Lines

Use this section as a pressure-to-owner route map for claims that exceed the
local progression/unlock proof operation.

| Pressure | Route |
| --- | --- |
| quest completion or quest acceptance | quest source owner and questbook lifecycle route with proof refs |
| universal rank, one global score, automatic rank assignment, or broad capability growth | bounded progression evidence plus `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |
| role, skill, technique, playbook, party, or campaign authority | `aoa-agents`, `aoa-skills`, `aoa-techniques`, and `aoa-playbooks` owner routes |
| runtime equip state, runtime activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |
| generated-card authority | generated support source, schema/example review, and bundle-local proof citation route |
| growth-cycle diagnosis, repair, harvest, closeout, or longitudinal movement | `mechanics/growth-cycle/`, `mechanics/antifragility/`, closeout, and comparison owner routes |

This part is the progression/unlock proof route. RPG parent questions route to
`mechanics/rpg/`; growth-cycle, repair, closeout, and longitudinal movement
route through their owning mechanics.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
