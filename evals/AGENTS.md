# AGENTS.md

Local route card for contributors working under `evals/`.

## Purpose

`evals/<claim-family>/<eval-name>/` is the source-owned eval bundle surface.
The authoritative objects remain each bundle's `EVAL.md` and `eval.yaml`.

Use [README.md](README.md) as the bundle source index before treating short
`notes/`, `checks/`, or `examples/` artifacts as debris.

## Operating Card

| Field | Route |
| --- | --- |
| role | source eval package tree |
| input | proof pressure, claim wording, eval metadata, and bundle-local evidence refs |
| output | bounded source eval claim plus local support artifacts |
| owner | bundle-local `EVAL.md` and `eval.yaml` for claim meaning |
| next route | `evals/README.md`, `mechanics/proof-object/README.md`, generated readers, or the nearest mechanic support part |
| tools | `scripts/validate_repo.py`, catalog builders, report-index builder |
| validation | this card's `Validation` section |

## Owns

This layer owns:
- bundle-local claim wording
- bundle-local verdict and scoring boundary wording
- bundle-local dependency fields such as `technique_dependencies` and `skill_dependencies`
- bundle-local evidence references, including `support_note` when a comparative bundle requires it

## Owner Routes

Use the owning surface when the change is outside bundle-local claim meaning:

| Need | Owner route |
| --- | --- |
| shared fixture families | mechanic-local proof-infra or the narrower mechanic part |
| shared scorer helpers | `mechanics/proof-infra/parts/reportable-contracts/` |
| shared runner contracts | `mechanics/proof-infra/parts/reportable-contracts/` |
| generated catalogs and capsules | `generated/` plus the builder and source inputs |
| repository doctrine or topology | `docs/`, especially `docs/PROOF_TOPOLOGY.md` and `docs/AGENT_INDEX.md` |

## Editing rules

When editing a bundle:
- keep `EVAL.md` and `eval.yaml` semantically aligned
- keep the bundle under the claim family implied by `eval.yaml`: category for
  non-comparison evals and `comparison/<baseline_mode>` for comparison evals
- keep the bounded claim narrow and reviewable
- keep `comparison_surface` mirrored across frontmatter and `eval.yaml` when `baseline_mode` is not `none`
- preserve `technique_dependencies` and `skill_dependencies` unless the task explicitly changes dependency meaning
- treat evidence entries as part of claim hygiene, not decoration

Bundle-local `AGENTS.md` overrides are exceptional. Use one only when a bundle
genuinely needs stronger local rules than the repository and `evals/` layer
already provide.

## Validation

For one touched bundle:

```bash
python scripts/validate_repo.py --eval <bundle-name>
```

For bundle index, generated reader, source-tree topology, or cross-bundle
wording changes:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
```

For validator, generated contract, report schema, source-tree topology
validator, or shared proof infrastructure changes:

```bash
python -m pytest -q
```
