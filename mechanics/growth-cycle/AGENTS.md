# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/growth-cycle/DIRECTION.md` for current operating direction, `mechanics/growth-cycle/PARTS.md` for active parts, and `mechanics/growth-cycle/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/growth-cycle/` and its active parts.

## Role

This package routes eval-side Growth Cycle diagnosis proof work for
`aoa-evals`.

It does not own executable diagnosis skills, repair workflows, checkpoint or
closeout control, owner acceptance, memory canon, runtime repair, quest
promotion, or derived stats summaries.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/README.md`
6. `mechanics/growth-cycle/README.md`
7. `mechanics/growth-cycle/PARTS.md`
8. the target part README
9. affected bundle `EVAL.md` and `eval.yaml`
10. `mechanics/growth-cycle/PROVENANCE.md` only for old deferred-placement
    questions

## Boundaries

- Keep source proof bundles under `bundles/`.
- Keep `diagnosis-gate` as the only active part until another stage has its own
  cross-root proof operation and validator coverage.
- Do not move repair proof from `antifragility`, progression/unlock proof from
  `rpg`, longitudinal-window readouts from `comparison-spine`, or quest source
  records from `questbook` merely because center Growth Cycle names those
  stages.
- Do not create new growth-cycle parts from one document, one quest, one
  closeout note, or one attractive center stage.
- Keep generated readers weaker than bundle and part-local source surfaces.

## Validation

Run the affected bundle validation first:

```bash
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
```

When package route, source-of-truth surfaces, or generated readers change, run:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which Growth Cycle part changed, which source bundle remained stronger,
which deferred stages stayed outside the package, which validators ran, and
whether any closeout, harvest, repair, rpg, comparison, or questbook pressure
needs a future evidence pass.
