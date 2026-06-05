"""Audit route, provenance, and candidate-evidence boundary contracts."""

from __future__ import annotations

from pathlib import Path

from validators import audit_route_paths as audit_paths
from validators import audit_route_tokens as audit_tokens
from validators.audit_route_helpers import DECISION_RECORDS_README_NAME, require_tokens
from validators.common import ValidationIssue


def validate_audit_parts_route_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = require_tokens(
        repo_root=repo_root,
        path_name=audit_paths.AUDIT_PARTS_README_NAME,
        tokens=audit_tokens.AUDIT_PARTS_README_REQUIRED_TOKENS,
        issues=issues,
    )
    if text:
        for forbidden_token in audit_tokens.AUDIT_PARTS_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        audit_paths.AUDIT_PARTS_README_NAME,
                        "audit parts index should expose a positive part-admission route",
                    )
                )
    return issues


def validate_audit_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (audit_paths.AUDIT_MECHANIC_README_NAME, audit_tokens.AUDIT_MECHANIC_REQUIRED_TOKENS),
        (audit_paths.AUDIT_MECHANIC_AGENTS_NAME, audit_tokens.AUDIT_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (audit_paths.AUDIT_MECHANIC_PROVENANCE_NAME, audit_tokens.AUDIT_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (audit_paths.AUDIT_LEGACY_INDEX_NAME, audit_tokens.AUDIT_LEGACY_INDEX_REQUIRED_TOKENS),
        (audit_paths.AUDIT_LEGACY_DISTILLATION_LOG_NAME, audit_tokens.AUDIT_LEGACY_DISTILLATION_REQUIRED_TOKENS),
        (audit_paths.AUDIT_LEGACY_RAW_README_NAME, audit_tokens.AUDIT_LEGACY_RAW_README_REQUIRED_TOKENS),
        (audit_paths.AUDIT_SELECTED_EVIDENCE_PART_README_NAME, audit_tokens.AUDIT_SELECTED_EVIDENCE_PART_README_REQUIRED_TOKENS),
        (
            audit_paths.AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_NAME,
            audit_tokens.AUDIT_ARTIFACT_VERDICT_HOOKS_PART_README_REQUIRED_TOKENS,
        ),
        (audit_paths.AUDIT_CANDIDATE_READERS_PART_README_NAME, audit_tokens.AUDIT_CANDIDATE_READERS_PART_README_REQUIRED_TOKENS),
        (audit_paths.AUDIT_INTEGRITY_REVIEW_PART_README_NAME, audit_tokens.AUDIT_INTEGRITY_REVIEW_PART_README_REQUIRED_TOKENS),
        (audit_paths.AUDIT_PART_CONTRACT_GUARD_DECISION_NAME, audit_tokens.AUDIT_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS),
        (
            DECISION_RECORDS_README_NAME,
            (audit_paths.AUDIT_PART_CONTRACT_GUARD_DECISION_NAME, "Audit Part Contract Guard"),
        ),
        (audit_paths.AUDIT_MECHANIC_DECISION_NAME, audit_tokens.AUDIT_MECHANIC_DECISION_REQUIRED_TOKENS),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    issues.extend(validate_audit_parts_route_surface(repo_root))
    return issues


__all__ = (
    "validate_audit_parts_route_surface",
    "validate_audit_route_surfaces",
)
