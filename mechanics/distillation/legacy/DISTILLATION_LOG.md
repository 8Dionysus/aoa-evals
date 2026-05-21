# Distillation Legacy Accounting

## 2026-05-20

- Created `mechanics/distillation/` as the AoA-aligned eval-side package for
  provenance-preserving and candidate-preserving distillation proof work.
- Moved `fixtures/compost-provenance-v1/README.md` behind
  `mechanics/distillation/parts/compost-provenance/`.
- Moved
  `mechanics/experience/parts/adoption-federation/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`
  behind `mechanics/distillation/parts/runtime-candidate-adoption/`.
- Kept `evals/artifact/aoa-compost-provenance-preservation/` and
  `evals/workflow/aoa-memo-reviewed-candidate-adoption-integrity/` under `evals/`
  because bundle-local proof meaning remains stronger than the mechanic route.
- Kept memo recall outside this package and routed it later through
  `mechanics/recurrence/parts/memory-recall/`.
- Kept memo contradiction, confirmed writeback-act proof, witness trace
  integrity, audit runtime-pack hooks, and generic Experience adoption outside
  this package.
