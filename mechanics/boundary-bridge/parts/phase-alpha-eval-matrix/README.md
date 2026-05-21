# Phase Alpha Eval Matrix Part

## Role

This part owns the bridge that maps sibling-owned Phase Alpha playbook runs to
local `aoa-evals` proof anchors.

It is a `boundary-bridge` part because the operation starts from
`aoa-playbooks` run truth and emits an eval-side matrix without absorbing
playbook, runtime, audit, checkpoint, or bundle authority.

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
- no playbook approval, runtime verdict, eval result receipt, bundle promotion,
  or sibling-owner acceptance.

## Stronger Owner Split

`aoa-playbooks` owns the Phase Alpha run matrix, reviewed run refs, and scenario
composition.

`mechanics/audit/` owns runtime evidence selection and artifact-to-verdict hook
shape. `mechanics/checkpoint/` owns checkpoint-specific hook examples. Source
proof bundles own their bounded claims.

`aoa-evals` owns only the local matrix that says which eval anchors and support
refs should be reviewed for each sibling-owned Phase Alpha run.

## Stop-Lines

Do not use this part to claim:

- a Phase Alpha run passed an eval;
- `aoa-playbooks` accepted local eval interpretation;
- runtime evidence is proof canon;
- an eval bundle was promoted;
- generated matrix entries are stronger than source bundle review;
- recurrence beacons or release checks are proof verdicts.

## Validation

```bash
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
