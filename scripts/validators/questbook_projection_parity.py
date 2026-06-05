"""Questbook generated catalog and dispatch parity checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from validators.common import ValidationIssue
from validators.questbook_io import (
    load_json_payload,
    relative_location,
    validate_against_schema,
)
from validators.questbook_source_constants import (
    QUEST_CATALOG_EXAMPLE_NAME,
    QUEST_CATALOG_NAME,
    QUEST_DISPATCH_EXAMPLE_NAME,
    QUEST_DISPATCH_NAME,
    QUEST_DISPATCH_SCHEMA_NAME,
)


def validate_generated_quest_projection_surfaces(
    repo_root: Path,
    *,
    valid_quest_ids: list[str],
    expected_catalog_entries: list[dict[str, Any]],
    expected_dispatch_entries: list[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    quest_catalog_path = repo_root / QUEST_CATALOG_NAME
    quest_dispatch_path = repo_root / QUEST_DISPATCH_NAME
    quest_catalog_example_path = repo_root / QUEST_CATALOG_EXAMPLE_NAME
    quest_dispatch_example_path = repo_root / QUEST_DISPATCH_EXAMPLE_NAME

    expected_catalog_by_id = {
        entry["id"]: entry for entry in expected_catalog_entries
    }
    actual_live_catalog = load_json_payload(quest_catalog_path, issues)
    actual_live_catalog_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(actual_live_catalog, list):
        unexpected_ids: list[str] = []
        for item in actual_live_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_live_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    f"generated quest catalog has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_live_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    "generated quest catalog is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_path, repo_root),
                "generated quest catalog must be an array",
            )
        )
    actual_catalog = load_json_payload(quest_catalog_example_path, issues)
    if isinstance(actual_catalog, list):
        actual_catalog_by_id: dict[str, dict[str, Any]] = {}
        unexpected_ids: list[str] = []
        for item in actual_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    f"generated quest catalog example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example is out of date or mismatched",
                )
            )
        elif any(
            actual_catalog_by_id.get(quest_id) != actual_live_catalog_by_id.get(quest_id)
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example must match generated quest catalog",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_example_path, repo_root),
                "generated quest catalog example must be an array",
            )
        )
    expected_dispatch_by_id = {
        entry["id"]: entry for entry in expected_dispatch_entries
    }
    actual_live_dispatch = load_json_payload(quest_dispatch_path, issues)
    actual_live_dispatch_by_id: dict[str, dict[str, Any]] = {}
    invalid_live_dispatch_ids: set[str] = set()
    if isinstance(actual_live_dispatch, list):
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_live_dispatch):
            location = f"{relative_location(quest_dispatch_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_live_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_live_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    f"generated quest dispatch has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_live_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_live_dispatch_ids
        ]
        if any(
            actual_live_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_live_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    "generated quest dispatch is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_path, repo_root),
                "generated quest dispatch must be an array",
            )
        )
    actual_dispatch = load_json_payload(quest_dispatch_example_path, issues)
    if isinstance(actual_dispatch, list):
        actual_dispatch_by_id: dict[str, dict[str, Any]] = {}
        invalid_example_dispatch_ids: set[str] = set()
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_dispatch):
            location = f"{relative_location(quest_dispatch_example_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_example_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    f"generated quest dispatch example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_example_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_example_dispatch_ids
        ]
        if any(
            actual_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example is out of date or mismatched",
                )
            )
        elif any(
            actual_dispatch_by_id.get(quest_id) != actual_live_dispatch_by_id.get(quest_id)
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example must match generated quest dispatch",
                )
            )
        else:
            for quest_id in comparable_example_dispatch_ids:
                item = actual_dispatch_by_id.get(quest_id)
                if item is None:
                    continue
                requires_artifacts = item.get("requires_artifacts")
                if not isinstance(requires_artifacts, list) or not requires_artifacts:
                    issues.append(
                        ValidationIssue(
                            relative_location(quest_dispatch_example_path, repo_root),
                            "dispatch example must keep requires_artifacts as a non-empty example-only list",
                        )
                    )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_example_path, repo_root),
                "generated quest dispatch example must be an array",
            )
        )


__all__ = ("validate_generated_quest_projection_surfaces",)
