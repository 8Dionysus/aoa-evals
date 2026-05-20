# AGENTS.md

## Applies to

`mechanics/agon-proof/` and the Agon pre-protocol proof alignment route.

## Role

This package protects the Agon proof alignment loop:

`seed config -> generated registry -> observe-only recurrence component -> Agon stop-line review -> bundle-local review or owner handoff`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/LEGACY_NAMING.md`
6. `mechanics/README.md`
7. `mechanics/agon-proof/README.md`
8. `docs/AGON_EVAL_PREBINDING_MODEL.md`
9. `docs/AGON_EVAL_OWNER_HANDOFFS.md`
10. `docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`
11. `bundles/aoa-recurrence-control-plane-integrity/EVAL.md`
12. `docs/decisions/0016-agon-proof-mechanic-package.md`

## Boundaries

- Keep Agon seed configs stronger than generated Agon registries.
- Keep observe-only recurrence components and hooks weaker than bundle-local
  proof review.
- Keep Agents-of-Abyss law stronger than local eval alignment wording.
- Do not move `docs/AGON_*`, `config/agon_*`, `generated/agon_*`,
  `manifests/recurrence/component.agon*`, or
  `quests/agon/captured/AOE-Q-AGON-*.md` from
  this package.
- Do not grant live verdict, closure, summon, memory write, rank mutation,
  Tree of Sophia promotion, hidden scheduler, or arena authority.
- Do not weaken `no_live_verdict` or other Agon stop-lines to make a registry
  pass.

## Validation

Run the touched Agon builder or validator, then normally run:

```bash
python scripts/build_agon_eval_prebinding_registry.py --check
python scripts/build_agon_ccs_eval_alignment_registry.py --check
python scripts/build_agon_vds_eval_alignment_registry.py --check
python scripts/build_agon_retention_rank_eval_alignment_registry.py --check
python scripts/build_agon_mechanical_trial_eval_suites.py --check
python scripts/build_agon_epistemic_eval_alignment_registry.py --check
python scripts/build_agon_slc_eval_alignment_registry.py --check
python scripts/build_agon_kag_eval_alignment_registry.py --check
python scripts/build_agon_sophian_eval_alignment_registry.py --check
python scripts/validate_agon_eval_prebindings.py
python scripts/validate_agon_ccs_eval_alignment.py
python scripts/validate_agon_vds_eval_alignment.py
python scripts/validate_agon_retention_rank_eval_alignment.py
python scripts/validate_agon_mechanical_trial_eval_suites.py
python scripts/validate_agon_epistemic_eval_alignment.py
python scripts/validate_agon_slc_eval_alignment_registry.py
python scripts/validate_agon_kag_eval_alignment_registry.py
python scripts/validate_agon_sophian_eval_alignment_registry.py
python -m pytest -q tests/test_agon*.py
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

## Closeout

Report which Agon family changed, which seed config or generated registry was
touched, which stop-lines were preserved, which builder and validator ran, and
whether stronger-owner surfaces were left untouched.
