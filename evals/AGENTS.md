# AGENTS.md

Local route card for contributors working under `evals/`.

## Purpose

`evals/<claim-family>/<eval-name>/` is the source-owned eval bundle surface.
The authoritative objects remain each bundle's `EVAL.md` and `eval.yaml`.

For classification of short `notes/`, `checks/`, or `examples/` artifacts,
[README.md](README.md) is the bundle source index that distinguishes owned
support from debris. Other bundle work does not require that human index by
convention.

## Operating Card

| Field | Route |
| --- | --- |
| role | source eval package tree |
| input | proof pressure, claim wording, eval metadata, and bundle-local evidence refs |
| output | bounded source eval claim plus local support artifacts |
| owner | bundle-local `EVAL.md` and `eval.yaml` for claim meaning |
| next route | `evals/README.md`, `mechanics/proof-object/README.md`, generated readers, or the nearest mechanic support part |
| tools | bundle and repository validation routes |
| validation | on-demand `VALIDATION.md` |

## Owns

This layer owns:
- bundle-local claim wording
- bundle-local verdict and scoring boundary wording
- bundle-local dependency fields such as `technique_dependencies`,
  `skill_dependencies`, and typed `capability_dependencies`
- bundle-local evidence references, including `support_note` when a comparative bundle requires it

## Owner Routes

Use the owning surface when the change is outside bundle-local claim meaning:

| Need | Owner route |
| --- | --- |
| shared fixture families | mechanic-local proof-infra or the narrower mechanic part |
| shared scorer helpers | `mechanics/proof-infra/parts/reportable-contracts/` |
| shared runner contracts | `mechanics/proof-infra/parts/reportable-contracts/` |
| generated catalogs and capsules | `generated/` plus the builder and source inputs |
| repository doctrine or topology | `docs/`, especially `docs/architecture/PROOF_TOPOLOGY.md` and `docs/architecture/AGENT_INDEX.md` |

## Editing rules

When editing a bundle:
- keep `EVAL.md` and `eval.yaml` semantically aligned
- keep the bundle under the claim family implied by `eval.yaml`: category for
  non-comparison evals and `comparison/<baseline_mode>` for comparison evals
- keep the bounded claim narrow and reviewable
- keep `comparison_surface` mirrored across frontmatter and `eval.yaml` when `baseline_mode` is not `none`
- preserve dependency fields unless the task explicitly changes dependency
  meaning; use `skill_dependencies` only for callable skills and
  `capability_dependencies` for modes, workflows, guards, tools, adapters, or
  other typed capability-graph nodes
- treat evidence entries as part of claim hygiene, not decoration

Bundle-local `AGENTS.md` overrides are exceptional. Use one only when a bundle
genuinely needs stronger local rules than the repository and `evals/` layer
already provide.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

For one touched bundle:
use the bundle-scoped `validate_repo.py --eval <bundle-name>` route.

For bundle index, generated reader, source-tree topology, or cross-bundle
wording changes:
use the source-tree topology route recorded in [VALIDATION.md](VALIDATION.md), including the catalog and report-index checks.

For validator, generated contract, report schema, source-tree topology
validator, or shared proof infrastructure changes:
