"""Shared helpers for source eval validator modules."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Sequence

import yaml
from jsonschema import Draft202012Validator, SchemaError

from validators.common import ValidationIssue


CONTRACT_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR_NAME = "schemas"


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_candidate = Path(schema_name)
    schema_relative_path = (
        schema_candidate
        if schema_candidate.parent != Path(".")
        else Path(SCHEMAS_DIR_NAME) / schema_candidate
    )
    with (CONTRACT_ROOT / schema_relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or CONTRACT_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Sequence[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def format_issues(issues: Sequence[ValidationIssue]) -> str:
    return "\n".join(f"- {issue.location}: {issue.message}" for issue in issues)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
) -> bool:
    active_validator = validator or get_schema_validator(schema_name)
    schema_errors = sorted(
        active_validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid YAML: {exc}"))
        return None
    return data


def load_json_payload(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid JSON: {exc}"))
        return None


def validate_inline_schema(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    if not isinstance(schema, dict):
        issues.append(ValidationIssue(location, "schema must parse to an object"))
        return False
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        issues.append(ValidationIssue(location, f"invalid JSON schema: {exc.message}"))
        return False
    return True


def validate_json_against_inline_schema(
    data: Any,
    schema: dict[str, Any],
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    validator = Draft202012Validator(schema)
    schema_errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"report violation at '{error_path}': {error.message}"
        else:
            message = f"report violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors
