"""Root design, architecture, and decision-surface contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_design_common import (
    DECISION_RECORDS_README_NAME,
    DESIGN_AGENTS_NAME,
    DESIGN_NAME,
    require_tokens,
)


ROOT_DESIGN_REQUIRED_TOKENS = (
    "bounded proof organ",
    "proof object",
    "generated surface helps navigation",
    "runtime candidates",
    "bundle-local review turns candidate help",
    "proof meaning comes from source refs, owner routes, generated parity",
    "Local owner truth stays authoritative",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "docs/architecture/ARCHITECTURE.md",
    "docs/guides/EVAL_PHILOSOPHY.md",
    "docs/decisions/",
)
ARCHITECTURE_PROOF_MODEL_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0093-architecture-proof-model-contract.md"
)
ARCHITECTURE_PROOF_MODEL_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k architecture_proof_model"
)
ARCHITECTURE_REQUIRED_TOKENS = (
    "technical proof model",
    "Use this file for the proof model",
    "DESIGN.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "### Mechanics",
    "proof-layer operation",
    "### Layer 5: proof operation support",
    "AoA-aligned mechanics",
    "Evals-native mechanics",
    "owner-named evals-native",
    "Artifact forms",
    "PROVENANCE.md",
    "single controlled bridge",
    "regression visibility with bounded comparison semantics",
    "growth tracking with explicit claim limits",
)
ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS = (
    "It is not the system design thesis",
    "but they are not themselves eval bundles",
    "but they are not themselves proof surfaces",
)
ARCHITECTURE_FORBIDDEN_ROUTE_SCAFFOLD = (
    "regression visibility without metric theater",
    "growth tracking without inflated claims",
)
ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS = (
    "Architecture Proof Model Contract",
    "technical proof model",
    "DESIGN.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "mechanics as operation support",
    "owner-named evals-native",
    "legacy bridge layering",
    "bounded comparison semantics",
    "explicit claim limits",
    ARCHITECTURE_PROOF_MODEL_COMMAND,
)
DESIGN_AGENTS_REQUIRED_TOKENS = (
    "agent-facing guidance",
    "nearest card",
    "bundle-local review",
    "source proof object",
    "generated companions",
    "Quest source records carry return routes",
    "Proof-meaning checks need source refs, owner routes, generated parity",
    "Active mechanic packages",
    "Before changing package boundaries",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "active mechanics, and file-movement boundaries",
    "Maintained agent lanes",
    ".agents/spark/",
    "closeout",
)
ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING = ("mechanic-ready",)
ROOT_DESIGN_FORBIDDEN_ROUTE_SCAFFOLD = (
    "without requiring a full local AoA deployment",
    "They do not become proof acceptance without",
    "A polished single run is not enough",
    "it is not ready to make a strong claim",
    "Green file presence alone is not proof",
    "This file does not override local owner truth",
    "without a compatibility decision",
)
DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING = (
    "Future mechanic packages",
    "Before package growth",
    "before mechanics or file movement",
)
DESIGN_AGENTS_FORBIDDEN_ROUTE_SCAFFOLD = (
    "they do not replace the\nsource surface",
    "not eval\nbundles and not roadmap direction",
    "Presence-only checks are not enough for proof meaning",
    "but they do not own proof meaning",
    "Negative boundaries stay narrow",
    "not a home base",
)
ROOT_AGENTS_DESIGN_REQUIRED_TOKENS = (
    "DESIGN.md",
    "DESIGN.AGENTS.md",
    "mechanics/EVIDENCE_CLUSTERS.md",
    "docs/decisions/",
)
DECISION_SURFACE_REQUIRED_TOKENS = (
    "bounded proof",
    "source surface",
    "generated",
    "runtime",
    "sibling",
)
DECISION_TEMPLATE_REQUIRED_TOKENS = (
    "## Context",
    "## Options Considered",
    "## Decision",
    "## Consequences",
    "## Current Applicability",
    "## Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "## Validation",
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0100-active-mechanics-topology-wording.md"
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k "
    "'root_design or design_agents or proof_topology'"
)
ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS = (
    "Active Mechanics Topology Wording",
    "active mechanics",
    "stale preparatory wording",
    "PROVENANCE.md",
    "archive details",
    ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND,
)


def validate_root_design_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    design_text = require_tokens(repo_root, DESIGN_NAME, ROOT_DESIGN_REQUIRED_TOKENS, issues)
    architecture_text = require_tokens(
        repo_root,
        "docs/architecture/ARCHITECTURE.md",
        ARCHITECTURE_REQUIRED_TOKENS,
        issues,
    )
    design_agents_text = require_tokens(
        repo_root,
        DESIGN_AGENTS_NAME,
        DESIGN_AGENTS_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(repo_root, "AGENTS.md", ROOT_AGENTS_DESIGN_REQUIRED_TOKENS, issues)
    require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        DECISION_SURFACE_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(
        repo_root,
        "docs/decisions/TEMPLATE.md",
        DECISION_TEMPLATE_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(
        repo_root,
        "docs/decisions/AGENTS.md",
        (
            "source surface",
            "validate_repo.py",
            "sibling",
            "Amendment Route",
            "Review Log",
            "Current Applicability",
            "Previous assumption",
            "New reality",
            "Status",
            "Superseded by",
            "strikethrough",
            "active route",
            "owner surface",
            "validation evidence",
        ),
        issues,
    )
    require_tokens(
        repo_root,
        ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
        ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(
        repo_root,
        ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
        ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS,
        issues,
    )
    require_tokens(
        repo_root,
        DECISION_RECORDS_README_NAME,
        (
            ARCHITECTURE_PROOF_MODEL_DECISION_NAME,
            "Architecture Proof Model Contract",
            ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME,
            "Active Mechanics Topology Wording",
        ),
        issues,
    )
    if design_text:
        for stale_phrase in ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in design_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_NAME,
                        f"root design must describe active mechanic authority, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in ROOT_DESIGN_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in design_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_NAME,
                        "root design should route proof pressure through positive owner "
                        f"language instead of stale scaffold '{stale_phrase}'",
                    )
                )
    if architecture_text:
        for stale_phrase in ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS:
            if stale_phrase in architecture_text:
                issues.append(
                    ValidationIssue(
                        "docs/architecture/ARCHITECTURE.md",
                        "architecture should route related surfaces positively instead of stale negative role scaffold "
                        f"'{stale_phrase}'",
                    )
                )
        for stale_phrase in ARCHITECTURE_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in architecture_text:
                issues.append(
                    ValidationIssue(
                        "docs/architecture/ARCHITECTURE.md",
                        "architecture long-term direction should name the proof route "
                        f"instead of stale scaffold '{stale_phrase}'",
                    )
                )
    if design_agents_text:
        for stale_phrase in DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING:
            if stale_phrase in design_agents_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_AGENTS_NAME,
                        f"agent design must describe active mechanic packages, not stale preparatory wording '{stale_phrase}'",
                    )
                )
        for stale_phrase in DESIGN_AGENTS_FORBIDDEN_ROUTE_SCAFFOLD:
            if stale_phrase in design_agents_text:
                issues.append(
                    ValidationIssue(
                        DESIGN_AGENTS_NAME,
                        "agent design should name owner routes before old "
                        f"negative scaffold '{stale_phrase}'",
                    )
                )
    return issues


__all__ = (
    "DESIGN_NAME",
    "DESIGN_AGENTS_NAME",
    "ROOT_DESIGN_REQUIRED_TOKENS",
    "ARCHITECTURE_PROOF_MODEL_DECISION_NAME",
    "ARCHITECTURE_PROOF_MODEL_COMMAND",
    "ARCHITECTURE_REQUIRED_TOKENS",
    "ARCHITECTURE_FORBIDDEN_NEGATIVE_ROLE_TOKENS",
    "ARCHITECTURE_FORBIDDEN_ROUTE_SCAFFOLD",
    "ARCHITECTURE_PROOF_MODEL_DECISION_REQUIRED_TOKENS",
    "DESIGN_AGENTS_REQUIRED_TOKENS",
    "ROOT_DESIGN_FORBIDDEN_STALE_MECHANIC_WORDING",
    "ROOT_DESIGN_FORBIDDEN_ROUTE_SCAFFOLD",
    "DESIGN_AGENTS_FORBIDDEN_STALE_MECHANIC_WORDING",
    "DESIGN_AGENTS_FORBIDDEN_ROUTE_SCAFFOLD",
    "ROOT_AGENTS_DESIGN_REQUIRED_TOKENS",
    "DECISION_SURFACE_REQUIRED_TOKENS",
    "DECISION_TEMPLATE_REQUIRED_TOKENS",
    "ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_NAME",
    "ACTIVE_MECHANICS_TOPOLOGY_WORDING_COMMAND",
    "ACTIVE_MECHANICS_TOPOLOGY_WORDING_DECISION_REQUIRED_TOKENS",
    "validate_root_design_surfaces",
)
