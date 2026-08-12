# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `b23108e477990bae31ff8eef8cc1056ee793964a0e206571a1e6181157bedfae`

## Semantic tree

- `aoa-evals` (capability, internal, healthy)
  - `skill.aoa-evals` (skill, advertised, challenger)
    - `mode.aoa-evals.evolve` (mode, internal, challenger)
    - `mode.aoa-evals.review` (mode, internal, challenger)
    - `mode.aoa-evals.select` (mode, internal, challenger)

## Typed relations

| kind | source | target | condition |
|---|---|---|---|
| hands-off-to | `mode.aoa-evals.review` | `mode.aoa-evals.evolve` | Review establishes a bounded proof-owner-evolution-request and the task asks for an owner change. |
| hands-off-to | `mode.aoa-evals.select` | `mode.aoa-evals.review` | Selection returns an exact source or owner-routed object as a central-proof-review-request. |
| implemented-by | `aoa-evals` | `skill.aoa-evals` | - |
| primary-parent | `mode.aoa-evals.evolve` | `skill.aoa-evals` | - |
| primary-parent | `mode.aoa-evals.review` | `skill.aoa-evals` | - |
| primary-parent | `mode.aoa-evals.select` | `skill.aoa-evals` | - |
| primary-parent | `skill.aoa-evals` | `aoa-evals` | - |
