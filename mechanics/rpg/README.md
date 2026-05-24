# RPG Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/rpg/` routes bounded proof work for progression evidence and unlock
support inside `aoa-evals`.

It receives RPG-shaped pressure as route-scoped evidence, axis deltas, cautions,
unlock candidates, quest refs, generated cards, and owner handoff context.

## Owned Operation

`mechanics/rpg/` owns the eval-side RPG proof operation:

`progression or unlock pressure -> multi-axis evidence -> bounded unlock proof -> owner handoff or held gate`

This package is AoA-aligned. It keeps the parent name `rpg` because the
operation materializes the center RPG mechanic on the proof side. The proof
forms stay as parts and source-support surfaces: `progression-unlocks`,
schemas, examples, generated cards, and quest records route through the active
part and source owners.

## Source Surfaces

- `mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md`
- `mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md`
- `mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json`
- `mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json`
- `mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json`
- `mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json`
- `quests/proof/captured/AOA-EV-Q-0005.yaml`
- `quests/unlock/triaged/AOA-EV-Q-0009.yaml`

## Parts

See [PARTS.md](PARTS.md).

The active part is `progression-unlocks`. It owns route-scoped progression
evidence and unlock proof support. Role, skill, technique, playbook, quest,
runtime, and stats pressure route through the owner map below before any
eval-side proof wording widens.

## Inputs

- quest-scoped, route-scoped, or campaign-scoped progression evidence;
- axis deltas, cautions, artifact refs, evaluator refs, and confidence;
- unlock candidates for abilities, feats, ceilings, cohort patterns, party
  templates, campaign lanes, artifact attunement, or control modes;
- source refs into bundles, quests, playbooks, and progression evidence;
- generated quest readers and unlock cards as derived navigation only.

## Outputs

- bounded progression evidence records;
- bounded unlock proof cards with `grant`, `gated_grant`, `hold`, or `revoke`
  posture;
- explicit cautions, conditions, and owner handoff routes;
- bounded owner-route statements for rank, score, quest, runtime, and
  owner-local authority pressure.

## Stronger Owner Split

`Agents-of-Abyss` owns RPG reflection grammar, progression-reading vocabulary,
and the center boundary that keeps RPG language adjunct.

`aoa-agents` owns roles, ranks, personas, and actor contracts. `aoa-skills`
owns skill-shaped ability truth. `aoa-techniques` owns feat-like reusable
practice truth. `aoa-playbooks` owns campaign choreography and party-template
method. Quest source owners own quest acceptance. `abyss-stack` owns runtime
state and equip behavior. `aoa-stats` owns derived summaries.

`aoa-evals` owns bounded proof wording, schemas, example posture, unlock proof
interpretation, cautions, and claim limits for the progression/unlock proof
surface.

## Stop-Lines

Use this section as a pressure-to-owner route map for claims that exceed the
eval-side progression/unlock proof operation.

| Pressure | Route |
| --- | --- |
| universal agent score or broad capability growth | `mechanics/rpg/parts/progression-unlocks/` can hold bounded evidence; broad growth reading routes through `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |
| rank, persona, or role assignment | `aoa-agents` role and actor-contract route with eval evidence as support |
| skill, technique, feat, party, or campaign authority | `aoa-skills`, `aoa-techniques`, and `aoa-playbooks` owner routes with cited proof refs |
| quest acceptance or completion | quest source owner route plus questbook lifecycle review |
| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates and proof review |
| routing hint, memo witness, or generated unlock card as proof | bundle-local proof review plus `aoa-memo` or generated-source route before the card is cited |
| derived stats or progression summary | `aoa-stats` derived summary route with source proof refs |

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge when former root placement, old
progression/unlock paths, generated card vocabulary, or landing history must be
audited. New RPG proof work starts from this README, [PARTS.md](PARTS.md), and
the active part.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this mechanic before changing progression-unlocks support, progression
evidence schemas, unlock proof bridge docs, generated unlock cards, or
quest-facing RPG evidence routes.

For role truth, skill truth, technique truth, playbook campaign truth, quest
acceptance, runtime equip state, or derived stats summaries, follow the
stronger owner route before changing eval-side proof support.
