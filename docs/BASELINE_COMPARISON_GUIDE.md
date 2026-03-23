# Baseline Comparison Guide

This guide defines when an eval bundle is ready to function as a baseline or comparison surface in `aoa-evals`.

Use it when a bundle already looks portable and useful,
but you still need to decide whether repeated comparison would mean something bounded and trustworthy.

See also:
- [Documentation Map](README.md)
- [Eval Review Guide](EVAL_REVIEW_GUIDE.md)
- [Score Semantics Guide](SCORE_SEMANTICS_GUIDE.md)

## What baseline means

A baseline bundle is not just a bundle that can be rerun.

A baseline bundle is a bundle whose repeated comparison surface is stable enough
that before-vs-after reading tells the truth in a bounded way.

## Baseline eligibility floor

Before calling a bundle baseline-ready, it should already have:
- a stable bounded claim
- explicit per-case and bundle-level result semantics
- a fixture surface that is stable or replaceable by contract
- a schema-backed public report artifact and runner contract when the comparison surface is already materialized publicly
- repeatability strong enough for bounded comparison
- blind spots named clearly
- a report shape that makes comparison legible

If those conditions are missing, comparison is likely to create theater rather than evidence.

## Comparison hygiene

A careful comparison should keep stable:
- the object under evaluation
- the claim class
- the fixture surface, or its declared replacement contract
- the scorer or verdict logic
- the interpretation contract

A careful comparison should also name:
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

Do not call the windows comparable if:
- the proof job changed between windows
- the case family drifted without disclosure
- report polish is the main visible difference
- reviewer or policy changes are large enough to swamp the bounded surface

If comparability is weakened materially, prefer:
- `mixed or unstable movement`
- or `no clear directional movement`

over a cleaner growth story.

## Improvement, regression, and noisy variation

| reading | use when | caution |
|---|---|---|
| improvement | The later result is stronger on the same bounded surface with no hidden semantic drift. | Do not confuse nicer summaries with stronger evidence. |
| regression | The later result is weaker on the same bounded surface in a way the contract can explain. | Name whether the regression is outcome, process, boundary, or comparison noise. |
| noisy variation | The movement is too small, too unstable, or too style-shaped for a stronger reading. | Prefer this over fake confidence. |

## Anti-style-drift discipline

Do not treat these as capability growth by default:
- cleaner prose
- shorter summaries
- more confident wording
- more polished report structure

Treat style-only movement as:
- artifact improvement
- report improvement
- or noisy variation

unless the evidence surface also improved in the bounded way the bundle claims to measure.

## When not to call a bundle baseline

Do not call a bundle baseline when:
- one run still depends too much on reviewer intuition
- the fixture surface is still too local or too flattering
- verdict meanings are still muddy
- style changes are likely to swamp real movement
- repeated runs do not preserve the same proof job

## Final note

Baseline is a trust claim about comparison.

If comparison meaning is still unstable,
the honest answer is not baseline yet.
