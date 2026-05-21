# Proof Infra Distillation Log

## 2026-05-20 Fixture Families

The remaining root shared fixture families were distilled into the
`fixture-families` part of `mechanics/proof-infra/`.

Why this route:

- each family is reusable proof support named by bundle-local
  `shared_fixture_family_path`;
- the source proof bundles still own the bounded claims and verdict logic;
- no family by itself proves a new parent mechanic;
- audit, distillation, memo, comparison, recurrence, checkpoint, and other
  nearby routes remain stronger only where their active package already owns
  the operation.

Accounting:

- active route:
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`
- old route:
  `fixtures/<family>/README.md`
- decision:
  `docs/decisions/0041-proof-infra-fixture-families.md`
- validation route:
  `python scripts/build_catalog.py`, `python scripts/build_catalog.py --check`,
  `python scripts/validate_repo.py`, `python scripts/validate_semantic_agents.py`

## 2026-05-20 Reportable Contracts

The remaining root shared runner surface, scorer helper, and shared reportable
contract schemas were distilled into the `reportable-contracts` part of
`mechanics/proof-infra/`.

Why this route:

- bundle-local `runners/contract.json` files already consume these surfaces
  through `runner_surface_path` and `scorer_helper_paths`;
- `validate_repo.py`, catalog generation, and tests treat them as shared proof
  artifact contracts;
- source proof bundles still own the bounded claims, report schemas, examples,
  and reviewed reports;
- the root `runners/`, `scorers/`, and `schemas/` districts become route cards,
  not active payload homes.

Accounting:

- active route:
  `mechanics/proof-infra/parts/reportable-contracts/`
- old routes:
  `runners/reportable_proof_contract.md`,
  `scorers/bounded_rubric_breakdown.py`,
  `schemas/fixture-contract.schema.json`,
  `schemas/runner-contract.schema.json`,
  `schemas/report-summary.schema.json`
- decision:
  `docs/decisions/0049-proof-infra-reportable-contracts.md`
- validation route:
  `python scripts/validate_repo.py`, `python scripts/build_catalog.py --check`,
  `python scripts/validate_semantic_agents.py`,
  `python -m pytest -q mechanics/proof-infra/parts/reportable-contracts/tests/test_bounded_rubric_breakdown.py tests/test_build_catalog.py tests/test_validate_repo.py`
