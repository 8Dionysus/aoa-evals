# bounded-change-paired-v2

Shared fixture family for the second matched artifact/process paired proof flow.

This family is meant to be reusable across:
- `aoa-bounded-change-quality`
- `aoa-artifact-review-rubric`
- `aoa-output-vs-process-gap`

## Shared case surface

Each case should remain a bounded change task with:
- one visible request surface
- one inspectable artifact-side reading
- one reviewable process-side reading
- one explicit matched-condition note that keeps the side-by-side read honest

## Required paired shapes

The family should preserve all four public pairing shapes:
- artifact outruns process
- process outruns artifact
- broadly aligned
- mixed or noise-limited with no honest winner

This second family should also preserve:
- one style-over-substance risk case
- one case where process discipline is stronger than the produced artifact
- one case where the bridge should stay mixed because matched-condition evidence is thin

## Replacement rule

Another repo may replace the concrete cases locally, but only if the replacement:
- preserves the same bounded change ask class
- keeps artifact-side and process-side evidence readable on the same case family
- keeps matched conditions visible before any bridge verdict is assigned
- preserves the possibility of all four paired shapes
- routes polished output through artifact-side evidence while workflow proof
  stays process-side

## Public safety

This family should stay public-safe:
- public-safe traces only
- house-style expectations visible in the case text
- deployment assumptions public or excluded
- matched-condition evidence present before side-by-side reading
