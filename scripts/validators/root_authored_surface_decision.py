"""Residual root-authored surface decision-route checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.mechanics_common import (
    DECISION_RECORDS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
)
from validators.root_authored_surface_common import (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
)


def validate_root_authored_surface_decision(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(
        repo_root=repo_root,
        path_name=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
        tokens=ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME,
            "Root-authored Surface Classification",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
            "unclassified root-authored surface",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )
    return issues


__all__ = ("validate_root_authored_surface_decision",)
