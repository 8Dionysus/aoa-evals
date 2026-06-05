"""Mechanic part payload inventory contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import (
    DECISION_RECORDS_README_NAME,
    MECHANIC_PART_ALLOWED_PAYLOAD_DIRS,
    MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
    MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
    MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS,
    MECHANIC_THIN_PART_REQUIRED_TOKENS,
    MECHANICS_AGENTS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
    markdown_heading_section,
    markdown_python_commands,
)


def validate_part_payload_inventory(
    *,
    repo_root: Path,
    part_root: Path,
    readme_name: str,
    readme_text: str,
    part_route_text: str,
    issues: list[ValidationIssue],
) -> None:
    payload_dir_count = 0
    for child in sorted(part_root.iterdir(), key=lambda item: item.name):
        child_relative = child.relative_to(repo_root).as_posix()
        if child.is_file():
            if child.name not in {"AGENTS.md", "README.md", "VALIDATION.md"}:
                issues.append(
                    ValidationIssue(
                        child_relative,
                        "unexpected part-root file must move under a payload subdirectory or be routed by the part contract",
                    )
                )
            continue
        if not child.is_dir():
            issues.append(
                ValidationIssue(
                    child_relative,
                    "unexpected part-root entry must be a payload subdirectory",
                )
            )
            continue
        if child.name not in MECHANIC_PART_ALLOWED_PAYLOAD_DIRS:
            issues.append(
                ValidationIssue(
                    child_relative,
                    "unexpected payload class directory under mechanic part",
                )
            )
            continue
        payload_dir_count += 1
        if not any(child.iterdir()):
            issues.append(
                ValidationIssue(
                    child_relative,
                    "empty payload subdirectory under mechanic part",
                )
            )
            continue
        if part_route_text:
            payload_tokens = (
                f"{child.name}/",
                f"`{child.name}`",
                child_relative,
            )
            if not any(token in part_route_text for token in payload_tokens):
                issues.append(
                    ValidationIssue(
                        readme_name,
                        f"part README must route payload subdirectory `{child.name}/`",
                    )
                )
    if payload_dir_count == 0 and readme_text:
        missing_thin_tokens = [
            token
            for token in MECHANIC_THIN_PART_REQUIRED_TOKENS
            if token not in readme_text
        ]
        if missing_thin_tokens:
            issues.append(
                ValidationIssue(
                    readme_name,
                    "mechanic part with no payload subdirectories must "
                    "declare an eval-backed thin support route; missing "
                    + ", ".join(repr(token) for token in missing_thin_tokens),
                )
            )


def validate_mechanic_part_payload_inventory_decision_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        tokens=MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    payload_decision_text = read_text_or_issue(
        repo_root / MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if payload_decision_text and markdown_python_commands(
        markdown_heading_section(payload_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PART_PAYLOAD_INVENTORY_DECISION_NAME,
            "Mechanic Part Payload Inventory",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload subdirectory", "mechanic part"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("payload subdirectory", "unexpected payload class"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    return issues


__all__ = (
    "validate_part_payload_inventory",
    "validate_mechanic_part_payload_inventory_decision_surfaces",
)
