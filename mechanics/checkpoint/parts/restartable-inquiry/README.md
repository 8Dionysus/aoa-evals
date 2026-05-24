# Checkpoint / Restartable Inquiry Part

## Role

This part owns the support route for checkpoint-and-relaunch proof in
`aoa-long-horizon-depth`.

It keeps the long-horizon restart fixture family and restartable-inquiry hook
example under the checkpoint mechanic while the source proof bundle stays under
`evals/`.

## Source Surfaces

- `evals/workflow/aoa-long-horizon-depth/EVAL.md`
- `mechanics/checkpoint/parts/restartable-inquiry/fixtures/long-horizon-restart-v1/README.md`
- `mechanics/checkpoint/parts/restartable-inquiry/examples/artifact_to_verdict_hook.restartable-inquiry-loop.example.json`

## Inputs

- inquiry checkpoints;
- decision ledgers;
- contradiction maps;
- memory and canon deltas;
- next-pass briefs and relaunch readouts.

## Outputs

- bounded checkpoint-and-relaunch proof readings;
- one fixture family contract;
- one artifact-to-verdict hook example for audit candidate readers;
- owner handoff route when relaunch evidence depends on memo, playbook, or
  canon truth.

## Stronger Owner Split

`Agents-of-Abyss` owns checkpoint law and long-horizon posture. `aoa-memo`
owns memo checkpoint schemas, memory objects, recall anchors, and writeback
contracts. `aoa-playbooks` owns restartable-inquiry choreography. The owner
repository owns canon meaning, raw transcript continuity, and final inquiry
truth.

`aoa-evals` owns the bounded checkpoint-and-relaunch proof reading: proof
wording, the part-local restart fixture, hook example, and bundle-local
interpretation for `aoa-long-horizon-depth`. Authority beyond that proof
reading routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep restartable-inquiry pressure with the owner that can act
on it:

| Pressure | Owner route |
| --- | --- |
| memo checkpoint schema authority pressure | `aoa-memo` checkpoint schema route |
| playbook choreography ownership pressure | `aoa-playbooks` restartable-inquiry route |
| canon meaning pressure | owner repository canon route |
| raw transcript continuity pressure | owner repository transcript route |
| final inquiry truth or final-answer grading pressure | owner repository inquiry acceptance route |
| broad long-horizon competence pressure | bundle-local proof object plus source-owner evidence review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
