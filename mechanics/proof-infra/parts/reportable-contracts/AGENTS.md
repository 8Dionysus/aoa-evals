# AGENTS.md

## Applies to

`mechanics/proof-infra/parts/reportable-contracts/`.

## Role

This card routes reportable proof contract support: the shared runner surface,
shared bounded scorer helper, shared schemas that each bundle-local runner
contract cites, and reusable experiment-control contracts whose run status
must remain weaker than bundle-local verdict review.

Source bundles, bundle-local reports, comparison mechanics, audit intake,
publication receipts, and sibling repositories keep stronger interpretation and
owner truth.

## Operating Card

| Field | Route |
| --- | --- |
| role | shared reportable runner, scorer, and schema support route |
| input | runner contract change, scorer helper change, schema pressure, root alias pressure, weak report pressure, bundle-local report contract drift, or C21-C23 experiment-control change |
| output | reportable contract route, bundle-local contract alignment, generated catalog check, focused scorer/schema test, honest experiment-status contract, or stronger-owner handoff |
| owner | this part owns reusable reportable contracts; source bundles and active mechanics own interpretation semantics |
| next route | parent `parts/AGENTS.md`, parent `PARTS.md`, this part `README.md`, runner/scorer/schema payload, affected bundle runner contract, and affected report schema |
| tools | nearest on-demand VALIDATION.md route, root validator, semantic AGENTS validator, catalog builder, and bounded rubric scorer test |
| validation | [VALIDATION.md](VALIDATION.md) |

## Boundary Routes

| Pressure | Route |
| --- | --- |
| Shared runner authority pressure | bundle-local interpretation boundary and reviewed report route. |
| `runner_surface_path` or `scorer_helper_paths` drift | affected bundle runner contract plus generated `proof_artifacts` parity. |
| Schema weakening pressure | proof-contract risk review plus focused scorer/schema validation. |
| Hidden harness logic or private evidence pressure | owner evidence route or sibling repository; this part keeps public-safe reusable support. |
| Root alias pressure for `runners/`, `scorers/`, or `schemas/` | route-card-only root districts plus active part-local paths. |
| Bundle-local report schema or reviewed report pressure | source bundle and bundle-local report route. |
| Experiment status reads as verdict or benefit | keep C23 execution-status-only and route the claim to bundle-local evidence and verdict logic. |
| C22 content changes after preregistration | require the canonical normalized self-digest to change, reject the old manifest, and create a new version with explicit run exclusion. |
| Pin or manifest wants training, production, policy, or memory authority | reject the widening and route it to the named sibling owner plus operator/effect owner. |

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Use this part's local on-demand VALIDATION.md route.
Run broader catalog and validation checks through the parent or affected bundle
route when bundle-local runner contracts or generated `proof_artifacts` change.

## Closeout

Report which reportable contract surface changed, which bundle-local contracts
consume it, whether generated `proof_artifacts` were rebuilt, C21-C23 status
and negative-case plus normalized-self-digest coverage when affected, and
which bundle-local
interpretation boundary stayed stronger.
