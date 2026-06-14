"""Mechanic part README contract surfaces."""

from __future__ import annotations

from pathlib import Path

from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import (
    MECHANIC_PART_README_REQUIRED_TOKENS,
    MECHANIC_PART_README_STOP_LINE_PRESSURE_HEADER,
    MECHANIC_PART_README_STOP_LINE_ROUTE_HEADERS,
    MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS,
    markdown_heading_section,
    markdown_table_rows,
    part_validation_route_text,
    require_tokens,
)
from validators.mechanic_part_role_headings import validate_mechanic_part_role_heading


def validate_stop_lines_route_table(
    *,
    readme_name: str,
    readme_text: str,
    issues: list[ValidationIssue],
) -> None:
    stop_lines_section = markdown_heading_section(readme_text, "Stop-Lines")
    if not stop_lines_section:
        return

    table_rows = markdown_table_rows(stop_lines_section)
    if not table_rows:
        issues.append(
            ValidationIssue(
                readme_name,
                "mechanic part README Stop-Lines must expose a pressure-to-owner route table",
            )
        )
        return

    header = [cell.strip().lower() for cell in table_rows[0]]
    has_pressure = (
        bool(header)
        and header[0] == MECHANIC_PART_README_STOP_LINE_PRESSURE_HEADER
    )
    has_route = any(cell in MECHANIC_PART_README_STOP_LINE_ROUTE_HEADERS for cell in header[1:])
    has_body_row = len(table_rows) > 1
    if not has_pressure or not has_route or not has_body_row:
        issues.append(
            ValidationIssue(
                readme_name,
                "mechanic part README Stop-Lines must expose a pressure-to-owner route table",
            )
        )


def validate_mechanic_part_readme_contract_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    from validators import mechanic_part_payload_inventory as payload_inventory_validator
    from validators import mechanic_part_source_surfaces as source_surfaces_validator

    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parent_root = repo_root / "mechanics" / parent_name
        parts_root = parent_root / "parts"
        parts_index_name = f"mechanics/{parent_name}/PARTS.md"
        if not parts_root.is_dir():
            issues.append(
                ValidationIssue(
                    f"mechanics/{parent_name}/parts",
                    "active mechanic parent must expose a parts/ directory",
                )
            )
            continue

        parts_index_text = read_text_or_issue(
            repo_root / parts_index_name,
            issues,
            root=repo_root,
        )

        for path in sorted(parts_root.iterdir(), key=lambda item: item.name):
            relative = path.relative_to(repo_root).as_posix()
            if path.is_file():
                if path.name not in {"AGENTS.md", "README.md"}:
                    issues.append(
                        ValidationIssue(
                            relative,
                            "unexpected mechanics parts root file must be a route README or a part directory",
                        )
                    )
                continue
            if not path.is_dir():
                issues.append(
                    ValidationIssue(
                        relative,
                        "unexpected mechanics parts root entry must be a part directory",
                    )
                )
                continue

            readme_name = f"{relative}/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            validate_mechanic_part_role_heading(
                path_name=readme_name,
                text=readme_text,
                parent_name=parent_name,
                part_name=path.name,
                role_name="Part",
                issues=issues,
            )
            validation_name = f"{relative}/VALIDATION.md"
            validation_path = repo_root / validation_name
            if validation_path.is_file():
                validation_text = read_text_or_issue(
                    validation_path,
                    issues,
                    root=repo_root,
                )
                validate_mechanic_part_role_heading(
                    path_name=validation_name,
                    text=validation_text,
                    parent_name=parent_name,
                    part_name=path.name,
                    role_name="Validation",
                    issues=issues,
                )
            part_route_text = "\n\n".join(
                (
                    readme_text,
                    part_validation_route_text(repo_root, readme_name),
                )
            )
            route_tokens = (
                readme_name,
                f"parts/{path.name}/README.md",
                f"`{path.name}`",
            )
            if parts_index_text and not any(token in parts_index_text for token in route_tokens):
                issues.append(
                    ValidationIssue(
                        parts_index_name,
                        f"parent PARTS.md must route concrete part `{readme_name}` by README path or exact part slug",
                    )
                )
            require_tokens(
                repo_root=repo_root,
                path_name=readme_name,
                tokens=MECHANIC_PART_README_REQUIRED_TOKENS,
                issues=issues,
            )
            for stale_lead_in in MECHANIC_PART_README_STALE_STOP_LINE_LEAD_INS:
                if readme_text and stale_lead_in in readme_text:
                    issues.append(
                        ValidationIssue(
                            readme_name,
                            "mechanic part README must introduce Stop-Lines as a local proof-operation boundary, not the old part-claim scaffold",
                        )
                    )
            validate_stop_lines_route_table(
                readme_name=readme_name,
                readme_text=readme_text,
                issues=issues,
            )
            source_surfaces_validator.validate_part_source_surface_refs(
                repo_root=repo_root,
                readme_name=readme_name,
                readme_text=readme_text,
                issues=issues,
            )
            payload_inventory_validator.validate_part_payload_inventory(
                repo_root=repo_root,
                part_root=path,
                readme_name=readme_name,
                readme_text=readme_text,
                part_route_text=part_route_text,
                issues=issues,
            )

    issues.extend(
        payload_inventory_validator.validate_mechanic_part_payload_inventory_decision_surfaces(
            repo_root
        )
    )
    issues.extend(
        source_surfaces_validator.validate_mechanic_part_source_surface_decision_surfaces(
            repo_root
        )
    )

    return issues


__all__ = ("validate_mechanic_part_readme_contract_surfaces",)
