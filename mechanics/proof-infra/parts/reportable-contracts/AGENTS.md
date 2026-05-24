# AGENTS.md

## Applies to

`mechanics/proof-infra/parts/reportable-contracts/`.

## Role

This card routes reportable proof contract support: the shared runner surface,
shared bounded scorer helper, and shared schemas that each bundle-local runner
contract cites.

Source bundles, bundle-local reports, comparison mechanics, audit intake,
publication receipts, and sibling repositories keep stronger interpretation and
owner truth.

## Operating Card

| Field | Route |
| --- | --- |
| role | shared reportable runner, scorer, and schema support route |
| input | runner contract change, scorer helper change, schema pressure, root alias pressure, weak report pressure, or bundle-local report contract drift |
| output | reportable contract route, bundle-local contract alignment, generated catalog check, focused scorer test, or stronger-owner handoff |
| owner | this part owns reusable reportable contracts; source bundles and active mechanics own interpretation semantics |
| next route | parent `parts/AGENTS.md`, parent `PARTS.md`, this part `README.md`, runner/scorer/schema payload, affected bundle runner contract, and affected report schema |
| tools | parent centralized child validation, root validator, semantic AGENTS validator, catalog builder, and bounded rubric scorer test |
| validation | [parent parts/AGENTS.md](../AGENTS.md#centralized-child-validation) |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `docs/PROOF_TOPOLOGY.md`
4. `mechanics/EVIDENCE_CLUSTERS.md`
5. `mechanics/proof-infra/README.md`
6. `mechanics/proof-infra/PARTS.md`
7. `mechanics/proof-infra/parts/AGENTS.md`
8. `mechanics/proof-infra/parts/reportable-contracts/README.md`
9. affected `evals/**/EVAL.md`
10. affected `evals/**/runners/contract.json`
11. affected `evals/**/reports/summary.schema.json`

## Boundary Routes

| Pressure | Route |
| --- | --- |
| Shared runner authority pressure | bundle-local interpretation boundary and reviewed report route. |
| `runner_surface_path` or `scorer_helper_paths` drift | affected bundle runner contract plus generated `proof_artifacts` parity. |
| Schema weakening pressure | proof-contract risk review plus focused scorer/schema validation. |
| Hidden harness logic or private evidence pressure | owner evidence route or sibling repository; this part keeps public-safe reusable support. |
| Root alias pressure for `runners/`, `scorers/`, or `schemas/` | route-card-only root districts plus active part-local paths. |
| Bundle-local report schema or reviewed report pressure | source bundle and bundle-local report route. |

## Validation

Use the centralized child validation lane in
[parent parts/AGENTS.md](../AGENTS.md#centralized-child-validation).
Run broader catalog and validation checks through the parent or affected bundle
route when bundle-local runner contracts or generated `proof_artifacts` change.

## Closeout

Report which reportable contract surface changed, which bundle-local contracts
consume it, whether generated `proof_artifacts` were rebuilt, and which
bundle-local interpretation boundary stayed stronger.
