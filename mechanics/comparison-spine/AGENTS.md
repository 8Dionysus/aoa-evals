# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/comparison-spine/DIRECTION.md` for current operating direction, `mechanics/comparison-spine/PARTS.md` for active parts, and `mechanics/comparison-spine/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/comparison-spine/` and comparison-spine route guidance.

## Role

This package routes baseline, peer-compare, and longitudinal-window proof
operations.

It keeps comparison evidence aligned with source proof objects, fixture
contracts, paired readouts, and generated comparison readers while preserving
bundle-local interpretation.

## Operating Card

| Field | Route |
| --- | --- |
| role | comparison route for baseline, peer-compare, and longitudinal-window proof operations |
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
| peer comparison fixture/readout | `mechanics/comparison-spine/parts/peer-compare/` |
| longitudinal-window fixture/readout | `mechanics/comparison-spine/parts/longitudinal-window/` |
| generated comparison reader | source bundle plus `python scripts/build_catalog.py --check` |
| promotion, deprecation, or report interpretation | bundle-local review and release/report owner route |

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/proof-object/README.md`
7. `mechanics/comparison-spine/README.md`
8. `mechanics/comparison-spine/PARTS.md`
9. `mechanics/comparison-spine/parts/README.md`
10. `docs/guides/COMPARISON_SPINE_GUIDE.md`
11. `docs/guides/BASELINE_COMPARISON_GUIDE.md`
12. `docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
13. affected `evals/**/EVAL.md` and `evals/**/eval.yaml`

## Local Law

- Keep comparison claim meaning in the source proof object.
- Keep `baseline_mode` and `comparison_surface` aligned across frontmatter and
  `eval.yaml`.
- Keep bundle-local `evals/<family>/<eval>/fixtures/contract.json` paths aligned
  with the part-local comparison fixture family paths.
- Keep `generated/comparison_spine.json` derived from source via
  `python scripts/build_catalog.py`.
- Keep fixed-baseline, peer-compare, and longitudinal-window semantics
  separate.
- Keep style-only movement weaker than capability movement.
- Keep `aoa-eval-integrity-check` as an integrity sidecar below promotion
  routes.

## Route Rules

- Check generated comparison readers from source and builder output.
- Treat one comparison result as bounded evidence for its declared comparison
  posture.
- Keep peer comparison, fixed baseline, and longitudinal-window semantics
  distinct.
- Route bundle promotion or deprecation through bundle-local review and release
  surfaces.

## Validation

Run the narrow package route checks:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```

If the change touches runtime candidate readers, quest readers, reports,
schemas, or phase-alpha matrices, also run the owning builder or validator.

## Closeout

Report which comparison mode changed, which source bundle or generated reader
was affected, whether `baseline_mode`, `comparison_surface`, and fixture
contracts stayed aligned, which anti-overread boundary was preserved, and
which validation ran.
