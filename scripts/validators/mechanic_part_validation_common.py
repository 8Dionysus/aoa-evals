"""Shared mechanic part validation route parsing helpers."""

from __future__ import annotations

import re
from pathlib import Path


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


PART_README_PATH_RE = re.compile(
    r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$"
)
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")


def part_readme_path_name(path_name: str) -> bool:
    return PART_README_PATH_RE.match(path_name) is not None


def mechanic_parent_readme_path_name(path_name: str) -> bool:
    return MECHANIC_PARENT_README_PATH_RE.match(path_name) is not None


def mechanic_part_validation_block(readme_text: str) -> str:
    return markdown_heading_section(readme_text, "Validation")


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


__all__ = (
    "MECHANIC_PARENT_README_PATH_RE",
    "PART_README_PATH_RE",
    "markdown_heading_section",
    "markdown_python_commands",
    "mechanic_parent_readme_path_name",
    "mechanic_parent_validation_route_text",
    "mechanic_part_validation_block",
    "part_readme_path_name",
    "part_validation_route_text",
)
