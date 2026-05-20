# AGENTS.md

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
8. `docs/SHARED_PROOF_INFRA_GUIDE.md`
9. affected `fixtures/`, `runners/`, `scorers/`, `schemas/`, `reports/`, or
   `templates/` local `AGENTS.md`
10. affected `bundles/*/EVAL.md` and `bundles/*/eval.yaml`

## Local Law

- Keep shared proof infrastructure weaker than the source proof object.
- Keep bundle-local `fixtures/contract.json`, `runners/contract.json`, and
  `reports/summary.schema.json` aligned with the bundle claim.
- Keep `shared_fixture_family_path` primary and use
  `additional_shared_fixture_family_paths` only for real secondary families.
- Keep `paired_readout_path` primary and use `additional_paired_readout_paths`
  only for real secondary dossiers.
- Keep `scorer_helper_paths` reviewable and bounded.
- Keep generated catalog `proof_artifacts` derived from source contracts.

## Boundaries

- Do not move shared infrastructure directories into this package.
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

Run `python -m pytest -q tests` when scorer, schema, catalog, or validator
logic changes.

## Closeout

Report which shared proof contract changed, which source bundle or source class
it supports, whether generated catalog proof_artifacts stayed derived, which
schemas or scorer helpers were involved, what validation ran, and which
bundle-local interpretation boundary stayed stronger.
