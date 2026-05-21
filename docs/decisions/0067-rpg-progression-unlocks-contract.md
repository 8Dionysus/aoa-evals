# 0067 RPG Progression-unlocks Contract

## Status

Accepted.

## Context

`mechanics/rpg/` is the active AoA-aligned parent for eval-side RPG proof. The
`progression-unlocks` part owns progression evidence and unlock proof support:
docs, schemas, examples, generated example cards, and quest source references.

The parent README and `PARTS.md` already name owner split and stop-lines, but
the part README still used a thin `Boundary` paragraph. That is risky because
progression and unlock language can easily become rank assignment, quest
completion, skill truth, role truth, playbook truth, hidden reward logic,
runtime equip state, or broad growth proof.

## Decision

Require `mechanics/rpg/parts/progression-unlocks/README.md` to expose:

- `## Inputs`
- `## Outputs`
- `## Stronger Owner Split`
- `## Stop-Lines`
- `## Validation`

`progression-unlocks` remains a part under `rpg`, not an RPG parent
substitute, growth-cycle claim, quest acceptance gate, runtime equip route, or
proof-adjective parent.

## Consequences

- Future RPG part edits must keep owner split and stop-lines explicit.
- Quest source records stay under `quests/`, and generated unlock cards remain
  derived navigation only.
- Role, rank, skill, technique, playbook, party, campaign, quest, runtime, and
  stats truth remain with stronger owners.
- Diagnosis, repair, harvest, closeout, and longitudinal movement remain
  outside this part until separate eval-side evidence proves their active
  routes.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_validate_repo.py -k rpg_progression_unlocks
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
python -m pytest -q
```
