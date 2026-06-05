"""Mechanic part validation-command reachability contracts."""

from __future__ import annotations

from pathlib import Path

from validators import mechanic_part_validation_command_sources as command_sources
from validators import mechanic_part_validation_command_tokens as command_tokens
from validators import mechanics as mechanics_validator
from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_part_contract_common import (
    MECHANICS_AGENTS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
)
from validators.mechanic_part_validation_command_parsing import (
    validation_command_referenced_paths,
)
from validators.mechanic_part_validation_common import (
    markdown_heading_section,
    markdown_python_commands,
    mechanic_part_validation_block,
)


def validate_mechanic_part_validation_command_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for parent_name in mechanics_validator.ACTIVE_MECHANIC_PARENT_NAMES:
        parts_root = repo_root / "mechanics" / parent_name / "parts"
        if not parts_root.is_dir():
            continue

        for part_root in sorted(parts_root.iterdir(), key=lambda item: item.name):
            if not part_root.is_dir():
                continue
            readme_name = part_root.relative_to(repo_root).as_posix() + "/README.md"
            readme_text = read_text_or_issue(
                repo_root / readme_name,
                issues,
                root=repo_root,
            )
            if not readme_text:
                continue

            sources = command_sources.mechanic_part_validation_sources(
                repo_root,
                parent_name,
                part_root,
                readme_name,
                readme_text,
                issues,
            )
            readme_validation_section = mechanic_part_validation_block(readme_text)
            readme_commands = markdown_python_commands(readme_validation_section)
            if readme_commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part README validation section must route executable commands to VALIDATION.md or parent parts/AGENTS.md instead of carrying python command blocks",
                    )
                )

            command_locations: dict[str, str] = {}
            commands: list[str] = []
            for location, source_text in sources:
                for command in markdown_python_commands(source_text):
                    if command in command_locations:
                        continue
                    command_locations[command] = location
                    commands.append(command)

            if not commands:
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must list at least one python command",
                    )
                )
                continue

            part_relative = part_root.relative_to(repo_root).as_posix()
            combined_validation_route = "\n\n".join(source_text for _, source_text in sources)
            if (
                command_sources.part_payload_directories(part_root)
                and not command_sources.validation_section_has_payload_coverage_anchor(
                    part_relative,
                    combined_validation_route,
                    commands,
                )
            ):
                issues.append(
                    ValidationIssue(
                        readme_name,
                        "part validation route must include a payload coverage anchor, such as a part-local path or specific `python scripts/validate_repo.py --eval ...`; route-wide commands need a part-local or bundle-specific anchor for parts with payload",
                    )
                )

            for command in commands:
                command_location = command_locations.get(command, readme_name)
                command_paths, parse_issue = validation_command_referenced_paths(command)
                if parse_issue:
                    issues.append(ValidationIssue(command_location, parse_issue))
                    continue
                for command_path in command_paths:
                    if any(token in command_path for token in ("*", "?", "[")):
                        continue
                    if command_path.startswith("/"):
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"validation command must use repo-relative path, not absolute path `{command_path}`",
                            )
                        )
                        continue
                    if not (repo_root / command_path).exists():
                        issues.append(
                            ValidationIssue(
                                command_location,
                                f"part validation command has stale validation path `{command_path}`",
                            )
                        )

    _require_tokens(
        repo_root=repo_root,
        path_name=command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        tokens=command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    validation_command_decision_text = read_text_or_issue(
        repo_root / command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
        issues,
        root=repo_root,
    )
    if validation_command_decision_text and markdown_python_commands(
        markdown_heading_section(validation_command_decision_text, "Validation")
    ):
        issues.append(
            ValidationIssue(
                command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
                "decision validation must route executable commands to mechanics/AGENTS.md#validation",
            )
        )
    _require_tokens(
        repo_root=repo_root,
        path_name=command_tokens.MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
        tokens=command_tokens.MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=(
            "Focused mechanic topology checks",
            command_tokens.MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name="docs/decisions/README.md",
        tokens=(
            command_tokens.MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME,
            command_tokens.MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME,
            "Mechanic Part Validation Command Reachability",
            "Mechanic Part Validation Command Ownership",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("payload coverage anchor", "stale validation path"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("part validation route", "payload coverage anchor"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


__all__ = ("validate_mechanic_part_validation_command_surfaces",)
