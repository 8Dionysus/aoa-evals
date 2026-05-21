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

`aoa-evals` owns only bounded A2A summon return checkpoint proof wording, the
part-local fixture family, hook example, seeded validation test, and
bundle-local interpretation for `aoa-a2a-summon-return-checkpoint`.

## Stop-Lines

This part must not claim:

- checkpoint doctrine;
- A2A control-plane implementation;
- summon skill truth;
- memo canon or memo writeback acceptance;
- live runtime execution or runtime closeout authority;
- owner acceptance or final child-output quality.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
