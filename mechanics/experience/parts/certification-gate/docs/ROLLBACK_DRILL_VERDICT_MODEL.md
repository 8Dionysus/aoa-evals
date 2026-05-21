# Rollback Drill Verdict Model

## Role

This model scopes rollback drill verdicts for Experience certification proof.

Rollback drill verdicts check whether rollback can be executed and verified
under the declared evidence and authority route.

## Reads

Use this surface when rollback readiness is part of certification-gate evidence
but no durable rollback decision is being made inside `aoa-evals`.

## Boundary

The model can expose whether rollback proof is missing, unverifiable, or
misrouted. It does not decide whether rollback is desirable, authorized, or live.

## Validation

Follow the certification-gate README. The expected output is a reviewable
verdict packet, not rollout or rollback permission.
