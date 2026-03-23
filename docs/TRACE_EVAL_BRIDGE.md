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

When a bounded route also exports `WitnessTrace`, that trace may travel as an
optional sidecar for `aoa-witness-trace-integrity`.
That sidecar is evidence-only.
It does not silently add a required playbook artifact.

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

## Hook surface

The schema-backed bridge surface for this seam is:

- `schemas/artifact-to-verdict-hook.schema.json`

The first derived examples are:

- `examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json`
- `examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json`

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
