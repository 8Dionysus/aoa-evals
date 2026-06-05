"""Shared helpers for root guidance validators."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue


def require_tokens(
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


def reject_tokens(
    *,
    text: str,
    path_name: str,
    tokens: Sequence[str],
    message_template: str,
    issues: list[ValidationIssue],
) -> None:
    for token in tokens:
        if token in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    message_template.format(token=token),
                )
            )
