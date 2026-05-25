# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/method-growth/DIRECTION.md` for current operating direction, `mechanics/method-growth/PARTS.md` for active parts, and `mechanics/method-growth/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/method-growth/` and its active parts.

## Role

This package routes method-growth proof work for `aoa-evals`.

It maps candidate-lineage and owner-landing proof pressure to source bundle
review, part-local fixtures, or stronger-owner handoffs for object, seed,
skill, technique, playbook, memory, and stats truth.

## Operating Card

| Field | Route |
| --- | --- |
| role | method-growth proof work route |
| input | candidate-lineage evidence, owner-fit routing evidence, fixture movement, generated proof_artifact drift, or method-growth owner question |
| output | active part route, source bundle review, fixture/provenance route, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded method-growth proof support; source bundles and stronger owners keep final meaning, object, seed, skill, technique, playbook, memory, and stats truth |
| next route | `mechanics/method-growth/README.md`, `DIRECTION.md`, `PARTS.md`, target part README, affected bundle `EVAL.md`, and affected bundle `eval.yaml` |
| tools | eval-specific validators, catalog builder, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/architecture/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/method-growth/README.md`
7. `mechanics/method-growth/PARTS.md`
8. the target part README
9. affected bundle `EVAL.md` and `eval.yaml`
10. `mechanics/method-growth/PROVENANCE.md` as the active-to-archive bridge for old root fixture paths

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep fixture families part-local only when they support this method-growth
  route.
- Create method-growth parts from a recurring proof operation with validator
  coverage.
- Route diagnosis, repair, progression, unlock, and distillation surfaces
  through their current owners until a separate evidence pass moves them.
- Keep generated readers weaker than bundle and part-local source surfaces.

## Validation

Run the affected bundle validation first:

```bash
python scripts/validate_repo.py --eval aoa-candidate-lineage-integrity
python scripts/validate_repo.py --eval aoa-owner-fit-routing-quality
```

When fixture paths or generated proof artifacts change, run:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which method-growth part changed, which source bundles remained stronger,
which old root fixture paths were mapped through provenance, which validators
ran, and which nearby growth-cycle, antifragility, rpg, or distillation surfaces
stayed outside this package.
