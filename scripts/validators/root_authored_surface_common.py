"""Shared parsing helpers for residual root-authored surface classification."""

from __future__ import annotations

from pathlib import Path

from validators.mechanics_common import (
    MECHANICS_EVIDENCE_CLUSTERS,
    _markdown_heading_section,
    _markdown_table_rows,
)

ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0085-root-authored-surface-classification.md"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND = (
    "python -m pytest -q tests/test_mechanics_topology.py"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION = "Residual Root-authored Surface Classification"
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS = (
    "Surface",
    "Root role",
    "Mechanic boundary",
    "Validation guard",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES = ("docs", "scripts", "tests")
ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS = (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    "Root role",
    "Mechanic boundary",
    "Validation guard",
    "root-owned",
    "mechanic-owned payload",
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS = (
    "Root-authored Surface Classification",
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
    "docs/",
    "scripts/",
    "tests/",
    "root-owned",
    "mechanic-owned payload",
    "unclassified root-authored surface",
    "validator allowlist retired",
    "ledger-derived surface map",
    "`mechanics/EVIDENCE_CLUSTERS.md` remains the source",
)


def _classification_section(repo_root: Path) -> str:
    evidence_path = repo_root / MECHANICS_EVIDENCE_CLUSTERS
    if not evidence_path.is_file():
        return ""
    text = evidence_path.read_text(encoding="utf-8")
    return _markdown_heading_section(text, ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION)


def _surface_name_from_cell(cell: str) -> str:
    return cell.strip().strip("`")


def root_authored_surface_classification_rows(repo_root: Path) -> tuple[tuple[str, ...], ...]:
    section = _classification_section(repo_root)
    rows: list[tuple[str, ...]] = []
    for cells in _markdown_table_rows(section):
        if not cells or cells[0] == ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS[0]:
            continue
        rows.append(tuple(cells))
    return tuple(rows)


def root_authored_surface_classification_districts(
    repo_root: Path,
) -> dict[str, tuple[str, ...]]:
    districts: dict[str, list[str]] = {
        district_name: [] for district_name in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES
    }
    for cells in root_authored_surface_classification_rows(repo_root):
        surface_name = _surface_name_from_cell(cells[0]) if cells else ""
        district_name, separator, file_name = surface_name.partition("/")
        if separator and file_name and district_name in districts:
            districts[district_name].append(file_name)
    return {
        district_name: tuple(file_names)
        for district_name, file_names in districts.items()
    }


def expected_root_authored_surfaces(repo_root: Path) -> set[str]:
    return {
        f"{district_name}/{file_name}"
        for district_name, file_names in root_authored_surface_classification_districts(
            repo_root
        ).items()
        for file_name in file_names
    }


__all__ = (
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_NAME",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DECISION_REQUIRED_TOKENS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS",
    "ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION",
    "expected_root_authored_surfaces",
    "root_authored_surface_classification_districts",
    "root_authored_surface_classification_rows",
)
