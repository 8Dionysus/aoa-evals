# AGENTS.md

## Applies to

`mechanics/runtime-evidence/` and the runtime evidence intake route.

## Role

This package protects the candidate-evidence loop:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/runtime-evidence/README.md`
7. `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
8. `docs/RUNTIME_INTEGRITY_REVIEW.md`
9. `docs/TRACE_EVAL_BRIDGE.md`
10. `schemas/runtime-evidence-selection.schema.json`
11. `schemas/artifact-to-verdict-hook.schema.json`
12. `scripts/generate_runtime_candidate_template_index.py`
13. `scripts/generate_runtime_candidate_intake.py`
14. `docs/decisions/0007-runtime-evidence-mechanic-package.md`

## Boundaries

- Do not treat runtime evidence as accepted proof before bundle-local review.
- Do not hand-edit generated runtime candidate readers.
- Do not include raw private logs, secrets, or host fingerprints in public
  examples.
- Do not let `abyss-stack` evidence become eval verdict authority.
- Do not turn artifact-to-verdict hooks into a runtime judge implementation.
- Do not widen candidate evidence into global capability, safety, intelligence,
  or agent-quality ranking.

## Validation

Run:

```bash
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report whether the change touched runtime evidence examples, artifact hooks,
schemas, generated readers, review docs, accepted legacy names, or stronger
owner boundaries.
