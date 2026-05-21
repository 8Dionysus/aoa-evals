# frozen-same-task-v1

Shared fixture family for the first materialized same-task baseline proof flow.

This family is meant to be reusable across:
- `aoa-regression-same-task`

## Shared case surface

Each case should remain a bounded change task with:
- one visible request surface
- one frozen baseline artifact set that stays inspectable after the target is frozen
- one candidate artifact set on the same bounded cases
- enough evidence to read the baseline note, candidate note, and comparative note without widening the claim

## Required comparative shapes

The family should preserve all four public same-task comparison readings:
- `no material regression`
- `bounded improvement present`
- `noisy variation`
- `regression present`

## Replacement rule

Another repo may replace the concrete cases locally, but only if the replacement:
- preserves the same bounded change ask class
- keeps the frozen baseline target explicit and inspectable
- keeps baseline and candidate on the same visible case family
- preserves the possibility of all four public comparative readings
- does not silently turn style-only shifts into a stronger regression or improvement claim

## Public safety

This family should stay public-safe:
- no secret-bearing traces
- no hidden reviewer-only context for reading the frozen baseline
- no baseline target so thin that same-task regression becomes theatrical
- no case families so broad that same-task comparison stops being bounded
