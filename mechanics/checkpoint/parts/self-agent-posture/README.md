# Self-Agent Posture Part

## Role

This part owns the eval-side reading route for self-agent checkpoint posture.

It keeps the posture note and approval-boundary hook example together under
the checkpoint mechanic without creating a new checkpoint-only proof canon.

## Source Surfaces

- `mechanics/checkpoint/parts/self-agent-posture/docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`
- `mechanics/checkpoint/parts/self-agent-posture/examples/artifact_to_verdict_hook.self-agent-checkpoint-rollout.example.json`
- `bundles/aoa-approval-boundary-adherence/EVAL.md`
- `bundles/aoa-bounded-change-quality/EVAL.md`

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

`aoa-evals` owns only bounded approval-boundary and route-quality proof
readings from checkpoint artifacts, plus the part-local posture note and hook
example.

## Stop-Lines

This part must not claim:

- `aoa-agents` self-agent checkpoint contract meaning;
- `aoa-playbooks` scenario composition;
- `aoa-memo` checkpoint writeback authority;
- checkpoint ontology;
- sovereign checkpoint proof canon;
- owner acceptance or runtime activation.

## Validation

Payload coverage anchor: `mechanics/checkpoint/parts/self-agent-posture/`.

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python scripts/validate_repo.py
```
