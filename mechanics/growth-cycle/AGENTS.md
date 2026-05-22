# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/growth-cycle/DIRECTION.md` for current operating direction, `mechanics/growth-cycle/PARTS.md` for active parts, and `mechanics/growth-cycle/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/growth-cycle/` and its active parts.

## Role

This package routes eval-side Growth Cycle diagnosis proof work for
`aoa-evals`.

It maps diagnosis-gate proof pressure to source bundle review, nearby mechanic
routes, or stronger-owner handoffs for skills, repair, checkpoint, memory,
runtime, quest, and stats truth.

## Operating Card

| Field | Route |
| --- | --- |
| role | Growth Cycle diagnosis proof work route |
| input | diagnosis-gate evidence, symptom/cause pressure, deferred growth-stage pressure, source bundle movement, or generated reader drift |
| output | diagnosis-gate route, source bundle review, nearby mechanic handoff, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded diagnosis proof support; stronger owners keep executable skills, repair workflows, closeout control, owner acceptance, memory, runtime, quest promotion, and stats summaries |
| next route | `mechanics/growth-cycle/README.md`, `DIRECTION.md`, `PARTS.md`, target part README, affected bundle `EVAL.md`, and affected bundle `eval.yaml` |
| tools | eval-specific validator, catalog builder, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

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

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep `diagnosis-gate` as the only active part until another stage has its own
  cross-root proof operation and validator coverage.
- Route repair proof through `antifragility`, progression/unlock proof through
  `rpg`, longitudinal-window readouts through `comparison-spine`, and quest
  source records through `questbook` until a separate evidence pass moves them.
- Create growth-cycle parts from a recurring proof operation with validator
  coverage.
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
