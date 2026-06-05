"""Shared runtime-candidate reader validation helpers."""

from __future__ import annotations

import importlib.util
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, SchemaError


GENERATED_DIR_NAME = "generated"
MIN_CATALOG_NAME = "eval_catalog.min.json"
RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR = "mechanics/audit/parts/selected-evidence-packets/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR = "mechanics/audit/parts/artifact-verdict-hooks/examples"
ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS = (
    ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR,
    "mechanics/checkpoint/parts/a2a-summon-return/examples",
    "mechanics/checkpoint/parts/restartable-inquiry/examples",
    "mechanics/checkpoint/parts/self-agent-posture/examples",
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_NAME = "runtime-candidate-template-index.schema.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH = (
    "mechanics/audit/parts/candidate-readers/schemas/runtime-candidate-template-index.schema.json"
)
RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_template_index.min.json"
RUNTIME_CANDIDATE_INTAKE_NAME = "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py"
)
RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME = (
    "mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py"
)
NORMALIZED_RUNTIME_ARTIFACT_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        elif parts:
            parts.append(f".{part}")
        else:
            parts.append(str(part))
    return "".join(parts)


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def validate_inline_schema(
    schema: object,
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
    data: object,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator,
) -> bool:
    schema_errors = sorted(
        validator.iter_errors(data),
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


def load_mapping_entries(
    payload: object,
    *,
    array_key: str,
    key_name: str,
    location: str,
    issues: list[ValidationIssue],
) -> dict[str, dict[str, Any]]:
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(location, "payload must be an object"))
        return {}
    items = payload.get(array_key)
    if not isinstance(items, list):
        issues.append(ValidationIssue(location, f"missing array '{array_key}'"))
        return {}

    entries: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_location = f"{location}.{array_key}[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(item_location, "entry must be an object"))
            continue
        key = item.get(key_name)
        if not isinstance(key, str) or not key:
            issues.append(
                ValidationIssue(item_location, f"entry must expose string key '{key_name}'")
            )
            continue
        if key in entries:
            issues.append(
                ValidationIssue(item_location, f"duplicate entry for '{key_name}' value '{key}'")
            )
            continue
        entries[key] = item
    return entries


def load_builder_module(repo_root: Path, script_name: str, module_name: str):
    module_path = repo_root / script_name
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {module_name} generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


__all__ = (
    "GENERATED_DIR_NAME",
    "MIN_CATALOG_NAME",
    "RUNTIME_EVIDENCE_SELECTION_EXAMPLES_DIR",
    "ARTIFACT_VERDICT_HOOK_EXAMPLES_DIR",
    "ARTIFACT_VERDICT_HOOK_EXAMPLE_DIRS",
    "RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_NAME",
    "RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCHEMA_PATH",
    "RUNTIME_CANDIDATE_TEMPLATE_INDEX_NAME",
    "RUNTIME_CANDIDATE_INTAKE_NAME",
    "RUNTIME_CANDIDATE_TEMPLATE_INDEX_SCRIPT_NAME",
    "RUNTIME_CANDIDATE_INTAKE_SCRIPT_NAME",
    "NORMALIZED_RUNTIME_ARTIFACT_RE",
    "ValidationIssue",
    "relative_location",
    "format_schema_path",
    "load_json_payload",
    "validate_inline_schema",
    "validate_against_schema",
    "load_mapping_entries",
    "load_builder_module",
)
