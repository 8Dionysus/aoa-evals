# EVAL_INDEX

This file is the repository-wide map of public eval bundles.

## Starter eval bundles

| name | category | status | summary |
|---|---|---|---|
| aoa-bounded-change-quality | workflow | draft | Checks whether a non-trivial agent change stays scoped, explicitly verified, and clearly reported without silent task expansion. |
| aoa-approval-boundary-adherence | boundary | draft | Checks whether an agent correctly distinguishes safe action, explicit-approval-required action, and out-of-bounds action. |

## Planned starter bundles

| name | category | target role |
|---|---|---|
| aoa-artifact-review-rubric | artifact | reviewable artifact-quality rubric surface |
| aoa-regression-same-task | regression | bounded same-task regression detector |
| aoa-ambiguity-handling | stress | incomplete-information and ambiguity probe |
| aoa-scope-drift-detection | boundary | silent task-expansion detector |
| aoa-verification-honesty | workflow | real-vs-symbolic verification checker |
| aoa-output-vs-process-gap | comparative | output polish vs process discipline comparator |
| aoa-longitudinal-growth-snapshot | longitudinal | bounded growth snapshot surface |
| aoa-eval-integrity-check | capability | scorer and verdict coherence check for other evals |

## Planned public states

| status | meaning |
|---|---|
| `draft` | The eval idea exists and is documented, but the bundle is not yet stable enough for strong portable claims. |
| `bounded` | The eval has a repeatable execution path, clear boundaries, and a reviewable verdict surface. |
| `portable` | The eval can be reused outside its birth context without losing its main meaning. |
| `baseline` | The eval is stable enough to serve as a comparison surface across changes. |
| `canonical` | The eval is recommended by default for its bounded claim class. |
| `deprecated` | The eval is historically preserved but no longer preferred as the main proof surface. |

## Category notes

- `capability` checks whether a bounded ability is present.
- `workflow` checks multi-step behavior rather than isolated answers.
- `boundary` checks scope, authority, safety, or approval adherence.
- `artifact` checks the quality of produced outputs.
- `regression` checks whether a change made behavior worse.
- `comparative` compares variants, versions, or modes.
- `longitudinal` checks change over time.
- `stress` probes edge conditions, ambiguity, or adversarial surfaces.

## Notes

- `draft` means the bundle shape is being established and the public claim should remain modest.
- starter bundles are meant to define the public proof surface, not to maximize repo size quickly.
- future versions may record additional metadata such as scoring surface, baseline mode, portability notes, and known blind spots directly in index-derived artifacts.
