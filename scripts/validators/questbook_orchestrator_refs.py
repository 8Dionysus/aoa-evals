"""Questbook strict sibling orchestrator reference checks."""

from __future__ import annotations

import os

from validators import questbook_context as questbook_context_validator
from validators.common import ValidationIssue
from validators.questbook_context import STRICT_SIBLING_COMPAT_ENV
from validators.questbook_io import load_json_payload, relative_location
from validators.questbook_orchestrator_constants import (
    ORCHESTRATOR_CLASS_CATALOG_NAME,
)


def strict_sibling_compat_checks_enabled() -> bool:
    return os.environ.get(STRICT_SIBLING_COMPAT_ENV, "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def load_live_orchestrator_class_ids(issues: list[ValidationIssue]) -> set[str] | None:
    aoa_agents_root = questbook_context_validator.AOA_AGENTS_ROOT
    catalog_path = aoa_agents_root / ORCHESTRATOR_CLASS_CATALOG_NAME
    if not strict_sibling_compat_checks_enabled() or not aoa_agents_root.exists():
        return None
    payload = load_json_payload(catalog_path, issues)
    if not isinstance(payload, dict):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, aoa_agents_root),
                "orchestrator class catalog must be an object",
            )
        )
        return set()
    entries = payload.get("orchestrator_classes")
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, aoa_agents_root),
                "orchestrator class catalog must expose an orchestrator_classes list",
            )
        )
        return set()
    class_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, aoa_agents_root)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must be an object",
                )
            )
            continue
        class_id = entry.get("id")
        if not isinstance(class_id, str) or not class_id:
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, aoa_agents_root)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must expose a string id",
                )
            )
            continue
        class_ids.add(class_id)
    return class_ids


def validate_orchestrator_class_ref(
    orchestrator_class_ref: object,
    *,
    location: str,
    issues: list[ValidationIssue],
    live_class_ids: set[str] | None,
) -> str | None:
    if not isinstance(orchestrator_class_ref, str):
        issues.append(ValidationIssue(location, "quest orchestrator_class_ref must be a string"))
        return None
    repo_name, separator, class_id = orchestrator_class_ref.partition(":")
    if separator != ":" or repo_name != "aoa-agents" or not class_id:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must use the form 'aoa-agents:<class_id>'",
            )
        )
        return None
    if live_class_ids is not None and class_id not in live_class_ids:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must resolve in aoa-agents/generated/orchestrator_class_catalog.min.json",
            )
        )
        return None
    return class_id


__all__ = (
    "strict_sibling_compat_checks_enabled",
    "load_live_orchestrator_class_ids",
    "validate_orchestrator_class_ref",
)
