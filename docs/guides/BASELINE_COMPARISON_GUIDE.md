# Baseline Comparison Guide

This guide defines when an eval bundle is ready to function as a baseline or comparison surface in `aoa-evals`.

Use it when a bundle already looks portable and useful, and the next decision is
whether repeated comparison would mean something bounded and trustworthy.

See also:
- [Documentation Map](../README.md)
- [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | baseline and comparison readiness guide |
| input | portable-looking bundle, repeated-run pressure, fixed-baseline pressure, longitudinal-window pressure, style-only movement, or baseline promotion pressure |
| output | baseline-ready route, deferral route, style-only route, or comparison hygiene route |
| owner | this guide owns docs-level baseline reading discipline; bundle-local `EVAL.md`, `eval.yaml`, comparison-spine parts, and reports own concrete evidence |
| next route | `mechanics/comparison-spine/parts/fixed-baseline/`, `mechanics/comparison-spine/parts/longitudinal-window/`, `docs/guides/FIXTURE_SURFACE_GUIDE.md`, `docs/guides/SCORE_SEMANTICS_GUIDE.md`, or bundle-local review |
| validation | `docs/AGENTS.md#validation` |

## What baseline means

A baseline bundle carries more than rerun ability.

A baseline bundle is a bundle whose repeated comparison surface is stable enough
that before-vs-after reading tells the truth in a bounded way.

## Baseline eligibility floor

Before calling a bundle baseline-ready, require:
- a stable bounded claim
- explicit per-case and bundle-level result semantics
- a fixture surface that is stable or replaceable by contract
- a schema-backed public report artifact and runner contract when the comparison surface is already materialized publicly
- repeatability strong enough for bounded comparison
- blind spots named clearly
- a report shape that makes comparison legible

Missing conditions route to bundle-local hardening before public comparison.

## Comparison hygiene

A careful comparison keeps stable:
- the object under evaluation
- the claim class
- the fixture surface, or its declared replacement contract
- the scorer or verdict logic
- the interpretation contract

A careful comparison also names:
- environment changes
- policy changes
- reviewer changes if they matter materially
- any case removals or additions

## Longitudinal-window hygiene

When `baseline_mode` is `longitudinal-window`, keep explicit:
- ordered named windows
- one named bounded surface that stays constant across those windows
- one public report or summary artifact per window
- one shared window-family contract or explicit replacement rule when the surface is materialized publicly
- context changes that materially affect comparability

Comparability pressure routes:

| Pressure | Route |
| --- | --- |
| proof job changed between windows | separate comparison family or fresh owner review |
| case family drift disclosure is missing | replacement-contract disclosure before movement verdict |
| report polish is the main visible difference | style-only route and `no clear directional movement` |
| reviewer or policy changes swamp the bounded surface | context disclosure plus owner review before comparison claim |

If comparability is weakened materially, prefer:
- `mixed or unstable movement`
- or `no clear directional movement`

before a cleaner growth story.

## Improvement, regression, and noisy variation

| reading | use when | caution |
|---|---|---|
| improvement | The later result is stronger on the same bounded surface with stable semantics. | Keep nicer summaries below stronger evidence. |
| regression | The later result is weaker on the same bounded surface in a way the contract can explain. | Name whether the regression is outcome, process, boundary, or comparison noise. |
| noisy variation | The movement is too small, too unstable, or too style-shaped for a stronger reading. | Use this to preserve uncertainty. |

## Anti-style-drift discipline

Style-only signals route by default to:
- artifact improvement
- report improvement
- noisy variation

Capability growth requires movement in the bounded evidence surface the bundle
claims to measure.

## Baseline deferral routes

| Pressure | Route |
| --- | --- |
| one run depends too much on reviewer intuition | bundle-local review hardening |
| fixture surface is too local or too flattering | `docs/guides/FIXTURE_SURFACE_GUIDE.md` and fixture replacement contract |
| verdict meanings are muddy | `docs/guides/SCORE_SEMANTICS_GUIDE.md` and bundle-level result semantics |
| style changes swamp real movement | noisy variation route plus comparison-spine readout |
| repeated runs preserve different proof jobs | reset comparison family before baseline claim |

## Final note

Baseline is a trust claim about comparison.

When comparison meaning stays unstable, route to baseline deferral until the
proof job, fixture contract, and verdict semantics stabilize.
