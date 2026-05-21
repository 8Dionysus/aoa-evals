# Progression Unlocks Part

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

This part must not claim:

- quest completion or quest acceptance;
- universal rank or one global score;
- automatic rank assignment from one event;
- role, skill, technique, playbook, party, or campaign authority;
- runtime equip state or runtime activation;
- hidden reward logic or penalties;
- generated-card authority;
- broad capability growth;
- growth-cycle diagnosis, repair, harvest, closeout, or longitudinal movement.

This part is a progression/unlock proof route, not an RPG parent substitute and
not a growth-cycle claim. Diagnosis, repair, harvest, closeout, and
longitudinal movement remain outside this part until their own evidence pass
proves a route.

## Validation

Payload coverage anchor: `mechanics/rpg/parts/progression-unlocks/`.

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
