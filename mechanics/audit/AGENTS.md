# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/audit/DIRECTION.md` for current operating direction, `mechanics/audit/PARTS.md` for active parts, and `mechanics/audit/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/audit/` and the runtime evidence intake route.

## Role

This package protects the candidate-evidence loop:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/audit/README.md`
7. `mechanics/audit/PARTS.md`
8. `mechanics/audit/parts/README.md`
9. `mechanics/audit/parts/selected-evidence-packets/docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`
10. `mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md`
11. `mechanics/audit/parts/artifact-verdict-hooks/docs/TRACE_EVAL_BRIDGE.md`
12. `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json`
13. `mechanics/audit/parts/artifact-verdict-hooks/schemas/artifact-to-verdict-hook.schema.json`
14. `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py`
15. `mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py`
16. `docs/decisions/0007-audit-mechanic-package.md`

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
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report whether the change touched runtime evidence examples, artifact hooks,
schemas, generated readers, review docs, accepted legacy names, or stronger
owner boundaries.
