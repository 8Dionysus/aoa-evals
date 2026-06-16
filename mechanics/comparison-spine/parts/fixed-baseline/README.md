# Comparison Spine / Fixed Baseline Part

## Role

This part owns the shared same-task fixed-baseline fixture family and readout
dossier.

## Source Surfaces

- `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`
- `mechanics/comparison-spine/parts/fixed-baseline/reports/same-task-baseline-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/fixed-baseline/reports/runtime-latency-tradeoff-proof-flow-v1.md`

## Inputs

- bundle-local `baseline_mode` values of `fixed-baseline` or
  `previous-version`;
- `comparison_surface` fields such as `anchor_surface`,
  `baseline_target_label`, `shared_family_path`, and `paired_readout_path`;
- the `frozen-same-task-v1` fixture-family contract;
- same-task baseline readout evidence and integrity sidecar refs;
- generated comparison-spine entries derived from bundle source metadata.

## Outputs

- fixed-baseline fixture-family route for same-task regression claims;
- `same-task-baseline-proof-flow-v1.md` readout dossier;
- `runtime-latency-tradeoff-proof-flow-v1.md` readout dossier;
- bounded baseline interpretation guidance for source bundles and generated
  readers;
- validation failures when fixed-baseline claims lack anchor surfaces, shared
  family paths, paired readouts, or anti-overread notes.

## Stronger Owner Split

Source proof bundles own the fixed-baseline claim, baseline target, verdict
logic, and blind spots.

This part owns shared fixture/readout support for fixed-baseline posture. It
routes bundle promotion, repo-global scoring, and broad growth pressure to
bundle-local review and owner surfaces.

## Boundary

The fixture family and dossier support fixed-baseline comparison claims. They
keep one baseline result inside the source bundle's bounded claim.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| one fixed-baseline result as repo-global score | source bundle review plus comparison-spine bounded read |
| broad growth from same-task regression evidence | `longitudinal-window` evidence plus growth/progression owner review |
| draft, portable, baseline, or canonical bundle promotion | bundle-local review and release/report owner route |
| baseline target as sibling-owner acceptance or runtime health | sibling owner or `abyss-stack` runtime route with comparison evidence as support |
| bundle-local fixture, runner, or report contracts | owning bundle contract path under `evals/` |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
