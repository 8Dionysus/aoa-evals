# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/method-growth/DIRECTION.md` for current operating direction, `mechanics/method-growth/PARTS.md` for active parts, and `mechanics/method-growth/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/method-growth/` and its active parts.

## Role

This package routes method-growth proof work for `aoa-evals`.

It does not own source bundle meaning, final owner objects, seed truth,
skill-shaped candidate identity, reusable technique canon, playbook method,
memory canon, or derived stats summaries.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/method-growth/README.md`
7. `mechanics/method-growth/PARTS.md`
8. the target part README
9. affected bundle `EVAL.md` and `eval.yaml`
10. `mechanics/method-growth/PROVENANCE.md` only for old root fixture paths

## Boundaries

- Keep source proof bundles under `bundles/`.
- Keep fixture families part-local only when they support this method-growth
  route.
- Do not create new method-growth parts from one document, one report, or one
  attractive center word.
- Do not move diagnosis, repair, progression, unlock, or distillation surfaces
  into this package without a separate evidence pass.
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
