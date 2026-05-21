# Agon Retention Rank Eval Alignment

## Role

This source note names the eval-side route for retention and rank pressure.

It lets `aoa-evals` inspect whether retention or rank evidence is bounded enough
for review while keeping standing and mutation authority elsewhere.

## Route

```text
retention pressure
-> rank alignment seed
-> generated alignment registry
-> no-mutation validation
```

## Reads

Use this surface for retention result legitimacy, repeated error detection, rank
mutation evidence floors, jurisdiction grants, revocations, and assistant drift
boundaries.

## Boundary

`aoa-evals` owns candidate alignment shape and no-mutation checks.

Agents-of-Abyss, stats, memory, runtime, and any future retention owner keep
rank truth, trust truth, retention execution, and durable state authority.

## Validation

Follow the commands in
`mechanics/agon/parts/retention-rank-alignment/README.md`.

A passing registry can flag promotion or caution pressure. It does not mutate
standing, execute retention, grant jurisdiction, or issue a live verdict.
