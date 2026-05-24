# Checkpoint / A2A Summon Return Part

## Role

This part owns the support route for
`aoa-a2a-summon-return-checkpoint`.

It keeps the public-safe fixture family, artifact-to-verdict hook example, and
seeded validation test together under the checkpoint mechanic while the source
proof bundle stays under `evals/`.

## Source Surfaces

- `evals/workflow/aoa-a2a-summon-return-checkpoint/EVAL.md`
- `mechanics/checkpoint/parts/a2a-summon-return/fixtures/a2a-summon-return-checkpoint-v1/README.md`
- `mechanics/checkpoint/parts/a2a-summon-return/examples/artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json`
- `mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py`

## Inputs

- summon requests and decisions;
- Codex-local target records;
- reviewed child task results;
- return plans and checkpoint bridge plans;
- memo writeback candidates and runtime dry-run receipt contracts.

## Outputs

- bounded A2A summon return checkpoint proof readings;
- one fixture family contract;
- one artifact-to-verdict hook example for audit candidate readers;
- owner handoff route when summon return evidence requires local execution or
  acceptance.

## Stronger Owner Split

`Agents-of-Abyss` owns checkpoint doctrine. `aoa-sdk` owns A2A checkpoint
controls, bridge plans, and summon return helper contracts. `aoa-skills` owns
summon and closeout skill truth. `aoa-memo` owns memo writeback acceptance.
`abyss-stack` owns runtime closeout execution after runtime gates. Owner
repositories own child-output acceptance.

`aoa-evals` owns the bounded A2A summon return checkpoint proof reading: proof
wording, the part-local fixture family, hook example, seeded validation test,
and bundle-local interpretation for `aoa-a2a-summon-return-checkpoint`.
Authority beyond that proof reading routes through the stronger owner split
above.

## Stop-Lines

Boundary routes keep A2A summon-return pressure with the owner that can act on
it:

| Pressure | Owner route |
| --- | --- |
| checkpoint doctrine pressure | Agents-of-Abyss center route |
| A2A control-plane implementation pressure | `aoa-sdk` A2A checkpoint-control route |
| summon skill truth pressure | `aoa-skills` summon and closeout skill route |
| memo canon or memo writeback acceptance pressure | `aoa-memo` writeback route |
| live runtime execution or runtime closeout authority pressure | `abyss-stack` runtime route |
| owner acceptance or final child-output quality pressure | owner repository child-output acceptance route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
