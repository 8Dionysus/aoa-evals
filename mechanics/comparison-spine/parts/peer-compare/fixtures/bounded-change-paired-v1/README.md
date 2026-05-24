# bounded-change-paired-v1

Shared fixture family for the first materialized artifact/process paired proof flow.

This family is meant to be reusable across:
- `aoa-bounded-change-quality`
- `aoa-artifact-review-rubric`
- `aoa-output-vs-process-gap`

## Shared case surface

Each case should remain a bounded change task with:
- one visible request surface
- one inspectable artifact surface
- one reviewable workflow surface
- enough evidence to read artifact-side and process-side results without widening the claim

## Required paired shapes

The family should preserve all four public pairing shapes:
- artifact outruns process
- process outruns artifact
- broadly aligned
- mixed or noise-limited with no honest winner

## Replacement rule

Another repo may replace the concrete cases locally, but only if the replacement:
- preserves the same bounded change ask class
- keeps the artifact surface inspectable without private context
- keeps the workflow surface inspectable enough for bounded review
- preserves the possibility of all four paired shapes
- routes style preference through the paired note instead of strengthening the
  proof surface

## Public safety

This family should stay public-safe:
- public-safe traces only
- house-style expectations visible in the case text
- deployment assumptions public or excluded
- task families bounded enough for artifact/process pairing
