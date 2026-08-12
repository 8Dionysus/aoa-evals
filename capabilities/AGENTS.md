# AGENTS.md

## Applies to

This card applies to the `aoa-evals` owner capability home under
`capabilities/`.

## Role

This home owns the semantic tree and typed composition contracts for the
existing `aoa-evals` central-proof skill. It does not own shared eval
selection/application, source-bundle proof meaning, task-local DAG instances,
runtime state, or generated graph authority.

## Editing posture

- Keep `aoa-evals` under the shared `engineering.evaluation` federation
  parent without copying shared `aoa-eval` procedure truth here.
- Keep one advertised `aoa-evals` bundle. `select`, `review`, and `evolve`
  remain internal modes until manual evidence supports an independent bundle.
- Give every node one primary parent and use typed relations for optional
  `select -> review -> evolve` composition.
- Keep raw trials, concrete task DAGs, reports, receipts, and proof evidence
  outside this authored capability source.
- Rebuild generated projections through `aoa-skills`; never hand-edit them as
  authority.

## Validation

From the matching `aoa-skills` checkout, run:

```bash
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-evals
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-evals
PYTHONPATH=scripts python scripts/build_capability_home_projection.py --owner-root /path/to/aoa-evals --check
PYTHONPATH=scripts python scripts/validate_capability_home_port.py --owner-root /path/to/aoa-evals --check-generated
```

Green structure checks do not prove routing, proof meaning, safety, or outcome
benefit. Manual isolated, negative, held-out, coexistence, and composed cases
remain primary.
