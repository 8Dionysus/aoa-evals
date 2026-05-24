# Comparison Spine / Part Index

`mechanics/comparison-spine/parts/` contains the active parts of the
comparison-spine operation.

The mechanic owns the route:

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `spine-overview` | Maintains the cross-mode read order for the public comparison spine. | `mechanics/comparison-spine/parts/spine-overview/reports/comparison-spine-proof-flow-v1.md` |
| `fixed-baseline` | Maintains fixed-baseline and same-task regression readout discipline. | `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`, `mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md` |
| `peer-compare` | Maintains artifact/process side-by-side peer comparison readout discipline. | `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md`, `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md`, `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md`, `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md` |
| `longitudinal-window` | Maintains repeated-window and stress-recovery window readout discipline. | `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md`, `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md`, `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`, `mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md` |

## Boundary

Parts carry comparison-spine fixture and readout surfaces under the parent
operation. Source claim meaning stays in `evals/**/EVAL.md` and
`evals/**/eval.yaml`, and generated comparison readers stay derived.

## Part Contract

Inputs are bundle-local comparison surfaces, shared proof artifacts, generated
comparison readers, and bounded reports that need a stable comparison read.

Outputs are part-local readout dossiers for spine overview, fixed baseline,
peer compare, longitudinal windows, and stress-recovery windows.

Owner split stays explicit: bundles own claim meaning; comparison-spine owns
comparison posture and read order; generated readers remain derived.

Stop-lines are pressure routes:

| Pressure | Route |
| --- | --- |
| style-only movement as capability movement | source bundle support note plus mode-specific report route |
| repo-global score or broad growth proof | source bundle review plus `longitudinal-window` evidence and growth/progression owner route |
| shared dossier stronger than source proof object | bundle-local `EVAL.md`, `eval.yaml`, and comparison surface route |
| generated comparison reader as source truth | source bundle, builder, and generated check route |
| bundle promotion or deprecation | bundle-local review and release/report owner route |

Validation routes through [AGENTS](AGENTS.md#validation), including generated
comparison-spine and repo validation lanes.
