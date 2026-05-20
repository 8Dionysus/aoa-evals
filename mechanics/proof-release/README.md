# Proof Release Mechanic

## Role

`mechanics/proof-release/` routes the operation that prepares and checks one
bounded `aoa-evals` release publication.

It is not the changelog, release automation, GitHub workflow owner, proof
bundle source, generated catalog, or authority to strengthen eval claims.

## Owned Operation

`bounded release scope -> changelog narrative -> release audit -> Repo Validation -> tag and GitHub release notes -> post-release proof posture`

This package routes release proof publication work. Source proof meaning stays
in `bundles/*/EVAL.md`, `bundles/*/eval.yaml`, reports, schemas, and authored
guides. Release publication carries those surfaces; it does not make them
stronger.

In shorter form: release publication does not strengthen eval claims.

## Source Surfaces

- `docs/RELEASING.md`
- `CHANGELOG.md`
- `scripts/release_check.py`
- `.github/workflows/repo-validation.yml`
- `.github/AGENTS.md`
- `README.md` current release line
- `docs/AGENTS_ROOT_REFERENCE.md`
- `reports/proof-release-readiness-audit-v1.json`
- `reports/strategic-closeout-audit-v1.json`
- `reports/release-prep-pr-handoff-v1.json`
- generated catalog check through `python scripts/build_catalog.py --check`
- repository validation through `python scripts/validate_repo.py`
- test gate through `python -m pytest -q tests`
- latest sibling canary route through `python scripts/run_sibling_canary.py --repo-root . --matrix scripts/sibling_canary_matrix.json`

## Inputs

- one bounded release scope
- the matching `CHANGELOG.md` section that anchors the public release narrative
- changed source proof bundles, docs, schemas, mechanics, generated surfaces, or
  support artifacts
- release audit output from `scripts/release_check.py`
- optional latest-sibling canary output when current sibling compatibility is
  part of the release claim
- GitHub `Repo Validation` result when landing through PR

## Outputs

- reviewable release-prep diff
- optional readiness audit such as
  `reports/proof-release-readiness-audit-v1.json`
- refreshed generated catalogs when source inputs changed
- local release audit result
- PR body or release handoff that names changed surfaces, validation, skipped
  checks, and remaining risk
- Git tag and GitHub release notes only after the release-prep change lands on
  `main`

## Stronger Owner Split

The release route packages and publishes proof surfaces. It does not decide
whether a proof claim is true.

Bundle-local proof objects remain stronger than release notes. `CHANGELOG.md`
is the human public release narrative, not proof authority. GitHub `Repo
Validation` is a landing gate, not a substitute for bundle-local review. The
Git tag records a published state; it does not promote draft, baseline, or
canonical status by itself.

Sibling repositories keep their own stronger truth. Latest-sibling canary
results may prove compatibility posture for release review, but they do not
transfer sibling authority into `aoa-evals`.

## Readiness Audit

`reports/proof-release-readiness-audit-v1.json` is a local readiness audit for
the accumulated strategic refactor diff.

It may say the diff is ready for release-prep review after local gates pass. It
must also say that no tag, GitHub Release, PR approval, GitHub `Repo
Validation`, eval result receipt, sibling mutation, or long-goal completion has
occurred.

## Strategic Closeout Audit

`reports/strategic-closeout-audit-v1.json` is a wider local handoff audit for
the accumulated strategic refactor plan.

It may say the local refactor is ready for owner/landing review. It must also
say that the long goal is not complete until the diff is landed, GitHub `Repo
Validation` is observed, and a final owner-visible completion audit can be made
honestly.

## Release Prep PR Handoff

`reports/release-prep-pr-handoff-v1.json` is the pre-PR owner landing handoff
snapshot for the accumulated strategic refactor.

It may prepare a candidate branch, commit message, PR title, PR body, changed
surface groups, validation list, and landing steps. It must also say that at
snapshot time no branch, commit, push, PR had occurred: no branch, commit, push,
PR, GitHub `Repo Validation`, merge, tag, GitHub Release, live receipt, runtime
acceptance, sibling mutation, or goal completion had occurred. After a branch or
PR exists, current git and GitHub state supersedes the snapshot for live status.

## Boundaries

- Do not batch unrelated proof changes into one release because the audit is
  green.
- Do not let `scripts/release_check.py` replace bundle-local review.
- Do not publish a tag or GitHub release from this package route alone.
- Do not treat a readiness audit as a published release.
- Do not turn release notes into eval verdict authority.
- Do not use `CHANGELOG.md` to rewrite source proof meaning.
- Do not weaken validation to make a release pass.
- Do not claim current sibling compatibility unless the relevant canary or CI
  path was run.
- Do not use repo-prefixed release titles when the repo's human-facing release
  convention expects a plain tag such as `v0.3.3`.

## Validation

After changing proof-release route surfaces, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/release_check.py
```

When generated surfaces are changed intentionally, rebuild from source and then
run:

```bash
python scripts/build_catalog.py --check
python scripts/generate_eval_report_index.py --check
python scripts/generate_runtime_candidate_template_index.py --check
python scripts/generate_runtime_candidate_intake.py --check
python scripts/generate_phase_alpha_eval_matrix.py --check
```

When release scope depends on current sibling refs, run:

```bash
python scripts/run_sibling_canary.py --repo-root . --format json
```

## Next Route

Use this package before:

- preparing a release section in `CHANGELOG.md`;
- changing `docs/RELEASING.md`;
- changing `scripts/release_check.py`;
- changing `.github/workflows/repo-validation.yml`;
- creating a PR intended to become a release-prep branch;
- creating or correcting a GitHub Release for `aoa-evals`.
