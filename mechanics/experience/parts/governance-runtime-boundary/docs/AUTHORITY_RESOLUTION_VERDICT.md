# Authority Resolution Verdict

## Role

This source note scopes authority-resolution verdicts for the governance and
runtime-boundary part.

Authority resolution verdicts verify whether denied actors, expired authority,
or mismatched scope are prevented from performing sovereign actions.

## Reads

Use this surface when an Experience governance packet needs to show that
authority was resolved before a runtime or owner-facing action was accepted.

## Boundary

`aoa-evals` owns the verdict support shape. Runtime law remains reviewable and
owner meaning remains owner-local.

The verdict may expose a missing or denied authority route. It does not grant
sovereign action, rewrite governance law, or enforce runtime behavior.

## Validation

Use `mechanics/experience/parts/governance-runtime-boundary/README.md` for the
part-level checks. Verdict packets should cite authority refs and fail closed
when authority is absent or out of scope.
