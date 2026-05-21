# Agon Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/agon/` owns the local `aoa-evals` operation that turns Agon
pressure into bounded proof-alignment artifacts.

It is not the Agon court, arena runtime, verdict authority, rank system,
memory writer, Tree of Sophia canon route, or replacement for
Agents-of-Abyss law.

## Owned Operation

`Agon pressure -> part-local seed/config/docs -> deterministic registry -> candidate-only checks -> observe-only recurrence hooks -> bundle-local review or owner handoff`

The mechanic is named `agon` because Agon is the parent operation. Proof,
prebinding, candidate-only, and stop-line posture belong inside its parts and
validators, not in the package name.

## Parts

Part ownership is listed in [PARTS.md](PARTS.md).

Current parts:

- `court-prebinding`
- `ccs-alignment`
- `vds-alignment`
- `mechanical-trial-suites`
- `retention-rank-alignment`
- `epistemic-alignment`
- `slc-alignment`
- `kag-alignment`
- `sophian-threshold-alignment`

## Package-Level Surfaces

- [docs/AGON_EVAL_OWNER_HANDOFFS.md](docs/AGON_EVAL_OWNER_HANDOFFS.md)
- [docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md](docs/AGON_EVAL_RECURRENCE_REVIEW_BOUNDARY.md)
- [PROVENANCE.md](PROVENANCE.md) as the single bridge to the legacy archive
- [PARTS.md](PARTS.md)

Former Agon markdown quest notes now live behind `PROVENANCE.md`. They are
Agon lineage and proof-pressure receipts, not active quest lifecycle source
records.

The bundle
`bundles/aoa-recurrence-control-plane-integrity/EVAL.md` remains a source proof
bundle. Agon uses it as a review boundary, not as a mechanic-owned file.

## Inputs

- part-local seed configs;
- part-local schemas and examples;
- part-local docs that define alignment intent and boundaries;
- part-local builders, validators, tests, recurrence manifests, and hook
  bindings;
- owner references into Agents-of-Abyss, abyss-stack, KAG, ToS, memo, stats,
  SDK, routing, and playbooks when an alignment surface cites stronger truth.

## Outputs

- deterministic part-local generated registries;
- candidate-only alignment or precheck surfaces;
- observe-only recurrence components and hook bindings;
- bounded review signals for proof bundles or owner handoffs.

## Stronger Owner Split

`aoa-evals` owns the bounded proof-alignment surface: seed shape, registry
derivation, candidate-only checks, stop-line review, and bundle-local
interpretation.

Agents-of-Abyss owns Agon law, federation law, court meaning, verdict bridge
meaning, and any future arena authority. Other sibling repositories keep their
own source truth when an Agon part points toward them.

## Naming and Legacy

Active topology uses `mechanics/agon/`.

Old wave names and file stems remain accepted lineage where they are part of
source artifacts, generated payloads, or historical receipts. They do not define
the active package name.

Use [PROVENANCE.md](PROVENANCE.md) before reading legacy files. Legacy is
preserved lineage behind the active parts, not the route for new Agon work.

## Boundaries

- Keep source configs, schemas, examples, generated registries, scripts, tests,
  recurrence manifests, and hooks in the owning part.
- Keep generated registries weaker than part-local source config and builder
  logic.
- Keep recurrence components observe-only.
- Keep new quest pressure in schema-backed `quests/<lane>/<state>/AOA-EV-Q-*.yaml`
  records, and keep former Agon markdown note lineage behind `PROVENANCE.md`.
- Keep bundle-local proof review stronger than Agon mechanic signals.
- Do not turn an eval alignment into a live verdict, arena action, or owner
  promotion.
- Preserve stop-lines such as `no_live_verdict`, `no_closure_grant`,
  `no_live_summon`, `no_durable_memory_write`, `no_rank_mutation`, and
  `no_tree_of_sophia_promotion`.

## Validation

Run the touched part first. For the current full Agon route:

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

When a generated registry intentionally changes, run that part builder without
`--check`, then rerun the part validator and tests.

## Next Route

Use this mechanic before adding or changing an Agon prebinding, alignment,
trial suite, wave-derived registry, recurrence component, observe-only hook, or
owner handoff surface.
