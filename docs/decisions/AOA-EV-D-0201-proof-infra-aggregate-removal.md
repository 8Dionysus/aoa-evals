# Proof Infra Aggregate Removal

- Decision ID: AOA-EV-D-0201
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused proof-infra route and shared-support validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, mechanics/topology, fixture/support, report/readout
- Mechanic parents: proof-infra, proof-object, proof-loop, cross-parent
- Guard families: source/topology
- Posture: active rationale

## Context

AOA-EV-D-0124 moved proof-infra checks out of root validation and into
`scripts/validators/proof_infra.py`. That was the right first boundary, but
the module still carried two different validator jobs:

- proof-infra route-card, provenance, legacy, decision-token, and stale phrase
  checks for the mechanic and its parts; and
- shared proof-infra guide exposure plus fixture/runner contract exercise
  checks against source eval bundles.

Both stay weaker than source bundle meaning, but they fail through different
owner routes.

## Decision

`scripts/validators/proof_infra.py` is removed.

Proof-infra validation now routes through focused modules:

- `proof_infra_routes.py` owns mechanic route cards, part route cards,
  provenance, legacy index, decision-token checks, and stale negative scaffold
  rejection.
- `proof_infra_route_tokens.py` owns route token sets and stale route phrases.
- `proof_infra_shared_support.py` owns shared guide exposure, fixtures/reports
  route-card support, reportable runner text, and source bundle support-contract
  exercise.
- `proof_infra_common.py` is helper-only path constants, route-text helpers,
  and source eval directory lookup.

Mechanics route orchestration calls the route validator directly. Source eval
domain validation calls the shared-support validator directly. Source eval
fixture and runner contract validators import schema paths from the helper.

## Rationale

Route-card posture and shared-support exercise are not the same gate. The first
answers whether proof-infra itself is routed correctly. The second answers
whether shared proof infrastructure is visible and exercised by source bundle
support contracts.

Keeping both inside one aggregate made future proof-infra pressure look like a
single historical bucket. Splitting them keeps source bundle meaning stronger
while preserving reusable support checks as real gates.

## Consequences

- Positive: no proof-infra aggregate validator remains.
- Positive: route failures and shared-support exercise failures now name
  separate owner modules.
- Positive: schema path constants remain available without keeping a validator
  facade.
- Tradeoff: tests and callers import the focused owner module for the behavior
  they exercise.

## Current Applicability

As of 2026-06-04:

- Still valid: proof-infra reusable support stays below source eval bundle
  meaning and bundle-local reports.
- Changed: proof-infra behavior no longer lives in `proof_infra.py`; it is
  split across route, shared-support, and helper modules.
- Further changed on 2026-06-05: AOA-EV-D-0230 moves route token matrices and
  stale phrases out of the blocking route validator.
- Supersedes: the aggregate module shape left by AOA-EV-D-0124.

## Boundaries

This decision does not make shared fixture families stronger than bundle-local
claims.

It does not make runner/scorer/schema support a repo-global score, a receipt, a
runtime acceptance signal, or a generated source of truth.

It does not move generated catalog projection ownership into proof-infra and
does not create a replacement proof-infra aggregate under another name.

## Validation

- `python -m py_compile scripts/validators/proof_infra_common.py scripts/validators/proof_infra_routes.py scripts/validators/proof_infra_shared_support.py scripts/validators/mechanics_routes.py scripts/validators/source_eval_domains.py scripts/validators/source_eval_fixture_contracts.py scripts/validators/source_eval_runner_contracts.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_infra`
- `python -m pytest -q tests/test_build_catalog.py tests/test_validate_repo.py tests/test_eval_source_topology.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_decision_indexes.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
