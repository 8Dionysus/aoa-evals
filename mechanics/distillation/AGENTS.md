# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/distillation/DIRECTION.md` for current operating direction, `mechanics/distillation/PARTS.md` for active parts, and `mechanics/distillation/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/distillation/` and its part-local support surfaces.

## Role

This package routes eval-side Distillation proof work.

It maps distillation proof pressure to compost-provenance,
runtime-candidate-adoption, bundle-local proof review, or stronger-owner
handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | Distillation proof work route on the eval side |
| input | compost provenance evidence, runtime-candidate adoption pressure, memo-reviewed candidate signal, or distillation owner question |
| output | active part route, source bundle review, audit/experience/proof-infra route, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded distillation proof support; stronger owners keep ToS canon, memo truth, runtime contracts, KAG lift, adoption, technique, skill, and playbook truth |
| next route | `mechanics/distillation/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, affected bundle `EVAL.md`, and source owner route |
| tools | eval-specific validators, catalog builder, root validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/EVIDENCE_CLUSTERS.md`
6. `mechanics/README.md`
7. `mechanics/distillation/README.md`
8. `mechanics/distillation/PARTS.md`
9. `mechanics/distillation/PROVENANCE.md` only for old placement or raw lineage
10. the affected bundle `EVAL.md`

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep runtime-pack bridge metadata under `mechanics/audit/` unless a
  distillation proof part owns a narrower support surface.
- Keep generic adoption, consent, compatibility, and KAG/ToS boundary verdict
  packets under `mechanics/experience/`.
- Keep memo recall, memo contradiction, and base writeback-act proof outside
  this package unless a later pass proves a Distillation part.
- Create Distillation parts from a recurring proof operation with validator
  coverage.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-compost-provenance-preservation
python scripts/validate_repo.py --eval aoa-memo-reviewed-candidate-adoption-integrity
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

## Closeout

Report which Distillation part changed, which bundle-local proof claim it
routes, which stronger owner stayed stronger, which validation ran, and which
nearby memo, audit, experience, or proof-infra surfaces intentionally stayed
outside this package.
