# Agon VDS Eval Alignment

## Role

This source note names the eval-side route for verdict draft status alignment.

It lets `aoa-evals` inspect verdict draft legitimacy, delta legitimacy, scar
request legitimacy, retention request legitimacy, and inscription bundle
legitimacy before any live verdict authority is involved.

## Route

```text
verdict draft pressure
-> VDS alignment seed
-> generated alignment registry
-> no-live-verdict validation
```

## Reads

Use this surface when a draft verdict record needs to show which legitimacy
questions are prepared for review and which effects remain unavailable.

## Boundary

`aoa-evals` owns draft-status alignment shape and no-live-verdict validation.

Agents-of-Abyss owns Agon verdict meaning, court posture, closure semantics, and
any future live verdict bridge.

## Validation

Follow the commands in `mechanics/agon/parts/vds-alignment/README.md`.

Registry success preserves draft-status reviewability. It does not emit, accept,
or execute a live verdict.
