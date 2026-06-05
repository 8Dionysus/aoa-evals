"""Shared source eval bundle topology helpers."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Sequence

import yaml

from validators.common import ValidationIssue, read_text_or_issue, relative_location

SOURCE_EVALS_DIR_NAME = "evals"
EVALS_DIR = Path(SOURCE_EVALS_DIR_NAME)
EVALS_README = EVALS_DIR / "README.md"
EVALS_AGENTS = EVALS_DIR / "AGENTS.md"
EVALS_AGENTS_NAME = EVALS_AGENTS.as_posix()
EVAL_INDEX_NAME = "EVAL_INDEX.md"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
ROADMAP_NAME = "ROADMAP.md"
NO_ADDITIONAL_STARTER_BUNDLES_TEXT = (
    "No additional planned starter bundles are currently named publicly."
)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    for token in tokens:
        if token not in text:
            issues.append(
                ValidationIssue(path_name, f"missing required text token: {token}")
            )
    return text


def markdown_heading_section(text: str, heading: str) -> str:
    marker = ""
    heading_level = 0
    start = -1
    for level in (3, 2):
        pattern = re.compile(rf"(?m)^{'#' * level} {re.escape(heading)}\s*$")
        match = pattern.search(text)
        if match:
            marker = match.group(0)
            heading_level = level
            start = match.start()
            break
    if start == -1:
        return ""
    next_h2 = text.find("\n## ", start + len(marker))
    next_h3 = text.find("\n### ", start + len(marker)) if heading_level > 2 else -1
    candidates = [index for index in (next_h2, next_h3) if index != -1]
    end = min(candidates) if candidates else len(text)
    return text[start:end]


def markdown_python_commands(section: str) -> list[str]:
    commands: list[str] = []
    commands.extend(re.findall(r"`(python3? [^`]+)`", section))
    in_fence = False
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("$ "):
            stripped = stripped[2:].strip()
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        if stripped.startswith("python ") or stripped.startswith("python3 "):
            commands.append(stripped)
    return list(dict.fromkeys(commands))


def read_mapping(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return None, f"eval manifest must be valid yaml: {exc}"
    if not isinstance(payload, dict):
        return None, "eval manifest must be a mapping"
    return payload, None


def load_yaml_file(
    path: Path,
    issues: list[ValidationIssue],
    *,
    repo_root: Path,
) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, repo_root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(relative_location(path, repo_root), f"invalid YAML: {exc}")
        )
        return None
    return data


def expected_manifest_parent(payload: dict[str, Any]) -> Path | None:
    name = payload.get("name")
    category = payload.get("category")
    baseline_mode = payload.get("baseline_mode", "none")
    if not isinstance(name, str) or not name:
        return None
    if baseline_mode and baseline_mode != "none":
        if not isinstance(baseline_mode, str):
            return None
        return EVALS_DIR / "comparison" / baseline_mode / name
    if not isinstance(category, str) or not category:
        return None
    return EVALS_DIR / category / name


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / EVALS_DIR
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


def extract_table_eval_names(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start_index = next(
            index for index, line in enumerate(lines) if line.strip() == heading
        )
    except StopIteration:
        return []

    table_lines: list[str] = []
    for line in lines[start_index + 1 :]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines and not stripped:
            break
        if table_lines:
            break

    pattern = re.compile(r"^\|\s*(aoa-[a-z0-9-]+)\s*\|")
    return [
        pattern.match(line).group(1)
        for line in table_lines
        if pattern.match(line)
    ]


def extract_bulleted_eval_names(text: str, label: str) -> list[str]:
    lines = text.splitlines()
    names: list[str] = []
    for index, line in enumerate(lines):
        if line.strip() != label:
            continue
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                break
            if not stripped.startswith("- "):
                break
            names.extend(re.findall(r"aoa-[a-z0-9-]+", stripped))
    return names


__all__ = (
    "EVALS_AGENTS",
    "EVALS_AGENTS_NAME",
    "EVALS_DIR",
    "EVALS_README",
    "EVAL_INDEX_NAME",
    "EVAL_SELECTION_NAME",
    "NO_ADDITIONAL_STARTER_BUNDLES_TEXT",
    "ROADMAP_NAME",
    "SOURCE_EVALS_DIR_NAME",
    "discover_eval_dirs",
    "expected_manifest_parent",
    "extract_bulleted_eval_names",
    "extract_table_eval_names",
    "load_yaml_file",
    "markdown_heading_section",
    "markdown_python_commands",
    "read_mapping",
    "require_tokens",
)
