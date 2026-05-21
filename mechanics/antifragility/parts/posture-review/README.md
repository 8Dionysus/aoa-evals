# Antifragility / Posture Review Part

## Role

This part owns the support route for `aoa-antifragility-posture`.

It keeps the repo-level report schema under the Antifragility mechanic while
the source eval package stays under `evals/`.

## Source Surfaces

- `evals/stress/aoa-antifragility-posture/EVAL.md`
- `evals/stress/aoa-antifragility-posture/eval.yaml`
- `evals/stress/aoa-antifragility-posture/reports/summary.schema.json`
- `evals/stress/aoa-antifragility-posture/reports/example-report.json`
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

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
