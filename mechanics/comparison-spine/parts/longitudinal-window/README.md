# Comparison Spine / Longitudinal Window Part

## Role

This part owns repeated-window fixture support plus repeated-window and
stress-recovery window readout dossiers.

## Source Surfaces

- `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v1.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md`
- `mechanics/comparison-spine/parts/longitudinal-window/reports/stress-recovery-window-proof-flow-v1.md`

## Inputs

- bundle-local `baseline_mode` value `longitudinal-window`;
- `comparison_surface` fields such as ordered windows, `anchor_surface`,
  `window_family_label`, `shared_family_path`, `paired_readout_path`, and
  `additional_paired_readout_paths`;
- repeated-window fixture-family contract and stress-recovery window readout
  refs;
- cross-window invariants and cautious movement interpretation notes;
- generated comparison-spine entries derived from source bundle metadata.

## Outputs

- repeated-window fixture-family route;
- repeated-window and stress-recovery proof-flow dossiers;
- bounded movement interpretation guidance for ordered windows;
- validation failures when windows are duplicate, out of order, missing
  invariants, missing readouts, or claiming more growth than the source bundle
  supports.

## Stronger Owner Split

Source proof bundles own the longitudinal claim, ordered windows, invariant
surface, verdict posture, and blind spots.

This part owns shared repeated-window and stress-recovery readout support. It
does not own broad growth proof, runtime health proof, or antifragility
acceptance.

## Boundary

Longitudinal-window fixture and dossier surfaces support ordered-window
reading. They do not turn style-only movement, cleaner later wording, or one
vivid stress-recovery window into broad growth proof.

## Stop-Lines

- Do not treat ordered-window movement as broad growth by association.
- Do not count cleaner later wording as capability movement unless the source
  bundle supports that claim.
- Do not collapse repeated-window and stress-recovery evidence into runtime
  health or antifragility acceptance.
- Do not hide cross-window context changes or invariant drift.
- Do not promote a bundle from repeated-window polish alone.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
