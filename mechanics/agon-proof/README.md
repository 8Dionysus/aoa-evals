# Agon Proof Mechanic

## Role

`mechanics/agon-proof/` routes the operation that keeps Agon pre-protocol
proof alignment surfaces reviewable, generated from seed inputs, and bounded
by stop-lines.

It is not an Agon runtime, arena owner, verdict bridge, rank system, memory
writer, Tree of Sophia canon route, or replacement for Agents-of-Abyss law.

## Owned Operation

The owned operation is:

`Agon proof pressure -> seed prebinding or alignment config -> deterministic generated registry -> observe-only recurrence component and hooks -> Agon stop-line review -> bundle-local proof or owner handoff`

This package turns Agon and wave vocabulary into a current proof-layer route
without renaming or moving the source surfaces.

## Source Surfaces

- `docs/AGON_EVAL_PREBINDING_MODEL.md`
- `docs/AGON_COURT_PREBINDING.md`
- `docs/AGON_CCS_EVAL_ALIGNMENT.md`
- `docs/AGON_VDS_EVAL_ALIGNMENT.md`
- `docs/AGON_RETENTION_RANK_EVAL_ALIGNMENT.md`
- `docs/AGON_MECHANICAL_TRIAL_EVAL_SUITES.md`
- `docs/AGON_EPISTEMIC_EVAL_ALIGNMENT.md`
- `docs/AGON_SLC_EVAL_ALIGNMENT.md`
- `docs/AGON_KAG_EVAL_ALIGNMENT.md`
- `docs/AGON_SOPHIAN_EVAL_ALIGNMENT.md`
- `docs/AGON_EVAL_OWNER_HANDOFFS.md`
- `docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md`
- `config/agon_eval_prebindings.seed.json`
- `config/agon_ccs_eval_alignment.seed.json`
- `config/agon_vds_eval_alignment.seed.json`
- `config/agon_retention_rank_eval_alignment.seed.json`
- `config/agon_mechanical_trial_eval_suites.seed.json`
- `config/agon_epistemic_eval_alignment.seed.json`
- `config/agon_slc_eval_alignment.seed.json`
- `config/agon_kag_eval_alignment.seed.json`
- `config/agon_sophian_eval_alignment.seed.json`
- `generated/agon_eval_prebinding_registry.min.json`
- `generated/agon_ccs_eval_alignment_registry.min.json`
- `generated/agon_vds_eval_alignment_registry.min.json`
- `generated/agon_retention_rank_eval_alignment_registry.min.json`
- `generated/agon_mechanical_trial_eval_suite_registry.min.json`
- `generated/agon_epistemic_eval_alignment_registry.min.json`
- `generated/agon_slc_eval_alignment_registry.min.json`
- `generated/agon_kag_eval_alignment_registry.min.json`
- `generated/agon_sophian_eval_alignment_registry.min.json`
- `manifests/recurrence/component.agon*.json`
- `manifests/recurrence/hooks/component.agon*.json`
- `quests/agon/captured/AOE-Q-AGON-*.md`
- `bundles/aoa-recurrence-control-plane-integrity/EVAL.md`

## Inputs

- Agon prebinding, alignment, or trial-suite seed configs;
- center-law or owner-route refs that the seeds cite;
- schema-backed examples and tests for Agon registries;
- recurrence component and hook manifests that observe Agon surfaces;
- bundle-local stop-line evidence from recurrence control-plane integrity.

## Outputs

- deterministic generated Agon registries;
- observe-only recurrence components and hook bindings;
- candidate-only alignment or precheck surfaces;
- bundle-local stop-line review routes;
- owner handoffs when an Agon surface depends on stronger owner truth.

## Stronger Owner Split

`aoa-evals` owns the bounded proof alignment surface: seed shape, generated
registry derivation, candidate-only posture, stop-line review, and local
bundle interpretation.

Agents-of-Abyss owns Agon law, federation law, verdict bridge meaning, and any
future arena or court authority. Tree of Sophia, aoa-kag, aoa-memo,
aoa-routing, aoa-playbooks, aoa-sdk, and aoa-stats keep their own stronger
truth when Agon alignment surfaces point toward them.

## Legacy Posture

`Agon` and wave labels stay accepted historical and generated-projection
vocabulary because existing docs, configs, registries, manifests, examples,
tests, and quests use them.

The active route for new proof-layer work is this package. The old names remain
lineage and accepted input, not permission to create live verdict authority or
make wave labels the repo-wide topology.

## Boundaries

- Do not move `docs/AGON_*`, `config/agon_*`, `generated/agon_*`,
  `manifests/recurrence/component.agon*`, `quests/agon/captured/AOE-Q-AGON-*.md`, or
  recurrence-control-plane bundle files into this package.
- Do not hand-edit generated Agon registries as source truth.
- Do not treat generated registry freshness as Agon owner acceptance.
- Do not issue live verdicts, grant closure, initiate summon, write memory,
  mutate rank, promote to Tree of Sophia, run a hidden scheduler, or activate
  an arena from this package.
- Do not weaken `no_live_verdict`, `no_closure_grant`, `no_live_summon`,
  `no_durable_memory_write`, `no_rank_mutation`, or
  `no_tree_of_sophia_promotion` stop-lines.
- Do not turn an observe-only recurrence component or hook into runtime
  authority.

## Validation

After changing Agon proof alignment surfaces, run the touched builder and
validator first. For the current full Agon route, run:

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

When a generated registry is intentionally refreshed, run the corresponding
builder without `--check`, then rerun the validator and test for that family.

## Next Route

Use this package before:

- adding a new Agon prebinding, alignment, wave, or trial-suite seed;
- changing Agon generated registry builders or validators;
- changing Agon recurrence component or observe-only hook posture;
- interpreting Agon stop-line evidence inside
  `aoa-recurrence-control-plane-integrity`;
- deciding whether an Agon family can become a source proof bundle or owner
  handoff.
