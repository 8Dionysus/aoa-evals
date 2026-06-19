# Releasing `aoa-evals`

This guide defines the lightweight publication flow for docs and public eval surfaces in `aoa-evals`.

This is a v1 guide.
It keeps release discipline bounded and routes automation, landing, and
publication state to their owner surfaces.

See also:
- [Documentation Map](../README.md)
- [Contributing](../../CONTRIBUTING.md)
- [Eval Review Guide](../guides/EVAL_REVIEW_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | root release process guide for docs and public eval surfaces |
| input | bounded release scope, docs-only release, draft bundle, baseline/regression release, status promotion, readiness audit, or publication question |
| output | release scope route, local check route, readiness/live-status route, changelog route, or publication record route |
| owner | this guide for the release procedure; `CHANGELOG.md` for public narrative; release-support mechanics for readiness and handoff artifacts; GitHub surfaces for live PR/CI/merge state |
| next route | `mechanics/release-support/AGENTS.md`, `mechanics/release-support/README.md`, `CHANGELOG.md`, `scripts/release_check.py`, `.github/AGENTS.md`, affected source bundle, or generated builder |
| tools | nearest `AGENTS.md`, release-support validation lane, root validation lane, release check, generated-reader checks, and latest-sibling canary when current sibling compatibility is part of the release claim |
| validation | `docs/AGENTS.md#validation` and `mechanics/release-support/AGENTS.md#validation` |

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
- follow `mechanics/release-support/AGENTS.md#validation` for release-route
  commands
- follow root `AGENTS.md#verify` when the release touches generated readers or
  repository-wide proof topology
- when release audit reaches the OS Abyss report-index artifact bundle check,
  provide `ABYSS_MACHINE_REPO_ROOT` or an installed `abyss_machine` verifier if
  there is no sibling `abyss-machine` checkout

When you need the latest-sibling canary rather than the pinned repo-validation
lane, use the boundary-bridge validation route in
`mechanics/boundary-bridge/AGENTS.md#validation`.

With pinned sibling repos unavailable locally, the validator stays permissive
about dependency-target existence. CI is the strict path-existence gate because
it checks sibling repos out into `.deps/` and exports the matching `AOA_*_ROOT`
variables, including `AOA_MEMO_ROOT`.
When no `abyss-stack` checkout exists beside `aoa-evals` or under
`~/src/abyss-stack`, export `ABYSS_STACK_ROOT` to the source checkout so
runtime evidence example refs resolve against tracked schemas.
The canary follows the same source-checkout rule and will prefer `~/src/abyss-stack` over a runtime-like sibling mirror when both exist.

The latest-sibling canary and GitHub `Repo Validation` answer different
questions: the canary checks current local sibling truth, while GitHub `Repo
Validation` checks the pinned public landing lane in
`.github/workflows/repo-validation.yml`.

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
- current public starters should ship `evals/<family>/<eval>/examples/example-report.md`
- current public starters should ship an integrity-review artifact such as `checks/eval-integrity-check.md`
- when a bundle claims machine-readable report artifacts, ship
  `evals/<family>/<eval>/reports/summary.schema.json` and
  `evals/<family>/<eval>/reports/example-report.json` together
- when a bundle claims reusable execution artifacts, ship bundle-local
  `evals/<family>/<eval>/fixtures/contract.json` and/or
  `evals/<family>/<eval>/runners/contract.json` together with the active
  mechanic-local shared surfaces they reference
- `EVAL_INDEX.md` should include the new public bundle
- `EVAL_SELECTION.md` should be updated if the chooser meaningfully changes

## Baseline or regression release

Before shipping a bundle with active baseline mode:
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
- [Eval Review Guide](../guides/EVAL_REVIEW_GUIDE.md) for promotion to `baseline`
- [Eval Review Guide](../guides/EVAL_REVIEW_GUIDE.md) for `baseline -> canonical`

Use bundle-local review as the promotion release gate; metadata carries
supporting evidence.

## Local-only boundary

Tracked public docs and bundles route away from local-only material such as:
- private seeds
- local planning files
- unpublished fixture sources
- hidden reviewer notes

A tracked surface that needs one of those for meaning stays in local review
until public-safe support exists.

## Final publication check

Before finalizing a change:
- confirm the public claim stayed bounded
- confirm summaries stay within the evidence
- confirm blind spots and interpretation notes still match the current wording
- confirm starter-bundle integrity artifacts still match current manifest and chooser wording
- confirm `generated/eval_catalog.json` and `generated/eval_catalog.min.json`
  were rebuilt from current markdown and manifest sources when the release route
  intentionally changes generated readers
- confirm release scope is small enough that reviewers can reason about it directly

For a large accumulated refactor, read the release-support artifacts through
their live-status routes:

| Artifact | Read as | Live route |
| --- | --- | --- |
| `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` | local release-prep reviewability evidence | current git, GitHub, tag, release, PR, and objective evidence |
| `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` | requirement-by-requirement handoff evidence | current objective audit and landing evidence |
| `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` | pre-PR snapshot for candidate branch, commit, PR title/body, validation, and landing steps | current git and GitHub evidence for live branch, commit, push, PR, GitHub `Repo Validation`, merge, tag, and GitHub Release status |

## Publication record

For current early releases:
- treat the matching `CHANGELOG.md` section as the source of truth for the public release narrative
- after the release-prep change lands on `main`, create a Git tag such as `v0.1.0`
- publish GitHub release notes using the matching changelog section or a clearly equivalent human-first shape

## Final note

`aoa-evals` should release proof surfaces carefully.

A smaller honest release is better than a larger blurry one.
