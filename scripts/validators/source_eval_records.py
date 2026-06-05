"""Source eval authored record parsing and schema contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import yaml

import eval_capsule_contract
import eval_section_contract
from validators.common import ValidationIssue
from validators.source_eval_common import relative_location, validate_against_schema


SOURCE_EVALS_DIR_NAME = "evals"
EVAL_FRONTMATTER_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json"
)
EVAL_MANIFEST_SCHEMA_NAME = (
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json"
)
MIRRORED_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "report_format",
    "comparison_surface",
)


@dataclass(frozen=True)
class EvalBundleRecord:
    name: str
    bundle_dir: Path
    eval_md_path: Path
    eval_yaml_path: Path
    metadata: dict[str, Any]
    manifest: dict[str, Any]
    sections: dict[str, str]


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


def validate_source_eval_command_ownership(
    repo_root: Path,
    records: Sequence[EvalBundleRecord],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for record in records:
        path_name = relative_location(record.eval_md_path, repo_root)
        try:
            text = record.eval_md_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            issues.append(ValidationIssue(path_name, "file is missing"))
            continue
        if markdown_python_commands(text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "source EVAL.md must route executable validation commands to evals/AGENTS.md or the nearest AGENTS.md",
                )
            )

    return issues


def parse_eval_markdown(
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    try:
        text = eval_md_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(eval_md_path), "file is missing"))
        return None, {}

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter opening delimiter",
            )
        )
        return None, {}

    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "missing YAML frontmatter closing delimiter",
            )
        )
        return None, {}

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        metadata = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                f"invalid frontmatter YAML: {exc}",
            )
        )
        return None, {}

    if not isinstance(metadata, dict):
        issues.append(
            ValidationIssue(
                relative_location(eval_md_path),
                "frontmatter must parse to a mapping",
            )
        )
        return None, {}

    sections: dict[str, str] = {}
    current_heading: str | None = None
    current_lines: list[str] = []
    for line in body.splitlines():
        heading_match = re.match(r"^##\s+(.+?)\s*$", line)
        if heading_match:
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return metadata, sections


def find_support_artifacts(bundle_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    for folder_name in ("examples", "checks", "notes"):
        folder = bundle_dir / folder_name
        if folder.is_dir():
            artifacts.extend(sorted(folder.glob("*.md")))
    return artifacts


def resolve_manifest_path(bundle_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return bundle_dir / candidate


def validate_eval_frontmatter(
    eval_name: str,
    metadata: dict[str, Any],
    eval_md_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_md_path)
    valid = validate_against_schema(metadata, EVAL_FRONTMATTER_SCHEMA_NAME, location, issues)
    if metadata.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "frontmatter 'name' must match the directory name")
        )
        valid = False
    return valid


def validate_eval_headings(
    sections: dict[str, str],
    eval_md_path: Path,
    repo_root: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_md_path)
    section_pairs, pair_issues = eval_section_contract.extract_section_pairs(
        eval_md_path,
        location=location,
    )
    contract_issues = eval_section_contract.collect_section_contract_issues(
        section_pairs or list(sections.items()),
        location=location,
    )
    capsule_source_issues = eval_capsule_contract.validate_capsule_source_sections(
        sections,
        eval_md_path,
        repo_root,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in [*pair_issues, *contract_issues, *capsule_source_issues]
    )


def validate_eval_manifest(
    eval_name: str,
    manifest: Any,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> bool:
    location = relative_location(eval_yaml_path)
    if not isinstance(manifest, dict):
        issues.append(ValidationIssue(location, "manifest must parse to a mapping"))
        return False

    valid = validate_against_schema(manifest, EVAL_MANIFEST_SCHEMA_NAME, location, issues)
    if manifest.get("name") != eval_name:
        issues.append(
            ValidationIssue(location, "'name' must match the directory name")
        )
        valid = False
    return valid


def validate_mirrored_manifest_fields(
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    eval_md_path: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    source_location = relative_location(eval_md_path)
    for field_name in MIRRORED_FIELDS:
        if metadata.get(field_name) != manifest.get(field_name):
            issues.append(
                ValidationIssue(
                    location,
                    f"field '{field_name}' does not match {source_location}",
                )
            )


__all__ = (
    "SOURCE_EVALS_DIR_NAME",
    "EVAL_FRONTMATTER_SCHEMA_NAME",
    "EVAL_MANIFEST_SCHEMA_NAME",
    "MIRRORED_FIELDS",
    "EvalBundleRecord",
    "markdown_python_commands",
    "validate_source_eval_command_ownership",
    "parse_eval_markdown",
    "find_support_artifacts",
    "resolve_manifest_path",
    "validate_eval_frontmatter",
    "validate_eval_headings",
    "validate_eval_manifest",
    "validate_mirrored_manifest_fields",
)
