"""Mechanic part route heading role contracts."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import markdown_h1, slug_compact_token


def validate_mechanic_part_role_heading(
    *,
    path_name: str,
    text: str,
    parent_name: str,
    part_name: str,
    role_name: str,
    issues: list[ValidationIssue],
) -> None:
    heading = markdown_h1(text)
    heading_compact = slug_compact_token(heading)
    missing: list[str] = []
    if slug_compact_token(parent_name) not in heading_compact:
        missing.append("parent mechanic")
    if slug_compact_token(part_name) not in heading_compact:
        missing.append("local role token")
    if role_name.lower() not in heading.lower():
        missing.append(role_name)
    if " / " not in heading:
        missing.append("Parent / Part heading shape")
    if missing:
        issues.append(
            ValidationIssue(
                path_name,
                "mechanic route H1 must name parent mechanic, local role token, and role; missing "
                + ", ".join(missing),
            )
        )


def validate_mechanic_index_surface_roles(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )
        validate_mechanic_part_role_heading(
            path_name=parts_index_name,
            text=parts_index_text,
            parent_name=parent_name,
            part_name="part",
            role_name="Index",
            issues=issues,
        )

        parts_route_name = f"mechanics/{parent_name}/parts/README.md"
        parts_route_path = repo_root / parts_route_name
        if parts_route_path.is_file():
            parts_route_text = read_text_or_issue(
                parts_route_path,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=parts_route_name,
                text=parts_route_text,
                parent_name=parent_name,
                part_name="parts",
                role_name="Route",
                issues=issues,
            )

    return issues


__all__ = (
    "validate_mechanic_part_role_heading",
    "validate_mechanic_index_surface_roles",
)
