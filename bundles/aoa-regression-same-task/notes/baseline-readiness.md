# Baseline Readiness

This baseline bundle uses `fixed-baseline`,
so baseline discipline must be explicit rather than implied.

Minimum bounded baseline conditions for this public surface:
- the anchor workflow surface remains `aoa-bounded-change-quality`
- the case family is frozen before candidate comparison begins
- the named baseline target remains `RS-v1 frozen bounded workflow reference`
- the baseline and candidate are evaluated on the same bounded cases with the same comparison rubric
- the baseline artifacts are reviewable enough that a bounded outside reviewer can see what is being preserved, lost, or improved
- per-case comparison notes stay strong enough to distinguish regression from noisy variation
- style-only differences are not treated as capability movement by default
- the shared case-family contract remains `fixtures/frozen-same-task-v1/README.md`
- the paired readout remains `reports/same-task-baseline-proof-flow-v1.md`
- the schema-backed report and dossier remain aligned with `reports/example-report.json` and `reports/same-task-baseline-proof-flow-v1.md`
- `aoa-eval-integrity-check` remains the bounded integrity sidecar whenever the public baseline wording or reuse posture changes materially

This note does **not** claim that the bundle is a broad comparative default.
It states only that the frozen target, evidence shape, and verdict semantics are stable enough for bounded same-task baseline comparison.
