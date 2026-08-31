# Recurrence / Stats Re-Grounding Boundary Part

## Role

`stats-regrounding-boundary` routes the support surface for
`aoa-stats-regrounding-boundary-integrity`.

It checks whether stats-derived surface profiles and source-coverage signals
trigger re-grounding without promoting stats, SDK policy or its advisory
routing hints, or eval wording into owner truth.

## Source Surfaces

- `evals/boundary/aoa-stats-regrounding-boundary-integrity/EVAL.md`
- `evals/boundary/aoa-stats-regrounding-boundary-integrity/fixtures/contract.json`
- `evals/boundary/aoa-stats-regrounding-boundary-integrity/reports/summary.schema.json`
- `evals/boundary/aoa-stats-regrounding-boundary-integrity/reports/example-report.json`
- `mechanics/recurrence/parts/stats-regrounding-boundary/fixtures/stats-regrounding-boundary-v1/README.md`
- `mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py`

## Inputs

- stats summary-surface catalog entries;
- source-coverage summaries and thin-signal flags;
- SDK re-grounding decisions;
- SDK routing advisory hints;
- owner-local truth targets and final consumer report wording.

## Outputs

- bounded stats re-grounding boundary reports;
- fixture replacement constraints for split-model consumer paths;
- anti-overclaim notes when derived signals are treated as proof or route
  approval.

## Stronger Owner Split

`aoa-stats` owns derived observability. `aoa-sdk` owns policy application and
canonical advisory routing hints. `aoa-routing` retains predecessor
compatibility only. Owner repositories own source truth.
`aoa-evals` owns the bounded boundary-proof interpretation. Authority beyond
that proof reading routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep stats-regrounding pressure with the owner that can act on
it:

| Pressure | Owner route |
| --- | --- |
| owner artifact correctness pressure | owner repository source-truth route |
| route approval pressure | `aoa-sdk` advisory route plus owner acceptance |
| project health pressure | owner repository review plus derived stats context |
| SDK optimality pressure | `aoa-sdk` policy and implementation route |
| routing authority pressure | `aoa-sdk` canonical route-authority boundary; `aoa-routing` only for predecessor compatibility |
| stats-as-proof pressure | `aoa-stats` derived-only route plus bundle-local proof review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable commands are owned by this part-local VALIDATION.md route.
