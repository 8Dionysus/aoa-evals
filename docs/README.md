# Documentation Map

This file is the human-first entrypoint for the repository's `docs/` surface.

Use it when you want to understand **which doc to open next** without guessing from filenames alone.

## Start Here

Choose the path that matches your question:

- I need to understand what this repository means by evaluation:
  - [Eval Philosophy](EVAL_PHILOSOPHY.md)
  - [Architecture](ARCHITECTURE.md)
- I need to pick or inspect an eval bundle:
  - [Eval Selection](../EVAL_SELECTION.md)
  - [Eval Index](../EVAL_INDEX.md)
- I need to understand status, review posture, or canonization:
  - [Eval Rubric](EVAL_RUBRIC.md)
  - [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- I need to understand score and verdict boundaries:
  - [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
  - [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
- I need to understand portability, fixtures, blind spots, or baseline comparison:
  - [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
  - [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
  - [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
  - [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- I need release process guidance:
  - [Releasing `aoa-evals`](RELEASING.md)

## Surface Types

### Generated reader surfaces

These are reader-facing navigation artifacts derived from authoritative markdown and generated data.

- [Eval Selection](../EVAL_SELECTION.md)
  - use when you need one bounded eval choice by category, status, claim type, or nearby relation
- [Eval Index](../EVAL_INDEX.md)
  - use when you need the current public eval map
- `generated/eval_catalog.json`
  - use when a reader or router needs the full derived catalog with dependency refs, relations, and evidence metadata
- `generated/eval_catalog.min.json`
  - use when a reader or router needs the thin projection surface for routing and indexing
- `generated/eval_capsules.json`
  - use when a local runtime needs compact eval cards derived from bounded claim, trigger boundary, blind spots, and interpretation guidance

### Authored review and governance guides

These are human-authored guides that define bounded review, score semantics, and publication discipline.

- [Eval Rubric](EVAL_RUBRIC.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
- [Releasing `aoa-evals`](RELEASING.md)

### Portability and boundary guides

These guides explain what makes an eval bundle portable, bounded, and honest about its limits.

- [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)

## Recommended Reading Paths

### New reader path

1. [README](../README.md)
2. [EVAL_INDEX](../EVAL_INDEX.md)
3. [Eval Philosophy](EVAL_PHILOSOPHY.md)
4. [Architecture](ARCHITECTURE.md)
5. [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
6. one concrete `EVAL.md` bundle

### Reviewer path

1. [Eval Rubric](EVAL_RUBRIC.md)
2. [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
3. [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
4. one eval bundle plus its `notes/`
5. [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
6. [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

### Eval author path

1. [Eval Philosophy](EVAL_PHILOSOPHY.md)
2. [Architecture](ARCHITECTURE.md)
3. [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)
4. [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)
5. [Fixture Surface Guide](FIXTURE_SURFACE_GUIDE.md)
6. [Blind Spot Disclosure Guide](BLIND_SPOT_DISCLOSURE_GUIDE.md)
7. [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)
8. [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)

## Companion Repository Surfaces

These are outside `docs/` but matter when navigating the repo:

- [README](../README.md)
- [EVAL_INDEX](../EVAL_INDEX.md)
- [EVAL_SELECTION](../EVAL_SELECTION.md)
- [CONTRIBUTING](../CONTRIBUTING.md)
- [Eval Template](../templates/EVAL.template.md)

## Notes

- Prefer generated reader surfaces when the question is "which eval should I inspect next?"
- Prefer `generated/eval_catalog*.json` when the question is "what is the deterministic machine-readable eval surface right now?"
- Prefer `generated/eval_capsules.json` when the question is "what is the smallest local runtime card for this eval?"
- Prefer authored guides when the question is "what does this repo mean by this score, verdict, or boundary?"
- Prefer boundary guides when the question is "is this bundle really portable and honest enough to publish?"
- Treat the docs listed here as the canonical wording layer for future public bundle authoring.
