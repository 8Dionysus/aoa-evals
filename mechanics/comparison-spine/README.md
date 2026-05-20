# Comparison Spine Mechanic

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

- `docs/COMPARISON_SPINE_GUIDE.md`
- `docs/BASELINE_COMPARISON_GUIDE.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `templates/EVAL.template.md`
- `generated/comparison_spine.json`
- `generated/eval_catalog.json`
- `reports/comparison-spine-proof-flow-v1.md`
- `reports/same-task-baseline-proof-flow-v1.md`
- `reports/repeated-window-proof-flow-v1.md`
- `reports/repeated-window-proof-flow-v2.md`
- `reports/artifact-process-paired-proof-flow-v1.md`
- `reports/artifact-process-paired-proof-flow-v2.md`
- shared fixture families under `fixtures/`
- bundle-local `fixtures/contract.json`, `runners/contract.json`, and
  `reports/summary.schema.json` when a comparison bundle ships them

## Inputs

- a bundle with `baseline_mode` other than `none`
- a machine-readable `comparison_surface`
- a shared fixture family path
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
- Do not hand-edit `generated/comparison_spine.json` as source truth.
- Do not treat one clean comparison as broad capability growth.
- Do not let style-only movement become capability movement.
- Do not promote a draft comparison bundle by improving generated metadata.
- Do not let `aoa-eval-integrity-check` become a promotion shortcut.
- Do not collapse fixed baseline, peer comparison, and longitudinal movement
  into one score.

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
