# Checkpoint / Self-Agent Posture Part

## Role

This part owns the eval-side reading route for self-agent checkpoint posture.

It keeps the posture note and approval-boundary hook example together under
the checkpoint mechanic while checkpoint-only proof-canon pressure routes to
stronger owners.

## Source Surfaces

- `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`
- `evals/boundary/aoa-approval-boundary-adherence/EVAL.md`
- `evals/workflow/aoa-bounded-change-quality/EVAL.md`

## Inputs

- approval records;
- rollback markers;
- health checks;
- improvement logs;
- self-agent checkpoint owner refs;
- playbook and memo checkpoint refs.

## Outputs

- bounded approval and route-quality proof readings;
- one artifact-to-verdict hook example for audit candidate readers;
- owner handoff route when checkpoint posture evidence belongs to agents,
  playbooks, or memo.

## Stronger Owner Split

`aoa-agents` owns self-agent checkpoint contracts, approval, rollback, health,
and role boundaries. `aoa-playbooks` owns scenario composition and rollout
choreography. `aoa-memo` owns checkpoint writeback and memory objects.
`Agents-of-Abyss` owns checkpoint law and vocabulary.

`aoa-evals` owns bounded approval-boundary and route-quality proof readings
from checkpoint artifacts, plus the part-local posture note and hook example.
Authority beyond that proof reading routes through the stronger owner split
above.

## Stop-Lines

Boundary routes keep self-agent checkpoint pressure with the owner that can act
on it:

| Pressure | Owner route |
| --- | --- |
| self-agent checkpoint contract meaning pressure | `aoa-agents` self-agent route |
| scenario composition pressure | `aoa-playbooks` scenario route |
| checkpoint writeback authority pressure | `aoa-memo` checkpoint writeback route |
| checkpoint ontology pressure | Agents-of-Abyss checkpoint doctrine route |
| sovereign checkpoint proof-canon pressure | Agents-of-Abyss doctrine plus bundle-local proof route |
| owner acceptance or runtime activation pressure | owner repository acceptance route plus `abyss-stack` runtime route |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
