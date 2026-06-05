"""Source eval entry validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from validators.common import ValidationIssue
from validators.eval_roadmap_parity import validate_roadmap_parity
from validators.eval_starter_surfaces import (
    validate_eval_index,
    validate_eval_selection,
    validate_starter_bundle_contract,
)


def validate_source_eval_entry_surfaces(
    repo_root: Path,
    *,
    starter_names: Sequence[str],
    selected_evals: set[str] | None,
    selected_starter_evals: set[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        validate_eval_index(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_eval_selection(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_starter_bundle_contract(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_starter_evals,
        )
    )
    issues.extend(
        validate_roadmap_parity(
            repo_root,
            starter_names=starter_names,
            selected_evals=selected_evals,
        )
    )
    return issues


__all__ = ("validate_source_eval_entry_surfaces",)
