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
- confirm the bounded release scope first
- update `CHANGELOG.md` with the release section that will anchor the human release narrative
- `python -m pip install -r requirements-dev.txt`
- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python -m pytest`

When you need the latest-sibling canary rather than the pinned repo-validation lane, run:
- `python scripts/run_sibling_canary.py --repo-root . --matrix scripts/sibling_canary_matrix.json`

If `aoa-techniques` or `aoa-skills` are not available locally,
the validator will stay permissive about dependency-target existence.
CI is the strict path-existence gate because it checks those sibling repos out into `.deps/`
and exports `AOA_TECHNIQUES_ROOT` plus `AOA_SKILLS_ROOT`.
If `abyss-stack` is not checked out beside `aoa-evals` and not under `~/src/abyss-stack`,
export `ABYSS_STACK_ROOT` to the source checkout so runtime-evidence example refs resolve against tracked schemas.
The canary follows the same source-checkout rule and will prefer `~/src/abyss-stack` over a runtime-like sibling mirror when both exist.

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
- the bundle should include a tracked `origin_need` evidence note
- current public starters should ship `examples/example-report.md`
- current public starters should ship an integrity-review artifact such as `checks/eval-integrity-check.md`
- when a bundle claims machine-readable report artifacts, ship `reports/summary.schema.json` and `reports/example-report.json` together
- when a bundle claims reusable execution artifacts, ship bundle-local `fixtures/contract.json` and/or `runners/contract.json` together with the top-level shared surfaces they reference
- `EVAL_INDEX.md` should include the new public bundle
- `EVAL_SELECTION.md` should be updated if the chooser meaningfully changes

## Baseline or regression release

Before shipping a bundle whose `baseline_mode` is not `none`:
- every `evidence.path` in `eval.yaml` should resolve to a tracked public file
- at least one `baseline_readiness` evidence note should be present
- the frozen baseline contract should be readable by a bounded outside reviewer
- comparative summaries should stay modest about what the bounded comparison proves
- if `report_format` is `comparative-summary`, at least one `support_note` should make the comparison contract explicit
- if the wave materially changes pairing, shared infra, longitudinal posture, or canonical candidacy, add an integrity-sidecar read such as `aoa-eval-integrity-check`

For `longitudinal-window` bundles specifically:
- windows should be ordered and named
- the bounded surface should stay constant across the window sequence
- one public report or summary artifact should exist per window
- context changes that affect comparability should be disclosed explicitly
- movement claims should stay weaker than any tempting growth narrative

## Status promotion releases

Status promotion should remain rare and explicit.

Before shipping a promoted public status:
- `portable`, `baseline`, and `canonical` bundles should carry `portable_review`
- when promoting to `baseline`, `portable_review` should be the public approval trail and should record the reuse boundary explicitly
- `canonical` bundles should also carry `canonical_readiness`
- `comparative-summary` bundles should already carry an explicit comparison-contract `support_note`

Use:
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md) for promotion to `baseline`
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

## Publication record

For current early releases:
- treat the matching `CHANGELOG.md` section as the source of truth for the public release narrative
- after the release-prep change lands on `main`, create a Git tag such as `v0.1.0`
- publish GitHub release notes using the matching changelog section or a clearly equivalent human-first shape

## Final note

`aoa-evals` should release proof surfaces carefully.

A smaller honest release is better than a larger blurry one.
