"""Release-support route-token loading helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from validators.common import ValidationIssue, read_text_or_issue

DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return ""
    search_text = text
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def require_route_tokens(
    repo_root: Path,
    issues: list[ValidationIssue],
    checks: Iterable[tuple[str, Iterable[str]]],
) -> None:
    for path_name, tokens in checks:
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)


__all__ = (
    "DECISION_INDEX_PATHS",
    "DECISION_RECORDS_README_NAME",
    "require_route_tokens",
    "require_tokens",
)
