# Source Eval Comparison Validator Boundary

- Decision ID: AOA-EV-D-0173
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/source_eval_comparison.py`, `evals/AGENTS.md`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, source/topology
- Mechanic parents: proof-object, proof-infra
- Guard families: source/topology, trace/eval
- Posture: active rationale

## Context

`scripts/validators/source_eval_contracts.py` still carried comparison-surface
rules for non-`none` baseline modes: allowed key sets, anchor/peer/integrity
target checks, repo-relative comparison paths, and consistency with
bundle-local fixture and runner contracts.

Those checks protect comparison route shape. They are not the same boundary as
EVAL.md parsing, manifest/frontmatter schema validation, evidence policy,
dependency refs, artifact contracts, generated comparison-spine parity, or score
interpretation.

## Decision

Source eval comparison-surface validation lives in
`scripts/validators/source_eval_comparison.py`.

The module owns:

- baseline-mode-specific `comparison_surface` allowed-key checks;
- anchor, peer, and integrity sidecar eval target checks;
- repo-relative `shared_family_path` and `paired_readout_path` existence checks;
- consistency with `evals/<family>/<eval>/fixtures/contract.json` shared fixture
  family paths; and
- consistency with `evals/<family>/<eval>/runners/contract.json` paired readout
  paths.

`scripts/validators/source_eval_contracts.py` keeps compatibility aliases and
delegates comparison-surface validation to the focused module.

## Rationale

Comparison surfaces are source manifest contracts, but they are a distinct
claim-family boundary. They describe how a comparison eval names its anchors,
peers, readouts, and support contracts.

Keeping those rules in the main source eval contract validator made the module
carry parsing, schema validation, command ownership, catalog projection inputs,
evidence policy adapters, dependency/reference adapters, artifact adapters, and
comparison semantics at once.

The split makes comparison route shape explicit without moving generated
comparison-spine parity or score interpretation into source validation.

## Consequences

- Positive: comparison-surface checks have their own validator, inventory entry,
  mechanics ledger row, and decision rationale.
- Positive: `source_eval_contracts.py` narrows to aggregate validation,
  catalog projection inputs, and compatibility adapters while authored record
  parsing later routes to `source_eval_records.py`.
- Positive: existing helper imports remain compatible through
  `source_eval_contracts.py`.
- Tradeoff: the comparison validator still reads bundle-local fixture and runner
  contracts because comparison surface consistency depends on those source
  support contracts.

## Current Applicability

As of 2026-06-04:

- Still valid: comparison source evals must expose baseline-mode-specific
  comparison surfaces that resolve to source eval targets and support contracts.
- Changed: comparison-surface key, target, repo-relative path, and fixture/runner
  consistency checks moved out of `source_eval_contracts.py` and into
  `source_eval_comparison.py`.
- Superseded by: none.

## Boundaries

This decision does not make `source_eval_comparison.py` the owner of EVAL.md
parsing, manifest schema meaning, evidence policy, source dependency refs,
bundle-local artifact contracts, generated comparison-spine parity, score
interpretation, release packaging, runtime outcomes, or public entry routing.

It checks authored comparison-surface route shape only.

## Validation

- `python -m py_compile scripts/validators/source_eval_contracts.py scripts/validators/source_eval_comparison.py`
- `python -m pytest -q tests/test_build_catalog.py tests/test_validate_repo.py tests/test_eval_source_topology.py`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
