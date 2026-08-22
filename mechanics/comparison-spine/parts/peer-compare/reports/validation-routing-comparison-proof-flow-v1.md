# Validation-routing comparison proof flow v1

## Purpose

This dossier routes a bounded peer comparison of validation activation methods
through the existing comparison spine. It is a support contract and seeded
measurement surface, not a new public eval bundle and not a final routing
policy.

## Contract

Each method sees the same scenario identity:

`workload_id + candidate_set_id + environment_id + source_ref`

The scenario declares a `full_owner_proof` route as the oracle and fallback.
Candidate methods may propose activation nodes, but they cannot turn a local
green proxy into complete proof. A stale graph, unknown dependency, malformed
or wrong-identity receipt, missing owner route, or unexplained miss remains
explicit; `hybrid_fail_closed` escalates to the full owner proof route and
reports incomplete when that fallback is not bound.

Version 1 admits only `evidence_kind=seeded_fixture` under
`source_posture=seeded_public_safe_only`. `real_session` evidence is not
admitted in this contract, so `real_case_count` and real miss counts remain
zero/null rather than being inferred from seeded cases. Every latency field
ending in `_synthetic_proxy` is a declared fixture-event proxy; it is not
observed runtime latency, a speed claim, or a method ranking.

A method-level rationale never explains a missing node. Only a non-empty,
node-keyed `missing_explanations[node]` entry may discharge that node's
explanation requirement. Missing nodes without that exact entry stay in
`unexplained_miss_nodes`, including when a generic method rationale is
present.

The report records:

- real and seeded miss accounting, with real counts left `null` when no real
  cases are admitted;
- excess activation nodes;
- precision and recall only when the fixture oracle denominator is complete;
- first-failure and total synthetic fixture-proxy latency;
- retry amplification;
- stale/unknown/malformed/wrong-identity state behavior;
- candidate explanations and unexplained misses; and
- fail-closed escalation details, including fallback status.

All fallback or external-owner timing remains unmeasured unless an actual
identity-bound receipt exists.

## Implemented candidate families

The seeded runner implements static paths, dependency signals, owner
contracts, bounded history correlation, claim/risk classification, and a
hybrid owner-DAG/fail-closed composition. API/ABI, coverage, mutation,
live-KAG-relations, and LLM-proposed additions remain explicit missing
candidates. The absence is a coverage limit, not a zero score.

## Evidence boundary

The input shadow report is a public-safe derivative of a bounded experiment.
Its local timing proxies and owner-route gaps guide fixture pressure; the
runner preserves them as seeded fixture declarations, not observations. No
raw sessions, private payloads, synthetic cases relabeled as real, external
receipts, or universal method conclusions enter this dossier.

The surface does not prove release readiness, KAG provider integrity, canonical
`aoa-stats` compatibility, runtime health, agent quality, or a winning routing
policy. Source proof bundles and stronger owner routes retain those meanings.

## Next campaign

Bind the exact `aoa-evals` commit to an `aoa-kag` checkout and canonical
`aoa-stats` envelope contract, obtain identity-safe owner receipts, and add one
source-only no-KAG control plus one controlled corruption fixture. Only then
reconsider admissible latency, recall, retry, or policy readings.
