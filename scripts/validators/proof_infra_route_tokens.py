"""Proof-infra route token constants."""

from __future__ import annotations

from validators import mechanic_provenance_bridge, proof_infra_common as common


MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    mechanic_provenance_bridge.MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
)
PROOF_INFRA_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/guides/SHARED_PROOF_INFRA_GUIDE.md",
    "fixtures/README.md",
    common.PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
    common.PROOF_INFRA_REPORTABLE_CONTRACTS_SCORER_NAME,
    common.FIXTURE_CONTRACT_SCHEMA_NAME,
    common.RUNNER_CONTRACT_SCHEMA_NAME,
    common.REPORT_SUMMARY_SCHEMA_NAME,
    "reports/README.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "generated catalog `proof_artifacts`",
    "shared_fixture_family_path",
    "mechanics/proof-infra/parts/fixture-families/fixtures/",
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "report_schema_path",
    "root infrastructure districts stay route-card districts unless a part-local owner exists",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "shared proof infrastructure",
    "fixtures/contract.json",
    "runners/contract.json",
    "reports/summary.schema.json",
    "generated catalog `proof_artifacts`",
    "bundle-local interpretation",
    "parts/fixture-families/fixtures/",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "fixture-families",
    "reportable-contracts",
    "bundle support need",
    "shared_fixture_family_path",
    "runner_surface_path",
    "Fixture-family parent pressure",
    "Boundary Routes",
    "AGENTS.md#validation",
)
PROOF_INFRA_FIXTURE_FAMILIES_REQUIRED_TOKENS = (
    "bundle support need",
    "public-safe reusable family",
    "shared_fixture_family_path",
    "ambiguity-bounded-v1",
    "verification-honesty-v1",
    "witness-trace-v1",
    "Family-name parent pressure",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_FIXTURE_FAMILIES_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "generic shared fixture-family support",
    "public-safe reusable support",
    "bundle-local `EVAL.md`",
    "evals/**/fixtures/contract.json",
    "shared_fixture_family_path",
    "Family-name parent pressure",
    "centralized-child-validation",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_REQUIRED_TOKENS = (
    "bundle-local runner contract",
    "reportable proof contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "fixture-contract.schema.json",
    "runner-contract.schema.json",
    "report-summary.schema.json",
    "`evals/<family>/<eval>/EVAL.md`",
    "tests/test_bounded_rubric_breakdown.py",
    "python scripts/validate_repo.py",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_AGENTS_REQUIRED_TOKENS = (
    "## Operating Card",
    "reportable-contracts",
    "bundle-local runner contract",
    "runner_surface_path",
    "scorer_helper_paths",
    "Schema weakening pressure",
    "Root alias pressure",
    "centralized-child-validation",
    "bounded rubric scorer test",
)
PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES = (
    "It does not own bundle meaning",
    "It does not own bundle-local meaning",
    "Keep the family weaker than the bundle-local claim",
    "Keep the shared runner surface weaker than bundle-local interpretation",
    "Do not add hidden benchmark cases",
    "Do not add hidden harness logic",
    "Do not recreate active root aliases",
)
PROOF_INFRA_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_INFRA_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/ambiguity-bounded-v1/README.md",
    "fixtures/verification-honesty-v1/README.md",
    "mechanics/proof-infra/parts/fixture-families/fixtures",
    "runners/reportable_proof_contract.md",
    "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
    "scorers/bounded_rubric_breakdown.py",
    "schemas/runner-contract.schema.json",
    "Former root paths are provenance only",
)
PROOF_INFRA_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/",
    "shared proof contract",
    "generated proof_artifacts",
    "Decision 0041",
    "Decision 0049",
    "bundle-local `EVAL.md`",
    "schema weakening",
    "repo-global scoring",
)
PROOF_INFRA_FIXTURE_FAMILIES_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/fixture-families/",
    "generic shared fixture families",
    "no narrower active mechanic",
    "Root `fixtures/` remains a compatibility route card",
    "does not make fixture families stronger than bundle-local meaning",
    "python scripts/build_catalog.py --check",
)
PROOF_INFRA_REPORTABLE_CONTRACTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-infra/parts/reportable-contracts/",
    "runner_surface_path",
    "scorer_helper_paths",
    "root `runners/`, `scorers/`, and `schemas/` remain compatibility route cards",
    "does not make reportable contracts stronger than bundle-local meaning",
    "python scripts/validate_repo.py",
)


__all__ = (
    "MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS",
    "PROOF_INFRA_PART_AGENTS_STALE_ROUTE_PHRASES",
    *(name for name in globals() if name.endswith("_TOKENS")),
)
