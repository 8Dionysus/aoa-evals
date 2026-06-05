"""Shared context for generated eval read-model parity validators."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

import eval_capsule_contract
import eval_catalog_contract
import eval_comparison_spine_contract
import eval_section_contract

from validators.common import ValidationIssue, relative_location

GENERATED_DIR_NAME = "generated"
FULL_CATALOG_NAME = eval_catalog_contract.FULL_CATALOG_NAME
MIN_CATALOG_NAME = eval_catalog_contract.MIN_CATALOG_NAME
CATALOG_VERSION = eval_catalog_contract.CATALOG_VERSION
CATALOG_SOURCE_OF_TRUTH = eval_catalog_contract.CATALOG_SOURCE_OF_TRUTH
CAPSULE_NAME = eval_capsule_contract.CAPSULE_NAME
CAPSULE_VERSION = eval_capsule_contract.CAPSULE_VERSION
CAPSULE_SOURCE_OF_TRUTH = eval_capsule_contract.CAPSULE_SOURCE_OF_TRUTH
SECTION_NAME = eval_section_contract.SECTIONS_NAME
SECTION_VERSION = eval_section_contract.SECTION_VERSION
SECTION_SOURCE_OF_TRUTH = eval_section_contract.SECTION_SOURCE_OF_TRUTH
COMPARISON_SPINE_NAME = eval_comparison_spine_contract.COMPARISON_SPINE_NAME
COMPARISON_SPINE_VERSION = eval_comparison_spine_contract.COMPARISON_SPINE_VERSION
COMPARISON_SPINE_SOURCE_OF_TRUTH = eval_comparison_spine_contract.COMPARISON_SPINE_SOURCE_OF_TRUTH


@dataclass(frozen=True)
class GeneratedReadModelContext:
    build_catalog_payloads: Callable[[Path, Sequence[Any]], tuple[dict[str, Any], dict[str, Any]]]
    build_capsule_payload: Callable[[Path, Sequence[Any], dict[str, Any]], dict[str, Any]]
    build_comparison_spine_payload: Callable[[Path, Sequence[Any], dict[str, Any]], dict[str, Any]]
    full_catalog_entry: Callable[[Path, Any], dict[str, Any]]
    project_min_catalog: Callable[[dict[str, Any]], dict[str, Any]]
    read_json_file: Callable[[Path, list[ValidationIssue], Path], Any | None]


def project_min_catalog_safely(
    full_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
    context: GeneratedReadModelContext,
) -> dict[str, Any] | None:
    try:
        return context.project_min_catalog(full_catalog)
    except (KeyError, TypeError):
        issues.append(
            ValidationIssue(
                location,
                f"{label} is malformed; min projection could not be computed",
            )
        )
        return None


def validate_catalog_metadata(
    actual_catalog: dict[str, Any],
    expected_catalog: dict[str, Any],
    *,
    location: str,
    label: str,
    issues: list[ValidationIssue],
) -> None:
    if (
        actual_catalog.get("catalog_version") != expected_catalog["catalog_version"]
        or actual_catalog.get("source_of_truth") != expected_catalog["source_of_truth"]
    ):
        issues.append(
            ValidationIssue(
                location,
                f"{label} metadata is out of date; run 'python scripts/build_catalog.py'",
            )
        )


def add_contract_issues(issues: list[ValidationIssue], contract_issues: Sequence[Any]) -> None:
    issues.extend(ValidationIssue(issue.location, issue.message) for issue in contract_issues)


def read_generated_object(
    path: Path,
    *,
    label: str,
    issues: list[ValidationIssue],
    repo_root: Path,
    context: GeneratedReadModelContext,
) -> dict[str, Any] | None:
    payload = context.read_json_file(path, issues, repo_root)
    if payload is None:
        return None
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(relative_location(path, repo_root), f"{label} payload must be an object"))
        return None
    return payload


def validate_versioned_source(
    payload: dict[str, Any],
    *,
    version_key: str,
    expected_version: Any,
    expected_source: str,
    source_message: str,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if payload.get(version_key) != expected_version:
        issues.append(ValidationIssue(location, f"{version_key} must be {expected_version}"))
    if payload.get("source_of_truth") != expected_source:
        issues.append(ValidationIssue(location, source_message))


def entries_by_name(
    payload: dict[str, Any],
    *,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, Any]:
    entries, entry_issues = eval_catalog_contract.catalog_entries_by_name(
        payload,
        array_key="evals",
        key_name="name",
        location=location,
    )
    add_contract_issues(issues, entry_issues)
    return entries


def validate_target_entry_parity(
    *,
    expected_payload: dict[str, Any],
    actual_payload: dict[str, Any],
    target_eval_names: Sequence[str],
    location: str,
    missing_message: str,
    drift_message: str,
    issues: list[ValidationIssue],
) -> None:
    expected_entries = entries_by_name(expected_payload, location=location, issues=issues)
    actual_entries = entries_by_name(actual_payload, location=location, issues=issues)
    for eval_name in target_eval_names:
        actual_entry = actual_entries.get(eval_name)
        if actual_entry is None:
            issues.append(ValidationIssue(location, missing_message.format(eval_name=eval_name)))
            continue
        if actual_entry != expected_entries[eval_name]:
            issues.append(ValidationIssue(location, drift_message.format(eval_name=eval_name)))
