# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/proof-infra/DIRECTION.md`, `mechanics/proof-infra/PARTS.md`, and `mechanics/proof-infra/PROVENANCE.md` routes as needed for the touched source.

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
| generated `proof_artifacts` | source contracts plus the local validation route |

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

Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

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
- Strengthen reports by fixing evidence or schema fit instead of loosening the
  shared contract.
- Keep shared fixture families and scorer helpers below bundle-local
  interpretation.
- Route promotion questions through bundle-local review and release surfaces.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Run the narrow package route checks:

When scorer, schema, catalog, or validator logic changes, run the focused
part-local scorer route:

## Closeout

Report which shared proof contract changed, which source bundle or source class
it supports, whether generated catalog proof_artifacts stayed derived, which
schemas or scorer helpers were involved, what validation ran, and which
bundle-local interpretation boundary stayed stronger.
