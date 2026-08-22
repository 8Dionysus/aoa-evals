# Validation-routing Peer-comparison Support

- Decision ID: AOA-EV-D-0254
- Status: Accepted
- Date: 2026-08-21
- Owner surface: `mechanics/comparison-spine/parts/peer-compare/`

## Index Metadata

- Original date: 2026-08-21
- Surface classes: comparison/readout, fixture/support, validation guard
- Mechanic parents: comparison-spine, proof-infra
- Guard families: source/topology, trace/eval
- Posture: active rationale

## Context

The validation-activation shadow identified useful path, dependency, owner,
history, claim-risk, and hybrid activation hypotheses, but its narrow timings
were not admissible savings because KAG, canonical stats, source-fast, and
advisory owner routes were missing or blocked. The next owner-local slice needs
fair comparison identities, seeded adversarial cases, explicit unsupported
candidate families, and a full owner-proof fallback without turning the shadow
into a routing policy.

## Options Considered

- Create a new validation framework beside the comparison spine.
- Add a new public eval bundle and choose a routing winner now.
- Extend the existing `peer-compare` support route with a measurement-only
  contract and seeded runner.

## Decision

Extend `mechanics/comparison-spine/parts/peer-compare/` with the
`validation-routing-bounded-v1` fixture family, a machine-readable comparison
contract, a deterministic runner, a report schema/example, adversarial cases,
and a proof-flow dossier.

Every peer method receives the same `workload_id`, `candidate_set_id`,
`environment_id`, and `source_ref` per scenario. The scenario's
`full_owner_proof` route remains the oracle/fallback. Stale, unknown,
malformed, wrong-identity, missing, and unexplained states remain explicit;
`hybrid_fail_closed` escalates rather than declaring local sufficiency.

The first slice implements static paths, dependency signals, owner contracts,
bounded history correlation, claim/risk classification, and hybrid owner-DAG
fail-closed composition. API/ABI, coverage, mutation, live KAG relations, and
LLM-proposed additions remain explicit unsupported candidates. The report is
measurement-only and keeps policy selection, public eval status, and external
validator acceptance outside this part.

## Rationale

`peer-compare` already owns matched-condition side-by-side reading, so it is the
narrowest existing owner surface that can carry competing activation methods
without introducing a parallel mini-framework or a new baseline mode. The
identity tuple prevents incomparable timings from being treated as a method
comparison. The oracle/fallback preserves the full proof boundary identified by
the shadow report. Explicit missing candidates and null denominators prevent
absence or incomplete external evidence from becoming a score or green result.

## Consequences

- Positive: future candidate methods can join one repeatable comparison
  contract without changing source bundle claim meaning.
- Positive: seeded stale/unknown/receipt/miss cases exercise fail-closed
  behavior and explanation coverage locally.
- Positive: the repo-wide support registry classifies the read-only part-local
  measurement runner as bounded comparison support, with proof and policy
  interpretations forbidden.
- Tradeoff: no real-session recall, external receipt timing, or population-level
  method choice is established by this slice.
- Follow-up: bind exact `aoa-evals` commits to `aoa-kag` and canonical
  `aoa-stats` owner routes, then add a no-KAG control and controlled corruption
  fixture before reconsidering policy or timing claims.

## Current Applicability

As of 2026-08-21:

- Still valid: validation-routing support remains under `peer-compare` and is
  measurement-only.
- Changed: peer-compare now includes a validation-routing fixture, runner,
  report, and explicit candidate coverage map.
- Superseded by: none.

## Boundaries

This decision does not make a seeded report real-session proof, a local green
route complete release evidence, a shadow report a verdict, a generated reader
source truth, or this part the owner of SDK routing policy, KAG provider
integrity, canonical stats semantics, runtime health, or external acceptance.

It does not require unsupported candidate families to be invented or scored as
zero, and it does not authorize weakening the full owner-proof route.

## Validation

The source route is validated by the comparison-spine route cards, the seeded
runner and focused tests, `python scripts/validate_repo.py`,
`python scripts/validate_semantic_agents.py`, the generated catalog check, and
decision-index parity. Hosted validation remains the acceptance boundary for a
landed change.
