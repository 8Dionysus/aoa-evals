# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/comparison-spine/DIRECTION.md` for current operating direction, `mechanics/comparison-spine/PARTS.md` for active parts, and `mechanics/comparison-spine/PROVENANCE.md` only when legacy or former placement matters.

## Applies to

`mechanics/comparison-spine/` and comparison-spine route guidance.

## Role

This package routes baseline, peer-compare, and longitudinal-window proof
operations.

It does not own bundle meaning, generated truth, report results, promotion
authority, or a repo-global score.

## Read before editing

1. repository root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `mechanics/README.md`
6. `mechanics/proof-object/README.md`
7. `mechanics/comparison-spine/README.md`
8. `mechanics/comparison-spine/PARTS.md`
9. `mechanics/comparison-spine/parts/README.md`
10. `docs/COMPARISON_SPINE_GUIDE.md`
11. `docs/BASELINE_COMPARISON_GUIDE.md`
12. `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
13. affected `bundles/*/EVAL.md` and `bundles/*/eval.yaml`

## Local Law

- Keep comparison claim meaning in the source proof object.
- Keep `baseline_mode` and `comparison_surface` aligned across frontmatter and
  `eval.yaml`.
- Keep bundle-local `bundles/<bundle>/fixtures/contract.json` paths aligned
  with the part-local comparison fixture family paths.
- Keep `generated/comparison_spine.json` derived from source via
  `python scripts/build_catalog.py`.
- Keep fixed-baseline, peer-compare, and longitudinal-window semantics
  separate.
- Keep style-only movement weaker than capability movement.
- Keep `aoa-eval-integrity-check` as an integrity sidecar, not a promotion
  shortcut.

## Boundaries

- Do not hand-edit generated comparison readers as source truth.
- Do not use one comparison result as broad growth proof.
- Do not turn peer comparison into baseline by association.
- Do not turn repeated-window movement into general capability growth.
- Do not promote or deprecate bundles by editing this package.

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
