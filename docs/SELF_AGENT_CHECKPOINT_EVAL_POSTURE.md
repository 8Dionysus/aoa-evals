# Self-Agent Checkpoint Eval Posture

## Purpose

This note defines the explicit eval-side landing for the first-wave
`aoa-self-agent-checkpoint` seed.

It explains how `AOA-P-0006 self-agent-checkpoint-rollout` is read through
existing bounded eval bundles.
It does not introduce a new checkpoint-only proof canon.

## Core rule

Self-agent checkpoint work is evaluated through existing bounded proof surfaces.

`aoa-evals` may read checkpoint artifacts as evidence.
It does not become the owner of:

- self-agent contract meaning in `aoa-agents`
- scenario composition in `aoa-playbooks`
- checkpoint memory objects in `aoa-memo`

## Route-level reading

For `AOA-P-0006`, keep two bounded reads distinct:

- `aoa-approval-boundary-adherence` is the primary gate-and-authority read
- `aoa-bounded-change-quality` is the companion route-quality read

This keeps approval posture and workflow posture legible without inventing a
new sovereign bundle that tries to own the whole checkpoint stack.

## Hook surface

The current explicit hook surface is:

- `examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`

That hook keeps the route bounded to:

- `approval_record`
- `rollback_marker`
- `health_check`
- `improvement_log`

`approval_record` remains the verification artifact for the primary approval
read.

## Artifact mapping posture

Use the current artifacts like this:

- `approval_record` shows whether the route stayed honest about approval gates
- `rollback_marker` shows whether reversal posture was explicit before mutation
- `health_check` shows whether the route exposed a real post-change boundedness read
- `improvement_log` shows whether the route preserved reviewable follow-up history

These artifacts are evidence inputs.
They are not a new checkpoint ontology inside `aoa-evals`.

## Boundary to preserve

- `aoa-agents` remains authoritative for `SELF_AGENT_CHECKPOINT_STACK` and the
  self-agent checkpoint schema
- `aoa-playbooks` remains authoritative for `AOA-P-0006`
- `aoa-memo` remains authoritative for checkpoint writeback and memory objects
- `aoa-evals` remains authoritative only for bounded proof wording
