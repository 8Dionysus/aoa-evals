# Comparison Spine Distillation Log

## 2026-05-20

Distilled comparison fixture families from the root `fixtures/` district into
the active comparison-spine parts:

- `fixtures/frozen-same-task-v1/` became
  `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/`.
- `fixtures/bounded-change-paired-v1/` and
  `fixtures/bounded-change-paired-v2/` became
  `mechanics/comparison-spine/parts/peer-compare/fixtures/` surfaces.
- `fixtures/repeated-window-bounded-v1/` became
  `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/`.

Source proof bundles stayed under `evals/`. Generated comparison readers
remain derived from bundle frontmatter, `eval.yaml`, and bundle-local contracts.
