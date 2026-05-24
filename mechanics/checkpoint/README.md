# Checkpoint Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/checkpoint/` routes bounded proof work for checkpoint return,
restartable inquiry, and self-agent checkpoint posture inside `aoa-evals`.

It receives checkpoint pressure as reviewable evidence, hook examples, bridge
plans, or support surfaces, then routes the work to a part-local review,
bundle-local interpretation, or owner handoff.

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
- owner handoff routes for implementation, memory, runtime, owner acceptance,
  scheduler, self-repair, child-output, and long-horizon competence pressure.

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

Boundary routes keep checkpoint proof pressure with the owner that can act on
it:

| Pressure | Owner route |
| --- | --- |
| checkpoint implementation authority pressure | Agents-of-Abyss law route plus `aoa-sdk` checkpoint-control route |
| memory canon or recall sovereignty pressure | `aoa-memo` memory route |
| live runtime activation pressure | `abyss-stack` runtime route |
| owner acceptance or promotion pressure | owner repository acceptance route |
| hidden scheduler behavior pressure | `aoa-playbooks` choreography route plus `abyss-stack` runtime route |
| autonomous self-repair pressure | `aoa-agents` role, approval, rollback, and health route |
| final child-output quality pressure | owner repository child-output acceptance route |
| broad long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge when old root fixture, doc, hook, or
test placement must be audited. New checkpoint proof work starts from this
README, [PARTS.md](PARTS.md), and the active parts.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this mechanic before changing A2A summon-return support, restartable
inquiry support, self-agent checkpoint posture, checkpoint hook examples, or
candidate audit bridges that feed checkpoint proof review.

For SDK controls, memory objects, runtime exports, routing behavior, or
playbook choreography, follow the stronger owner named in this package before
changing eval-side proof support.
