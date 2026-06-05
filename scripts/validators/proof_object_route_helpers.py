"""Proof-object route token lookup helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
PART_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$")
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


def markdown_heading_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^(##+)\s+{re.escape(heading)}\s*$", flags=re.MULTILINE)
    start = -1
    heading_level = 0
    marker = ""
    for match in pattern.finditer(text):
        marker = match.group(1)
        level = len(marker)
        if level >= 2:
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


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    agents_path = repo_root / "mechanics" / match.group(1) / "AGENTS.md"
    if not agents_path.is_file():
        return ""
    return agents_path.read_text(encoding="utf-8")


def part_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = PART_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    parent_name, part_name = match.groups()
    part_relative = f"mechanics/{parent_name}/parts/{part_name}"
    validation_name = f"{part_relative}/VALIDATION.md"
    chunks: list[str] = []
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        chunks.append(validation_path.read_text(encoding="utf-8"))
    agents_path = repo_root / "mechanics" / parent_name / "parts" / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
        if child_section:
            chunks.append(child_section)
    return "\n\n".join(chunks)


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
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        token_search_text = search_text
        if PART_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif MECHANIC_PARENT_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in token_search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


__all__ = (
    "DECISION_RECORDS_README_NAME",
    "MECHANIC_PARENT_README_PATH_RE",
    "PART_README_PATH_RE",
    "markdown_heading_section",
    "mechanic_parent_validation_route_text",
    "part_validation_route_text",
    "require_tokens",
)
