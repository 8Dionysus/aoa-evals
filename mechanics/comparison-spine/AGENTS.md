# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/comparison-spine/DIRECTION.md`, `mechanics/comparison-spine/PARTS.md`, and `mechanics/comparison-spine/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/comparison-spine/` and comparison-spine route guidance.

## Role

This package routes baseline, peer-compare (including validation-routing method
support), and longitudinal-window proof operations.

It keeps comparison evidence aligned with source proof objects, fixture
contracts, paired readouts, and generated comparison readers while preserving
bundle-local interpretation.

## Operating Card

| Field | Route |
| --- | --- |
| role | comparison route for baseline, peer-compare, validation-routing method support, and longitudinal-window proof operations |
| input | `baseline_mode`, `comparison_surface`, fixture contract changes, paired readouts, and generated comparison reader drift |
| output | source bundle alignment, part-local comparison fixture/readout route, generated reader check, or bundle-local review handoff |
| owner | source proof bundle owns claim meaning; comparison-spine owns comparison shape and anti-overread route |
| next route | `mechanics/comparison-spine/README.md`, `DIRECTION.md`, `PARTS.md`, affected part README, and affected source bundle |
| tools | `build_catalog.py --check`, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Owner Routes

| Need | Owner route |
| --- | --- |
| source claim meaning | affected `evals/**/EVAL.md` and `evals/**/eval.yaml` |
| fixed baseline fixture/readout | `mechanics/comparison-spine/parts/fixed-baseline/` |
| peer comparison fixture/readout, including validation-routing method support | `mechanics/comparison-spine/parts/peer-compare/` |
| longitudinal-window fixture/readout | `mechanics/comparison-spine/parts/longitudinal-window/` |
| generated comparison reader | source bundle plus the local validation route |
| promotion, deprecation, or report interpretation | bundle-local review and release/report owner route |

## Local Law

- Keep comparison claim meaning in the source proof object.
- Keep `baseline_mode` and `comparison_surface` aligned across frontmatter and
  `eval.yaml`.
- Keep bundle-local `evals/<family>/<eval>/fixtures/contract.json` paths aligned
  with the part-local comparison fixture family paths.
- Keep `generated/comparison_spine.json` derived from source through the
  catalog builder routed by the local validation companion.
- Keep fixed-baseline, peer-compare, and longitudinal-window semantics
  separate.
- Keep style-only movement weaker than capability movement.
- Keep `aoa-eval-integrity-check` as an integrity sidecar below promotion
  routes.

Each package keeps current operating direction in `DIRECTION.md`; the active-to-archive bridge in `PROVENANCE.md` is consulted only when legacy names are involved.

## Route Rules

- Check generated comparison readers from source and builder output.
- Treat one comparison result as bounded evidence for its declared comparison
  posture.
- Keep peer comparison, fixed baseline, and longitudinal-window semantics
  distinct.
- Keep validation-routing method measurements under `peer-compare`; identical
  identity fields and full-owner-proof fallback are required, while policy
  selection and external validator execution remain outside this support part.
- Route bundle promotion or deprecation through bundle-local review and release
  surfaces.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

If the change touches runtime candidate readers, quest readers, reports,
schemas, or phase-alpha matrices, also run the owning builder or validator.

## Closeout

Report which comparison mode changed, which source bundle or generated reader
was affected, whether `baseline_mode`, `comparison_surface`, and fixture
contracts stayed aligned, which anti-overread boundary was preserved, and
which validation ran.
