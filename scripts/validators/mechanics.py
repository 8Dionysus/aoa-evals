"""Mechanics-facing root-authored surface contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.mechanics_common import (
    DECISION_RECORDS_README_NAME,
    MECHANICS_AGENTS_NAME,
    MECHANICS_EVIDENCE_CLUSTERS,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
)
from validators.mechanic_evidence_dimensions import (
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS,
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS,
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS,
    validate_mechanic_evidence_dimension_ledger,
)
from validators.mechanic_evidence_route_refs import (
    MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS,
    MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND,
    MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME,
    MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS,
    MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS,
    MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT,
    MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES,
    MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS,
    MECHANIC_EVIDENCE_ROUTE_REFS_SECTION,
    validate_mechanic_evidence_route_refs,
)
from validators.mechanic_parent_registry import (
    ACTIVE_MECHANIC_PARENT_NAMES,
    AOA_ALIGNED_MECHANIC_PARENT_NAMES,
    EVALS_NATIVE_MECHANIC_PARENT_NAMES,
    FORMER_WRONG_MECHANIC_PARENT_ROUTES,
    MECHANIC_PARENT_CLASS_DECISION_NAME,
    MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS,
    validate_mechanic_parent_class_surfaces,
)
from validators.mechanics_root_districts import (
    MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
    MECHANIC_ROOT_DISTRICT_RECON_COLUMNS,
    MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
    MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS,
    MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS,
    MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS,
    MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS,
    MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS,
    validate_mechanic_root_district_recon_surfaces,
)
from validators.root_authored_surface_common import (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    expected_root_authored_surfaces,
    root_authored_surface_classification_districts,
)
from validators.root_authored_surface_decision import validate_root_authored_surface_decision
from validators.root_authored_surface_inventory import validate_root_authored_surface_inventory
from validators.root_authored_surface_ledger import validate_root_authored_surface_ledger

PART_LOCAL_TEST_PLACEMENT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0050-part-local-test-placement.md"
)

MECHANICS_REQUIRED_TOKENS = (
    "operation atlas",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "proof-object",
    "proof-loop",
    "comparison-spine",
    "proof-infra",
    "publication-receipts",
    "release-support",
    "titan",
    "agon",
    "questbook",
    "audit",
    "boundary-bridge",
    "Candidate families",
    "Candidate families stay evidence-only",
    "Current candidate promotion state: empty",
    "recurrence",
    "checkpoint",
    "experience",
    "antifragility",
    "method-growth",
    "rpg",
    "growth-cycle",
    "distillation",
    "Package taxonomy requires source surfaces, inputs, outputs, boundaries",
    "proof-layer operation",
    "Parent Class Summary",
    "AoA-aligned parents",
    "Evals-native parents",
    "owner-named evals-native",
    "Concrete wrong-parent mappings live in",
)
MECHANICS_AGENTS_REQUIRED_TOKENS = (
    "repeatable proof-layer operations",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "source proof objects",
    "generated readers",
    "runtime candidates",
)
MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS = (
    "parent-mechanic evidence gate",
    "Evidence Standard",
    "Root District Reconnaissance Ledger",
    "AoA-aligned parents",
    "Evals-native parents",
    "Class Membership Contract",
    "cross-root evidence",
    "owner-named evals-native",
    "aoa-agents` keeps stronger Titan law",
    "`agon`",
    "`audit`",
    "`boundary-bridge`",
    "`recurrence`",
    "`checkpoint`",
    "`experience`",
    "`antifragility`",
    "`method-growth`",
    "`rpg`",
    "`growth-cycle`",
    "`distillation`",
    "`release-support`",
    "`titan`",
    "`agon-proof`",
    "`titan-canaries`",
    "`proof-release`",
    "`runtime-evidence`",
    "`sibling-proof-refs`",
    "`repair`",
    "Legacy Rule",
    "PROVENANCE.md",
    "legacy archive",
    "diagnosis-cause discipline routes through `growth-cycle/diagnosis-gate` as the active diagnosis lane.",
    "Single documents, reports, and canary forms route as parts under the right parent",
)
PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS = (
    "Part-local Test Placement",
    "mechanics/<mechanic>/parts/<part>/tests/",
    "Root `tests/` remains the repository-wide test district",
    "python -m pytest -q",
    "does not create a new parent mechanic from a test name",
)


def validate_mechanics_root_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=MECHANICS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=MECHANICS_AGENTS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_EVIDENCE_CLUSTERS_NAME,
        tokens=MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PART_LOCAL_TEST_PLACEMENT_DECISION_NAME,
        tokens=PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(PART_LOCAL_TEST_PLACEMENT_DECISION_NAME, "Part-local Test Placement"),
        issues=issues,
    )
    return issues


def validate_root_authored_surface_classification(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(validate_root_authored_surface_inventory(repo_root))
    issues.extend(validate_root_authored_surface_ledger(repo_root))
    issues.extend(validate_root_authored_surface_decision(repo_root))
    return issues


__all__ = (
    "ACTIVE_MECHANIC_PARENT_NAMES",
    "AOA_ALIGNED_MECHANIC_PARENT_NAMES",
    "DECISION_RECORDS_README_NAME",
    "EVALS_NATIVE_MECHANIC_PARENT_NAMES",
    "FORMER_WRONG_MECHANIC_PARENT_ROUTES",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_COLUMNS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_COMMAND",
    "MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_NAME",
    "MECHANIC_EVIDENCE_ROUTE_REFS_DECISION_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_FORBIDDEN_GENERIC_REFS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_MIN_COUNT",
    "MECHANIC_EVIDENCE_ROUTE_REFS_RATIONALE_ONLY_PREFIXES",
    "MECHANIC_EVIDENCE_ROUTE_REFS_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_ROUTE_REFS_SECTION",
    "MECHANIC_PARENT_CLASS_DECISION_NAME",
    "MECHANIC_PARENT_CLASS_DECISION_REQUIRED_TOKENS",
    "MECHANIC_ROOT_DISTRICT_RECON_COLUMNS",
    "MECHANIC_ROOT_DISTRICT_RECON_COMMAND",
    "MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME",
    "MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS",
    "MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS",
    "MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS",
    "MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS",
    "MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS",
    "MECHANICS_AGENTS_NAME",
    "MECHANICS_AGENTS_REQUIRED_TOKENS",
    "MECHANICS_EVIDENCE_CLUSTERS",
    "MECHANICS_EVIDENCE_CLUSTERS_NAME",
    "MECHANICS_EVIDENCE_CLUSTERS_REQUIRED_TOKENS",
    "MECHANICS_README_NAME",
    "MECHANICS_REQUIRED_TOKENS",
    "PART_LOCAL_TEST_PLACEMENT_DECISION_NAME",
    "PART_LOCAL_TEST_PLACEMENT_DECISION_REQUIRED_TOKENS",
    "PROOF_TOPOLOGY_NAME",
    "ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS",
    "ROADMAP_NAME",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION",
    "expected_root_authored_surfaces",
    "root_authored_surface_classification_districts",
    "validate_mechanic_evidence_dimension_ledger",
    "validate_mechanic_evidence_route_refs",
    "validate_mechanic_parent_class_surfaces",
    "validate_mechanic_root_district_recon_surfaces",
    "validate_mechanics_root_route_surfaces",
    "validate_root_authored_surface_classification",
)
