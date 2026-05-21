# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/rpg/DIRECTION.md` for current operating direction, `mechanics/rpg/PARTS.md` for active parts, and `mechanics/rpg/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/rpg/` and its active parts.

## Role

This package routes eval-side RPG proof work for `aoa-evals`.

It does not own role truth, skill truth, technique truth, playbook campaign
truth, quest acceptance, runtime equip state, or derived stats summaries.

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
10. `mechanics/rpg/PROVENANCE.md` only for old root progression/unlock paths

## Boundaries

- Keep RPG proof work under the active `rpg` parent, not `rpg-proof`,
  `unlock-proof`, or `progression-proof` parent packages.
- Keep progression evidence and unlock proof as parts and support surfaces.
- Do not create new RPG parts from one document, one generated card, or one
  attractive center word.
- Do not move growth-cycle diagnosis, harvest, repair, or closeout surfaces
  into this package without a separate evidence pass.
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
