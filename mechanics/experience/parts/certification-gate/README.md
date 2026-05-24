# Experience / Certification Gate Part

## Role

This part owns the support route for experience certification gate proof.

It keeps certification, release-gate, deployment-integrity, rollback,
watchtower, and certification-adjacent verdict support together while the
source eval package stays under `evals/`.

## Source Surfaces

- `evals/boundary/aoa-experience-certification-gate-integrity/EVAL.md`
- `mechanics/experience/parts/certification-gate/docs/`
- `mechanics/experience/parts/certification-gate/examples/`
- `mechanics/experience/parts/certification-gate/schemas/`
- `mechanics/experience/parts/certification-gate/fixtures/experience-certification-gate-integrity-v1/README.md`
- `mechanics/experience/parts/certification-gate/tests/`
- `mechanics/experience/parts/certification-gate/schemas/rollback_drill_verdict_v1.json`

## Inputs

- candidate evidence bundles;
- regression pack coverage;
- rollback drill evidence;
- compatibility or recharter notes;
- operator review markers;
- certification, deployment, rollback, watchtower, and release-certification
  verdict packets.

## Outputs

- bounded readiness-for-operator-review proof readings;
- schema/example contracts for certification-adjacent verdicts;
- one fixture family contract;
- owner handoff route when a verdict requires certification, release,
  deployment, or rollback authority.

## Stronger Owner Split

`Agents-of-Abyss` owns Experience release posture and certification language.
Owner repositories own operator certification, release approval, deployment
approval, rollout promotion, and durable rollback permission. `abyss-stack`
owns runtime health and deployment execution. `aoa-stats` owns derived
observability without approval authority.

`aoa-evals` owns this part's bounded readiness-for-operator-review proof
readings, schema/example contracts, regression evidence, and bundle-local
interpretation. Authority beyond those proof readings routes through the
stronger owner split above.

## Stop-Lines

Boundary routes keep certification-gate pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| certification authority pressure | Agents-of-Abyss and owner operator certification route |
| release approval pressure | release-support and owner approval route |
| deployment approval or rollout promotion pressure | `abyss-stack` runtime route and operator review route |
| durable rollback permission pressure | owner rollback route and release-support review route |
| stats approval pressure | `aoa-stats` derived observability route |
| owner acceptance pressure | owner repository acceptance route |
| runtime health pressure | `abyss-stack` runtime health route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
