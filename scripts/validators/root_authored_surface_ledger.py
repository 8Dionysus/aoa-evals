"""Residual root-authored surface ledger row checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.mechanics_common import (
    MECHANICS_EVIDENCE_CLUSTERS,
    _markdown_heading_section,
    _markdown_table_rows,
)
from validators.root_authored_surface_common import (
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION,
)


def validate_root_authored_surface_ledger(repo_root: Path) -> list[ValidationIssue]:
    issues: list[tuple[str, str]] = []
    evidence_path = repo_root / MECHANICS_EVIDENCE_CLUSTERS
    if not evidence_path.is_file():
        return [
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                "mechanics evidence cluster map is missing",
            )
        ]

    text = evidence_path.read_text(encoding="utf-8")
    section = _markdown_heading_section(text, ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION)
    if not section:
        issues.append(
            (
                MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                f"mechanics evidence cluster map must contain section {ROOT_AUTHORED_SURFACE_CLASSIFICATION_SECTION!r}",
            )
        )

    for token in ROOT_AUTHORED_SURFACE_CLASSIFICATION_REQUIRED_TOKENS:
        if token not in section:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface classification must mention {token!r}",
                )
            )

    ledger_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(section):
        if not cells or cells[0] == "Surface":
            continue
        surface_name = cells[0].strip("`")
        if surface_name in ledger_rows:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must appear only once in the residual classification ledger",
                )
            )
        ledger_rows[surface_name] = cells
        district_name, separator, file_name = surface_name.partition("/")
        if (
            not separator
            or not file_name
            or district_name not in ROOT_AUTHORED_SURFACE_CLASSIFICATION_DISTRICT_NAMES
        ):
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` must route under docs/, scripts/, or tests/",
                )
            )
        if len(cells) != len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS):
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must have {len(ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS)} columns",
                )
            )
            continue
        for column_name, cell in zip(
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COLUMNS[1:],
            cells[1:],
            strict=True,
        ):
            if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                issues.append(
                    (
                        MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                        f"root-authored surface `{surface_name}` row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        if "mechanic-owned payload" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its mechanic-owned payload boundary",
                )
            )
        if "root-owned" not in row_text:
            issues.append(
                (
                    MECHANICS_EVIDENCE_CLUSTERS.as_posix(),
                    f"root-authored surface `{surface_name}` row must state its root-owned role",
                )
            )

    return [ValidationIssue(location, message) for location, message in issues]


__all__ = ("validate_root_authored_surface_ledger",)
