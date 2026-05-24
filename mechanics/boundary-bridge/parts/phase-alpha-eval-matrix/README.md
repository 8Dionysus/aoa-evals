# Boundary Bridge / Phase Alpha Eval Matrix Part

## Role

This part owns the bridge that maps sibling-owned Phase Alpha playbook runs to
local `aoa-evals` proof anchors.

It is a `boundary-bridge` part because the operation starts from
`aoa-playbooks` run truth and emits an eval-side matrix while playbook,
runtime, audit, checkpoint, and bundle authority stay with their owners.

## Owned Operation

`aoa-playbooks phase-alpha run matrix -> local eval-surface plan -> eval anchor and support-ref check -> generated phase-alpha eval matrix -> release or recurrence verification`

## Source Surfaces

- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/examples/phase_alpha_eval_matrix.example.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/schemas/phase-alpha-eval-matrix.schema.json`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`
- `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/generated/phase_alpha_eval_matrix.min.json`
- `repo:aoa-playbooks/generated/phase_alpha_run_matrix.min.json`

## Inputs

- `aoa-playbooks` Phase Alpha run ids, sequence, playbook ids, reviewed-run
  refs, and runtime lane keys;
- local eval anchor mappings for each Phase Alpha run;
- support refs from `mechanics/audit/`, `mechanics/checkpoint/`, `aoa-memo`,
  and `aoa-playbooks`;
- verdict interpretation text and optional control-path rerun flags.

## Outputs

- one generated eval matrix that routes each playbook run to required evals and
  evidence refs;
- schema-backed drift detection when local eval mappings stop matching the
  sibling playbook matrix;
- release-support and recurrence-beacon verification commands;
- playbook approval, runtime verdict, eval result receipt, bundle promotion,
  and sibling-owner acceptance pressure routed to stronger owners.

## Stronger Owner Split

`aoa-playbooks` owns the Phase Alpha run matrix, reviewed run refs, and scenario
composition.

`mechanics/audit/` owns runtime evidence selection and artifact-to-verdict hook
shape. `mechanics/checkpoint/` owns checkpoint-specific hook examples. Source
proof bundles own their bounded claims.

`aoa-evals` owns only the local matrix that says which eval anchors and support
refs should be reviewed for each sibling-owned Phase Alpha run.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| Phase Alpha run reads as having passed an eval | route to bundle-local eval result review |
| `aoa-playbooks` acceptance of local eval interpretation is inferred | route to `aoa-playbooks` owner review |
| runtime evidence reads as proof canon | route to runtime owner and bundle-local proof review |
| eval bundle promotion is inferred | route to bundle lifecycle and proof owner review |
| generated matrix entries read as stronger than source bundle review | return to source bundle review |
| recurrence beacons or release checks read as proof verdicts | route to recurrence or release-support verification with verdict authority retained by proof owners |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
