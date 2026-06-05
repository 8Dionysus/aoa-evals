"""Generated eval comparison-spine projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import eval_comparison_spine_contract

from validators.common import ValidationIssue, relative_location
from validators.generated_eval_readmodel_common import (
    COMPARISON_SPINE_NAME,
    COMPARISON_SPINE_SOURCE_OF_TRUTH,
    COMPARISON_SPINE_VERSION,
    FULL_CATALOG_NAME,
    GENERATED_DIR_NAME,
    GeneratedReadModelContext,
    add_contract_issues,
    read_generated_object,
    validate_target_entry_parity,
    validate_versioned_source,
)


def validate_generated_comparison_spine(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: GeneratedReadModelContext,
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    comparison_spine_path = repo_root / GENERATED_DIR_NAME / COMPARISON_SPINE_NAME
    comparison_spine_location = relative_location(comparison_spine_path, repo_root)
    comparison_target_names = {record.name for record in records if record.manifest.get("baseline_mode") != "none"}
    if target_eval_names is not None:
        comparison_target_names &= set(target_eval_names)
    if not comparison_target_names and target_eval_names is not None:
        return issues

    expected_full, _expected_min = context.build_catalog_payloads(repo_root, records)
    expected_comparison_spine = context.build_comparison_spine_payload(repo_root, records, expected_full)
    actual_comparison_spine = read_generated_object(
        comparison_spine_path,
        label="generated comparison spine",
        issues=issues,
        repo_root=repo_root,
        context=context,
    )
    if actual_comparison_spine is None:
        return issues

    validate_versioned_source(
        actual_comparison_spine,
        version_key="comparison_spine_version",
        expected_version=COMPARISON_SPINE_VERSION,
        expected_source=COMPARISON_SPINE_SOURCE_OF_TRUTH,
        source_message="source_of_truth does not match the comparison spine contract",
        location=comparison_spine_location,
        issues=issues,
    )

    if target_eval_names is None:
        if actual_comparison_spine != expected_comparison_spine:
            issues.append(
                ValidationIssue(
                    comparison_spine_location,
                    "generated comparison spine is out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        validate_target_entry_parity(
            expected_payload=expected_comparison_spine,
            actual_payload=actual_comparison_spine,
            target_eval_names=sorted(comparison_target_names),
            location=comparison_spine_location,
            missing_message="generated comparison spine is missing eval '{eval_name}'",
            drift_message=(
                "generated comparison spine entry for '{eval_name}' is out of date; "
                "run 'python scripts/build_catalog.py'"
            ),
            issues=issues,
        )

    actual_full = context.read_json_file(full_path, issues, repo_root)
    if not isinstance(actual_full, dict):
        return issues

    contract_issues = eval_comparison_spine_contract.validate_comparison_spine_alignment(
        actual_full,
        actual_comparison_spine,
        location=comparison_spine_location,
        target_eval_names=comparison_target_names if comparison_target_names else None,
    )
    add_contract_issues(issues, contract_issues)
    return issues
