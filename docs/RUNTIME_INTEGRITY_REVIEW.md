# Runtime Integrity Review

This document defines the owner-local review contract for W10-shaped runtime
continuity evidence entering `aoa-evals`.

Use it when runtime continuity artifacts look meaningful enough to review, but
still must remain weaker than proof canon, weaker than activation authority,
and weaker than the center owner split.

See also:
- [Documentation Map](README.md)
- [Trace Eval Bridge](TRACE_EVAL_BRIDGE.md)
- [Runtime Bench Promotion Guide](RUNTIME_BENCH_PROMOTION_GUIDE.md)
- [Self-Agent Checkpoint Eval Posture](SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md)

## Core rule

`aoa-evals` may host one owner-local runtime integrity review surface.

Its status stays `candidate_only`.
Its `human_review_needed` flag stays `true`.
Its `budget_ref` points upward to the Experience continuity-context owner split rather than
defining new budget law locally.

It does not become proof canon.
It does not activate runtime continuity.

## Required contract surface

The review surface keeps these fields explicit:

- `budget_ref`
- `evidence_refs`
- `replay_requirements`
- `human_review_needed`
- `forbidden_claims`

The machine-readable contract lives in:

- `schemas/runtime-integrity-review.schema.json`
- `examples/runtime_integrity_review.example.json`

## Evidence posture

The review may gather bounded evidence from adjacent owner surfaces such as:

- `aoa-routing` live-session reentry review
- `aoa-agents` self-agency continuity lane
- `aoa-memo` inquiry checkpoint and continuity writeback boundary
- local `aoa-evals` bridge and promotion guides

That evidence stays selected and replay-bounded.
It is not a free-form license to treat runtime artifacts as finished verdicts.

## Replay requirements

`replay_requirements` must preserve all of the following:

- selected evidence only
- owner-local replay before publication
- fail-closed posture
- publication remains review-required

Dry-run receipts, route hints, or helper exports may support review.
They do not replace replay and they do not mint a sealed verdict.

## Boundary to preserve

The review surface must explicitly refuse these authority jumps:

- `sealed_verdict`
- `activation_authority`
- `owner_override`
- `canon_write`

The review stays weaker than the W10 center contract.
It stays weaker than future runtime-owner implementation work.
It stays weaker than bundle-local proof meaning.

## Non-goals

- no runtime self-authorization
- no hidden owner override
- no canon write through eval review
- no proof-family promotion by receipt accumulation
- no collapse of routing, memo, and eval meaning into one runtime judge
