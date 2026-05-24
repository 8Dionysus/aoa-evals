# RPG Direction

RPG in `aoa-evals` should make progression and unlock proof bounded,
multi-axis, and owner-reviewable without becoming a universal rank or equip
system.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active RPG part map.
- `parts/`: progression-unlocks support.
- `PROVENANCE.md`: controlled bridge from active route to old progression and unlock placement.
- `legacy/`: archive-local route for old progression and unlock placement
  after `PROVENANCE.md`.
- `quests/`: source obligations that remain weaker than owner acceptance.

## Current contour

- Keep the parent name `rpg`; progression and unlock support are parts.
- Keep evidence multi-axis and route-scoped.
- Keep generated unlock cards derived and example-level until owner review.
- Route role, skill, playbook, runtime equip, and stats pressure through the
  stronger owner map before changing eval-side proof wording.

## Growth rule

Add RPG parts only when a repeated proof operation concerns progression,
unlock, equipment posture, or quest-facing RPG evidence with its own validation
and owner split.

## Stop-lines

| Pressure | Route |
| --- | --- |
| universal score, automatic rank, or broad capability growth | bounded progression evidence plus comparison/growth owner review |
| quest acceptance or completion | quest owner and questbook lifecycle route |
| role, skill, technique, playbook, party, or campaign authority | `aoa-agents`, `aoa-skills`, `aoa-techniques`, and `aoa-playbooks` owner routes |
| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |
| generated-card authority | generated card source route plus bundle-local proof review |

## Validation

Use the validation lane in [mechanics/rpg/AGENTS.md](AGENTS.md#validation).
