# Changelog

All notable changes to `aoa-evals` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

## [0.3.0] - 2026-04-10

### Added

- local-text and ring-discipline eval bundles plus antifragility posture and
  fourth-wave stress-recovery evals
- live eval-result receipt contracts and publisher support together with a
  latest-sibling canary workflow
- repo-local project-foundation, session-harvest, and automation-opportunity
  skill surfaces for proof-repo follow-through

### Changed

- hardened proof validation, portable-eval expectations, and compact proof
  lineage readers across the current public corpus
- clarified proof-route, validator, and AGENTS guidance around the next-wave
  bounded proof posture

## [0.2.0] - 2026-04-01

Second public release of `aoa-evals`.

This changelog entry uses the release-prep merge date.

### Summary

- current public corpus now ships as `18` public eval bundles, up from `15` in `v0.1.0`
- this release extends the repo with progression evidence, downstream feed contracts, questbook source-proof surfaces, and runtime candidate intake/template-index surfaces
- review posture is stronger for operator-facing runtime audit and intake flows while the repository remains bounded proof canon rather than a generic benchmark dump

### Added

- progression evidence adjunct surfaces for the current public proof contour
- eval downstream feed contracts for sibling consumers
- questbook source-proof surfaces and live questbook projections from quest YAML
- runtime candidate template index surfaces under `generated/runtime_candidate_template_index.min.json`
- runtime candidate intake surfaces under `generated/runtime_candidate_intake.min.json`

### Changed

- hardened runtime candidate template indexing for operator audit and review prep
- clarified portable-eval and contract wording across the public proof surface
- fixed source-root handling around `abyss-stack`-adjacent resolution in the local validation path

### Included in this release

- `18` public eval bundles under `bundles/`
- current generated reader and comparison surfaces under `generated/`, including the runtime candidate template/index families

### Validation

- `python scripts/build_catalog.py`
- `python scripts/build_catalog.py --check`
- `python scripts/validate_repo.py`
- `python -m pytest`

### Notes

- this remains a bounded proof release, not a claim that every current public bundle is equally mature or that `aoa-evals` has become a generic runtime QA repository

## [0.1.0] - 2026-03-23

First public release of `aoa-evals` as the bounded proof-canon repository in the AOA public surface.

This changelog entry uses the release-prep merge date.

### Summary

- current public corpus now ships as one bounded release with `15` public eval bundles
- current public maturity is explicitly mixed rather than flattened:
  - `9` `bounded` bundles
  - `1` `baseline` bundle
  - `5` `draft` bundles
- release messaging remains intentionally modest:
  - only `aoa-regression-same-task` is a public `baseline` surface
  - `draft`, `comparative`, and `longitudinal` surfaces should not be read more strongly than their current status and wording support

### Added

- first public release of `aoa-evals` as a portable proof-surface repository for bounded claims about workflow quality, boundaries, artifact quality, regressions, and repeated-window movement
- public eval corpus across workflow, boundary, stress, artifact, regression, comparative, capability, and longitudinal surfaces
- derived reader and runtime surfaces:
  - `generated/eval_catalog.json`
  - `generated/eval_catalog.min.json`
  - `generated/eval_capsules.json`
  - `generated/comparison_spine.json`
  - `generated/eval_sections.full.json`
- shared proof-flow dossiers under `reports/` for same-task baseline, artifact/process paired reading, comparison-spine reading, and repeated-window reading
- repo-owned validation helpers under `scripts/` plus the GitHub Actions repo validation workflow under `.github/workflows/repo-validation.yml`
- public repository entry and governance surfaces including `README.md`, `docs/README.md`, `docs/ARCHITECTURE.md`, `docs/EVAL_PHILOSOPHY.md`, `docs/RELEASING.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `EVAL_INDEX.md`, and `EVAL_SELECTION.md`

### Included in this release

- eval bundles under `bundles/` plus the current repository-wide chooser and index in `EVAL_SELECTION.md` and `EVAL_INDEX.md`
- shared fixtures, scorers, runner contracts, schemas, templates, examples, and report artifacts that keep the current eval corpus reviewable and portable
- the current comparison-spine layer anchored by:
  - `aoa-regression-same-task` as the only public `baseline` starter
  - `aoa-output-vs-process-gap` as a draft bridge surface
  - `aoa-longitudinal-growth-snapshot` as a draft repeated-window surface
  - `aoa-eval-integrity-check` as the bounded integrity sidecar
- the current artifact/process and trace-adjacent proof surfaces, including shared dossiers under `reports/` and bridge guidance in `docs/TRACE_EVAL_BRIDGE.md`

### Validation

Documented local validation path for this release:

- `python -m pip install -r requirements-dev.txt`
- `python scripts/build_catalog.py`
- `python scripts/validate_repo.py`
- `python -m pytest`

### Notes

- this is the first public release of the repository, not a claim that every current public bundle is equally mature
- only `aoa-regression-same-task` currently has public `baseline` status; the other comparative and longitudinal surfaces remain draft and should stay weaker than any broad growth or baseline-by-association reading
- this release remains a repository release of docs, eval bundles, schemas, generated reader surfaces, and validation helpers rather than a package or registry artifact
- publishing to PyPI, npm, or other registries is out of scope for `v0.1.0`
