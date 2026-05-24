# Runtime Integrity Review

This document defines the owner-local review contract for W10-shaped runtime
continuity evidence entering `aoa-evals`.

Use it when runtime continuity artifacts look meaningful enough to review, but
still need a candidate route before proof canon, activation authority, or the
center owner split can act.

See also:
- [Documentation Map](../../../../../docs/README.md)
- [Trace Eval Bridge](../../artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md)
- [Runtime Bench Promotion Guide](../../selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md)
- [Self-Agent Checkpoint Eval Posture](../../../../../mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md)

## Core rule

`aoa-evals` may host one owner-local runtime integrity review surface.

Its status stays `candidate_only`.
Its `human_review_needed` flag stays `true`.
Its `budget_ref` points upward to the Experience continuity-context owner split rather than
defining new budget law locally.

Proof-canon pressure routes to bundle-local proof review.
Runtime-continuity activation pressure routes to Experience and runtime-owner
gates.

## Required contract surface

The review surface keeps these fields explicit:

- `budget_ref`
- `evidence_refs`
- `replay_requirements`
- `human_review_needed`
- `forbidden_claims`

The machine-readable contract lives in:

- `mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json`
- `mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json`

## Evidence posture

The review may gather bounded evidence from adjacent owner surfaces such as:

- `aoa-routing` live-session reentry review
- `aoa-agents` self-agency continuity lane
- `aoa-memo` inquiry checkpoint and continuity writeback boundary
- local `aoa-evals` bridge and promotion guides

That evidence stays selected and replay-bounded.
Finished-verdict pressure routes to the owning eval bundle and reviewer.

## Replay requirements

`replay_requirements` must preserve all of the following:

- selected evidence only
- owner-local replay before publication
- fail-closed posture
- publication remains review-required

Dry-run receipts, route hints, or helper exports may support review.
Replay remains required, and sealed verdict pressure routes to bundle-local
proof review.

## Boundary to preserve

The review surface must explicitly refuse these authority jumps:

- `sealed_verdict`
- `activation_authority`
- `owner_override`
- `canon_write`

The review stays candidate-scoped until the W10 center contract,
runtime-owner implementation route, or bundle-local proof owner accepts the
next step.

## Authority Routes

| Pressure | Route |
| --- | --- |
| runtime self-authorization | runtime owner plus Experience owner gate |
| owner override | the named owner repo and review surface |
| canon write through eval review | `aoa-memo` canon route or the owning canon surface |
| proof-family promotion by receipt accumulation | bundle-local proof review with cited evidence |
| routing, memo, and eval meaning collapse into one runtime judge | keep routing in `aoa-routing`, memory in `aoa-memo`, and proof in `aoa-evals` |
