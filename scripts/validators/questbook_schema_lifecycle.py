"""Questbook schema envelope and lifecycle matrix checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from validators import questbook_io as questbook_io_validator
from validators import questbook_route_paths as questbook_route_paths_validator
from validators import questbook_route_tokens as questbook_route_tokens_validator
from validators import questbook_source_constants as questbook_source_constants_validator
from validators.common import ValidationIssue


@dataclass
class QuestSchemaLifecycleValidation:
    issues: list[ValidationIssue]
    quest_schema: dict[str, Any] | None


def validate_quest_schema_envelope(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    expected_title: str,
    expected_schema_version: str,
) -> bool:
    if not questbook_io_validator.validate_inline_schema(
        schema,
        location=location,
        issues=issues,
    ):
        return False
    if not isinstance(schema, dict):
        return False

    ok = True
    if schema.get("title") != expected_title:
        issues.append(
            ValidationIssue(location, f"schema title must be '{expected_title}'")
        )
        ok = False
    if schema.get("type") != "object":
        issues.append(ValidationIssue(location, "schema must describe an object"))
        ok = False
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(location, "schema must forbid additional properties")
        )
        ok = False
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(ValidationIssue(location, "schema properties must be an object"))
        return False
    schema_version = properties.get("schema_version")
    if (
        not isinstance(schema_version, dict)
        or schema_version.get("const") != expected_schema_version
    ):
        issues.append(
            ValidationIssue(
                location,
                f"schema_version must be a const of '{expected_schema_version}'",
            )
        )
        ok = False
    required = schema.get("required")
    if not isinstance(required, list):
        issues.append(ValidationIssue(location, "schema required list is missing"))
        ok = False
    else:
        for field in ("schema_version", "id", "public_safe"):
            if field not in required:
                issues.append(
                    ValidationIssue(location, f"schema must require '{field}'")
                )
                ok = False
    return ok


def validate_quest_lifecycle_surface(
    repo_root: Path,
    quest_schema: dict[str, Any] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    lifecycle_text = questbook_io_validator.require_tokens(
        repo_root=repo_root,
        path_name=questbook_route_paths_validator.QUEST_LIFECYCLE_NAME,
        tokens=questbook_route_tokens_validator.QUEST_LIFECYCLE_REQUIRED_TOKENS,
        issues=issues,
    )
    if not lifecycle_text:
        return issues

    schema_states: list[str] = []
    if isinstance(quest_schema, dict):
        properties = quest_schema.get("properties")
        if isinstance(properties, dict):
            state_schema = properties.get("state")
            if isinstance(state_schema, dict):
                raw_enum = state_schema.get("enum")
                if isinstance(raw_enum, list):
                    schema_states = [item for item in raw_enum if isinstance(item, str)]
    if not schema_states:
        schema_states = list(questbook_source_constants_validator.QUEST_SOURCE_STATES)

    if tuple(schema_states) != questbook_source_constants_validator.QUEST_SOURCE_STATES:
        issues.append(
            ValidationIssue(
                questbook_source_constants_validator.QUEST_SCHEMA_NAME,
                "quest state enum must match the lifecycle state order",
            )
        )

    for state in schema_states:
        table_token = f"| `{state}` |"
        if table_token not in lifecycle_text:
            issues.append(
                    ValidationIssue(
                    questbook_route_paths_validator.QUEST_LIFECYCLE_NAME,
                    f"quest lifecycle matrix must include state '{state}'",
                )
            )

    for state in sorted(questbook_source_constants_validator.CLOSED_QUEST_STATES):
        if f"`{state}` | closed; not listed as open" not in lifecycle_text:
            issues.append(
                ValidationIssue(
                    questbook_route_paths_validator.QUEST_LIFECYCLE_NAME,
                    f"closed state '{state}' must be marked closed in the lifecycle matrix",
                )
            )
    for state in questbook_source_constants_validator.QUEST_SOURCE_STATES:
        if (
            state not in questbook_source_constants_validator.CLOSED_QUEST_STATES
            and f"| `{state}` | listed in `QUESTBOOK.md`" not in lifecycle_text
        ):
            issues.append(
                ValidationIssue(
                    questbook_route_paths_validator.QUEST_LIFECYCLE_NAME,
                    f"open state '{state}' must be marked listed in QUESTBOOK.md",
                )
            )
    return issues


def validate_quest_schema_lifecycle_surfaces(
    repo_root: Path,
) -> QuestSchemaLifecycleValidation:
    issues: list[ValidationIssue] = []
    quest_schema_path = repo_root / questbook_source_constants_validator.QUEST_SCHEMA_NAME
    quest_dispatch_schema_path = repo_root / questbook_source_constants_validator.QUEST_DISPATCH_SCHEMA_NAME

    quest_schema_payload = questbook_io_validator.load_json_payload(
        quest_schema_path,
        issues,
    )
    quest_schema = quest_schema_payload if isinstance(quest_schema_payload, dict) else None
    if quest_schema_payload is not None:
        validate_quest_schema_envelope(
            quest_schema_payload,
            location=questbook_io_validator.relative_location(
                quest_schema_path,
                repo_root,
            ),
            issues=issues,
            expected_title=questbook_source_constants_validator.QUEST_SCHEMA_TITLE,
            expected_schema_version=questbook_source_constants_validator.QUEST_SCHEMA_VERSION,
        )

    issues.extend(validate_quest_lifecycle_surface(repo_root, quest_schema))

    quest_dispatch_schema = questbook_io_validator.load_json_payload(
        quest_dispatch_schema_path,
        issues,
    )
    if quest_dispatch_schema is not None:
        validate_quest_schema_envelope(
            quest_dispatch_schema,
            location=questbook_io_validator.relative_location(
                quest_dispatch_schema_path,
                repo_root,
            ),
            issues=issues,
            expected_title=questbook_source_constants_validator.QUEST_DISPATCH_SCHEMA_TITLE,
            expected_schema_version=questbook_source_constants_validator.QUEST_DISPATCH_SCHEMA_VERSION,
        )

    return QuestSchemaLifecycleValidation(
        issues=issues,
        quest_schema=quest_schema,
    )


__all__ = (
    "QuestSchemaLifecycleValidation",
    "validate_quest_schema_envelope",
    "validate_quest_lifecycle_surface",
    "validate_quest_schema_lifecycle_surfaces",
)
