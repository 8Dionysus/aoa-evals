# Example Report

## Bundle

- bundle: `aoa-runtime-latency-tradeoff`
- bundle shape: `comparative`
- verdict: `mixed tradeoff signal`
- machine-readable companion: `reports/example-report.json`
- shared proof dossier: `mechanics/comparison-spine/parts/fixed-baseline/reports/runtime-latency-tradeoff-proof-flow-v1.md`

This is a draft runtime tradeoff surface, not a runtime leaderboard or quality
ranking.

## Matched Conditions

- baseline target: `sanitized local runtime baseline variant`
- case family: `draft matched fixture family`
- latency metric: chosen first-token latency aggregate under the matched fixture
  family
- resource metric: chosen runtime memory-pressure aggregate under the matched
  fixture family
- matched fixture: same public-safe fixture family, preset, timeout, retry, and
  metric semantics

## Per-Case Breakdown

| case id | baseline note | candidate note | latency reading | resource reading | comparison note |
|---|---|---|---|---|---|
| DRAFT-01 | baseline target is named and inspectable for review | candidate evidence is represented only as a draft comparison input | candidate may show lower latency only under the named matched metric | candidate resource cost remains visible and separate from latency | draft readout preserves matched-condition comparison while avoiding a broad quality claim |

## Bundle-Level Reading

The draft matched fixture family supports only a `mixed tradeoff signal`.

The candidate may improve the named latency metric under the matched condition,
but that movement stays paired with visible resource-use cost. The honest
reading is therefore a tradeoff, not a winner story.

## Interpretation Boundary

This report does **not** rank reasoning quality, agent behavior, hosts, hardware
tiers, or global runtime health.

It says only that under the named matched fixture conditions, one runtime
variant can carry a visible latency/resource tradeoff that remains safe to read
as a bounded draft comparison.
