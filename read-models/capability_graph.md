# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `3e4b1cf96587273db199c498b7c8b6a3d75e31dbad7628e3ebc5b9caf0be2033`

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
