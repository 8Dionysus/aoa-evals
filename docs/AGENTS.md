# AGENTS.md

## Applies to

`docs/` source guidance, docs maps, durable reference docs, and docs-local
decision records unless a deeper `AGENTS.md` applies.

## Role

`docs/` explains eval philosophy, comparison posture, trace seams,
repeated-window discipline, shared proof infrastructure, proof topology, legacy
naming posture, and documentation wayfinding.

It may clarify proof meaning. Specific eval claims keep authority in
bundle-local `EVAL.md` and `eval.yaml`.

## Operating Card

| Field | Route |
| --- | --- |
| role | docs guidance, topology, proof-guide, and wayfinding district |
| input | proof questions, route questions, topology changes, guide lookup, and durable docs edits |
| output | next source surface, topology explanation, proof guide, or decision route |
| owner | target doc for its meaning; nearest `AGENTS.md` for edit and validation route |
| next route | `docs/README.md`, `docs/architecture/AGENT_INDEX.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `docs/decisions/`, mechanics, or bundle-local proof |
| tools | root validator, semantic AGENTS validator, and generated-reader builders when route maps touch derived surfaces |
| validation | this card's `Validation` section |

## Surface Split

- `docs/README.md` is a route map. Keep it link-driven and reader-oriented.
- `docs/architecture/AGENT_INDEX.md` is an agent-facing pass-through index. Keep it weaker
  than source truth, route cards, decisions, generated readers, and validators.
- `docs/architecture/PROOF_TOPOLOGY.md`, `docs/architecture/ARCHITECTURE.md`, and proof guides may carry
  source meaning about authority classes, review posture, and proof limits.
- `docs/decisions/` owns durable rationale; follow `docs/decisions/AGENTS.md`
  there.
- Operational edit law, mutation posture, and local verification expectations
  belong in the nearest `AGENTS.md`, not hidden inside ordinary guide prose.

## Read Before Editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md` when agent-facing guidance shape changes
4. the target doc
5. `EVAL_INDEX.md` and `EVAL_SELECTION.md` when public routing changes
6. the affected bundle when a doc changes bundle interpretation

## Owner Routes

| Need | Owner route |
| --- | --- |
| specific eval claim | bundle-local `EVAL.md` and `eval.yaml` |
| generated reader truth | `generated/AGENTS.md`, builder, and source inputs |
| runtime, trace, receipt, sibling, recurrence, or checkpoint interpretation | owning mechanic, source surface, or sibling owner before bundle-local review |
| decision rationale | `docs/decisions/AGENTS.md` and the source surface being explained |
| roadmap direction | root `ROADMAP.md` |
| mechanics topology | `mechanics/AGENTS.md`, `mechanics/README.md`, and the target package card |

## Route Rules

- Keep anti-overread language sharp: bounded evals are not total intelligence
  scores, general safety claims, or universal readiness proofs.
- Keep generated readers weaker than authored source docs and bundle-local proof.
- Keep runtime, trace, receipt, sibling, recurrence, and checkpoint surfaces below
  bundle-local review unless an owning source surface explicitly accepts a
  bounded interpretation.
- Keep docs-map cleanup separate from decision rationale, roadmap direction, and
  mechanics topology unless the same slice intentionally updates those owners.

## Validation

Verify docs-only route and meaning changes with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

When docs-map changes touch public eval readers, generated report indexes,
runtime-candidate readers, or boundary-bridge matrices, add the relevant
non-mutating checks:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python -m pytest -q
```

For mechanic-owned payload docs, use `mechanics/AGENTS.md` and the package card
before broadening to the root route.

## Closeout

Report which doc surface changed, which proof meaning or route map it owns,
whether bundle-local meaning changed, and which validation ran.
