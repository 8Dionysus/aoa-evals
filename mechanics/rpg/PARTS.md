# RPG / Part Index

`mechanics/rpg/parts/` contains the active parts of the eval-side RPG proof
operation.

The mechanic owns the route:

`progression or unlock pressure -> bounded proof evidence -> unlock or hold reading -> owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `progression-unlocks` | Maintains route-scoped progression evidence and unlock proof support while routing rank, quest, playbook, runtime, and stats pressure to stronger owners. | `mechanics/rpg/parts/progression-unlocks/README.md` |

## Part Contract

Inputs are quest, route, or campaign scopes; artifact refs; evaluator refs;
axis deltas; confidence; cautions; unlock candidates; conditions; and
source-owned playbook, quest, bundle, or progression refs.

Outputs are bounded progression evidence records, unlock proof cards,
conditions, cautions, and owner handoff routes.

Owner split stays explicit: `Agents-of-Abyss` owns RPG reflection grammar;
`aoa-agents`, `aoa-skills`, `aoa-techniques`, `aoa-playbooks`, quest owners,
`abyss-stack`, and `aoa-stats` own their local role, ability, feat, campaign,
quest, runtime, and summary truths; `aoa-evals` owns proof wording, schemas,
examples, unlock-card posture, and claim limits.

Stop-lines are pressure routes:

| Pressure | Route |
| --- | --- |
| universal score, automatic rank, or broad capability growth | bounded progression evidence plus comparison/growth owner review |
| quest acceptance or completion | quest source owner and questbook lifecycle route |
| role, skill, technique, playbook, party, or campaign authority | stronger owner repository route with eval evidence as support |
| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |
| generated-card authority | source support plus generated-reader route before citation |
| derived stats summary | `aoa-stats` derived route with proof refs |

Validation is the root repository validation, generated quest projection
freshness, semantic agent validation, and the RPG route checks in
`scripts/validate_repo.py`.

## Deferred Part Families

`growth-cycle` diagnosis, repair, harvest, closeout, and progression-lift
surfaces keep their current owners until a separate evidence pass proves an
RPG route.

Repeated-window movement stays under `comparison-spine` unless a later
growth-cycle package routes it as a stage input without stealing comparison
authority.
