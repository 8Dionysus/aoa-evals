"""Generated eval catalog and min-catalog projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators.common import ValidationIssue, relative_location
from validators.generated_eval_readmodel_common import (
    CATALOG_SOURCE_OF_TRUTH,
    CATALOG_VERSION,
    FULL_CATALOG_NAME,
    GENERATED_DIR_NAME,
    MIN_CATALOG_NAME,
    GeneratedReadModelContext,
    entries_by_name,
    project_min_catalog_safely,
    validate_catalog_metadata,
)


def validate_generated_catalogs(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: GeneratedReadModelContext,
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    min_path = repo_root / GENERATED_DIR_NAME / MIN_CATALOG_NAME

    expected_full, expected_min = context.build_catalog_payloads(repo_root, records)
    actual_full = context.read_json_file(full_path, issues, repo_root)
    actual_min = context.read_json_file(min_path, issues, repo_root)

    if actual_full is None or actual_min is None:
        return issues

    full_location = relative_location(full_path, repo_root)
    min_location = relative_location(min_path, repo_root)
    if target_eval_names is None:
        if actual_full != expected_full:
            issues.append(
                ValidationIssue(
                    full_location,
                    "generated catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min != expected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "generated min catalog is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min = project_min_catalog_safely(
            actual_full,
            location=full_location,
            label="generated catalog",
            issues=issues,
            context=context,
        )
        if projected_min is None:
            return issues
        if actual_min != projected_min:
            issues.append(
                ValidationIssue(
                    min_location,
                    "min catalog must stay a projection of the full catalog",
                )
            )
        return issues

    validate_catalog_metadata(
        actual_full,
        expected_full,
        location=full_location,
        label="generated catalog",
        issues=issues,
    )
    validate_catalog_metadata(
        actual_min,
        expected_min,
        location=min_location,
        label="generated min catalog",
        issues=issues,
    )

    full_entries = entries_by_name(actual_full, location=full_location, issues=issues)
    min_entries = entries_by_name(actual_min, location=min_location, issues=issues)

    expected_full_entries = {record.name: context.full_catalog_entry(repo_root, record) for record in records}
    expected_min_entries = {
        name: context.project_min_catalog(
            {
                "catalog_version": CATALOG_VERSION,
                "source_of_truth": CATALOG_SOURCE_OF_TRUTH,
                "evals": [entry],
            }
        )["evals"][0]
        for name, entry in expected_full_entries.items()
    }

    for eval_name in target_eval_names:
        actual_full_entry = full_entries.get(eval_name)
        actual_min_entry = min_entries.get(eval_name)
        if actual_full_entry is None:
            issues.append(ValidationIssue(full_location, f"generated catalog is missing eval '{eval_name}'"))
            continue
        if actual_min_entry is None:
            issues.append(ValidationIssue(min_location, f"generated min catalog is missing eval '{eval_name}'"))
            continue

        expected_full_entry = expected_full_entries[eval_name]
        expected_min_entry = expected_min_entries[eval_name]
        if actual_full_entry != expected_full_entry:
            issues.append(
                ValidationIssue(
                    full_location,
                    f"generated catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )
        if actual_min_entry != expected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' is out of date; run 'python scripts/build_catalog.py'",
                )
            )

        projected_min_catalog_payload = project_min_catalog_safely(
            {
                "catalog_version": actual_full.get("catalog_version"),
                "source_of_truth": actual_full.get("source_of_truth"),
                "evals": [actual_full_entry],
            },
            location=full_location,
            label=f"generated catalog entry for '{eval_name}'",
            issues=issues,
            context=context,
        )
        if projected_min_catalog_payload is None:
            continue
        projected_min_entry = projected_min_catalog_payload["evals"][0]
        if actual_min_entry != projected_min_entry:
            issues.append(
                ValidationIssue(
                    min_location,
                    f"generated min catalog entry for '{eval_name}' must stay a projection of the full catalog",
                )
            )

    return issues
