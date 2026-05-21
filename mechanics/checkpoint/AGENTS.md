# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/checkpoint/DIRECTION.md` for current operating direction, `mechanics/checkpoint/PARTS.md` for active parts, and `mechanics/checkpoint/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/checkpoint/` and checkpoint-owned part-local support surfaces.

## Role

This package routes checkpoint proof work inside `aoa-evals`.

It does not own checkpoint doctrine, SDK controls, skill workflow truth,
self-agent role policy, memory objects, runtime exports, routing behavior,
playbook choreography, stats visibility, or owner artifact promotion.

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/checkpoint/README.md`
6. `mechanics/checkpoint/PARTS.md`
7. target part `README.md`
8. `mechanics/checkpoint/PROVENANCE.md` only for old placement or raw lineage
9. `mechanics/audit/parts/artifact-verdict-hooks/README.md` when hook examples
   or candidate readers change

## Boundaries

- Keep source proof bundles under `bundles/`.
- Keep checkpoint support artifacts part-local when a checkpoint part owns their
  fixture, hook example, posture doc, or validation route.
- Keep artifact-to-verdict hook schema and generated candidate readers under
  `mechanics/audit/`.
- Keep checkpoint hook examples candidate-only until bundle-local review
  accepts the evidence.
- Do not create new checkpoint parts from one document, one report, or one
  hook form.

## Validation

```bash
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
```

## Closeout

Report which checkpoint proof route changed, which owner truth stayed stronger,
which generated surfaces were refreshed, and which checkpoint family remains
deferred or bundle-local.
