"""Shared helpers for bundle-local source eval artifact validators."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_catalog_contract
from validators.common import ValidationIssue


def requires_materialized_comparison_artifacts(manifest: dict[str, Any] | None) -> bool:
    if not isinstance(manifest, dict):
        return False
    return (
        manifest.get("report_format") == "comparative-summary"
        and manifest.get("baseline_mode") != "none"
    )


def ensure_repo_relative_path(raw_path: str, location: str, issues: list[ValidationIssue]) -> str:
    value, contract_issues = eval_catalog_contract.ensure_repo_relative_path(raw_path, location)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return value


def validate_repo_relative_contract_path(
    repo_root: Path,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    normalized_path = ensure_repo_relative_path(raw_path, location, issues)
    if not normalized_path:
        return None
    resolved_path = repo_root / normalized_path
    if not resolved_path.exists():
        issues.append(
            ValidationIssue(
                location,
                f"path '{normalized_path}' does not exist",
            )
        )
        return None
    return normalized_path


def validate_raw_repo_relative_path(
    raw_value: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_value, str):
        return None
    normalized_path = ensure_repo_relative_path(raw_value, location, issues)
    return normalized_path or None


def validate_raw_repo_relative_path_list(
    payload: dict[str, Any],
    key: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> list[str]:
    raw_values = payload.get(key, [])
    if not isinstance(raw_values, list):
        return []

    normalized_paths: list[str] = []
    for index, raw_value in enumerate(raw_values):
        normalized_path = validate_raw_repo_relative_path(
            raw_value,
            location=f"{location}.{key}[{index}]",
            issues=issues,
        )
        if normalized_path is not None:
            normalized_paths.append(normalized_path)
    return normalized_paths


__all__ = (
    "requires_materialized_comparison_artifacts",
    "ensure_repo_relative_path",
    "validate_repo_relative_contract_path",
    "validate_raw_repo_relative_path",
    "validate_raw_repo_relative_path_list",
)
