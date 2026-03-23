# Same-Task Baseline Proof Flow v1

This dossier defines the first materialized same-task baseline proof flow across:
- `aoa-regression-same-task`

## Shared case family

Use `fixtures/frozen-same-task-v1/README.md` as the shared public case-family contract.

The same-task read should preserve:
- one visible request surface
- one named frozen baseline target
- one candidate run family on the same bounded cases
- one honest per-case comparison note before any bundle-level verdict

## Read order

1. Read the frozen baseline target on the bounded case family.
2. Read the candidate on the same bounded cases.
3. Assign per-case comparison notes before the bundle-level verdict.
4. Read the bounded same-task verdict.
5. If the baseline surface is being used for a maturity or wording wave, add `aoa-eval-integrity-check` as the sidecar that checks whether the public baseline read is still bounded and non-theatrical.

## Required comparison shapes

- `no material regression`
- `bounded improvement present`
- `noisy variation`
- `regression present`

## Distinctness boundary

This same-task proof flow is not a substitute for `aoa-longitudinal-growth-snapshot`.

`aoa-longitudinal-growth-snapshot` asks whether ordered windows on one bounded workflow surface show movement over time.
This dossier asks whether one candidate materially regressed against one frozen baseline on the same bounded task family.

## Anti-overread rule

Do not collapse this baseline flow into:
- one scalar score
- proof of general capability growth
- proof that one clean same-task comparison explains every nearby diagnostic change
- a replacement for one-run workflow or trace-aware diagnosis
