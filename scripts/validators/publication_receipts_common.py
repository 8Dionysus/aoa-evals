"""Shared schema and reference helpers for publication receipt validators."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml
from jsonschema import Draft202012Validator, SchemaError

from validators.common import ValidationIssue


STATS_EVENT_ENVELOPE_SCHEMA_NAME = "stats-event-envelope.schema.json"
EVAL_RESULT_RECEIPT_SCHEMA_NAME = "eval-result-receipt.schema.json"
PUBLICATION_RECEIPTS_PARTS_ROOT = "mechanics/publication-receipts/parts"
STATS_EVENT_ENVELOPE_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/stats-envelope-mirror/schemas/{STATS_EVENT_ENVELOPE_SCHEMA_NAME}"
)
EVAL_RESULT_RECEIPT_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/schemas/{EVAL_RESULT_RECEIPT_SCHEMA_NAME}"
)
LIVE_EVAL_RECEIPT_LOG_NAME = ".aoa/live_receipts/eval-result-receipts.jsonl"
SCHEMAS_DIR_NAME = "schemas"
REPO_REF_PREFIX = "repo:"
EVAL_REPORT_INDEX_NAME = "generated/eval_report_index.min.json"
SOURCE_EVALS_DIR_NAME = "evals"

RFC3339_DATE_TIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)
FORMAT_CHECKER = Draft202012Validator.FORMAT_CHECKER


@FORMAT_CHECKER.checks("date-time", raises=(ValueError,))
def _is_date_time(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if RFC3339_DATE_TIME_RE.fullmatch(value) is None:
        return False
    normalized = value[:-1] + "+00:00" if value[-1:].lower() == "z" else value
    normalized = normalized.replace("t", "T", 1)
    parsed = datetime.fromisoformat(normalized)
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        raise FileNotFoundError(f"missing source eval directory at {source_root}")

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_name = eval_dir.name
        if eval_name in eval_dirs:
            raise ValueError(
                "duplicate source eval directory name "
                f"'{eval_name}' at {relative_location(eval_dirs[eval_name], repo_root)} "
                f"and {relative_location(eval_dir, repo_root)}"
            )
        eval_dirs[eval_name] = eval_dir
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    try:
        return discover_eval_dirs(repo_root).get(
            eval_name,
            repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
        )
    except (FileNotFoundError, ValueError):
        return repo_root / SOURCE_EVALS_DIR_NAME / eval_name


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


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def load_yaml_file(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
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


def get_schema_validator_with_format(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
    fallback_repo_root: Path,
) -> bool:
    active_validator = validator
    if active_validator is None:
        schema_paths_by_name = {
            STATS_EVENT_ENVELOPE_SCHEMA_NAME: Path(STATS_EVENT_ENVELOPE_SCHEMA_PATH),
            EVAL_RESULT_RECEIPT_SCHEMA_NAME: Path(EVAL_RESULT_RECEIPT_SCHEMA_PATH),
        }
        schema_path = fallback_repo_root / schema_paths_by_name[schema_name]
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        active_validator = get_schema_validator_with_format(schema)

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


def parse_repo_ref(
    raw_ref: Any,
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
        issues.append(ValidationIssue(location, f"reference target does not exist: {repo_name}/{path_text}"))
        return None

    return repo_name, target, anchor or None
