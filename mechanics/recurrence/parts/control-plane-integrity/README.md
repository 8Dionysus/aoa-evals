# Recurrence / Control Plane Integrity Part

## Role

This part owns the support machinery for
`aoa-recurrence-control-plane-integrity`.

It keeps the recurrence dossier schema, public-safe fixtures, example dossier,
runner, scorer, seeded tests, control-plane eval note, and recurrence component
manifest together under one route.

## Source Surfaces

- `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md`
- `mechanics/recurrence/parts/control-plane-integrity/docs/RECURRENCE_CONTROL_PLANE_EVALS.md`
- `mechanics/recurrence/parts/control-plane-integrity/docs/RECURRENCE_LIVE_OBSERVATION_PRODUCERS.md`
- `mechanics/recurrence/parts/control-plane-integrity/fixtures/recurrence-control-plane-integrity-v1/README.md`
- `mechanics/recurrence/parts/control-plane-integrity/examples/recurrence_control_plane_integrity.dossier.example.json`
- `mechanics/recurrence/parts/control-plane-integrity/schemas/recurrence-control-plane-integrity-dossier.schema.json`
- `mechanics/recurrence/parts/control-plane-integrity/scripts/run_recurrence_control_plane_integrity_eval.py`
- `mechanics/recurrence/parts/control-plane-integrity/scorers/recurrence_control_plane_integrity.py`
- `mechanics/recurrence/parts/control-plane-integrity/tests/test_recurrence_control_plane_integrity_eval_seed.py`
- `mechanics/recurrence/parts/control-plane-integrity/manifests/recurrence/component.recurrence-control-plane-integrity-eval.json`

## Inputs

- recurrence control-plane run dossiers;
- manifest scan, graph closure, hook run, beacon, review decision, downstream
  projection, and Agon diagnostic evidence;
- optional expected axis status for seeded fixture checks.

## Outputs

- one recurrence control-plane integrity report;
- per-axis status and evidence notes;
- missing-axis limitations;
- advisory followthrough suggestions that remain below owner acceptance;
- owner handoff route when dossier evidence depends on runtime, routing,
  downstream projection, or Agon source truth.

## Stronger Owner Split

`Agents-of-Abyss` owns recurrence doctrine and center law. `abyss-stack` owns
runtime return policy, runtime status, runtime logs, and live observation
producer behavior. `aoa-routing` owns live routing behavior. `aoa-agents` owns
self-agent and handoff posture. `aoa-playbooks` owns recurrence choreography.
Downstream owner repositories own projection truth and owner review
acceptance. Agon source truth stays with the Agon owner surface.

`aoa-evals` owns bounded recurrence control-plane proof wording, dossier schema
expectations, runner/scorer behavior, seeded fixture checks, report
interpretation, and bundle-local review for
`aoa-recurrence-control-plane-integrity`. Authority beyond that proof reading
routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep recurrence control-plane pressure with the owner that can
act on it:

| Pressure | Owner route |
| --- | --- |
| recurrence doctrine pressure | Agents-of-Abyss recurrence route |
| global recurrence completeness pressure | Agents-of-Abyss law plus source-owner proof review |
| hidden continuity pressure | `aoa-memo` anchor route plus `aoa-agents` handoff posture route |
| runtime status or runtime activation pressure | `abyss-stack` runtime route |
| runtime self-healing pressure | `abyss-stack` repair and recovery route after owner gates |
| promotion readiness pressure | owner repository acceptance route plus bundle-local proof review |
| owner review acceptance pressure | owner repository review route |
| downstream projection truth pressure | downstream source owner route |
| Agon source truth pressure | Agon owner surface |
| automatic recursor or agent-spawn pressure | `aoa-agents` role route plus `aoa-sdk` readiness route |
| beacon verdict authority pressure | portable-proof-beacon decision closure plus bundle-local proof review |
| portable proof acceptance by recurrence manifest pressure | source bundle authoring and owner-reviewed portable eval route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
