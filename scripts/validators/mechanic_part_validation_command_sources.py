"""Mechanic part validation-command source helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import MECHANIC_PART_ALLOWED_PAYLOAD_DIRS
from validators.mechanic_part_source_surfaces import SOURCE_SURFACE_CODE_REF_RE
from validators.mechanic_part_validation_common import (
    markdown_heading_section,
    markdown_python_commands,
    mechanic_part_validation_block,
)


def part_payload_directories(part_root: Path) -> list[Path]:
    return [
        child
        for child in sorted(part_root.iterdir(), key=lambda item: item.name)
        if child.is_dir() and child.name in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS
    ]


def validation_section_has_payload_coverage_anchor(
    part_relative: str,
    validation_section: str,
    commands: Sequence[str],
) -> bool:
    part_prefix = f"{part_relative.rstrip('/')}/"
    if any(part_prefix in command for command in commands):
        return True
    if any("scripts/validate_repo.py --eval " in command for command in commands):
        return True

    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(validation_section):
        ref = match.group(1).strip().rstrip("/")
        if ref == part_relative or ref.startswith(part_prefix):
            return True
    return False


def mechanic_part_validation_sources(
    repo_root: Path,
    parent_name: str,
    part_root: Path,
    readme_name: str,
    readme_text: str,
    issues: list[ValidationIssue],
) -> list[tuple[str, str]]:
    sources: list[tuple[str, str]] = []

    readme_section = mechanic_part_validation_block(readme_text)
    sources.append((readme_name, readme_section))

    part_relative = part_root.relative_to(repo_root).as_posix()
    validation_name = f"{part_relative}/VALIDATION.md"
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        validation_text = read_text_or_issue(validation_path, issues, root=repo_root)
        if validation_text:
            sources.append((validation_name, validation_text))
    else:
        issues.append(
            ValidationIssue(
                validation_name,
                "part validation route marker is missing",
            )
        )

    parts_agents_name = f"mechanics/{parent_name}/parts/AGENTS.md"
    parts_agents_path = repo_root / parts_agents_name
    if parts_agents_path.is_file():
        agents_text = read_text_or_issue(parts_agents_path, issues, root=repo_root)
        if agents_text:
            child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
            if child_section:
                sources.append((parts_agents_name, child_section))
            else:
                issues.append(
                    ValidationIssue(
                        parts_agents_name,
                        f"missing centralized child validation block for `{validation_name}`",
                    )
                )
    else:
        issues.append(
            ValidationIssue(
                parts_agents_name,
                "parent parts AGENTS validation lane is missing",
            )
        )

    return sources


__all__ = (
    "mechanic_part_validation_sources",
    "part_payload_directories",
    "validation_section_has_payload_coverage_anchor",
)
