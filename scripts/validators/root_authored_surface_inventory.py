"""Residual root-authored surface inventory drift checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_authored_surface_common import (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS,
)


def _actual_district_names(repo_root: Path, district_name: str) -> set[str]:
    district = repo_root / district_name
    if district_name == "docs":
        return {
            path.relative_to(district).as_posix()
            for path in district.rglob("*")
            if path.is_file() and path.relative_to(district).parts[:1] != ("decisions",)
        }
    if district_name == "scripts":
        return {
            path.relative_to(district).as_posix()
            for path in district.rglob("*")
            if path.is_file() and "__pycache__" not in path.relative_to(district).parts
        }
    return {path.name for path in district.iterdir() if path.is_file()}


def validate_root_authored_surface_inventory(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for district_name, allowed_names in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICTS.items():
        district = repo_root / district_name
        if not district.is_dir():
            issues.append(
                ValidationIssue(district_name, "classified root-authored district is missing")
            )
            continue
        allowed = set(allowed_names)
        actual_names = _actual_district_names(repo_root, district_name)
        for file_name in sorted(actual_names - allowed):
            issues.append(
                ValidationIssue(
                    f"{district_name}/{file_name}",
                    "unclassified root-authored surface must be routed, moved, or added to the residual classification ledger",
                )
            )
        for file_name in sorted(allowed - actual_names):
            issues.append(
                ValidationIssue(
                    f"{district_name}/{file_name}",
                    "classified root-authored surface is missing; update the residual classification ledger if it moved",
                )
            )
    return issues


__all__ = ("validate_root_authored_surface_inventory",)
