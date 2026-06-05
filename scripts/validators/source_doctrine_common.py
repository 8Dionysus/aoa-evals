"""Shared helpers for source doctrine validators."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from validators.common import ValidationIssue


SOURCE_EVALS_DIR_NAME = "evals"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
EVAL_INDEX_NAME = "EVAL_INDEX.md"
ARTIFACT_PROCESS_GUIDE_NAME = "docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md"
REPEATED_WINDOW_GUIDE_NAME = "docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md"
COMPARISON_SPINE_GUIDE_NAME = "docs/guides/COMPARISON_SPINE_GUIDE.md"
INTEGRITY_RISK_CLASSES = (
    "style-over-substance",
    "artifact/process collapse",
    "baseline by association",
    "growth by association",
    "peer-compare blur",
    "fixed-baseline drift",
    "longitudinal overclaim",
    "schema-clean but claim-overstated",
    "routing overreach",
)


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


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
        issues.append(
            ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}")
        )
        return None


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return {}

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_dirs.setdefault(eval_dir.name, eval_dir)
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    return discover_eval_dirs(repo_root).get(
        eval_name,
        repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
    )


__all__ = (
    "SOURCE_EVALS_DIR_NAME",
    "EVAL_SELECTION_NAME",
    "EVAL_INDEX_NAME",
    "ARTIFACT_PROCESS_GUIDE_NAME",
    "REPEATED_WINDOW_GUIDE_NAME",
    "COMPARISON_SPINE_GUIDE_NAME",
    "INTEGRITY_RISK_CLASSES",
    "ValidationIssue",
    "relative_location",
    "read_text_or_issue",
    "load_json_payload",
    "discover_eval_dirs",
    "source_eval_dir",
)
