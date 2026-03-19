# Fixture Surface Guide

This guide defines how fixture surfaces should be described, bounded, and published in `aoa-evals`.

Use it when an eval bundle already has cases,
but you still need to decide whether the case surface is public-safe, representative enough, and replaceable by contract.

See also:
- [Documentation Map](README.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)

## Core question

A fixture surface is not just a pile of cases.

It is the bounded case family that gives the bundle its actual meaning.

The real question is:
- does this case surface support the stated claim class honestly?

## What every bundle should state

Every public bundle should name:
- the unit of evaluation
- what kinds of cases are included
- what is intentionally excluded
- whether fixtures are static, generated, or mixed
- whether the surface is public-safe
- how another repo should replace the fixtures if direct reuse is impossible

If these points are missing, the fixture surface is too implicit.

## Public-safe fixture rules

Public fixtures should not depend on:
- secrets
- private logs or private traces
- unpublished datasets
- local answer keys hidden in reviewer memory
- sensitive operational details that should not be public
- personal data or reconstructable private identifiers

Sanitized fixtures should remain safe even if a public reader inspects them closely.

## Good fixture shapes

Strong public fixture surfaces often use one of these shapes:
- public static fixtures
- curated public case families
- generated fixtures with bounded generation rules
- mixed surfaces where the replacement contract is explicit

Weak fixture surfaces often look like:
- one local scenario copied from origin context
- cases that only make sense to the original team
- huge mixed scenario soups with no clear boundary
- tiny toy cases used to imply much larger claims

## Replacement contract

When direct reuse is not possible, the bundle should describe how to replace the fixtures without changing the proof job.

A useful replacement contract should preserve:
- the bounded claim class
- the main failure surface
- the object under evaluation
- the difficulty band
- the interpretation contract

It should also say:
- what can change
- what must not change
- what substitutions would invalidate comparison

## Composite and diagnostic fixture patterns

Composite bundles may use a broader case family,
but they should still explain why those cases belong together.

Diagnostic bundles should keep the fixture surface tighter.

If a diagnostic bundle mixes too many nearby failure classes,
it stops being diagnostic and becomes harder to interpret.

## Fixture representativeness

A fixture surface does not need to be universal.
It does need to be representative enough for the exact bounded claim.

Good signs:
- the included cases match the claim class
- the excluded cases are named
- nearby misuse is anticipated
- the case family exposes the intended failure surface

Bad signs:
- the bundle relies on one flattering scenario
- easy cases dominate a claim about robustness
- the cases reward style more than substance
- the fixture family changes meaning from run to run without explanation

## Signs the fixture surface is still too local-shaped

A surface is still too local-shaped when:
- another repo could not tell what counts as a comparable replacement
- private context silently determines success
- the cases depend on one specific file layout, team habit, or hidden policy
- the bundle cannot say which fixture properties are invariant

In that state, the bundle may still be useful locally,
but it is not yet a strong public surface.

## Final note

Fixtures are part of the proof contract.

If the cases are muddy, private, or flattering,
the result surface will be muddy too.
