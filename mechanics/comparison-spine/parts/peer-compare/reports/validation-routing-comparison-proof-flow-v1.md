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

The report records:

- real and seeded miss accounting, with real counts left `null` when no real
  cases are admitted;
- excess activation nodes;
- precision and recall only when the fixture oracle denominator is complete;
- first-failure and total candidate-route latency;
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
Its observed local timing proxies and owner-route gaps guide fixture pressure;
no raw sessions, private payloads, synthetic cases relabeled as real, external
receipts, or universal method conclusions enter this dossier.

The surface does not prove release readiness, KAG provider integrity, canonical
`aoa-stats` compatibility, runtime health, agent quality, or a winning routing
policy. Source proof bundles and stronger owner routes retain those meanings.

## Next campaign

Bind the exact `aoa-evals` commit to an `aoa-kag` checkout and canonical
`aoa-stats` envelope contract, obtain identity-safe owner receipts, and add one
source-only no-KAG control plus one controlled corruption fixture. Only then
reconsider admissible latency, recall, retry, or policy readings.
