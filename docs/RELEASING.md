# Releasing `aoa-evals`

This guide defines the lightweight publication flow for docs and public eval surfaces in `aoa-evals`.

This is a v1 guide.
It describes bounded release discipline, not full release automation.

See also:
- [Documentation Map](README.md)
- [Contributing](../CONTRIBUTING.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Release units

Common release-sized changes include:
- docs-only doctrine updates
- one new draft eval bundle
- one focused improvement to an existing bundle
- one status transition such as `portable -> baseline`
- one validator or schema improvement

Prefer bounded releases over mixed large batches.

## Local release checks

Recommended local release loop:
- `python -m pip install -r requirements-dev.txt`
- `python scripts/build_catalog.py`
- `python scripts/validate_repo.py`
- `python -m pytest`

## Docs-only release

Before shipping docs-only changes:
- all tracked links in `docs/README.md` should resolve
- wording should align with canonical guides
- local-only working files should remain unreferenced
- the update should clarify doctrine rather than widen claims casually

## New public draft bundle

Before shipping a new public draft bundle:
- the bundle should follow the canonical `EVAL.md` shape
- the bounded claim should be explicit
- fixtures should be public-safe or replaceable by contract
- scoring or verdict logic should be reviewable
- blind spots should be named clearly
- the bundle should include explicit manifest evidence for its public support artifacts
- current public starters should ship `examples/example-report.md`
- current public starters should ship an integrity-review artifact such as `checks/eval-integrity-check.md`
- `EVAL_INDEX.md` should include the new public bundle
- `EVAL_SELECTION.md` should be updated if the chooser meaningfully changes

## Baseline or regression release

Before shipping a bundle whose `baseline_mode` is not `none`:
- every `evidence.path` in `eval.yaml` should resolve to a tracked public file
- at least one `baseline_readiness` evidence note should be present
- the frozen baseline contract should be readable by a bounded outside reviewer
- comparative summaries should stay modest about what the bounded comparison proves

For `longitudinal-window` bundles specifically:
- windows should be ordered and named
- the bounded surface should stay constant across the window sequence
- one public report or summary artifact should exist per window
- context changes that affect comparability should be disclosed explicitly
- movement claims should stay weaker than any tempting growth narrative

## Status promotion releases

Status promotion should remain rare and explicit.

Use:
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md) for `portable -> baseline`
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md) for `baseline -> canonical`

Do not use metadata alone as a release gate for promotion.

## Local-only boundary

Tracked public docs and bundles should not depend on local-only material such as:
- private seeds
- local planning files
- unpublished fixture sources
- hidden reviewer notes

If a tracked surface needs one of those to make sense,
it is not ready to publish in its current form.

## Final publication check

Before finalizing a change:
- confirm the public claim stayed bounded
- confirm summaries do not overstate the evidence
- confirm blind spots and interpretation notes still match the current wording
- confirm starter-bundle integrity artifacts still match current manifest and chooser wording
- confirm `generated/eval_catalog.json` and `generated/eval_catalog.min.json` were rebuilt from current markdown and manifest sources
- confirm release scope is small enough that reviewers can reason about it directly

## Final note

`aoa-evals` should release proof surfaces carefully.

A smaller honest release is better than a larger blurry one.
