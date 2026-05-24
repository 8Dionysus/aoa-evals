# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/rpg/DIRECTION.md` for current operating direction, `mechanics/rpg/PARTS.md` for active parts, and `mechanics/rpg/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/rpg/` and its active parts.

## Role

This package routes eval-side RPG proof work for `aoa-evals`.

It maps progression evidence and unlock proof pressure to part-local support
surfaces, generated projections, source bundle review, or stronger-owner
handoffs for role, skill, technique, playbook, quest, runtime, and stats truth.

## Operating Card

| Field | Route |
| --- | --- |
| role | RPG proof work route on the eval side |
| input | progression evidence, unlock proof, schema/example change, quest or generated card pressure, or RPG owner question |
| output | progression-unlocks route, source bundle review, generated projection check, provenance route, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded RPG proof support; stronger owners keep role, skill, technique, playbook, quest acceptance, runtime equip, and stats truth |
| next route | `mechanics/rpg/README.md`, `DIRECTION.md`, `PARTS.md`, target part README, affected schema/example/quest/generated card, and source owner route |
| tools | root validator, catalog builder, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/rpg/README.md`
7. `mechanics/rpg/PARTS.md`
8. the target part README
9. affected schema, example, quest, generated card, or validator
10. `mechanics/rpg/PROVENANCE.md` as the active-to-archive bridge for old root progression/unlock paths

## Route Rules

- Keep RPG proof work under the active `rpg` parent; `rpg-proof`,
  `unlock-proof`, and `progression-proof` stay legacy parent vocabulary.
- Keep progression evidence and unlock proof as parts and support surfaces.
- Create RPG parts from a recurring proof operation with validator coverage.
- Route growth-cycle diagnosis, harvest, repair, and closeout surfaces through
  their current owners until a separate evidence pass moves them.
- Keep generated readers weaker than schemas, docs, quests, and part-local
  source surfaces.

## Validation

Run the root validation after changing this package:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```

If quest owner surfaces or generated quest projections change, rebuild first:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
```

## Closeout

Report which RPG part changed, which old root paths were mapped through
provenance, which generated projections were rebuilt, which validators ran, and
which stronger-owner boundaries stayed outside this package.
