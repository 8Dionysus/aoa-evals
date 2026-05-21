# Post-Release Regression Verdict

## Role

This note scopes post-release regression verdicts for the certification gate.

They compare live canaries and watch records against certified regression
promises after a release path has moved.

## Route

```text
certified promise
-> live canary or watch record
-> post-release regression verdict
-> continue watch, pause, quarantine, or owner handoff
```

## Boundary

`aoa-evals` may read post-release evidence as bounded regression proof. Runtime
and release owners keep live health, rollback, promotion, and deployment
decisions.

## Validation

Use the certification-gate README and
[Regression Proof Surfaces](../../../../../docs/REGRESSION_PROOF_SURFACES.md)
for route context.

The verdict should name the promise, evidence, and interpretation boundary.
