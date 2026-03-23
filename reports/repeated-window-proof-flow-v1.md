# Repeated-Window Proof Flow v1

This dossier defines the first materialized repeated-window proof flow across:
- `aoa-longitudinal-growth-snapshot`

## Shared window family

Use `fixtures/repeated-window-bounded-v1/README.md` as the shared public window-family contract.

The repeated-window read should preserve:
- one named anchor workflow surface
- ordered named windows
- one public report or summary artifact per window
- one honest movement read that stays weaker than the strongest-looking local change

## Read order

1. Name the ordered windows and the anchor workflow surface.
2. Read the public report or summary artifact for each window.
3. Assign per-window or per-transition movement notes before the bundle-level verdict.
4. Read the bounded longitudinal verdict.
5. If the longitudinal surface is being used for a maturity or wording wave, add `aoa-eval-integrity-check` as the sidecar that checks whether the public movement read is still bounded and non-theatrical.

## Required movement shapes

- `bounded improvement signal`
- `no clear directional movement`
- `mixed or unstable movement`
- `bounded regression signal`

## Distinctness boundary

This repeated-window proof flow is not a substitute for `aoa-regression-same-task`.

`aoa-regression-same-task` asks whether one candidate materially regressed against one frozen baseline on the same bounded task family.
This dossier asks whether one named bounded workflow surface shows modest directional movement across ordered windows.

## Anti-overread rule

Do not collapse this repeated-window flow into:
- proof of broad capability growth
- proof that every nearby workflow diagnostic improved
- a replacement for same-task frozen-baseline comparison
- a myth-making dashboard for long-horizon progress
