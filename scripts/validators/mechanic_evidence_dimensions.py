"""Active mechanic parent evidence dimension ledger contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanic_parent_registry import (
    ACTIVE_MECHANIC_PARENT_NAMES,
    AOA_ALIGNED_MECHANIC_PARENT_NAMES,
    EVALS_NATIVE_MECHANIC_PARENT_NAMES,
)
from validators.mechanics_common import (
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    _markdown_heading_section,
    _markdown_table_rows,
    _require_tokens,
)


MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0083-mechanic-evidence-dimension-ledger.md"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_dimension"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS = (
    "Active Parent Evidence Dimension Ledger",
    "Meaning/doctrine",
    "Proof pressure",
    "Contracts/payloads",
    "Builders/readouts",
    "Quest/deferred pressure",
    "Owner split and stop-lines",
    "Legacy/provenance",
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS = (
    "Parent",
    "Class",
    "Meaning/doctrine",
    "Proof pressure",
    "Contracts/payloads",
    "Builders/readouts",
    "Quest/deferred pressure",
    "Owner split and stop-lines",
    "Legacy/provenance",
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS = (
    "Mechanic Evidence Dimension Ledger",
    "Active Parent Evidence Dimension Ledger",
    "meaning/doctrine",
    "proof pressure",
    "contracts/payloads",
    "builders/readouts",
    "quest/deferred pressure",
    "owner split and stop-lines",
    "owner-named evals-native",
    "legacy/provenance",
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
)


def validate_mechanic_evidence_dimension_ledger(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = read_text_or_issue(repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME, issues, root=repo_root)
    if not text:
        return issues
    dimension_section = _markdown_heading_section(text, "Active Parent Evidence Dimension Ledger")
    if not dimension_section:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                "mechanics evidence cluster map must contain section 'Active Parent Evidence Dimension Ledger'",
            )
        )

    for token in MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS:
        if token not in dimension_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanics evidence dimension ledger must mention {token!r}",
                )
            )

    expected_class_by_parent = {
        parent_name: "AoA-aligned" for parent_name in AOA_ALIGNED_MECHANIC_PARENT_NAMES
    }
    expected_class_by_parent.update(
        {parent_name: "evals-native" for parent_name in EVALS_NATIVE_MECHANIC_PARENT_NAMES}
    )
    ledger_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(dimension_section):
        parent_cell = cells[0] if cells else ""
        parent_name = parent_cell.strip("`")
        if parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
            if parent_name in ledger_rows:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"active parent `{parent_name}` must appear only once in the evidence dimension ledger",
                    )
                )
            ledger_rows[parent_name] = cells
            if len(cells) != len(MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS):
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence dimension ledger row for `{parent_name}` must have {len(MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS)} columns",
                    )
                )
                continue
            expected_class = expected_class_by_parent[parent_name]
            if cells[1] != expected_class:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"evidence dimension ledger row for `{parent_name}` must use class `{expected_class}`",
                    )
                )
            for column_name, cell in zip(
                MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS[2:],
                cells[2:],
                strict=True,
            ):
                if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                    issues.append(
                        ValidationIssue(
                            MECHANICS_EVIDENCE_CLUSTERS_NAME,
                            f"evidence dimension ledger row for `{parent_name}` must fill `{column_name}`",
                        )
                    )

    for parent_name in ACTIVE_MECHANIC_PARENT_NAMES:
        if parent_name not in ledger_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"active parent `{parent_name}` must appear in the evidence dimension ledger",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME,
        tokens=MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=(
            "Active Parent Evidence Dimension Ledger",
            "meaning/doctrine",
            "owner-named evals-native",
        ),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=(
            "Active Parent Evidence Dimension Ledger",
            "owner split and stop-lines",
            "owner-named evals-native",
        ),
        issues=issues,
    )
    return issues


__all__ = (
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_COLUMNS",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_NAME",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_DECISION_REQUIRED_TOKENS",
    "MECHANIC_EVIDENCE_DIMENSION_LEDGER_REQUIRED_TOKENS",
    "validate_mechanic_evidence_dimension_ledger",
)
