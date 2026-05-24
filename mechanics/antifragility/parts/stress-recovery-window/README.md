# Antifragility / Stress Recovery Window Part

## Role

This part owns the antifragility support route for
`aoa-stress-recovery-window`.

It keeps the stress-specific guidance, shared window family, and repo-level
schema under the Antifragility mechanic while comparison readout discipline
stays under `mechanics/comparison-spine/`.

## Source Surfaces

- `evals/comparison/longitudinal-window/aoa-stress-recovery-window/EVAL.md`
- `evals/comparison/longitudinal-window/aoa-stress-recovery-window/eval.yaml`
- `mechanics/antifragility/parts/stress-recovery-window/docs/STRESS_RECOVERY_WINDOW_EVALS.md`
- `mechanics/antifragility/parts/stress-recovery-window/fixtures/stress-recovery-window-bounded-v1/README.md`
- `mechanics/antifragility/parts/stress-recovery-window/schemas/stress_recovery_window_eval_report_v1.json`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md`
- `mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.runtime-chaos-window.example.json`

## Inputs

- ordered windows on one named owner surface and stressor family;
- owner receipts and owner-local artifacts;
- handoff, playbook, route, KAG, and memo evidence kept weaker than owner
  evidence;
- selected runtime-chaos evidence from `mechanics/audit/` as candidate-only
  sidecar input.

## Outputs

- bounded longitudinal stress recovery posture;
- split-axis comparative readout;
- mixed or suppressed result when owner evidence is thin;
- owner handoff route when comparison evidence exposes a stronger-owner gap.

## Stronger Owner Split

`Agents-of-Abyss` owns antifragility law and the center meaning of stress and
recovery pressure. The owner repository owns local incident facts, recovery
actions, and source receipts. `comparison-spine` owns comparison posture and
paired readout discipline. `audit` owns candidate runtime evidence selection.

`aoa-evals` owns the bounded stress-window proof wording, stress-specific
support artifacts, report-schema expectations, and bundle-local interpretation
for `aoa-stress-recovery-window`.

## Stop-Lines

Boundary routes keep stress-recovery pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| federation-wide resilience pressure | `Agents-of-Abyss` doctrine route plus owner evidence review |
| live health or runtime recovery authority pressure | runtime owner or `abyss-stack` runtime route |
| one-score antifragility movement pressure | `aoa-stats` vector-window route plus AoA doctrine review |
| route, KAG, memo, playbook, or generated-reader authority pressure | owning route, KAG, memo, playbook, generated-source, and owner-evidence routes |
| comparison acceptance pressure | `mechanics/comparison-spine/parts/longitudinal-window/` readout route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
