# Stress Recovery Window Part

## Role

This part owns the antifragility support route for
`aoa-stress-recovery-window`.

It keeps the stress-specific guidance, shared window family, and repo-level
schema under the Antifragility mechanic while comparison readout discipline
stays under `mechanics/comparison-spine/`.

## Source Surfaces

- `bundles/aoa-stress-recovery-window/EVAL.md`
- `bundles/aoa-stress-recovery-window/eval.yaml`
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

This part must not claim:

- federation-wide resilience;
- live health or runtime recovery authority;
- one-score antifragility movement;
- route, KAG, memo, playbook, or generated-reader authority over owner
  evidence;
- comparison acceptance without the `comparison-spine` readout boundary.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-stress-recovery-window
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
