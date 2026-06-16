# Runtime Latency Tradeoff Proof Flow v1

This dossier defines the fixed-baseline runtime latency and resource-use
tradeoff proof flow for:

- `aoa-runtime-latency-tradeoff`

## Shared case family

Use `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`
as the shared public case-family contract only when the baseline and candidate
runtime variants are judged on the same public-safe fixture family.

The runtime tradeoff read should preserve:

- one named baseline runtime variant;
- one named candidate runtime variant;
- matched fixture, preset, timeout, retry, and metric semantics;
- one latency reading and one resource-use reading kept separate;
- one honest per-case comparison note before any bundle-level verdict.

## Read order

1. Read the baseline runtime variant under the matched fixture family.
2. Read the candidate runtime variant under the same fixture family.
3. Confirm latency and resource-use metrics are defined the same way on both
   sides.
4. Assign per-case comparison notes before the bundle-level verdict.
5. Read the bounded runtime tradeoff verdict.
6. Add `aoa-eval-integrity-check` as the sidecar when public starter wording,
   routing, or maturity posture is under review.

## Required comparison shapes

- `mixed tradeoff signal`
- `candidate stronger`
- `baseline stronger`
- `noisy variation`
- `not reviewable`

## Distinctness boundary

This runtime tradeoff proof flow routes to `aoa-runtime-latency-tradeoff`.

`aoa-regression-same-task` asks whether one candidate materially regressed
against one frozen baseline on the same bounded task family. This dossier asks
whether one local runtime variant comparison preserves a latency/resource-use
tradeoff without becoming a reasoning-quality, agent-behavior, runtime-health,
host, or hardware leaderboard claim.

## Route Checks

| Pressure | Route |
| --- | --- |
| lower latency as general quality | runtime tradeoff verdict plus bundle-local interpretation |
| resource cost hidden behind a winner story | per-case resource-use notes before verdict |
| raw private runtime evidence | sanitized candidate packet and bundle-local review |
| cross-host performance or hardware ranking | `abyss-stack` runtime route or sibling runtime owner with this proof flow only as bounded support |
