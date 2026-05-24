# Eval Rubric

This document defines the Stage 1 machine-readable fields used in `EVAL.md` frontmatter.

Markdown stays authoritative.
Any generated catalog, selection surface, or summary artifact should remain derived from tracked markdown plus `schemas/`.

See also:
- [Documentation Map](README.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | Stage 1 metadata meaning guide for `EVAL.md` frontmatter |
| input | frontmatter field, generated catalog pressure, export pressure, relation pressure, maturity pressure, or review evidence gap |
| output | field interpretation, evidence floor, review route, export posture, or bounded metadata repair |
| owner | this guide owns metadata semantics; schemas validate shape; bundle-local files and review notes own concrete claims |
| next route | `docs/EVAL_REVIEW_GUIDE.md`, `docs/SCORE_SEMANTICS_GUIDE.md`, `mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json`, generated catalog builders, or the affected bundle |
| validation | `docs/AGENTS.md#validation` |

## Metadata And Canonical Review

Stage 1 metadata can inform selection, bounded review, portability review, baseline readiness, and canonical review,
while explicit review judgment remains the promotion authority.

- frontmatter fields help reviewers understand maturity, repeatability, portability, and verdict posture
- the same bounded frontmatter layer can support later generated selection and reporting surfaces
- `status` is the primary public maturity signal for low-context readers and generated routing surfaces
- baseline and canonical promotion pressure routes through explicit bounded review
- promotion to `baseline` and `baseline -> canonical` decisions should follow the bounded review contract in [Eval Review Guide](EVAL_REVIEW_GUIDE.md)

## Field meanings

| field | meaning |
|---|---|
| `maturity_score` | Coarse readiness signal from `1` to `5`. Use `5` for canonical default proof surfaces, `4` for strong baseline evals, `3` for portable evals, and lower values for earlier public states. |
| `rigor_level` | Contract strictness for normal use. `light` fits advisory or exploratory evals, `bounded` fits reusable public bundles with clear limits, `strict` fits evals with hard score semantics, strong fixture discipline, or regression-critical verdict surfaces. |
| `repeatability` | Expected run stability. `low` means results vary meaningfully across runs or environments, `moderate` means some movement is expected but bounded interpretation is still possible, `high` means the result shape should be stable enough for disciplined comparison. |
| `portability_level` | How well the bundle survives outside its birth context. `local-shaped` means still closely tied to one environment, `portable` means generally reusable with bounded adaptation, `broad` means suitable as a wider default proof surface. This metadata stays no stronger than the bundle `status`. |
| `baseline_mode` | Whether the bundle is primarily standalone or comparative. Suggested values include `none`, `fixed-baseline`, `previous-version`, `peer-compare`, and `longitudinal-window`. |
| `verdict_shape` | Main result type. Suggested values include `pass-fail`, `categorical`, `scalar-with-interpretation`, `comparative`, and `mixed`. |
| `review_required` | Whether normal public use should still expect explicit human review before strong conclusions are drawn from the eval result. |
| `validation_strength` | Evidence strength for the eval bundle itself. `baseline` means mostly structural validation, `source_backed` means it is grounded in real evaluation needs or repeated failure surfaces, `cross_context` means the bundle has shown stable meaning beyond one local context or review cycle. Treat this as review metadata; routing and recommendation authority stays with bounded review. |
| `public_safety_reviewed_at` | Most recent public-safety review date for the published bundle, formatted as `YYYY-MM-DD`. |
| `export_ready` | Whether the bundle is safe for Stage 1 structured catalog publication. This is about machine-readable publication safety for repo-local outputs; graph or AoA export routes stay outside this field. |
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
| `conflicts_with` | The eval and another surface separate compatibility on the same bounded surface. |
| `used_together_for` | The eval and another bundle often appear in one bounded comparison or review flow. |
| `derived_from` | The eval is a direct bounded derivative of another in-repo eval surface. |
| `checks_integrity_of` | The eval checks the coherence, score semantics, or verdict behavior of another eval bundle. |

Graph inference, automatic ranking, and fully automated canonization route
outside Stage 1 metadata.

## Evidence kinds

| kind | meaning |
|---|---|
| `origin_need` | Note describing the real quality question, repeated failure mode, or regression surface that caused the eval to exist. |
| `portable_review` | Note showing that the bundle remained meaningful outside its birth context, including the public approval trail for baseline promotion. |
| `baseline_readiness` | Review note showing the eval is stable enough to function as a bounded comparison surface. |
| `canonical_readiness` | Review note showing the eval is strong enough to be recommended by default for its bounded proof class. |
| `integrity_check` | Evidence that the scorer, verdict logic, or report contract was itself checked for coherence. |
| `support_note` | Other tracked support note that materially explains limits, rollout, or interpretation, including comparison-contract notes for comparative summaries. |

## Evidence floor by public posture

Current public expectations should stay small but explicit:

- public starter bundles should carry `origin_need`, `integrity_check`, and
  `evals/<family>/<eval>/examples/example-report.md`
- status `bounded` should carry a `support_note` that records the bounded review outcome plus failure and readout distinctions
- status `portable`, `baseline`, and `canonical` should carry `portable_review`; baseline promotions should use this as the public review trail
- status `canonical` should also carry `canonical_readiness`
- any bundle with `baseline_mode != none` should carry `baseline_readiness`
- any bundle with `report_format: comparative-summary` should carry a `support_note` that names the comparison contract
- once a bundle claims reusable proof artifacts, those artifacts should become reviewable too: shared fixture contract, runner contract, report schema, and example report

Comparison-contract notes should stay bounded:

- `fixed-baseline` and `previous-version` notes should name the baseline target, noisy variation, and style-only overread limits
- `peer-compare` notes should name matched conditions and side-by-side interpretation limits
- `longitudinal-window` notes should name ordered windows, cross-window invariants, and cautious movement language

## Stage 1 discipline

Current intended repo posture:

- `export_ready` is a publication floor; recommendation signals route through
  bounded review
- `status` should remain the dominant public maturity signal on thin routing surfaces
- `portability_level` should stay monotonic with `status` rather than outrun it
- `maturity_score` should remain coarse and reviewable
- `repeatability` should describe interpretation risk while uncertainty remains explicit
- `blind_spot_disclosure` should be taken seriously; missing blind spots should block strong claims
- `score_interpretation_bound` should prevent score theater and false universality

Concrete reasons a future bundle might be `export_ready: false`:

- the markdown bundle is public-safe, but its structured metadata still needs trust hardening
- the score semantics are still too unstable for machine-readable publication
- the bundle has unresolved blind-spot or interpretation problems
- the fixture surface is still too local-shaped for public structured selection output

## Review Pressure Routes

Keep frontmatter values operational and reviewable.

| Pressure | Route |
| --- | --- |
| `relations` wants to become a large graph design surface | keep Stage 1 relations direct and bounded; route graph work to a later owner surface |
| `export_ready` wants to authorize broader AoA or graph export | keep it as repo-local structured publication safety |
| `maturity_score` wants to replace bounded review | route promotion through [Eval Review Guide](EVAL_REVIEW_GUIDE.md) |
| generated catalog output drifts from markdown | fix markdown or rerun the generator; generated artifacts stay derived |
