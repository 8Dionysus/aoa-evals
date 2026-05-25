# Validator Orchestrator Domain Modules

- Status: Accepted
- Date: 2026-05-25
- Owner surface: `scripts/validate_repo.py`, `scripts/validators/`, `tests/test_validate_repo.py`

## Index Metadata

- Surface classes: validation guard, root/topology, generated/readout
- Mechanic parents: proof-object, cross-parent
- Guard families: route residue, generated/report/receipt/runtime, decision index/read-model
- Posture: active rationale

## Context

The docs refactor made `docs/` more agent-operable and moved decision lookup
crosswalks into generated read models. That exposed the next pressure:
`scripts/validate_repo.py` was still acting as a very large validator and as
the hidden home for several contracts that now have clearer owner surfaces.

The goal is not to remove the root validator. The root validator remains the
single repo-wide entrypoint. The pressure is to make it an orchestrator that
delegates domain contracts to focused modules whose names match the route being
protected.

## Options Considered

- Keep all docs, generated, mechanics, and eval-tree contract checks inside
  `scripts/validate_repo.py`.
- Move only the decision-index and docs-topology checks, leaving the remaining
  domains for a later validator refactor.
- Add the named validator modules now, each with a bounded contract, and keep
  `scripts/validate_repo.py` as the caller.

## Decision

`scripts/validate_repo.py` now delegates focused contracts to:

- `scripts/validators/docs_decisions.py`
- `scripts/validators/docs_topology.py`
- `scripts/validators/docs_routes.py`
- `scripts/validators/mechanics.py`
- `scripts/validators/eval_bundles.py`
- `scripts/validators/generated_parity.py`

The delegated contracts cover decision metadata/generated parity, docs topology,
docs route/link shape, residual root-authored mechanics classification, source
eval bundle topology, and generated/read-model route parity.

`scripts/validate_repo.py` remains the repo-wide command surface. The modules
own domain-specific contract logic; tests keep the wrappers and current repo
state honest.

## Rationale

This gives future agents a clearer operational map: open the root validator to
see orchestration, then open the focused module for the contract details. It
also prevents the docs refactor from becoming only a prose cleanup while the
validator surface stays monolithic and harder to change safely.

The module split is intentionally bounded. It extracts domain contracts that
are already named by the docs/index goal without rewriting unrelated bundle,
receipt, route-residue, or sibling validators.

## Consequences

- Positive: validator ownership is easier to inspect by route domain.
- Positive: new docs and generated read-model contracts are backed by modules
  rather than hidden token lists.
- Tradeoff: root-authored validator modules must be tracked in the residual
  surface classification ledger.
- Follow-up: the broader validator refactor can continue by moving additional
  domain contracts only when their owner surfaces are clear.

## Current Applicability

As of 2026-05-25:

- Still valid: `scripts/validate_repo.py` is the repo-wide validator entrypoint.
- Changed: the docs/index/generated/eval-tree/mechanics contracts now have
  focused modules under `scripts/validators/`.
- Superseded by: none.

## Boundaries

This decision does not claim that every validation domain has been extracted.

It does not move mechanic-owned payload validators into root `scripts/`; those
remain part-local unless the root validator owns a cross-surface contract.

## Validation

Use the focused wrapper tests and full repo validator:

- `python -m pytest -q tests/test_validate_repo.py -k 'docs_route_contracts or generated_parity_contracts or eval_bundle_topology_contracts or root_authored_surface_classification or decision_index_read_models'`
- `python scripts/validate_repo.py`
