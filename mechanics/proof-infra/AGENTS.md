# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/proof-infra/DIRECTION.md` for current operating direction, `mechanics/proof-infra/PARTS.md` for active parts, and `mechanics/proof-infra/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/proof-infra/` and shared proof infrastructure route guidance.

## Role

This package routes shared fixture, runner, scorer, schema, report, and
template contract work.

It keeps reusable proof infrastructure aligned with the source bundle claim and
routes shared contract pressure to the narrowest active owner.

## Operating Card

| Field | Route |
| --- | --- |
| role | shared proof infrastructure route for fixtures, runners, scorers, schemas, reports, and templates |
| input | shared fixture family need, runner or scorer contract change, schema pressure, generated proof_artifacts drift, and reportable proof contract work |
| output | part-local fixture family, reportable contract route, bundle-local contract alignment, generated catalog check, or stronger-owner handoff |
| owner | source proof bundle owns interpretation; proof-infra owns reusable support contracts |
| next route | `mechanics/proof-infra/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, and affected source bundle |
| tools | `build_catalog.py --check`, `generate_eval_report_index.py --check`, root validator, semantic AGENTS validator, bounded rubric tests |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| bundle meaning and interpretation | affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| generic shared fixture-family support | `mechanics/proof-infra/parts/fixture-families/` |
| reportable contract runner/scorer/schema work | `mechanics/proof-infra/parts/reportable-contracts/` |
| comparison semantics | `mechanics/comparison-spine/` |
| receipt publication | `mechanics/publication-receipts/` |
| generated `proof_artifacts` | source contracts plus `python scripts/build_catalog.py --check` |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/proof-object/README.md`
7. `mechanics/proof-infra/README.md`
8. `mechanics/proof-infra/PARTS.md`
9. `docs/SHARED_PROOF_INFRA_GUIDE.md`
10. affected `parts/fixture-families/`, `parts/reportable-contracts/`, or
   root route-card local `AGENTS.md`
11. affected `evals/**/EVAL.md` and `evals/**/eval.yaml`

## Local Law

- Keep shared proof infrastructure weaker than the source proof object.
- Keep bundle-local `evals/<family>/<eval>/fixtures/contract.json`,
  `evals/<family>/<eval>/runners/contract.json`, and
  `evals/<family>/<eval>/reports/summary.schema.json` aligned with the bundle
  claim.
- Keep `shared_fixture_family_path` primary and use
  `additional_shared_fixture_family_paths` only for real secondary families.
- Keep generic part-local fixture families under
  `parts/fixture-families/fixtures/` when no narrower active mechanic owns the
  family.
- Keep shared reportable proof contracts under
  `parts/reportable-contracts/` when bundle-local runner contracts consume
  `runner_surface_path`, `scorer_helper_paths`, or shared schemas.
- Keep `paired_readout_path` primary and use `additional_paired_readout_paths`
  only for real secondary dossiers.
- Keep `scorer_helper_paths` reviewable and bounded.
- Keep generated catalog `proof_artifacts` derived from source contracts.

## Route Rules

- Move only infrastructure with a concrete bundle support route into this
  package.
- Keep former root fixture-family aliases as historical compatibility
  vocabulary after a family has an active mechanic-local path.
- Keep active runner, scorer, and schema payloads in reportable contracts once
  mechanic-local paths exist.
- Route fixture families to narrower active mechanics when they own the
  operation.
- Check generated `proof_artifacts` from source contracts and builders.
- Strengthen reports by fixing evidence or schema fit, not by loosening the
  shared contract.
- Keep shared fixture families and scorer helpers below bundle-local
  interpretation.
- Route promotion questions through bundle-local review and release surfaces.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/validate_semantic_agents.py
```

When scorer, schema, catalog, or validator logic changes, run the focused
part-local scorer route:

```bash
python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py
```

## Closeout

Report which shared proof contract changed, which source bundle or source class
it supports, whether generated catalog proof_artifacts stayed derived, which
schemas or scorer helpers were involved, what validation ran, and which
bundle-local interpretation boundary stayed stronger.
