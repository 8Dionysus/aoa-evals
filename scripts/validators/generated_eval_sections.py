"""Generated eval section projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import eval_section_contract

from validators.common import ValidationIssue, relative_location
from validators.generated_eval_readmodel_common import (
    FULL_CATALOG_NAME,
    GENERATED_DIR_NAME,
    SECTION_NAME,
    SECTION_SOURCE_OF_TRUTH,
    SECTION_VERSION,
    GeneratedReadModelContext,
    add_contract_issues,
    entries_by_name,
    read_generated_object,
    validate_target_entry_parity,
    validate_versioned_source,
)


def validate_generated_sections(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: GeneratedReadModelContext,
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    sections_path = repo_root / GENERATED_DIR_NAME / SECTION_NAME
    sections_location = relative_location(sections_path, repo_root)

    expected_sections, section_contract_issues = eval_section_contract.build_sections_payload(repo_root, records)
    add_contract_issues(issues, section_contract_issues)
    if section_contract_issues:
        return issues

    actual_sections = read_generated_object(
        sections_path,
        label="generated sections",
        issues=issues,
        repo_root=repo_root,
        context=context,
    )
    if actual_sections is None:
        return issues
    validate_versioned_source(
        actual_sections,
        version_key="section_version",
        expected_version=SECTION_VERSION,
        expected_source=SECTION_SOURCE_OF_TRUTH,
        source_message="source_of_truth does not match the section contract",
        location=sections_location,
        issues=issues,
    )

    if target_eval_names is None:
        if actual_sections != expected_sections:
            issues.append(
                ValidationIssue(
                    sections_location,
                    "generated sections are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        validate_target_entry_parity(
            expected_payload=expected_sections,
            actual_payload=actual_sections,
            target_eval_names=target_eval_names,
            location=sections_location,
            missing_message="generated sections are missing eval '{eval_name}'",
            drift_message=(
                "generated section entry for '{eval_name}' is out of date; "
                "run 'python scripts/build_catalog.py'"
            ),
            issues=issues,
        )

    actual_full = context.read_json_file(full_path, issues, repo_root)
    if not isinstance(actual_full, dict):
        return issues

    issue_count = len(issues)
    catalog_entries = entries_by_name(actual_full, location=relative_location(full_path, repo_root), issues=issues)
    section_entries = entries_by_name(actual_sections, location=sections_location, issues=issues)
    if len(issues) > issue_count:
        return issues

    catalog_names = set(catalog_entries)
    section_names = set(section_entries)
    if target_eval_names is not None:
        target_name_set = set(target_eval_names)
        catalog_names &= target_name_set
        section_names &= target_name_set

    for missing in sorted(catalog_names - section_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections are missing eval '{missing}' from generated/eval_catalog.json",
            )
        )
    for extra in sorted(section_names - catalog_names):
        issues.append(
            ValidationIssue(
                sections_location,
                f"generated sections include unknown eval '{extra}' from generated/eval_catalog.json",
            )
        )

    for eval_name in sorted(catalog_names & section_names):
        catalog_entry = catalog_entries[eval_name]
        section_entry = section_entries[eval_name]
        for field_name in ("category", "status", "verdict_shape", "eval_path"):
            if section_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    ValidationIssue(
                        sections_location,
                        f"generated section entry for '{eval_name}' must align with full catalog field '{field_name}'",
                    )
                )

    return issues
