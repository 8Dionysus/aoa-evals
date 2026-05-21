# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/agon/DIRECTION.md` for current operating direction, `mechanics/agon/PARTS.md` for active parts, and `mechanics/agon/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/agon/` and all Agon mechanic parts.

## Role

This package protects the local Agon proof-alignment loop:

`part source -> generated registry -> candidate-only check -> observe-only recurrence signal -> bundle-local review or owner handoff`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/LEGACY_NAMING.md`
6. `mechanics/README.md`
7. `mechanics/agon/README.md`
8. `mechanics/agon/PARTS.md`
9. `mechanics/agon/PROVENANCE.md` when legacy or former root paths are involved
10. the target part docs, config, schemas, scripts, tests, and manifests
11. `mechanics/agon/docs/AGON_EVAL_OWNER_HANDOFFS.md`
12. `mechanics/agon/docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`
13. `evals/boundary/aoa-recurrence-control-plane-integrity/EVAL.md` when recurrence
    review posture changes
14. `docs/decisions/0016-agon-mechanic-package.md`

## Boundaries

- Treat `mechanics/agon/` as the parent mechanic and `parts/*` as owned
  artifact families.
- Keep part-local source config stronger than generated registry output.
- Keep part-local builders and validators with the artifacts they build and
  validate.
- Keep Agents-of-Abyss law stronger than local eval alignment wording.
- Keep recurrence manifests and hooks observe-only.
- Keep quest source records under `quests/` unless the questbook mechanic moves
  them with source-path compatibility.
- Do not grant live verdict, closure, summon, memory write, rank mutation, KAG
  promotion, Tree of Sophia promotion, hidden scheduler, or arena authority.
- Preserve explicit stop-line tokens such as `no_live_verdict`,
  `no_closure_grant`, `no_live_summon`, `no_durable_memory_write`,
  `no_rank_mutation`, and `no_tree_of_sophia_promotion`.
- Do not weaken Agon stop-lines to make a registry pass.

## Validation

Run the touched part builder, validator, and test first. For a full Agon pass:

```bash
python mechanics/agon/parts/court-prebinding/scripts/build_agon_eval_prebinding_registry.py --check
python mechanics/agon/parts/ccs-alignment/scripts/build_agon_ccs_eval_alignment_registry.py --check
python mechanics/agon/parts/vds-alignment/scripts/build_agon_vds_eval_alignment_registry.py --check
python mechanics/agon/parts/retention-rank-alignment/scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python mechanics/agon/parts/mechanical-trial-suites/scripts/build_agon_mechanical_trial_eval_suites.py --check
python mechanics/agon/parts/epistemic-alignment/scripts/build_agon_epistemic_eval_alignment_registry.py --check
python mechanics/agon/parts/slc-alignment/scripts/build_agon_slc_eval_alignment_registry.py --check
python mechanics/agon/parts/kag-alignment/scripts/build_agon_kag_eval_alignment_registry.py --check
python mechanics/agon/parts/sophian-threshold-alignment/scripts/build_agon_sophian_eval_alignment_registry.py --check
python mechanics/agon/parts/court-prebinding/scripts/validate_agon_eval_prebindings.py
python mechanics/agon/parts/ccs-alignment/scripts/validate_agon_ccs_eval_alignment.py
python mechanics/agon/parts/vds-alignment/scripts/validate_agon_vds_eval_alignment.py
python mechanics/agon/parts/retention-rank-alignment/scripts/validate_agon_retention_rank_eval_alignment.py
python mechanics/agon/parts/mechanical-trial-suites/scripts/validate_agon_mechanical_trial_eval_suites.py
python mechanics/agon/parts/epistemic-alignment/scripts/validate_agon_epistemic_eval_alignment.py
python mechanics/agon/parts/slc-alignment/scripts/validate_agon_slc_eval_alignment_registry.py
python mechanics/agon/parts/kag-alignment/scripts/validate_agon_kag_eval_alignment_registry.py
python mechanics/agon/parts/sophian-threshold-alignment/scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q mechanics/agon/parts/*/tests/test_agon*.py
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which Agon part changed, which source and generated artifacts moved or
changed, which stop-lines were preserved, and which validation ran.
