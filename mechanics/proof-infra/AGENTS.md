# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/proof-infra/DIRECTION.md` for current operating direction, `mechanics/proof-infra/PARTS.md` for active parts, and `mechanics/proof-infra/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/proof-infra/` and shared proof infrastructure route guidance.

## Role

This package routes shared fixture, runner, scorer, schema, report, and
template contract work.

It does not own bundle meaning, generated truth, comparison semantics, runtime
evidence, receipt publication, or a repo-global score.

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
11. affected `bundles/*/EVAL.md` and `bundles/*/eval.yaml`

## Local Law

- Keep shared proof infrastructure weaker than the source proof object.
- Keep bundle-local `bundles/<bundle>/fixtures/contract.json`,
  `bundles/<bundle>/runners/contract.json`, and
  `bundles/<bundle>/reports/summary.schema.json` aligned with the bundle
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

## Boundaries

- Do not move whole shared infrastructure districts into this package by theme.
- Keep former root fixture-family aliases as historical compatibility
  vocabulary after a family has an active mechanic-local path.
- Do not recreate active root runner, scorer, or schema payload aliases after
  reportable contracts have an active mechanic-local path.
- Do not keep a family in `proof-infra` if a narrower active mechanic owns the
  operation.
- Do not hand-edit generated proof_artifacts as source truth.
- Do not weaken schemas to pass weak reports.
- Do not let a shared fixture family or scorer helper replace bundle-local
  interpretation.
- Do not turn shared proof infrastructure into a promotion shortcut.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```

Run `python -m pytest -q` when scorer, schema, catalog, or validator logic
changes; use part-local pytest paths for focused checks.

## Closeout

Report which shared proof contract changed, which source bundle or source class
it supports, whether generated catalog proof_artifacts stayed derived, which
schemas or scorer helpers were involved, what validation ran, and which
bundle-local interpretation boundary stayed stronger.
