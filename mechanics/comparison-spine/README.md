# Comparison Spine Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/comparison-spine/` routes the operation that keeps baseline,
peer-compare, and longitudinal-window proof claims bounded.

Source bundles and reports keep result meaning, status, and promotion posture.
This package keeps comparison claim posture, shared comparison artifacts,
generated spine derivation, and bounded comparison reading visible.

## Owned Operation

`comparison claim -> bundle comparison_surface -> shared proof artifacts -> generated comparison spine -> bounded comparison read`

This package routes the comparison operation. Source claim meaning stays in
`evals/**/EVAL.md` and `evals/**/eval.yaml`.

## Source Surfaces

- `mechanics/comparison-spine/PARTS.md`
- `mechanics/comparison-spine/parts/README.md`
- `docs/COMPARISON_SPINE_GUIDE.md`
- `docs/BASELINE_COMPARISON_GUIDE.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
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
- bundle-local `evals/<family>/<eval>/fixtures/contract.json`,
  `evals/<family>/<eval>/runners/contract.json`, and
  `evals/<family>/<eval>/reports/summary.schema.json` when a comparison bundle
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
- source-aligned comparison metadata in eval frontmatter and `eval.yaml`
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

| Pressure | Route |
| --- | --- |
| comparison bundle placement | keep source comparison bundles under `evals/` |
| bundle-local fixture, runner, or report contract placement | keep contracts under the owning bundle unless a part-local shared artifact owns the route |
| `generated/comparison_spine.json` drift | fix the source bundle, builder, or part-local readout and rerun the generated check |
| one clean comparison read as broad capability growth | return to the declared comparison mode and bounded bundle claim |
| style-only movement read as capability movement | keep style-only movement below capability movement |
| draft comparison bundle looks promoted by generated metadata | route promotion through bundle-local review and release surfaces |
| `aoa-eval-integrity-check` used as a promotion shortcut | keep it as an integrity sidecar below promotion routes |
| fixed baseline, peer comparison, and longitudinal movement collapse into one score | keep the three comparison modes separate |

## Provenance

Use `mechanics/comparison-spine/PROVENANCE.md` as the active-to-archive bridge when auditing former root
comparison fixture family placement. New comparison work starts from this
README, `PARTS.md`, and the active part.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this package before:

- changing `baseline_mode`;
- adding or changing `comparison_surface`;
- editing comparison spine docs or generated comparison readers;
- changing fixed-baseline, peer-compare, or longitudinal-window report routes;
- changing wording that could imply broad growth, global scoring, or promotion
  by association.
