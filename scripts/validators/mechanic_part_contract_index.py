"""Mechanic parent PARTS.md contract-token surfaces."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.mechanic_part_contract_common import (
    DECISION_RECORDS_README_NAME,
    MECHANIC_PART_CONTRACT_FILES,
    MECHANIC_PART_CONTRACT_REQUIRED_TOKENS,
    MECHANIC_PART_README_CONTRACT_DECISION_NAME,
    MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS,
    require_tokens,
)


def validate_mechanic_part_contract_index_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name in MECHANIC_PART_CONTRACT_FILES:
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=MECHANIC_PART_CONTRACT_REQUIRED_TOKENS,
            issues=issues,
        )
    require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_PART_README_CONTRACT_DECISION_NAME,
        tokens=MECHANIC_PART_README_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=DECISION_RECORDS_README_NAME,
        tokens=(
            MECHANIC_PART_README_CONTRACT_DECISION_NAME,
            "Mechanic Part README Contract",
        ),
        issues=issues,
    )
    return issues


__all__ = ("validate_mechanic_part_contract_index_surfaces",)
