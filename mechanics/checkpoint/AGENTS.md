# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/checkpoint/DIRECTION.md` for current operating direction, `mechanics/checkpoint/PARTS.md` for active parts, and `mechanics/checkpoint/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/checkpoint/` and checkpoint-owned part-local support surfaces.

## Role

This package routes checkpoint proof work inside `aoa-evals`.

It maps eval-side checkpoint pressure to part-local fixtures, hook examples,
posture docs, generated candidate readers, bundle-local review, or
stronger-owner handoff routes.

## Operating Card

| Field | Route |
| --- | --- |
| role | checkpoint proof work route inside `aoa-evals` |
| input | checkpoint fixture, hook example, posture doc, candidate-only evidence, generated reader change, or checkpoint owner question |
| output | active part route, audit hook/candidate route, bundle-local review, or stronger-owner handoff |
| owner | `aoa-evals` owns bounded checkpoint proof support; stronger owners keep doctrine, SDK controls, skill workflows, role policy, memory, runtime exports, routing, playbooks, stats, and artifact promotion |
| next route | `mechanics/checkpoint/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, `mechanics/audit/`, and source proof bundle |
| tools | part-local pytest, runtime candidate builders, catalog builder, root validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `docs/architecture/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/checkpoint/README.md`
6. `mechanics/checkpoint/PARTS.md`
7. target part `README.md`
8. `mechanics/checkpoint/PROVENANCE.md` as the active-to-archive bridge for old placement or raw lineage
9. `mechanics/audit/parts/artifact-verdict-hooks/README.md` when hook examples
   or candidate readers change

## Route Rules

- Keep source proof bundles under `evals/`.
- Keep checkpoint support artifacts part-local when a checkpoint part owns their
  fixture, hook example, posture doc, or validation route.
- Keep artifact-to-verdict hook schema and generated candidate readers under
  `mechanics/audit/`.
- Keep checkpoint hook examples candidate-only until bundle-local review
  accepts the evidence.
- Create checkpoint parts from a multi-surface checkpoint proof operation with
  validator coverage.

## Validation

```bash
python -m pytest -q mechanics/checkpoint/parts/a2a-summon-return/tests/test_a2a_summon_return_checkpoint_fixture.py
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check
python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```

## Closeout

Report which checkpoint proof route changed, which owner truth stayed stronger,
which generated surfaces were refreshed, and which checkpoint family remains
deferred or bundle-local.
