# Eval Rubric

This document defines the Stage 1 machine-readable fields used in `EVAL.md` frontmatter.

Markdown stays authoritative.
Any generated catalog, selection surface, or summary artifact should remain derived from tracked markdown plus `schemas/`.

See also:
- [Documentation Map](README.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Metadata And Canonical Review

Stage 1 metadata can inform selection, bounded review, portability review, baseline readiness, and canonical review,
but it does not replace explicit review judgment.

- frontmatter fields help reviewers understand maturity, repeatability, portability, and verdict posture
- the same bounded frontmatter layer can support later generated selection and reporting surfaces
- they do not auto-promote an eval bundle to `baseline` or `canonical`
- `portable -> baseline` and `baseline -> canonical` decisions should follow the bounded review contract in [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Field meanings

| field | meaning |
|---|---|
| `maturity_score` | Coarse readiness signal from `1` to `5`. Use `5` for canonical default proof surfaces, `4` for strong baseline evals, `3` for portable evals, and lower values for earlier public states. |
| `rigor_level` | Contract strictness for normal use. `light` fits advisory or exploratory evals, `bounded` fits reusable public bundles with clear limits, `strict` fits evals with hard score semantics, strong fixture discipline, or regression-critical verdict surfaces. |
| `repeatability` | Expected run stability. `low` means results vary meaningfully across runs or environments, `moderate` means some movement is expected but bounded interpretation is still possible, `high` means the result shape should be stable enough for disciplined comparison. |
| `portability_level` | How well the bundle survives outside its birth context. `local-shaped` means still closely tied to one environment, `portable` means generally reusable with bounded adaptation, `broad` means suitable as a wider default proof surface. |
| `baseline_mode` | Whether the bundle is primarily standalone or comparative. Suggested values include `none`, `fixed-baseline`, `previous-version`, `peer-compare`, and `longitudinal-window`. |
| `verdict_shape` | Main result type. Suggested values include `pass-fail`, `categorical`, `scalar-with-interpretation`, `comparative`, and `mixed`. |
| `review_required` | Whether normal public use should still expect explicit human review before strong conclusions are drawn from the eval result. |
| `validation_strength` | Evidence strength for the eval bundle itself. `baseline` means mostly structural validation, `source_backed` means it is grounded in real evaluation needs or repeated failure surfaces, `cross_context` means the bundle has shown stable meaning beyond one local context or review cycle. |
| `public_safety_reviewed_at` | Most recent public-safety review date for the published bundle, formatted as `YYYY-MM-DD`. |
| `export_ready` | Whether the bundle is safe for Stage 1 structured catalog publication. This is about machine-readable publication safety for repo-local outputs, not about graph or AoA export. |
| `relations` | Small structured links to other in-repo eval bundles. Keep the list bounded to direct reusable relationships only. |
| `evidence` | Structured list of tracked note files or review artifacts that justify the bundle's current public posture. |
| `blind_spot_disclosure` | Whether the bundle explicitly names its main blind spots. Suggested values: `required-and-present`, `partial`, `missing`. |
| `score_interpretation_bound` | Whether the bundle explicitly limits how far a score or verdict may be interpreted. Suggested values: `explicit`, `partial`, `missing`. |

## Relation types

Stage 1 keeps relation semantics intentionally small:

| type | use |
|---|---|
| `requires` | The eval assumes another eval surface, scorer, fixture family, or prerequisite proof contract. |
| `complements` | The eval is commonly used alongside another without depending on it directly. |
| `supersedes` | The eval replaces another for the same bounded proof job. |
| `conflicts_with` | The eval should not be treated as jointly compatible with another on the same bounded surface. |
| `used_together_for` | The eval and another bundle often appear in one bounded comparison or review flow. |
| `derived_from` | The eval is a direct bounded derivative of another in-repo eval surface. |
| `checks_integrity_of` | The eval checks the coherence, score semantics, or verdict behavior of another eval bundle. |

This rubric does not introduce graph inference, automatic ranking, or fully automated canonization.

## Evidence kinds

| kind | meaning |
|---|---|
| `origin_need` | Note describing the real quality question, repeated failure mode, or regression surface that caused the eval to exist. |
| `portable_review` | Note showing that the bundle remained meaningful outside its birth context. |
| `baseline_readiness` | Review note showing the eval is stable enough to function as a bounded comparison surface. |
| `canonical_readiness` | Review note showing the eval is strong enough to be recommended by default for its bounded proof class. |
| `integrity_check` | Evidence that the scorer, verdict logic, or report contract was itself checked for coherence. |
| `support_note` | Other tracked support note that materially explains limits, rollout, or interpretation, including comparison-contract notes for comparative summaries. |

## Evidence floor by public posture

Current public expectations should stay small but explicit:

- public starter bundles should carry `origin_need`, `integrity_check`, and `examples/example-report.md`
- status `bounded` should carry a `support_note` that records the bounded review outcome plus failure and readout distinctions
- status `portable`, `baseline`, and `canonical` should carry `portable_review`
- status `canonical` should also carry `canonical_readiness`
- any bundle with `baseline_mode != none` should carry `baseline_readiness`
- any bundle with `report_format: comparative-summary` should carry a `support_note` that names the comparison contract

Comparison-contract notes should stay bounded:

- `fixed-baseline` and `previous-version` notes should name the baseline target, noisy variation, and style-only overread limits
- `peer-compare` notes should name matched conditions and side-by-side interpretation limits
- `longitudinal-window` notes should name ordered windows, cross-window invariants, and cautious movement language

## Stage 1 discipline

Current intended repo posture:

- `export_ready` should be treated as a publication floor, not a recommendation signal
- `maturity_score` should remain coarse and reviewable
- `repeatability` should describe interpretation risk, not pretend to eliminate uncertainty
- `blind_spot_disclosure` should be taken seriously; missing blind spots should block strong claims
- `score_interpretation_bound` should prevent score theater and false universality

Concrete reasons a future bundle might be `export_ready: false`:

- the markdown bundle is public-safe, but its structured metadata is not trustworthy enough yet
- the score semantics are still too unstable for machine-readable publication
- the bundle has unresolved blind-spot or interpretation problems
- the fixture surface is still too local-shaped for public structured selection output

## Review posture reminders

- Keep frontmatter values operational and reviewable.
- Do not treat `relations` as a large graph design surface yet.
- Do not treat `export_ready` as permission for broader AoA or graph export work.
- Do not treat `maturity_score` as a substitute for bounded review.
- If generated catalog output drifts from markdown, fix markdown or rerun the generator; do not hand-edit generated artifacts.
