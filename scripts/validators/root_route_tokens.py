"""Root route-token companion lookup helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Sequence

from validators import decision_index_paths
from validators.common import ValidationIssue, read_text_or_issue

PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROUTE_RESIDUE_GUARDS_NAME = "docs/architecture/ROUTE_RESIDUE_GUARDS.md"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
ROADMAP_NAME = "ROADMAP.md"

PART_README_PATH_RE = re.compile(
    r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$"
)
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


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


def part_readme_path_name(path_name: str) -> bool:
    return PART_README_PATH_RE.match(path_name) is not None


def mechanic_parent_readme_path_name(path_name: str) -> bool:
    return MECHANIC_PARENT_README_PATH_RE.match(path_name) is not None


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""

    parent_name = match.group(1)
    agents_path = repo_root / "mechanics" / parent_name / "AGENTS.md"
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
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    decision_index_text = ""
    companion_texts: list[str] = []
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in decision_index_paths.GENERATED_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        decision_index_text = "\n\n".join(index_texts)
    if path_name == PROOF_TOPOLOGY_NAME:
        route_guard_path = repo_root / ROUTE_RESIDUE_GUARDS_NAME
        if route_guard_path.is_file():
            companion_texts.append(route_guard_path.read_text(encoding="utf-8"))
    for token in tokens:
        search_text = text
        if decision_index_text:
            search_text = "\n\n".join((text, decision_index_text))
        if companion_texts:
            search_text = "\n\n".join((search_text, *companion_texts))
        if part_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join(
                (
                    text,
                    part_validation_route_text(repo_root, path_name),
                )
            )
        elif mechanic_parent_readme_path_name(path_name) and token.lstrip("`").startswith("python "):
            search_text = "\n\n".join(
                (
                    text,
                    mechanic_parent_validation_route_text(repo_root, path_name),
                )
            )
        if token not in search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def context_require_tokens(
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    return require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=list(tokens),
        issues=issues,
    )


__all__ = (
    "DECISION_RECORDS_README_NAME",
    "MECHANIC_PARENT_README_PATH_RE",
    "PART_README_PATH_RE",
    "PROOF_TOPOLOGY_NAME",
    "ROADMAP_NAME",
    "ROUTE_RESIDUE_GUARDS_NAME",
    "context_require_tokens",
    "markdown_heading_section",
    "mechanic_parent_readme_path_name",
    "mechanic_parent_validation_route_text",
    "part_readme_path_name",
    "part_validation_route_text",
    "require_tokens",
)
