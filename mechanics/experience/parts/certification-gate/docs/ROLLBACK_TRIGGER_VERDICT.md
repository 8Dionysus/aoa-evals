# Rollback Trigger Verdict

## Role

This note scopes rollback-trigger verdict support for certification-gate proof.

Rollback-trigger verdicts interpret whether the evidence points toward rollback,
pause, quarantine, continued watch, or owner escalation.

## Reads

Use this surface when alarm, canary, regression, or contract-fidelity evidence
needs to become a bounded review signal.

## Boundary

`aoa-evals` may classify trigger evidence. The owner route decides live rollback,
pause, quarantine, and continued operation.

## Validation

Use the certification-gate README for commands. A trigger verdict should cite
evidence and authority refs, and should fail closed when either is missing.
