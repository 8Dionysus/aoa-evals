# Proof Infra Mechanic

## Role

`mechanics/proof-infra/` routes the operation that keeps shared fixture,
runner, scorer, schema, report, and template contracts reusable without hiding
bundle-local meaning.

It is not the fixture directory, schema directory, report directory, scorer
implementation owner, generated catalog, or proof bundle source.

## Owned Operation

`bundle proof need -> shared proof contract -> bundle-local contract -> generated proof_artifacts -> bounded review`

This package routes shared proof infrastructure. Source proof meaning stays in
`bundles/*/EVAL.md` and `bundles/*/eval.yaml`.

## Source Surfaces

- `docs/SHARED_PROOF_INFRA_GUIDE.md`
- `fixtures/README.md`
- `fixtures/AGENTS.md`
- `runners/README.md`
- `runners/AGENTS.md`
- `runners/reportable_proof_contract.md`
- `scorers/README.md`
- `scorers/AGENTS.md`
- `scorers/bounded_rubric_breakdown.py`
- `schemas/fixture-contract.schema.json`
- `schemas/runner-contract.schema.json`
- `schemas/report-summary.schema.json`
- `reports/README.md`
- `reports/AGENTS.md`
- `templates/EVAL.template.md`
- `generated/eval_report_index.min.json`
- generated catalog `proof_artifacts` entries derived from bundle-local
  contracts

## Inputs

- a source proof object that needs reusable proof support
- a shared fixture family such as `fixtures/<family>/README.md`
- a bundle-local `fixtures/contract.json`
- a bundle-local `runners/contract.json`
- a bundle-local `reports/summary.schema.json` and example report when the
  bundle ships a machine-readable report
- bundle-local `*.report.json` files only when a real reviewed run exists;
  these must validate against the bundle-local `reports/summary.schema.json`
- optional shared scorer helpers such as `scorers/bounded_rubric_breakdown.py`
- optional shared report dossiers under `reports/`

## Outputs

- explicit `shared_fixture_family_path`
- optional `additional_shared_fixture_family_paths`
- explicit `runner_surface_path`
- explicit `scorer_helper_paths`
- explicit `report_schema_path`
- generated report-index entries that point back to real bundle-local reports
- explicit `paired_readout_path`
- optional `additional_paired_readout_paths`
- generated catalog `proof_artifacts` that point back to source contracts
- public-safe replacement guidance that preserves the bounded claim surface

## Stronger Owner Split

Shared proof infrastructure supports proof objects. It does not own the proof
claim, verdict meaning, comparison semantics, runtime evidence interpretation,
receipt publication, sibling owner truth, or release promotion.

When infrastructure points into a bundle, the bundle remains stronger. When a
bundle points into shared infrastructure, the shared path is reusable support,
not a stronger claim.

## Boundaries

- Do not move `fixtures/`, `runners/`, `scorers/`, `schemas/`, `reports/`, or
  `templates/` into this package.
- Do not hand-edit generated catalog `proof_artifacts` as source truth.
- Do not weaken schemas to make a report pass.
- Do not let a shared fixture family replace bundle-local interpretation.
- Do not let scorer helpers become a repo-global score.
- Do not force one shared report shape across unrelated bundles.
- Do not promote draft bundles by giving them nicer shared infrastructure.

## Validation

After changing proof-infra route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/validate_semantic_agents.py
```

If scorer code changes, also run:

```bash
python -m pytest -q tests
```

If generated runtime, quest, comparison, or receipt surfaces change, run their
owning builders or validators too.

## Next Route

Use this package before:

- adding or changing a shared fixture family;
- changing bundle-local `fixtures/contract.json`;
- changing bundle-local `runners/contract.json`;
- changing bundle-local `reports/summary.schema.json`;
- adding or changing bundle-local `*.report.json` run artifacts;
- changing shared scorer helper behavior;
- changing top-level report dossiers;
- changing generated catalog proof-artifact derivation.
