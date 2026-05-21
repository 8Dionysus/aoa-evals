# Certification Gate Part

## Role

This part owns the support route for experience certification gate proof.

It keeps certification, release-gate, deployment-integrity, rollback,
watchtower, and certification-adjacent verdict support together while the
source proof bundle stays under `bundles/`.

## Source Surfaces

- `bundles/aoa-experience-certification-gate-integrity/EVAL.md`
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

`aoa-evals` owns only bounded readiness-for-operator-review proof readings,
schema/example contracts, regression evidence, and bundle-local interpretation.

## Stop-Lines

This part must claim no certification, release approval, deployment approval,
rollout promotion, durable rollback permission, stats approval, owner
acceptance, or runtime health.

## Validation

```bash
python -m pytest -q mechanics/experience/parts/certification-gate/tests
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
