# Fixture Surface Guide

This guide defines the route for describing, bounding, and publishing fixture
surfaces in `aoa-evals`.

Use it when an eval bundle already has cases, and the next decision is whether
the case surface is public-safe, representative enough, and replaceable by
contract.

See also:
- [Documentation Map](README.md)
- [Portable Eval Boundary Guide](PORTABLE_EVAL_BOUNDARY_GUIDE.md)
- [Baseline Comparison Guide](BASELINE_COMPARISON_GUIDE.md)

## Operating Card

| Field | Route |
| --- | --- |
| role | fixture surface and replacement-contract guide |
| input | bundle cases, public-safety pressure, representativeness pressure, replacement pressure, or local-shaped fixture pressure |
| output | public-safe route, fixture hardening route, replacement contract route, or bundle-local review route |
| owner | this guide owns docs-level fixture reading discipline; bundle-local `evals/<family>/<eval>/fixtures/contract.json`, shared fixture-family parts, and bundle `EVAL.md` own concrete evidence |
| next route | `mechanics/proof-infra/parts/fixture-families/`, narrower mechanic fixture family, bundle-local fixture contract, `docs/PORTABLE_EVAL_BOUNDARY_GUIDE.md`, or `docs/BASELINE_COMPARISON_GUIDE.md` |
| validation | `docs/AGENTS.md#validation` |

## Core question

A fixture surface is the bounded case family that gives the bundle its actual
meaning.

The real question is:
- does this case surface support the stated claim class honestly?

## Bundle Fixture Card

Every public bundle names:
- the unit of evaluation
- what kinds of cases are included
- what is intentionally excluded
- whether fixtures are static, generated, or mixed
- whether the surface is public-safe
- how another repo replaces the fixtures when direct reuse is impossible

Missing points route to fixture hardening before public recommendation.

## Public-Safe Routes

| Pressure | Route |
| --- | --- |
| secrets | source owner retention or sanitized public fixture |
| private logs or private traces | selected public-safe packet before fixture publication |
| unpublished datasets | published replacement dataset or generated bounded fixture |
| local answer keys hidden in reviewer memory | explicit public answer key, rubric, or reviewer rule |
| sensitive operational details | reduced fixture that preserves the bounded failure surface |
| personal data or reconstructable private identifiers | anonymized or synthetic public-safe case family |

Sanitized fixtures remain safe even when a public reader inspects them closely.

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

When direct reuse is impossible, the bundle describes how to replace the
fixtures while preserving the proof job.

A useful replacement contract preserves:
- the bounded claim class
- the main failure surface
- the object under evaluation
- the difficulty band
- the interpretation contract

It also says:
- what can change
- which fixture properties are invariant
- what substitutions would invalidate comparison

## Composite and diagnostic fixture patterns

Composite bundles may use a broader case family,
and they explain why those cases belong together.

Diagnostic bundles keep the fixture surface tighter.

If a diagnostic bundle mixes too many nearby failure classes,
it stops being diagnostic and becomes harder to interpret.

## Fixture representativeness

A fixture surface can be bounded rather than universal.
It stays representative enough for the exact bounded claim.

Good signs:
- the included cases match the claim class
- the excluded cases are named
- nearby misuse is anticipated
- the case family exposes the intended failure surface

Representativeness pressure routes:

| Pressure | Route |
| --- | --- |
| one flattering scenario carries the bundle | add bounded counter-cases or defer public recommendation |
| easy cases dominate a robustness claim | widen difficulty band inside the same claim class |
| cases reward style more than substance | route to style-over-substance review before stronger claim |
| fixture family changes meaning from run to run | replacement contract and comparison disclosure before rerun comparison |

## Signs the fixture surface is still too local-shaped

A surface is still too local-shaped when:
- another repo lacks comparable replacement criteria
- private context silently determines success
- the cases depend on one specific file layout, team habit, or hidden policy
- the bundle lacks fixture invariants

In that state, the bundle may remain useful locally and routes to fixture
hardening before strong public-surface posture.

## Final note

Fixtures are part of the proof contract.

If the cases are muddy, private, or flattering,
the result surface will be muddy too.
