# Stay Order Enforcement Verdict

## Role

This note scopes stay-order enforcement verdicts for governance/runtime proof.

Stay order verdicts distinguish active scoped holds from expired, irrelevant, or
misapplied holds.

## Reads

Use this surface when a governance packet needs to show whether a hold should
block or shape a runtime-facing action.

## Boundary

`aoa-evals` owns the verdict support and interpretation boundary. Governance and
runtime owners keep stay-order authority, enforcement, expiry, and action
decisions.

Runtime law remains reviewable. Owner meaning remains owner-local.

## Validation

Use the governance-runtime-boundary README. The verdict should cite stay scope,
authority, expiry, and target action.
