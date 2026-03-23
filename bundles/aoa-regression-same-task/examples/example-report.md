# Example Report

## Bundle

- bundle: `aoa-regression-same-task`
- bundle shape: `comparative`
- verdict: `mixed regression signal`
- machine-readable companion: `reports/example-report.json`
- shared proof dossier: `reports/same-task-baseline-proof-flow-v1.md`

## Frozen Baseline Target

- baseline target: `RS-v1 frozen bounded workflow reference`
- shared case family: `frozen-same-task-v1 bounded workflow set`
- compared object: current candidate run family on the same bounded cases
- baseline posture: first public `baseline` starter for same-task regression in `aoa-evals`

## Per-Case Breakdown

| case id | baseline note | candidate note | comparative reading | comparison note |
|---|---|---|---|---|
| RS-01 | baseline stayed scoped and reported verification limits clearly | candidate matched the same bounded workflow surface with no visible loss | no material regression | the frozen baseline strength was preserved closely enough that the read stayed bounded and stable |
| RS-02 | baseline left a reviewable verification trail and one explicit verification boundary | candidate produced a cleaner-looking summary but skipped the visible check that made the baseline reviewable | regression present | the candidate lost a reviewable workflow strength the frozen baseline had |
| RS-03 | baseline outcome was modest, but the path was bounded and explicit | candidate changed phrasing and report structure while keeping the same bounded workflow evidence | noisy variation | the visible difference stayed style-shaped and too weak to justify a stronger claim |
| RS-04 | baseline handled the task cleanly but left one uncertainty implicit | candidate kept the same bounded workflow surface and made the uncertainty explicit without widening scope | bounded improvement present | the candidate is reviewably stronger on this case, but one improved case does not erase the regression elsewhere |

## Bundle-Level Reading

The frozen same-task surface does not support a clean `no material regression` call.

The main downgrade came from:
- one case where the candidate lost a reviewable workflow strength that the baseline had
- one case where the difference looked more like noisy variation than clear progress

Even with one bounded improvement signal,
the honest top-line read stays `mixed regression signal`
because the frozen baseline still shows one material loss on the same surface.

## Interpretation Boundary

This report does **not** say that the candidate got worse in general.
It says only that on `RS-v1 frozen bounded workflow reference`,
the regression signal was mixed and included at least one material loss relative to the frozen baseline.

For one-run root-cause diagnosis,
use this report together with the relevant starter bundle such as `aoa-bounded-change-quality` or `aoa-trace-outcome-separation`.
