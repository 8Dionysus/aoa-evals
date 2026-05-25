# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/audit/DIRECTION.md` for current operating direction, `mechanics/audit/PARTS.md` for active parts, and `mechanics/audit/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/audit/` and the runtime evidence intake route.

## Role

This package protects the candidate-evidence loop:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

## Operating Card

| Field | Route |
| --- | --- |
| role | audit candidate-evidence loop for runtime and trace artifacts |
| input | runtime or trace artifact, selected evidence packet, artifact-to-verdict hook, runtime candidate reader drift, schema change, or stronger-owner evidence question |
| output | selected evidence route, generated reader check, bundle-local review handoff, integrity review, or stronger-owner handoff |
| owner | `aoa-evals` owns candidate evidence routing; runtime owners keep runtime truth and bundle-local review owns accepted proof |
| next route | `mechanics/audit/README.md`, `DIRECTION.md`, `PARTS.md`, affected part docs/schemas/scripts, and affected source bundle |
| tools | candidate reader builders, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
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

## Route Rules

- Keep runtime evidence candidate-scoped until bundle-local review accepts it.
- Rebuild generated runtime candidate readers from their source surfaces.
- Keep raw private logs, secrets, and host fingerprints out of public examples.
- Route `abyss-stack` evidence through eval review before verdict adoption.
- Keep artifact-to-verdict hooks as review metadata, below runtime judge
  implementation.
- Keep candidate evidence bounded to its local claim instead of global
  capability, safety, intelligence, or agent-quality ranking.

## Validation

Run:

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

If source examples changed and generated readers are intentionally refreshed,
rebuild them before rerunning the checks:

```bash
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py
```

## Closeout

Report whether the change touched runtime evidence examples, artifact hooks,
schemas, generated readers, review docs, accepted legacy names, or stronger
owner boundaries.
