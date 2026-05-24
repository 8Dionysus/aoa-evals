# Self-Agent Checkpoint Eval Posture

## Purpose

This note defines the explicit eval-side landing for the first-wave
`aoa-self-agent-checkpoint` seed.

It explains how `AOA-P-0006 self-agent-checkpoint-rollout` is read through
existing bounded eval bundles.
Checkpoint-only proof-canon pressure routes back to stronger owners.

## Core rule

Self-agent checkpoint work is evaluated through existing bounded proof surfaces.

`aoa-evals` may read checkpoint artifacts as evidence.

| Pressure | Owner route |
| --- | --- |
| self-agent contract meaning | `aoa-agents` |
| scenario composition | `aoa-playbooks` |
| checkpoint memory objects | `aoa-memo` |

## Route-level reading

For `AOA-P-0006`, keep two bounded reads distinct:

- `aoa-approval-boundary-adherence` is the primary gate-and-authority read
- `aoa-bounded-change-quality` is the companion route-quality read

This keeps approval posture and workflow posture legible while sovereign-bundle
pressure routes back to the checkpoint owner split.

## Hook surface

The current explicit hook surface is:

- `mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`

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
Checkpoint ontology pressure routes to Agents-of-Abyss checkpoint doctrine.

## Boundary to preserve

- `aoa-agents` remains authoritative for `SELF_AGENT_CHECKPOINT_STACK` and the
  self-agent checkpoint schema
- `aoa-playbooks` remains authoritative for `AOA-P-0006`
- `aoa-memo` remains authoritative for checkpoint writeback and memory objects
- `aoa-evals` remains authoritative for bounded proof wording
