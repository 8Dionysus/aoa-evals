"""Mechanic part source-surface reference contracts."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

from validators.common import ValidationIssue
from validators.mechanic_part_contract_common import (
    DECISION_RECORDS_README_NAME,
    MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
    MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS,
    MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
    MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _require_tokens,
    markdown_heading_section,
)


SOURCE_SURFACE_CODE_REF_RE = re.compile(r"`([^`\n]+)`")
SOURCE_SURFACE_FILE_REF_RE = re.compile(r"\.[A-Za-z0-9][A-Za-z0-9_.-]*$")


def mechanic_part_source_surface_refs(readme_text: str) -> list[str]:
    section = markdown_heading_section(readme_text, "Source Surfaces")
    refs: list[str] = []
    for match in SOURCE_SURFACE_CODE_REF_RE.finditer(section):
        ref = match.group(1).strip()
        if not ref:
            continue
        if source_surface_ref_is_path_like(ref):
            refs.append(ref)
    return list(dict.fromkeys(refs))


def source_surface_ref_is_path_like(ref: str) -> bool:
    return (
        ref.startswith(("repo:", ".", "/"))
        or "/" in ref
        or "*" in ref
        or "?" in ref
        or "[" in ref
        or SOURCE_SURFACE_FILE_REF_RE.search(ref) is not None
    )


def source_surface_ref_resolution_issue(repo_root: Path, ref: str) -> str | None:
    if ref.startswith("repo:"):
        return None
    if ref.startswith(("http://", "https://")):
        return None
    if ref.startswith("/"):
        return "source surface ref must be repo-relative or repo-qualified, not absolute"
    if ".." in PurePosixPath(ref).parts:
        return "source surface ref must not traverse outside the repository"
    if "<" in ref or ">" in ref:
        return None

    if any(char in ref for char in "*?["):
        if any(repo_root.glob(ref)):
            return None
        return "stale source surface ref must resolve as a repo-relative glob"

    if (repo_root / ref.rstrip("/")).exists():
        return None
    return "stale source surface ref must resolve as a repo-relative path"


def validate_part_source_surface_refs(
    *,
    repo_root: Path,
    readme_name: str,
    readme_text: str,
    issues: list[ValidationIssue],
) -> None:
    source_refs = mechanic_part_source_surface_refs(readme_text)
    if readme_text and "## Source Surfaces" in readme_text and not source_refs:
        issues.append(
            ValidationIssue(
                readme_name,
                "part README Source Surfaces must name at least one path-like source ref",
            )
        )
    for ref in source_refs:
        ref_issue = source_surface_ref_resolution_issue(repo_root, ref)
        if ref_issue is not None:
            issues.append(
                ValidationIssue(
                    readme_name,
                    f"{ref_issue}: `{ref}`",
                )
            )


def validate_mechanic_part_source_surface_decision_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PART_SOURCE_SURFACE_REF_DECISION_NAME,
            "Mechanic Part Source Surface Reference Guard",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Source Surfaces", "stale source surface ref"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "repo-relative path"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANIC_LOWER_INDEX_DIRECTION_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
        tokens=MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PART_SOURCE_SURFACES_SECTION_DECISION_NAME,
            "Mechanic Part Source Surfaces Section Contract",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("## Source Surfaces", "at least one path-like source ref"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Source Surfaces", "plural section"),
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
    "SOURCE_SURFACE_CODE_REF_RE",
    "SOURCE_SURFACE_FILE_REF_RE",
    "mechanic_part_source_surface_refs",
    "source_surface_ref_is_path_like",
    "source_surface_ref_resolution_issue",
    "validate_part_source_surface_refs",
    "validate_mechanic_part_source_surface_decision_surfaces",
)
