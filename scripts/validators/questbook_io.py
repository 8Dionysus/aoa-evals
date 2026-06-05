"""Questbook JSON, YAML, schema, and text loading helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator, SchemaError

from validators.common import ValidationIssue
from validators.questbook_context import REPO_ROOT


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def format_schema_path(path_parts: Iterable[Any]) -> str:
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


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or REPO_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


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


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    for token in tokens:
        if token not in text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


__all__ = (
    "format_schema_path",
    "get_schema_validator",
    "load_json_payload",
    "load_schema",
    "load_yaml_file",
    "read_text_or_issue",
    "relative_location",
    "require_tokens",
    "validate_against_schema",
    "validate_inline_schema",
)
