"""Shared Phase Alpha matrix validation helpers."""

from __future__ import annotations

import importlib.util
import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Mapping

from jsonschema import Draft202012Validator, SchemaError


PHASE_ALPHA_EVAL_MATRIX_PART_NAME = "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix"
PHASE_ALPHA_EVAL_MATRIX_SCHEMA_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/schemas/phase-alpha-eval-matrix.schema.json"
)
PHASE_ALPHA_EVAL_MATRIX_EXAMPLE_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/examples/phase_alpha_eval_matrix.example.json"
)
PHASE_ALPHA_EVAL_MATRIX_SCRIPT_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/scripts/generate_phase_alpha_eval_matrix.py"
)
PHASE_ALPHA_EVAL_MATRIX_NAME = (
    f"{PHASE_ALPHA_EVAL_MATRIX_PART_NAME}/generated/phase_alpha_eval_matrix.min.json"
)
PHASE_ALPHA_PLAYBOOK_MATRIX_NAME = "generated/phase_alpha_run_matrix.min.json"
REPO_REF_PREFIX = "repo:"
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
EXPECTED_RUNTIME_LANES = {"primary": "llama.cpp", "control": "llama.cpp-second-pass"}


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def display_location(path: Path, visible_roots: Iterable[Path]) -> str:
    for root in visible_roots:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            continue
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


def load_json_payload(
    path: Path,
    issues: list[ValidationIssue],
    *,
    root: Path | None = None,
    visible_roots: Iterable[Path] = (),
) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        location = relative_location(path, root) if root is not None else display_location(path, visible_roots)
        issues.append(ValidationIssue(location, "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        location = relative_location(path, root) if root is not None else display_location(path, visible_roots)
        issues.append(ValidationIssue(location, f"invalid JSON: {exc}"))
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


def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def parse_repo_ref(
    raw_ref: object,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(
            ValidationIssue(location, "reference must include a repo name and repo-relative path")
        )
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = repo_ref_roots.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if repo_name != "aoa-evals" and not strict_sibling_compat:
        return repo_name, target, anchor or None
    if not repo_root.exists():
        issues.append(
            ValidationIssue(
                location,
                f"strict sibling compatibility requires available repo root for {repo_name}: {repo_root}",
            )
        )
        return None
    if not target.exists():
        issues.append(
            ValidationIssue(
                location,
                f"reference target does not exist: {repo_name}/{path_text}",
            )
        )
        return None

    if anchor:
        if target.suffix.lower() != ".md":
            issues.append(
                ValidationIssue(location, f"markdown anchor refs must target a .md file: '{raw_ref}'")
            )
            return None
        if anchor not in markdown_anchors(target):
            issues.append(
                ValidationIssue(location, f"markdown anchor does not exist for ref '{raw_ref}'")
            )
            return None

    return repo_name, target, anchor or None


def ensure_repo_relative_path(
    raw_path: str,
    location: str,
    issues: list[ValidationIssue],
) -> str:
    if not isinstance(raw_path, str) or not raw_path:
        issues.append(ValidationIssue(location, "path must be a non-empty string"))
        return ""
    if raw_path.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "path must be repo-relative, not repo-qualified"))
        return ""
    if "\\" in raw_path:
        issues.append(ValidationIssue(location, "path must use forward slashes"))
        return ""
    path = PurePosixPath(raw_path)
    if path.is_absolute():
        issues.append(ValidationIssue(location, "path must be repo-relative"))
        return ""
    if any(part in {"", ".", ".."} for part in path.parts):
        issues.append(ValidationIssue(location, "path must not contain empty, '.' or '..' segments"))
        return ""
    return path.as_posix()


def validate_repo_relative_contract_path(
    repo_root: Path,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    normalized_path = ensure_repo_relative_path(raw_path, location, issues)
    if not normalized_path:
        return None
    resolved_path = repo_root / normalized_path
    if not resolved_path.exists():
        issues.append(ValidationIssue(location, f"path '{normalized_path}' does not exist"))
        return None
    return normalized_path


def load_builder_module(repo_root: Path):
    module_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_SCRIPT_NAME
    spec = importlib.util.spec_from_file_location(
        "generate_phase_alpha_eval_matrix",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load phase alpha eval matrix generator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
