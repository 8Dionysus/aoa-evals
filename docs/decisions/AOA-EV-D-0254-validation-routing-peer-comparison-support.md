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
- Positive: the repo-wide support registry classifies the optionally
  caller-write-capable part-local measurement runner as bounded comparison
  support, with proof and policy interpretations forbidden.
- Tradeoff: no real-session recall, external receipt timing, or population-level
  method choice is established by this slice.
- Follow-up: bind exact `aoa-evals` commits to `aoa-kag` and canonical
  `aoa-stats` owner routes, then add a no-KAG control and controlled corruption
  fixture before reconsidering policy or timing claims.

## Current Applicability

As of 2026-08-22:

- Still valid: validation-routing support remains under `peer-compare` and is
  measurement-only.
- Changed: peer-compare now includes a validation-routing fixture, runner,
  report, explicit candidate coverage map, seeded-only evidence policy, and
  strict nested report ABI. The runner is read-only by default but is
  optionally caller-write-capable when `--output` is supplied; that effect is
  bounded to the caller-selected report path and does not change its
  measurement-only claim posture.
- Superseded by: none.

## Review Log

On 2026-08-21, the Sol review kept this surface at `candidate_only` and
identified four contract repairs before landing: generic rationale could
over-explain missing nodes; the report schema did not constrain nested ABI;
seeded and real evidence posture could disagree; and fixture latency was
worded as observed timing. The repair keeps the report measurement-only,
requires node-keyed missing explanations, strictly validates emitted nested
identity/method/measurement/scenario/event/oracle/escalation objects, admits
only `seeded_fixture` evidence in v1, and names every latency value as a
synthetic fixture proxy. It does not promote a seeded candidate to policy,
proof, or a runtime performance result, and it leaves the owner gate intact.

### 2026-08-22 - Receipt classification and effect currentness follow-up

- Previous assumption: a declared owner-contract failure state could be used
  as receipt evidence, and the runner could be described simply as read-only.
- New reality: receipt shape and complete identity are the source-owned
  classifier; `--output` can create directories and write the caller-selected
  report path.
- Reason: exact-head review exposed coverage disagreement for a complete
  receipt mislabeled `malformed` and stale effect metadata in this decision.
- Source surfaces updated: peer-compare runner/tests/fixture contract note and
  this decision's applicability and consequence wording.
- Validation: focused classifier matrix, peer-compare runner checks, owner
  validators, generated parity, and hosted review remain separate evidence
  layers.

### 2026-08-22 - Normalized evidence boundary repair

- Previous assumption: adversarial dependency classes and copied input metadata
  could be checked independently from the normalized report evidence.
- New reality: signal shape/state normalization, fixture adversarial coverage,
  compact-example parity, and `input_evidence.allowed_use` must share the
  source-owned measurement-only boundary.
- Reason: exact-head review exposed malformed dependency nodes fabricating stale
  or unknown coverage, an omitted external-owner example, and caller-controlled
  policy text in `allowed_use`.
- Source surfaces updated: peer-compare runner, contract/schema, fixture note,
  example, and focused negative/parity tests.
- Validation: the new shape matrix, exact allowed-use admission/schema checks,
  and fixture/example parity assertion remain separate from hosted and KAG
  owner-family gates.

## Boundaries

This decision does not make a seeded report real-session proof, a local green
route complete release evidence, a shadow report a verdict, a generated reader
source truth, or this part the owner of SDK routing policy, KAG provider
integrity, canonical stats semantics, runtime health, or external acceptance.

It does not require unsupported candidate families to be invented or scored as
zero, and it does not authorize weakening the full owner-proof route.

## Validation

The source route is validated by the comparison-spine route cards, the seeded
runner and focused negative tests, strict report-schema validation, the
repository and semantic-agent validators, generated catalog and decision-index
parity, and the owner-generated KAG family check. Hosted validation remains the
acceptance boundary for a landed change.
