# Fixtures Route

This directory is the compatibility route card for former root shared fixture
families in `aoa-evals`.

No active fixture family remains in root `fixtures/` after the proof-infra
fixture-family slice. Active families now live under the owning mechanic part.

Use [AGENTS.md](AGENTS.md) for replacement, naming, and safety rules. This
README is the route map.

Generic shared fixture families now live under the proof-infra part:

- `mechanics/proof-infra/parts/fixture-families/fixtures/ambiguity-bounded-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/approval-boundary-bounded-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/local-text-contract-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/memo-contradiction-guardrail-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/memo-writeback-act-guardrail-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/ring-application-discipline-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/scope-drift-bounded-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/tool-trajectory-bounded-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/trace-outcome-bounded-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/verification-honesty-v1/README.md`
- `mechanics/proof-infra/parts/fixture-families/fixtures/witness-trace-v1/README.md`

Comparison-spine shared fixture families now live under active
comparison-spine parts:
- `mechanics/comparison-spine/parts/fixed-baseline/fixtures/frozen-same-task-v1/README.md`
  for frozen same-task regression against one named baseline target
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v1/README.md`
  for artifact/process pairing on the bounded change corpus
- `mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md`
  for a second matched artifact/process pairing slice on the same bounded
  change corpus
- `mechanics/comparison-spine/parts/longitudinal-window/fixtures/repeated-window-bounded-v1/README.md`
  for ordered repeated-window movement on one named workflow surface

Recurrence support fixture families now live under active recurrence parts:
- `mechanics/recurrence/parts/anchor-return/fixtures/return-anchor-v1/README.md`
  for bounded return-anchor integrity
- `mechanics/recurrence/parts/memory-recall/fixtures/memo-recall-guardrail-v1/README.md`
  for bounded memo recall integrity
- `mechanics/recurrence/parts/recursor-boundary/fixtures/recursor-readiness-boundary-v1/`
  for recursor readiness-only boundary cases
- `mechanics/recurrence/parts/stats-regrounding-boundary/fixtures/stats-regrounding-boundary-v1/README.md`
  for stats-derived consumer re-grounding boundary checks

Method-growth shared fixture families now live under their active parts:
- `mechanics/method-growth/parts/candidate-lineage/fixtures/candidate-lineage-v1/README.md`
  for bounded growth-refinery lineage-chain coherence
- `mechanics/method-growth/parts/owner-landing/fixtures/owner-fit-routing-v1/README.md`
  for bounded reviewed owner-fit routing on growth-refinery candidates
