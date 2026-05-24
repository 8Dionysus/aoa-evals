# Proof Infra Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/proof-infra/` routes the operation that keeps shared fixture,
runner, scorer, schema, report, and template contracts reusable while
bundle-local meaning stays visible.

Source bundles and domain mechanics keep proof meaning. This package keeps
reusable support contracts visible, versioned, reachable, and weaker than
bundle-local interpretation.

## Owned Operation

`bundle proof need -> shared proof contract -> bundle-local contract -> generated proof_artifacts -> bounded review`

This package routes shared proof infrastructure. Source proof meaning stays in
`evals/**/EVAL.md` and `evals/**/eval.yaml`.

## Source Surfaces

- `docs/SHARED_PROOF_INFRA_GUIDE.md`
- root route cards `fixtures/README.md` and `fixtures/AGENTS.md`
- `mechanics/proof-infra/PARTS.md`
- `mechanics/proof-infra/parts/fixture-families/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/*/README.md`
- `mechanics/proof-infra/parts/reportable-contracts/README.md`
- `mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md`
- `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/fixture-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/runner-contract.schema.json`
- `mechanics/proof-infra/parts/reportable-contracts/schemas/report-summary.schema.json`
- root route cards `runners/README.md` and `runners/AGENTS.md`
- root route cards `scorers/README.md` and `scorers/AGENTS.md`
- root route card `schemas/AGENTS.md`
- root route cards `reports/README.md` and `reports/AGENTS.md`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- `generated/eval_report_index.min.json`
- generated catalog `proof_artifacts` entries derived from bundle-local
  contracts

## Inputs

- a source proof object that needs reusable proof support
- a shared fixture family such as
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`
  when proof-infra is the narrowest active owner for the family
- a bundle-local `evals/<family>/<eval>/fixtures/contract.json`
- a bundle-local `evals/<family>/<eval>/runners/contract.json`
- a bundle-local `evals/<family>/<eval>/reports/summary.schema.json` and example
  report when the bundle ships a machine-readable report
- bundle-local `*.report.json` files only when a real reviewed run exists;
  these must validate against the bundle-local
  `evals/<family>/<eval>/reports/summary.schema.json`
- optional shared scorer helpers such as `mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py`
- shared contract schemas under
  `mechanics/proof-infra/parts/reportable-contracts/schemas/`
- optional shared report dossiers only through an explicit root route-card
  decision; current active reports are bundle-local or mechanic part-local

## Outputs

- explicit `shared_fixture_family_path`
- optional `additional_shared_fixture_family_paths`
- a part-local fixture-family library route when the family is generic proof
  support rather than an AoA-aligned mechanic part
- explicit `runner_surface_path`
- explicit `scorer_helper_paths`
- explicit `report_schema_path`
- part-local shared schemas for fixture, runner, and summary-report contract
  validation
- generated report-index entries that point back to real bundle-local reports
- explicit `paired_readout_path`
- optional `additional_paired_readout_paths`
- generated catalog `proof_artifacts` that point back to source contracts
- public-safe replacement guidance that preserves the bounded claim surface

## Stronger Owner Split

Proof-infra owns reusable support contracts: shared fixture families,
reportable runner surfaces, scorer helpers, schemas, report routes, templates,
and generated `proof_artifacts` derivation.

Stronger owner routes keep interpretation and acceptance:

| Need | Stronger owner route |
| --- | --- |
| proof claim or verdict meaning | bundle-local `EVAL.md`, `eval.yaml`, report schema, and reviewed report |
| AoA mechanic truth or comparison semantics | owning mechanic package |
| runtime evidence interpretation | runtime owner plus bundle-local proof review |
| receipt publication or release promotion | `mechanics/publication-receipts/` or `mechanics/release-support/` |
| sibling owner truth | sibling repository owner route |

When infrastructure points into a bundle, the bundle remains stronger. When a
bundle points into shared infrastructure, the shared path stays reusable
support.

## Boundaries

| Pressure | Route |
| --- | --- |
| whole root infrastructure district wants to move by theme | root infrastructure districts stay route-card districts unless a part-local owner exists |
| generic fixture family needs a shared support home | use `parts/fixture-families/fixtures/` when it is reusable proof support, proof-infra is the narrowest active owner, and bundle-local meaning remains stronger |
| shared reportable proof contract needs a support home | use `parts/reportable-contracts/` when bundle-local runner contracts and generated `proof_artifacts` consume it |
| domain-specific or AoA-aligned fixture family appears | route it to the owning mechanic part, such as `comparison-spine`, `recurrence`, `checkpoint`, `experience`, `antifragility`, `method-growth`, or `distillation` |
| generated catalog `proof_artifacts` drifts | fix the source contract or builder and rerun the generated check |
| report fails schema validation | fix evidence or schema fit through the owning route |
| shared fixture family starts carrying interpretation | return interpretation to the bundle-local proof object |
| scorer helper looks like a repo-global score | keep it as bounded scoring support for the consuming bundle contract |
| root `runners/`, `scorers/`, or `schemas/` wants active payload aliases | keep active payloads in the reportable-contracts part-local route |
| one shared report shape spreads across unrelated bundles | keep each bundle bound to its local report schema and reviewed report route |
| draft bundle gains polish through shared infrastructure | route promotion through bundle-local review and release surfaces |

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- adding or changing a shared fixture family;
- changing bundle-local `evals/<family>/<eval>/fixtures/contract.json`;
- changing bundle-local `evals/<family>/<eval>/runners/contract.json`;
- changing bundle-local `evals/<family>/<eval>/reports/summary.schema.json`;
- adding or changing bundle-local `*.report.json` run artifacts;
- changing shared scorer helper behavior;
- changing top-level report dossiers;
- changing generated catalog proof-artifact derivation.
