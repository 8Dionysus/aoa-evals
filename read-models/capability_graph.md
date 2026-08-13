# Capability graph

Derived from `capabilities/families/*.yaml`. This file is a read model, not capability authority.

Source content hash: `e4c101ea893456759d2e3f4634d776cbfb5df8eb6b0797b0c30b01073aa603ae`

## Semantic tree

- `aoa-evals` (capability, internal, healthy)
  - `aoa-evals-skills` (capability, internal, healthy)
    - `skill.aoa-evals-skills` (skill, advertised, challenger)
      - `mode.aoa-evals-skills.evolve` (mode, internal, challenger)
      - `mode.aoa-evals-skills.review` (mode, internal, challenger)
      - `mode.aoa-evals-skills.select` (mode, internal, challenger)

## Typed relations

| kind | source | target | condition |
|---|---|---|---|
| hands-off-to | `mode.aoa-evals-skills.review` | `mode.aoa-evals-skills.evolve` | Review establishes a bounded proof-owner-evolution-request and the task asks for an owner change. |
| hands-off-to | `mode.aoa-evals-skills.select` | `mode.aoa-evals-skills.review` | Selection returns an exact source or owner-routed object as a central-proof-review-request. |
| implemented-by | `aoa-evals-skills` | `skill.aoa-evals-skills` | - |
| primary-parent | `aoa-evals-skills` | `aoa-evals` | - |
| primary-parent | `mode.aoa-evals-skills.evolve` | `skill.aoa-evals-skills` | - |
| primary-parent | `mode.aoa-evals-skills.review` | `skill.aoa-evals-skills` | - |
| primary-parent | `mode.aoa-evals-skills.select` | `skill.aoa-evals-skills` | - |
| primary-parent | `skill.aoa-evals-skills` | `aoa-evals-skills` | - |
