# RPG Parts

`mechanics/rpg/parts/` contains the active parts of the eval-side RPG proof
operation.

The mechanic owns the route:

`progression or unlock pressure -> bounded proof evidence -> unlock or hold reading -> owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `progression-unlocks` | Maintains route-scoped progression evidence and unlock proof support without turning RPG language into rank, quest, playbook, or runtime authority. | `mechanics/rpg/parts/progression-unlocks/README.md` |

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

Stop-lines forbid universal scores, automatic rank assignment, quest
acceptance, role/skill/technique/playbook/runtime authority, hidden reward
logic, generated-card authority, and broad capability growth.

Validation is the root repository validation, generated quest projection
freshness, semantic agent validation, and the RPG route checks in
`scripts/validate_repo.py`.

## Deferred Part Families

`growth-cycle` diagnosis, repair, harvest, closeout, and progression-lift
surfaces remain outside this package until a separate evidence pass proves
their active route.

Repeated-window movement stays under `comparison-spine` unless a later
growth-cycle package routes it as a stage input without stealing comparison
authority.
