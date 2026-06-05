"""Questbook source records and generated projection builders."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

from validators.questbook_io import format_schema_path
from validators.questbook_source_constants import (
    FOUNDATION_QUEST_NAMES,
    QUESTBOOK_INTEGRATION_NAME,
    QUESTBOOK_NAME,
    QUEST_CATALOG_EXAMPLE_NAME,
    QUEST_DISPATCH_ARTIFACT_OVERRIDES,
    QUEST_DISPATCH_EXAMPLE_NAME,
    QUEST_DISPATCH_SCHEMA_NAME,
    QUEST_DISPATCH_SCHEMA_VERSION,
    QUEST_SCHEMA_NAME,
    QUEST_SCHEMA_VERSION,
    QUEST_SOURCE_LANES,
    QUEST_SOURCE_STATES,
)


def validate_quest_projection_record(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> None:
    schema_path = repo_root / QUEST_SCHEMA_NAME
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"{schema_path.relative_to(repo_root).as_posix()} could not be loaded for quest projection: {exc}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(quest_data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        error_path = format_schema_path(error.absolute_path)
        detail = f" at '{error_path}'" if error_path else ""
        raise ValueError(
            f"{quest_path.relative_to(repo_root).as_posix()} violates {QUEST_SCHEMA_NAME}{detail}: {error.message}"
        )


def quest_sort_key(quest_name: str) -> tuple[int, str]:
    suffix = quest_name.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_name)
    except ValueError:
        return (sys.maxsize, quest_name)


def discover_quest_paths(repo_root: Path) -> list[Path]:
    quests_dir = repo_root / "quests"
    if not quests_dir.is_dir():
        return []
    return sorted(
        {
            path
            for path in quests_dir.rglob("AOA-EV-Q-*.yaml")
            if path.is_file()
        },
        key=lambda path: quest_sort_key(path.stem),
    )


def discover_quest_names(repo_root: Path) -> list[str]:
    quest_names = sorted(
        {path.stem for path in discover_quest_paths(repo_root)},
        key=quest_sort_key,
    )
    if not quest_names:
        return list(FOUNDATION_QUEST_NAMES)
    return quest_names


def missing_foundation_quest_names(quest_names: Iterable[str]) -> list[str]:
    quest_name_set = set(quest_names)
    return [quest_name for quest_name in FOUNDATION_QUEST_NAMES if quest_name not in quest_name_set]


def should_validate_questbook_surface(repo_root: Path) -> bool:
    questbook_paths = (
        repo_root / QUESTBOOK_NAME,
        repo_root / QUESTBOOK_INTEGRATION_NAME,
        repo_root / QUEST_SCHEMA_NAME,
        repo_root / QUEST_DISPATCH_SCHEMA_NAME,
        repo_root / QUEST_CATALOG_EXAMPLE_NAME,
        repo_root / QUEST_DISPATCH_EXAMPLE_NAME,
    )
    if any(path.exists() for path in questbook_paths):
        return True
    return bool(discover_quest_paths(repo_root))


def quest_source_path_shape_issue(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> str | None:
    relative_path = quest_path.relative_to(repo_root).as_posix()
    parts = quest_path.relative_to(repo_root).parts
    if len(parts) != 4 or parts[0] != "quests" or not parts[3].endswith(".yaml"):
        return "quest source path must use quests/<lane>/<state>/<quest-id>.yaml"
    lane = parts[1]
    state = parts[2]
    if lane not in QUEST_SOURCE_LANES:
        allowed = ", ".join(QUEST_SOURCE_LANES)
        return f"quest lane '{lane}' is not allowed; expected one of: {allowed}"
    if state not in QUEST_SOURCE_STATES:
        allowed = ", ".join(QUEST_SOURCE_STATES)
        return f"quest state directory '{state}' is not allowed; expected one of: {allowed}"
    quest_state = quest_data.get("state")
    if isinstance(quest_state, str) and state != quest_state:
        return f"quest state directory '{state}' must match state '{quest_state}'"
    if quest_path.stem != quest_data.get("id"):
        return f"quest source filename in {relative_path} must match quest id"
    return None


def build_expected_quest_catalog_entry(
    quest: dict[str, Any],
    *,
    source_path: str,
) -> dict[str, Any]:
    entry = {
        "id": quest["id"],
        "title": quest["title"],
        "repo": quest["repo"],
        "theme_ref": quest.get("theme_ref", ""),
        "milestone_ref": quest.get("milestone_ref", ""),
        "state": quest["state"],
        "band": quest["band"],
        "kind": quest["kind"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "owner_surface": quest["owner_surface"],
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    for optional_key in (
        "orchestrator_class_ref",
        "capability_target",
        "playbook_family_refs",
        "proof_surface_refs",
        "memory_surface_refs",
    ):
        if optional_key in quest:
            entry[optional_key] = quest[optional_key]
    return entry


def build_expected_quest_dispatch_entry(
    quest: dict[str, Any],
    *,
    quest_name: str,
    source_path: str,
) -> dict[str, Any]:
    activation = quest.get("activation")
    if not isinstance(activation, dict):
        activation = {}
    requires_artifacts = QUEST_DISPATCH_ARTIFACT_OVERRIDES.get(quest_name)
    if requires_artifacts is None:
        kind = quest.get("kind")
        if kind == "harvest":
            requires_artifacts = ["recurrence_evidence", "promotion_decision"]
        else:
            requires_artifacts = ["bounded_plan", "work_result", "verification_result"]
    entry = {
        "schema_version": QUEST_DISPATCH_SCHEMA_VERSION,
        "id": quest["id"],
        "repo": quest["repo"],
        "state": quest["state"],
        "band": quest["band"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "control_mode": quest["control_mode"],
        "delegate_tier": quest["delegate_tier"],
        "split_required": quest["split_required"],
        "write_scope": quest["write_scope"],
        "requires_artifacts": requires_artifacts,
        "activation_mode": activation.get("mode"),
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    if "fallback_tier" in quest:
        entry["fallback_tier"] = quest.get("fallback_tier")
    if "wrapper_class" in quest:
        entry["wrapper_class"] = quest.get("wrapper_class")
    for optional_key in ("orchestrator_class_ref", "capability_target"):
        if optional_key in quest:
            entry[optional_key] = quest.get(optional_key)
    return entry


def load_quest_projection_records(repo_root: Path) -> list[tuple[str, dict[str, Any], str]]:
    records: list[tuple[str, dict[str, Any], str]] = []
    quest_paths = discover_quest_paths(repo_root)
    if not quest_paths:
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in FOUNDATION_QUEST_NAMES
        ]
    quest_names = [path.stem for path in quest_paths]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    if duplicate_names:
        raise ValueError(f"duplicate quest source id(s): {', '.join(duplicate_names)}")
    missing_foundation = missing_foundation_quest_names(quest_names)
    if missing_foundation:
        missing_display = ", ".join(missing_foundation)
        raise ValueError(f"missing required foundation quest files: {missing_display}")
    for quest_path in quest_paths:
        quest_name = quest_path.stem
        try:
            quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is missing") from exc
        except yaml.YAMLError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is invalid YAML: {exc}") from exc
        if not isinstance(quest_data, dict):
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must be a YAML mapping")
        validate_quest_projection_record(repo_root, quest_path, quest_data)
        shape_issue = quest_source_path_shape_issue(repo_root, quest_path, quest_data)
        if shape_issue is not None:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()}: {shape_issue}")
        if quest_data.get("schema_version") != QUEST_SCHEMA_VERSION:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep schema_version '{QUEST_SCHEMA_VERSION}'")
        if quest_data.get("repo") != "aoa-evals":
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep repo 'aoa-evals'")
        if quest_data.get("id") != quest_name:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep id '{quest_name}'")
        if quest_data.get("public_safe") is not True:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep public_safe true")
        records.append((quest_name, quest_data, quest_path.relative_to(repo_root).as_posix()))
    return records


def build_quest_catalog_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_catalog_entry(quest_data, source_path=source_path)
        for _, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


def build_quest_dispatch_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_dispatch_entry(
            quest_data,
            quest_name=quest_name,
            source_path=source_path,
        )
        for quest_name, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


__all__ = (
    "validate_quest_projection_record",
    "quest_sort_key",
    "discover_quest_paths",
    "discover_quest_names",
    "missing_foundation_quest_names",
    "should_validate_questbook_surface",
    "quest_source_path_shape_issue",
    "build_expected_quest_catalog_entry",
    "build_expected_quest_dispatch_entry",
    "load_quest_projection_records",
    "build_quest_catalog_projection",
    "build_quest_dispatch_projection",
)
