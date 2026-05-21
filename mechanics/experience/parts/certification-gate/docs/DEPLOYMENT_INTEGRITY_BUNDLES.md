# Deployment Integrity Bundles

## Role

This source note scopes deployment-integrity proof support for the Experience
certification gate.

Eval bundles judge whether deployment state transitions remain reviewable under
valid authority, clean evidence, open alarm handling, rollback readiness, and
contract fidelity.

## Route

```text
deployment transition
-> evidence packet
-> deployment-integrity bundle read
-> judge verdict
-> operator or owner handoff
```

## Boundary

`aoa-evals` may evaluate the proof shape of a deployment transition. Runtime
owners keep deployment execution, promotion, rollback, and health authority.

The bundle read should expose missing authority or evidence gaps rather than
papering over them.

## Validation

Use the certification-gate part README for commands and source-surface routing.
Passing eval support means the transition was inspectable, not approved.
