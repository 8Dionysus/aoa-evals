# Agon Mechanical Trial Eval Suites

## Role

This source note names the eval-suite route for mechanical trial dry-run
pressure.

The suites describe what `aoa-evals` may inspect about mechanical trials. They
do not run the trials or govern an arena.

## Route

```text
trial-suite pressure
-> eval-suite seed
-> generated suite registry
-> candidate-only validation
```

## Reads

Use this surface when a trial-facing proof question needs to inspect event-log
shape, stop-line preservation, expected terminal candidates, or outcome
legitimacy before live protocol authority exists.

## Boundary

`aoa-evals` owns the candidate eval-suite registry and local proof-alignment
checks.

Agents-of-Abyss and runtime owners keep mechanical trial law, trial execution,
arena state, run truth, and verdict authority.

## Validation

Follow the commands in
`mechanics/agon/parts/mechanical-trial-suites/README.md`.

Registry success means the suite is shaped for review. It does not issue live
verdicts, write scars, mutate rank or trust, retain candidates, or promote canon.
