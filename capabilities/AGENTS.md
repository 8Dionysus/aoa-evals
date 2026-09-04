# AGENTS.md

## Applies to

This card applies to the `aoa-evals` owner capability home under
`capabilities/`.

## Role

This home owns the semantic tree and typed composition contracts for the
existing `aoa-evals-skills` central-proof skill family. It does not own shared eval
selection/application, source-bundle proof meaning, task-local DAG instances,
runtime state, or generated graph authority.

## Editing posture

- Keep `aoa-evals` under the shared
  `engineering.evaluation.central-proof` branch without copying shared
  `aoa-eval` procedure truth here. The sibling
  `engineering.evaluation.use` branch remains owned by `aoa-skills`.
- Keep one advertised `aoa-evals-skills` bundle. `select`, `review`, and `evolve`
  remain internal modes until manual evidence supports an independent bundle.
- Give every node one primary parent and use typed relations for optional
  `select -> review -> evolve` composition.
- Keep raw trials, concrete task DAGs, reports, receipts, and proof evidence
  outside this authored capability source.
- Rebuild generated projections through `aoa-skills`; never hand-edit them as
  authority.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

From the matching `aoa-skills` checkout, follow the owner validation route in [VALIDATION.md](VALIDATION.md).

Green structure checks do not prove routing, proof meaning, safety, or outcome
benefit. Manual isolated, negative, held-out, coexistence, and composed cases
remain primary.
