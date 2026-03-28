# Trace Eval Bridge

## Purpose

This document defines the bounded trace-and-eval bridge for `aoa-evals`.

It makes runtime artifacts and trace surfaces readable as evidence inputs for
existing eval bundles.
It does not move verdict logic into `aoa-agents`, `aoa-playbooks`, or runtime
implementation.

## Source seed

Source seed ref:

- `Dionysus/seed_expansion/seed.aoa.agents-runtime-pack.v0.md#aoa-seed-r4-trace-and-eval-bridge`

## Core rule

`aoa-evals` may read runtime artifacts and trace surfaces as evidence.

It remains the owner of:

- verdict logic
- contract tests
- report interpretation
- bounded proof wording

It does not take ownership of:

- playbook-level `eval_anchors`
- agent-layer artifact contracts
- memo-layer `WitnessTrace` meaning
- memo-layer `inquiry_checkpoint` meaning
- runtime routing or transport

## Preserved vocabulary

Keep this seam legible in the same public terms:

- `WitnessTrace`
- `trace grading`
- `eval hooks`
- `contract test`
- `verification artifact`

## Primary bridge routes

### `AOA-P-0006 self-agent-checkpoint-rollout`

Use `aoa-approval-boundary-adherence` as the primary verdict anchor for the
approval-gated checkpoint route.

`aoa-bounded-change-quality` remains the companion workflow reading for the same
route.
It does not require a second sovereign checkpoint bundle.

Primary evidence inputs:

- `approval_record`
- `rollback_marker`
- `health_check`
- `improvement_log`

`approval_record` stays the verification artifact for this bridge.

Read this route as bounded approval and checkpoint discipline, not as a proof
that self-agent work is generally safe or complete.

### `AOA-P-0008 long-horizon-model-tier-orchestra`

Use `aoa-tool-trajectory-discipline` as the primary verdict anchor for the
first model-tier route.

Primary evidence inputs:

- `route_decision`
- `bounded_plan`
- `verification_result`
- `transition_decision`
- `distillation_pack`

`verification_result` stays the verification artifact for the first hook
surface.

When the route exposes both a visible outcome surface and visible path evidence,
`aoa-trace-outcome-separation` may travel as an adjacent split-reading
diagnostic surface.
Its current bounded proof flow is anchored in
`fixtures/trace-outcome-bounded-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.
That sidecar stays on keeping outcome and path readable before any combined
reading.
It does not replace `aoa-tool-trajectory-discipline` as the narrower
tool-path anchor for this route.

When a bounded route also exports `WitnessTrace`, that trace may travel as an
optional sidecar for `aoa-witness-trace-integrity`.
That sidecar is evidence-only.
It does not silently add a required playbook artifact.
Its current draft public proof flow is anchored in
`fixtures/witness-trace-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.

When the route emits an explicit return decision, anchor refs, and bounded
re-entry note, `aoa-return-anchor-integrity` may travel as an adjacent
diagnostic surface.
That sidecar stays on anchor fidelity and honest re-entry.
It does not replace `aoa-tool-trajectory-discipline` as the primary
route-quality anchor.

### `AOA-P-0009 restartable-inquiry-loop`

Use `aoa-long-horizon-depth` as the primary verdict anchor for the first
restartable inquiry bridge.

Primary evidence inputs:

- `inquiry_checkpoint`
- `decision_ledger`
- `contradiction_map`
- `memory_delta`
- `canon_delta`
- `next_pass_brief`

`inquiry_checkpoint` stays the verification artifact for this bridge.

This route should be read as checkpoint-and-relaunch evidence, not as final
answer grading.
`memory_delta` and `canon_delta` must remain distinct.

When the restart route also emits explicit return-aware artifacts,
`aoa-return-anchor-integrity` may travel as an adjacent diagnostic surface.
It remains narrower than `aoa-long-horizon-depth` and does not replace
checkpoint-and-relaunch reading.

## Hook surface

The schema-backed bridge surface for this seam is:

- `schemas/artifact-to-verdict-hook.schema.json`

The first derived examples are:

- `examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`
- `examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json`
- `examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json`

Runtime benchmark evidence selection is adjacent to this bridge, not a replacement for it.
See [RUNTIME_BENCH_PROMOTION_GUIDE.md](RUNTIME_BENCH_PROMOTION_GUIDE.md) when `abyss-stack` latency, load, recovery, or context-stress artifacts need bounded promotion discipline before they travel upward as selected proof inputs.
See [RECURRENCE_PROOF_PROGRAM.md](RECURRENCE_PROOF_PROGRAM.md) when the question is whether return-aware artifacts and runtime sidecars support a narrower anchor-integrity read.

These hook surfaces bind together:

- playbook-owned artifact inputs
- neighboring artifact contract refs
- the selected eval anchor bundle
- contract-test refs from that bundle
- the expected report shape
- optional trace sidecars

They are derived bridge metadata.
They are not a second proof canon and not a runtime judge implementation.

## Non-goals

- no secret internal judge
- no verdict logic in `aoa-agents`
- no final-text-only grading
- no MCP or A2A transport commitments
- no bundle maturity or status promotion

## Boundary to preserve

- `aoa-playbooks` remains authoritative for scenario composition and `eval_anchors`
- `aoa-agents` remains authoritative for runtime artifact contracts
- `aoa-memo` remains authoritative for `WitnessTrace` and `inquiry_checkpoint`
- `aoa-evals` remains authoritative for verdict meaning and interpretation

The bridge exists so those surfaces can meet without collapsing into one hidden
runtime monolith.
