# Watchtower Alarm Verdict Model

## Role

This model scopes watchtower alarm verdicts for certification-gate evidence.

Alarm verdicts classify alarms as `false_positive`, `non_material`, `material`,
`critical`, or `authority_breach`.

## Reads

Use this surface when watch records need to travel into certification or
post-release regression proof without becoming runtime health authority.

## Boundary

`aoa-evals` owns the alarm verdict shape and interpretation boundary. Runtime
owners keep live alarm handling, emergency action, rollback, and health status.

Durable rollback needs the owner route or emergency authority named by the
owning system.

## Validation

Follow `mechanics/experience/parts/certification-gate/README.md`. The verdict
should make alarm severity reviewable and route authority gaps back to owners.
