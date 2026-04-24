# Changelog

All notable changes to `aoa-evals` will be documented in this file.

The format is intentionally simple and human-first.
Tracking starts with the community-docs baseline for this repository.

## [Unreleased]

## [0.3.3] - 2026-04-23

### Summary

- this patch expands proof coverage across reviewed closeout carry, Agon
  prebindings, contradiction closure, verdict-delta scars, mechanical trials,
  retention rank, schools/lineages/campaigns, KAG/Sophian alignment, and
  Wave XV epistemic evals
- recurrence control-plane integrity, recursor readiness, stats re-grounding,
  Titan canaries/incarnation checks, Experience protocol integrity,
  certification gates, adoption verdicts, governance refs, and post-W10
  runtime integrity review surfaces are added or tightened
- `aoa-evals` remains the bounded proof layer: it carries verdict and
  integrity evidence without becoming owner truth for runtime, memory, roles,
  routing, or source-authored meaning

### Added

- reviewed workspace closeout proof-pressure and carry-note surfaces
- Agon eval prebindings and alignment surfaces across contradiction closure,
  verdict-delta scar, mechanical trial, retention rank, schools/lineages,
  campaigns, KAG/Sophian, and epistemic waves
- recurrence integrity, recursor readiness, stats re-grounding boundary,
  Titan runtime and incarnation canaries, Experience protocol integrity,
  certification gates, adoption verdicts, governance verdict refs, and
  post-W10 runtime integrity proof surfaces

### Changed

- eval review follow-up drift, validator follow-ups, recurrence scorer
  evidence checks, Experience verdict metadata, adoption/gateway metadata, and
  wave4 governance verdict references were tightened

### Validation

- `python scripts/release_check.py`

### Notes

- this patch adds proof and integrity surfaces only; it does not promote evals
  into source, runtime, memory, routing, or role authority

## [0.3.2] - 2026-04-19

### Summary

- this patch adds chaos-wave trace and proof lanes, A2A summon return
  coverage, and a bounded memo writeback-act proof surface
- proof gates, receipt loops, playbook pinning, and sibling-root-aware memo
  evidence handling are tightened across the eval layer
- `aoa-evals` remains the bounded proof and audit layer without absorbing
  owner truth

### Added

- `aoa-memo-writeback-act-integrity` as a bounded draft proof surface for one
  real Phase Alpha runtime-to-memo writeback act
- `runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json`
  plus schema-backed report artifacts for the new writeback-act lane
- chaos wave 1 trace eval bridge surfaces, early proof-pressure evidence,
  A2A summon return checkpoint coverage, and reviewed candidate adoption eval
  lanes

### Changed

- refreshed memo-pilot roadmap, selector, and runtime-promotion guidance so the
  writeback-act lane sits beside recall and contradiction without overclaiming
- eval proof gates, receipt loops, release-audit playbooks pinning, memo
  report sibling-root handling, and proof-carry notes are tightened for the
  current wave

### Validation

- `python scripts/release_check.py`

### Notes

- this patch keeps the release line focused on bounded proof surfaces for
  memo, playbook, A2A, and chaos-wave follow-through


## [0.3.1] - 2026-04-12

### Summary

- this patch adds continuity-oriented eval bundles, diagnosis-cause-discipline
  coverage, and checkpoint proof follow-through
- proof publication and catalog surfaces are refreshed for the current wave
  without widening eval ownership
- `aoa-evals` remains the bounded proof and audit layer

### Added

- checkpoint proof follow-through quest capture, growth-refinery lineage eval
  bundles, diagnosis-cause-discipline coverage, and self-agency continuity
  eval bundles.

### Changed

- proof-artifact publication, catalog surfaces, and dependency alignment are
  refreshed for the current continuity wave.

### Validation

- `python scripts/release_check.py`

### Notes

- detailed continuity-oriented bundle, catalog, and checkpoint-proof changes for this patch remain enumerated below under `Added` and `Changed`

## [0.3.0] - 2026-04-10

### Summary

- this release adds local-text and ring-discipline eval bundles, live eval-result receipt contracts, and latest-sibling canary support
- proof validation, portable-eval expectations, and compact proof lineage readers are hardened across the public corpus
- `aoa-evals` remains the bounded proof and audit layer rather than turning into generic runtime QA ownership

### Validation

- `python scripts/release_check.py`

### Notes

- detailed bundle, report, generated-surface, and operating-surface coverage for this release remains enumerated below under `Added`, `Changed`, and `Included in this release`

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

### Included in this release

- proof-corpus expansions across `bundles/`, `docs/`, `generated/`,
  `examples/`, `fixtures/`, `schemas/`, and `reports/`, including Phase Alpha
  routing surfaces, RPG unlock proof, runtime candidate hardening, and new
  bounded audit posture
- repo-local operating and follow-through surfaces under `.agents/`, `.github/`,
  `AGENTS.md`, `AUDIT.md`, `README.md`, `EVAL_INDEX.md`, `EVAL_SELECTION.md`,
  `QUESTBOOK.md`, `quests/`, `scripts/`, and `tests/`, including quest and
  automation harvest installs, latest-sibling canary support, and route
  clarifications

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
