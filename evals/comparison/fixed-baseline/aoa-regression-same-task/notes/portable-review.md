# Portable Review

This note is the `portable_review` evidence for moving `aoa-regression-same-task` to `baseline`.

Outcome: approve for baseline

Approve for baseline when:
- the frozen baseline target stays explicit as `RS-v1 frozen bounded workflow reference`
- baseline and candidate stay on the same bounded case family with the same comparison rubric
- per-case comparison notes stay visible before any bundle-level regression verdict
- style-only differences stay bounded to noisy variation unless the workflow evidence also moved

Reuse boundary:
- another repo must preserve the same frozen case family, baseline dossier, and comparison rubric
- another repo must preserve the same evidence shape: baseline note, candidate note, and comparative reading per case
- another repo may rename local cases, but it should not widen the workflow surface or move the baseline target after freezing it

Why this is baseline but not canonical:
- this is the first public baseline starter for same-task regression in `aoa-evals`
- it is comparison-usable across bounded updates, but it is not yet the default proof surface for every comparative claim class
- portability here is about preserving the frozen comparison contract, not about broad cross-context default use
