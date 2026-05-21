# Posture Review Part

## Role

This part owns the support route for `aoa-antifragility-posture`.

It keeps the repo-level report schema under the Antifragility mechanic while
the source proof bundle stays under `bundles/`.

## Source Surfaces

- `bundles/aoa-antifragility-posture/EVAL.md`
- `bundles/aoa-antifragility-posture/eval.yaml`
- `bundles/aoa-antifragility-posture/reports/summary.schema.json`
- `bundles/aoa-antifragility-posture/reports/example-report.json`
- `mechanics/antifragility/parts/posture-review/schemas/antifragility_eval_report_v1.json`

## Inputs

- one owner-local surface;
- one named stressor family;
- source-owned stressor receipts;
- degraded continuation or explicit safe-stop posture;
- split-axis report evidence.

## Outputs

- bounded antifragility posture read;
- split-axis status and blind spots;
- owner handoff route when evidence points outside eval-side proof.

## Stronger Owner Split

`Agents-of-Abyss` owns antifragility doctrine, via negativa posture, and the
meaning of owner-request vocabulary. The owner repository owns the local
surface, source receipts, incident facts, degraded continuation, and safe-stop
execution.

`aoa-evals` owns only the bounded posture proof wording, split-axis report
shape, blind spots, and bundle-local interpretation for
`aoa-antifragility-posture`.

## Stop-Lines

This part must not claim:

- repo-global resilience;
- repeated-window improvement;
- runtime repair or live self-healing;
- source-ownership transfer;
- proof that route hints, stats, memory, or generated readers outrank owner
  receipts.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-antifragility-posture
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
