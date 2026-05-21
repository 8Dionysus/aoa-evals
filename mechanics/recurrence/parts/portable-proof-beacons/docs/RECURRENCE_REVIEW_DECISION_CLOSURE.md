# Recurrence review decision closure for evals

Eval beacons may mark portable proof pressure, progression-evidence pressure, or overclaim risk. A decision packet may record that runtime evidence should remain local, travel as sidecar evidence, or begin owner-reviewed portable eval authoring.

The packet does not make runtime evidence proof canon. Claim wording, verdict semantics, fixtures, and interpretation remain under `aoa-evals` owner review.

## Role

This note is the closure read for recurrence portable-proof beacons.

It tells future agents how to interpret a review decision without treating the
decision packet as a promotion event by itself.

## Route

```text
beacon pressure
-> review decision packet
-> local-only, sidecar, or authoring-candidate posture
-> owner-reviewed eval authoring when warranted
```

## Validation

Use the recurrence parent and portable-proof-beacons part route before changing
claim wording or promoting runtime evidence into a portable eval.
