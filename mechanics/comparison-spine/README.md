# Comparison Spine Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Role

`mechanics/comparison-spine/` routes the operation that keeps baseline,
peer-compare, and longitudinal-window proof claims bounded.

It is not the comparison result, generated catalog, report directory, bundle
owner, or promotion authority.

## Owned Operation

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

This package routes the comparison operation. Source claim meaning stays in
`bundles/*/EVAL.md` and `bundles/*/eval.yaml`.

## Source Surfaces

- `mechanics/comparison-spine/PARTS.md`
- `mechanics/comparison-spine/parts/README.md`
- `docs/COMPARISON_SPINE_GUIDE.md`
- `docs/BASELINE_COMPARISON_GUIDE.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `mechanics/proof-object/parts/bundle-authoring/templates/EVAL.template.md`
- `generated/comparison_spine.json`
- `generated/eval_catalog.json`
- `mechanics/comparison-spine/parts/spine-overview/reports/comparison-spine-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`
- `mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md`
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md`
- bundle-local `bundles/<bundle>/fixtures/contract.json`,
  `bundles/<bundle>/runners/contract.json`, and
  `bundles/<bundle>/reports/summary.schema.json` when a comparison bundle
  ships them

## Inputs

- a bundle with `baseline_mode` other than `none`
- a machine-readable `comparison_surface`
- a part-local shared fixture family path
- a paired readout path
- an integrity sidecar
- a selection question
- comparison-mode-specific anchors:
  - `anchor_surface` and `baseline_target_label` for `fixed-baseline` and
    `previous-version`
  - `peer_surfaces` and `matched_surface` for `peer-compare`
  - `anchor_surface` and `window_family_label` for `longitudinal-window`

## Outputs

- one bounded comparison read
- source-aligned comparison metadata in bundle frontmatter and `eval.yaml`
- generated `generated/comparison_spine.json` entries derived from source
- report routes that preserve the comparison mode
- explicit anti-overread language for baseline drift, peer-compare blur,
  longitudinal movement, and style-only movement

## Stronger Owner Split

Comparison may cite skills, techniques, runtime candidates, sibling owner
surfaces, reports, or generated readers.

Those cited surfaces remain weaker than the source proof object for the bounded
claim. Comparison routing does not make one result a repo-global score, broad
growth proof, runtime health proof, or sibling owner acceptance.

## Comparison Modes

### `fixed-baseline`

Use when one candidate is compared against one frozen baseline target on the
same bounded task family.

The current default public baseline surface is `aoa-regression-same-task`.

### `peer-compare`

Use when two peer readings are compared side by side on matched bounded cases.

Peer comparison is not baseline by association.

### `longitudinal-window`

Use when ordered named windows stay on one bounded workflow surface.

Repeated-window movement is not broad growth by association.

## Boundaries

- Do not move comparison bundles into this package.
- Do not move bundle-local fixture, runner, or report contracts into this
  package.
- Do not hand-edit `generated/comparison_spine.json` as source truth.
- Do not treat one clean comparison as broad capability growth.
- Do not let style-only movement become capability movement.
- Do not promote a draft comparison bundle by improving generated metadata.
- Do not let `aoa-eval-integrity-check` become a promotion shortcut.
- Do not collapse fixed baseline, peer comparison, and longitudinal movement
  into one score.

## Provenance

Use `mechanics/comparison-spine/PROVENANCE.md` only when auditing former root
comparison fixture family placement. New comparison work starts from this
README, `PARTS.md`, and the active part.

## Validation

After changing comparison-spine route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```

If comparison examples, reports, schemas, runtime candidate readers, or
phase-alpha matrices also change, run their owning checks too.

## Next Route

Use this package before:

- changing `baseline_mode`;
- adding or changing `comparison_surface`;
- editing comparison spine docs or generated comparison readers;
- changing fixed-baseline, peer-compare, or longitudinal-window report routes;
- changing wording that could imply broad growth, global scoring, or promotion
  by association.
