# Proof Infra Validator Module Boundary

- Decision ID: AOA-EV-D-0124
- Status: Accepted
- Date: 2026-06-03
- Historical owner surface: `scripts/validators/proof_infra.py`, `mechanics/proof-infra/`
- Refined by: AOA-EV-D-0201

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, mechanics/topology, fixture/support, report/readout
- Mechanic parents: proof-infra, proof-object, proof-loop, cross-parent
- Guard families: source/topology, generated/readout
- Posture: active rationale

## Context

Proof-infra validation still lived in two root-validator areas:

- the broad mechanics pass checked parent route cards, fixture-family and
  reportable-contract part cards, provenance, legacy routing, and decisions;
- the source doctrine pass checked the shared proof-infra guide plus bundle
  contract exercise for additional shared fixture families and paired readouts.

Those checks protect one reusable support boundary. They do not define source
bundle meaning, generated catalog truth, receipt publication, or runtime
acceptance.

## Options Considered

- Keep proof-infra checks inside `scripts/validate_repo.py`.
- Split only route-card checks while leaving shared guide checks in root source
  doctrine.
- Move proof-infra route, provenance, legacy, shared-guide, and reusable
  support exercise checks into `scripts/validators/proof_infra.py` while
  keeping `scripts/validate_repo.py` as the compatibility entrypoint.

## Decision

Proof-infra validation lives in `scripts/validators/proof_infra.py`.

`scripts/validate_repo.py` delegates proof-infra route-card, part-contract,
decision, provenance, legacy, shared-guide, and contract-exercise checks to the
focused module.

Tests import proof-infra constants from `scripts/validators/proof_infra.py`
directly. `scripts/validate_repo.py` no longer re-exports `PROOF_INFRA_*`
compatibility aliases.

## Rationale

Proof-infra is reusable support below bundle meaning. It provides shared
fixture families, runner surfaces, scorer helpers, schemas, and guidance that
bundles may reference.

If root validation owns these details directly, the root script becomes a pile
of historical mechanic gates. If generated validators own them, reusable
support can accidentally become source truth. A focused proof-infra validator
keeps the support contract visible while preserving the stronger authority of
`evals/**/EVAL.md`, `evals/**/eval.yaml`, and bundle-local reports.

## Consequences

- Positive: another coherent mechanics/support boundary leaves the root
  validator.
- Positive: shared proof-infra guide checks stay beside fixture-family and
  reportable-contract route checks.
- Positive: proof-infra test fixtures now route to the focused module instead
  of preserving root compatibility aliases.
- Follow-up: generated `proof_artifacts` projection checks can move later only
  if they stay in the generated/read-model lane.

## Current Applicability

As of 2026-06-03:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: proof-infra route and shared support checks now have a focused
  validator module.
- Further changed on 2026-06-04: AOA-EV-D-0201 removes
  `scripts/validators/proof_infra.py`; active proof-infra validation is split
  across route, shared-support, and helper modules.
- Superseded by: AOA-EV-D-0201 for the aggregate module shape.

## Boundaries

This decision does not make shared fixture families stronger than
bundle-local claims.

It does not make runner/scorer/schema support a repo-global score, a receipt,
a runtime acceptance signal, or a generated source of truth.

It does not move generated catalog projection ownership into proof-infra.

## Validation

- `python -m py_compile scripts/validators/proof_infra_common.py scripts/validators/proof_infra_routes.py scripts/validators/proof_infra_shared_support.py scripts/validators/mechanics_routes.py scripts/validators/source_eval_domains.py scripts/validators/source_eval_fixture_contracts.py scripts/validators/source_eval_runner_contracts.py tests/test_mechanic_surface_contracts.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_infra`
- `python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_test_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/validate_repo.py`
