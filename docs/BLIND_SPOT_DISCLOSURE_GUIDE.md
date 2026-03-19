# Blind Spot Disclosure Guide

This guide defines the minimum blind-spot disclosure expected from public eval bundles in `aoa-evals`.

Use it when a bundle looks useful,
but you still need to make explicit what the bundle does not prove and where it may mislead.

See also:
- [Documentation Map](README.md)
- [Eval Philosophy](EVAL_PHILOSOPHY.md)
- [Verdict Interpretation Guide](VERDICT_INTERPRETATION_GUIDE.md)

## Why blind spots are mandatory

Blind spots are part of the proof contract.

They are not optional cautions added after the real work.
They are one of the main ways a bundle tells the truth honestly.

A bundle that cannot name its blind spots is not ready for strong claims.

## Minimum disclosure

Every public bundle should disclose at least:
- what the eval does not prove
- one or more likely false-pass paths
- one or more likely false-fail or misleading-result paths when relevant
- any strong local-shape or environment assumptions
- any nearby claim class that should use a different bundle instead

The exact wording can vary.
The minimum truth contract should not.

## Common blind-spot classes

| class | what to name |
|---|---|
| fixture limits | narrow case family, flattering cases, weak coverage, or origin-shaped fixtures |
| scorer limits | tacit reviewer judgment, opaque thresholds, or score gaming risk |
| environment limits | missing tools, unstable setup, hidden policy assumptions, or bounded sandbox effects |
| interpretation limits | what a pass, fail, or mixed result still does not justify saying |
| portability limits | what breaks when the bundle leaves its birth context |
| nearby-claim confusion | where another bundle should be used for a narrower or different proof job |

## Good disclosure posture

Good blind-spot disclosure is:
- concrete
- bounded
- specific to the bundle
- visible enough that summaries cannot quietly bypass it

Weak disclosure sounds like:
- "this does not prove everything"
- "results may vary"
- "use judgment"

Those statements may be true,
but they are not enough by themselves.

## Summary and report interaction

Bundle summaries should remain downstream of blind-spot disclosure.

If the blind spots say:
- fixture coverage is narrow
- authority ambiguity is excluded
- the bundle is composite rather than diagnostic

then the compact summary should not quietly imply the opposite.

## Review blocking cases

Strong review should usually defer when:
- the blind spots are missing
- the blind spots are generic and not bundle-shaped
- the summary language is broader than the disclosed limits
- the bundle hides likely false-pass paths

Missing blind spots do not just weaken style.
They weaken the truthfulness of the public surface.

## Final note

Blind spots are not where the bundle becomes weaker.

They are where the bundle becomes honest enough to trust.
