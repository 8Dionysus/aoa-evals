# Baseline Readiness

This bundle uses `longitudinal-window`,
so its readiness claim is about comparable ordered windows rather than one frozen baseline.

Minimum readiness for this surface:
- the anchor workflow surface remains `aoa-bounded-change-quality`
- the windows are named and ordered before longitudinal reading begins
- each window has a public report or summary artifact
- the bounded workflow surface stays the same across windows
- context changes that affect comparison are disclosed
- the summary can distinguish:
  - bounded improvement
  - bounded regression
  - no clear directional movement
  - mixed or unstable movement
- each window uses `context_note` as a comparability disclosure rather than filler summary prose
- each non-initial window uses `transition_note` to explain why movement relative to the previous window is real, flat, unstable, or regressive
- the shared window-family contract remains `fixtures/repeated-window-bounded-v1/README.md`
- the paired readout remains `reports/repeated-window-proof-flow-v1.md`
- the schema-backed report and dossiers remain aligned with `reports/example-report.json`, `reports/repeated-window-proof-flow-v1.md`, and `reports/repeated-window-proof-flow-v2.md`
- `aoa-eval-integrity-check` remains the integrity sidecar whenever the public longitudinal wording or maturity posture changes materially

If those conditions do not hold,
the honest result is not a stronger longitudinal claim.

