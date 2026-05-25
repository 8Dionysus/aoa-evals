# Blind Spot Disclosure Guide

This guide defines the minimum blind-spot disclosure expected from public eval bundles in `aoa-evals`.

Use it when a bundle looks useful and needs explicit unsupported claims,
likely misleading paths, and nearby-bundle routes before stronger review.

See also:
- [Documentation Map](../README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | blind-spot disclosure guide for public eval bundles |
| input | bundle claim, verdict, summary, likely false-pass path, likely false-fail path, local-shape assumption, or nearby-claim confusion |
| output | unsupported-claim boundary, blind-spot class, review deferral route, or summary correction route |
| owner | this guide owns docs-level blind-spot disclosure discipline; bundle-local `EVAL.md`, reports, and review notes own concrete blind-spot evidence |
| next route | affected bundle, [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md), [Eval Review Guide](EVAL_REVIEW_GUIDE.md), or nearby bundle owner |
| validation | [docs/AGENTS.md#validation](../AGENTS.md#validation) |

## Why blind spots are mandatory

Blind spots are part of the proof contract.

They are first-class truth surfaces.
They are one of the main ways a bundle tells the truth honestly.

A bundle names its blind spots before strong claims.

## Minimum disclosure

Every public bundle discloses at least:
- unsupported claim classes
- one or more likely false-pass paths
- one or more likely false-fail or misleading-result paths when relevant
- any strong local-shape or environment assumptions
- any nearby claim class and its stronger bundle route

The exact wording can vary.
The minimum truth contract stays stable.

## Common blind-spot classes

| class | what to name |
|---|---|
| fixture limits | narrow case family, flattering cases, weak coverage, or origin-shaped fixtures |
| scorer limits | tacit reviewer judgment, opaque thresholds, or score gaming risk |
| environment limits | missing tools, unstable setup, hidden policy assumptions, or bounded sandbox effects |
| interpretation limits | unsupported interpretations after a pass, fail, or mixed result |
| portability limits | what breaks when the bundle leaves its birth context |
| nearby-claim confusion | narrower or different proof job route |

## Disclosure Posture

Good blind-spot disclosure is:
- concrete
- bounded
- specific to the bundle
- visible enough that summaries route through it

Disclosure needs a review gap route when it stays at:
- generic umbrella caveat
- vague variance caveat
- judgment-only instruction

Route those gaps back to bundle-specific unsupported claims,
false-pass or false-fail paths, local-shape assumptions, or nearby-bundle routes.

## Summary and report interaction

Bundle summaries remain downstream of blind-spot disclosure.

If the blind spots say:
- fixture coverage is narrow
- authority ambiguity is excluded
- the bundle is composite rather than diagnostic

then the compact summary routes through those same limits.

## Review Deferral Routes

Review defers through these gap routes:
- blind-spot section is missing
- blind spots need bundle-shaped specificity
- the summary language is broader than the disclosed limits
- likely false-pass paths need exposure

Missing blind spots weaken the truthfulness of the public surface.

## Final note

Blind spots are where the bundle becomes honest enough to trust.
