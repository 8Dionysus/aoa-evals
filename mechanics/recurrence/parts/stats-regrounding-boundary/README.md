# Stats Re-Grounding Boundary

## Role

`stats-regrounding-boundary` routes the support surface for
`aoa-stats-regrounding-boundary-integrity`.

It checks whether stats-derived surface profiles and source-coverage signals
trigger re-grounding without promoting stats, SDK policy, routing hints, or
eval wording into owner truth.

## Source Surfaces

- `bundles/aoa-stats-regrounding-boundary-integrity/EVAL.md`
- `bundles/aoa-stats-regrounding-boundary-integrity/fixtures/contract.json`
- `bundles/aoa-stats-regrounding-boundary-integrity/reports/summary.schema.json`
- `bundles/aoa-stats-regrounding-boundary-integrity/reports/example-report.json`
- `mechanics/recurrence/parts/stats-regrounding-boundary/fixtures/stats-regrounding-boundary-v1/README.md`
- `mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py`

## Inputs

- stats summary-surface catalog entries;
- source-coverage summaries and thin-signal flags;
- SDK re-grounding decisions;
- routing advisory hints;
- owner-local truth targets and final consumer report wording.

## Outputs

- bounded stats re-grounding boundary reports;
- fixture replacement constraints for split-model consumer paths;
- anti-overclaim notes when derived signals are treated as proof or route
  approval.

## Stronger Owner Split

`aoa-stats` owns derived observability. `aoa-sdk` owns policy application.
`aoa-routing` owns advisory hints. Owner repositories own source truth.
`aoa-evals` owns only the bounded boundary-proof interpretation.

## Stop-Lines

Do not use this part to claim owner artifact correctness, route approval,
project health, SDK optimality, routing authority, or stats-as-proof.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-stats-regrounding-boundary-integrity
python -m pytest -q mechanics/recurrence/parts/stats-regrounding-boundary/tests/test_stats_regrounding_boundary_eval.py
python scripts/build_catalog.py --check
```
