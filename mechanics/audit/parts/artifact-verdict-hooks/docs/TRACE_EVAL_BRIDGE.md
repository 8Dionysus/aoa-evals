# Trace Eval Bridge

## Purpose

This document defines the bounded trace-and-eval bridge for `aoa-evals`.

It makes runtime artifacts and trace surfaces readable as evidence inputs for
existing eval bundles.
Verdict logic routes to `aoa-evals`; artifact production, scenario composition,
and runtime implementation route to their owning layers.

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

Neighbor owners retain:

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
Additional checkpoint-bundle pressure routes to the checkpoint mechanic and
bundle-local review.

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
Its current bounded proof flow is anchored in
`mechanics/proof-infra/parts/fixture-families/fixtures/tool-trajectory-bounded-v1/README.md`, bundle-local fixture and
runner contracts, and a schema-backed companion report artifact.

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
`mechanics/proof-infra/parts/fixture-families/fixtures/trace-outcome-bounded-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.
That sidecar stays on keeping outcome and path readable before any combined
reading.
Primary tool-path anchor pressure stays with `aoa-tool-trajectory-discipline`
for this route.

When a bounded route also exports `WitnessTrace`, that trace may travel as an
optional sidecar for `aoa-witness-trace-integrity`.
That sidecar is evidence-only.
Required-playbook-artifact pressure routes to `aoa-playbooks` before the bridge
can depend on it.
Its current draft public proof flow is anchored in
`mechanics/proof-infra/parts/fixture-families/fixtures/witness-trace-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.

When the route emits an explicit return decision, anchor refs, and bounded
re-entry note, `aoa-return-anchor-integrity` may travel as an adjacent
diagnostic surface.
That sidecar stays on anchor fidelity and honest re-entry.
Primary route-quality anchor pressure stays with `aoa-tool-trajectory-discipline`.

### `AOA-P-0009 restartable-inquiry-loop`

Use `aoa-long-horizon-depth` as the primary verdict anchor for the first
restartable inquiry bridge.
Its current draft proof flow is anchored in
`mechanics/checkpoint/parts/restartable-inquiry/fixtures/long-horizon-restart-v1/README.md`, bundle-local fixture and runner
contracts, and a schema-backed companion report artifact.

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
It remains narrower than `aoa-long-horizon-depth`.
Primary checkpoint-and-relaunch pressure stays with `aoa-long-horizon-depth`.

## Hook surface

The schema-backed bridge surface for this seam is:

- `mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json`

The first derived examples are:

- `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.local-stack-diagnosis.example.json`
- `mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`
- `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.validation-driven-remediation.example.json`
- `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.long-horizon-model-tier-orchestra.example.json`
- `mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json`
- `mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json`
- `mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.trace-integrity-chaos.example.json`

Runtime benchmark evidence selection is adjacent to this bridge; replacement
pressure routes through selected evidence review.
See [RUNTIME_BENCH_PROMOTION_GUIDE.md](../../selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md) when `abyss-stack` latency, load, recovery, or context-stress artifacts need bounded promotion discipline before they travel upward as selected proof inputs.
See [RECURRENCE_PROOF_PROGRAM.md](../../../../../mechanics/recurrence/docs/RECURRENCE_PROOF_PROGRAM.md) when the question is whether return-aware artifacts and runtime sidecars support a narrower anchor-integrity read.
See [TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md](TRACE_EVAL_BRIDGE_CHAOS_WAVE1.md) for the bounded chaos-wave variant where runtime stress lanes, re-entry gates, and witness sidecars remain weaker than owner-local receipts and later verdict review.

These hook surfaces bind together:

- playbook-owned artifact inputs
- neighboring artifact contract refs
- the selected eval anchor bundle
- contract-test refs from that bundle
- the expected report shape
- runtime policy boundary metadata for policy-sensitive hooks
- optional trace sidecars

They are derived bridge metadata.
Runtime-produced hook packets remain review candidates until `aoa-evals` confirms their bounded use against the owning eval bundle.
Proof-canon pressure routes to the owning eval bundle; runtime-judge
implementation pressure routes to the runtime owner.

Policy-sensitive hooks must name a `runtime_policy_boundary` object. That
object records which hook artifacts are authorization, approval, or
fallback/rollback evidence and keeps these stop-lines explicit:

- the hook does not grant tool permission;
- the hook does not prove runtime policy enforcement;
- the hook does not replace runtime owner approval;
- the hook does not prove cost or time cap compliance.

This is metadata for eval review, not a runtime policy engine.

When a bounded verdict later needs one machine-readable publication sidecar,
use [EVAL_RESULT_RECEIPT_GUIDE.md](../../../../../mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md).
That seam records publication facts and stays weaker than bundle-local proof
meaning.

## Authority Routes

| Pressure | Route |
| --- | --- |
| secret internal judge | public eval bundle, scorer, runner, and report contract |
| verdict logic in `aoa-agents` | `aoa-evals` verdict owner |
| final-text-only grading | trace/outcome separated evidence route |
| MCP or A2A transport commitment | transport owner route before proof adoption |
| bundle maturity or status promotion | bundle-local review plus root audit gate |

## Boundary to preserve

- `aoa-playbooks` remains authoritative for scenario composition and `eval_anchors`
- `aoa-agents` remains authoritative for runtime artifact contracts
- `aoa-memo` remains authoritative for `WitnessTrace` and `inquiry_checkpoint`
- `aoa-evals` remains authoritative for verdict meaning and interpretation

The bridge lets those surfaces meet through visible handoffs and reviewable
evidence.
