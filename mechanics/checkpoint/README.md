# Checkpoint Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Owned Operation

`mechanics/checkpoint/` owns the eval-side checkpoint proof operation:

`checkpoint pressure -> bounded checkpoint proof question -> part-local support surface -> bundle-local review -> bounded report or owner handoff`

This package is AoA-aligned. It keeps the parent name `checkpoint` because the
operation materializes the center checkpoint mechanic on the proof side.

## Source Surfaces

- `evals/workflow/aoa-a2a-summon-return-checkpoint/EVAL.md`
- `evals/workflow/aoa-long-horizon-depth/EVAL.md`
- `mechanics/checkpoint/parts/a2a-summon-return/README.md`
- `mechanics/checkpoint/parts/restartable-inquiry/README.md`
- `mechanics/checkpoint/parts/self-agent-posture/README.md`
- `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`

## Parts

See [PARTS.md](PARTS.md).

The current active parts are `a2a-summon-return`,
`restartable-inquiry`, and `self-agent-posture`.

## Inputs

- checkpoint bridge plans, return plans, inquiry checkpoints, reviewed child
  results, memo writeback candidates, approval records, rollback markers,
  health checks, improvement logs, dry-run runtime receipts, and owner-source
  refs;
- selected artifact-to-verdict hook examples that stay below bundle-local
  review;
- source proof bundles that explicitly name checkpoint proof boundaries.

## Outputs

- bounded checkpoint proof readings;
- checkpoint fixture family contracts;
- artifact-to-verdict hook candidates for audit candidate readers;
- owner handoff notes or adjacent bundle route notes;
- no checkpoint implementation, memory canon, runtime activation, or owner
  acceptance.

## Stronger Owner Split

`Agents-of-Abyss` owns checkpoint law, vocabulary, owner map, and stop-lines.
`aoa-sdk` owns checkpoint controls, A2A helpers, local ledgers, and context
builders.
`aoa-skills` owns checkpoint-note and closeout-bridge skill truth.
`aoa-agents` owns self-agent checkpoint posture, approval, rollback, health,
and role boundaries.
`aoa-memo` owns inquiry checkpoints, memory objects, recall anchors, and
checkpoint-to-memory writeback.
`aoa-playbooks` owns recurring checkpoint choreography.
`abyss-stack` owns runtime checkpoint exports and dry-run or live runtime
plumbing after runtime gates.
`aoa-routing` owns re-entry hints without checkpoint meaning.

`aoa-evals` owns bounded checkpoint proof wording, regression readings, report
interpretation, and local support-surface validation.

## Stop-Lines

Do not use this package to claim:

- checkpoint implementation authority;
- memory canon or recall sovereignty;
- live runtime activation;
- owner acceptance or promotion;
- hidden scheduler behavior;
- autonomous self-repair;
- final child-output quality;
- broad long-horizon competence.

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) only when old root fixture, doc, hook, or
test placement must be audited. New checkpoint proof work starts from this
README, [PARTS.md](PARTS.md), and the active parts.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.
