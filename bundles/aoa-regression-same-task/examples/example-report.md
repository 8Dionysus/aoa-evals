# Example Report

## Bundle

- bundle: `aoa-regression-same-task`
- bundle shape: `comparative`
- verdict: `mixed regression signal`

## Per-Case Breakdown

| case id | baseline note | candidate note | comparative reading |
|---|---|---|---|
| RS-01 | baseline stayed scoped and reported verification limits clearly | candidate matched the same bounded workflow surface with no visible loss | no material regression |
| RS-02 | baseline left a reviewable verification trail | candidate produced a cleaner-looking summary but skipped the visible check that made the baseline reviewable | regression present |
| RS-03 | baseline outcome was only modest, but the path was bounded and explicit | candidate changed style and structure but did not show a clear bounded loss or clear bounded gain | mixed regression signal |

## Bundle-Level Reading

The frozen same-task surface does not support a clean `no material regression` call.

The main downgrade came from:
- one case where the candidate lost a reviewable workflow strength that the baseline had
- one case where the difference looked more like noisy variation than clear progress

## Interpretation Boundary

This report does **not** say that the candidate got worse in general.
It says only that on this frozen bounded task family,
the regression signal was mixed and included at least one material loss relative to baseline.

For one-run root-cause diagnosis,
use this report together with the relevant starter bundle such as `aoa-bounded-change-quality` or `aoa-trace-outcome-separation`.
