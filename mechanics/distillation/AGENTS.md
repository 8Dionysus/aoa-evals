# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/distillation/DIRECTION.md` for current operating direction, `mechanics/distillation/PARTS.md` for active parts, and `mechanics/distillation/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/distillation/` and its part-local support surfaces.

## Role

This package routes eval-side Distillation proof work.

It does not own ToS canon, memo truth, runtime artifact contracts, KAG lift,
owner-local adoption, reusable technique truth, executable skill truth, or
playbook scenario truth.

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

## Boundaries

- Keep source proof bundles under `bundles/`.
- Keep runtime-pack bridge metadata under `mechanics/audit/` unless a
  distillation proof part owns a narrower support surface.
- Keep generic adoption, consent, compatibility, and KAG/ToS boundary verdict
  packets under `mechanics/experience/`.
- Keep memo recall, memo contradiction, and base writeback-act proof outside
  this package unless a later pass proves a Distillation part.
- Do not create new Distillation parts from one document, one report, or one
  attractive word.

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
