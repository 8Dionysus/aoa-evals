"""Source eval dependency and doctrine validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    proof_infra_shared_support as proof_infra_validator,
    root_context,
    source_artifact_process_doctrine as source_artifact_process_doctrine_validator,
    source_comparison_doctrine as source_comparison_doctrine_validator,
    source_eval_records as source_eval_records_validator,
    source_integrity_taxonomy as source_integrity_taxonomy_validator,
    source_repeated_window_doctrine as source_repeated_window_doctrine_validator,
)
from validators.common import ValidationIssue


def source_eval_dependency_roots() -> dict[str, Path]:
    return {
        "aoa-techniques": root_context.AOA_TECHNIQUES_ROOT,
        "aoa-skills": root_context.AOA_SKILLS_ROOT,
    }


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def validate_source_eval_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    selected_evals: set[str] | None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    issues.extend(
        _module_issues(
            source_eval_records_validator.validate_source_eval_command_ownership(
                repo_root, records
            )
        )
    )
    issues.extend(
        _module_issues(
            source_comparison_doctrine_validator.validate_comparison_doctrine_surfaces(
                repo_root,
                records,
                selected_evals=selected_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            source_artifact_process_doctrine_validator.validate_artifact_process_doctrine_surfaces(
                repo_root,
                records,
                selected_evals=selected_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            source_repeated_window_doctrine_validator.validate_repeated_window_doctrine_surfaces(
                repo_root,
                records,
                selected_evals=selected_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            source_integrity_taxonomy_validator.validate_integrity_taxonomy_surfaces(
                repo_root,
                selected_evals=selected_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            proof_infra_validator.validate_shared_proof_infra_surfaces(
                repo_root,
                selected_evals=selected_evals,
            )
        )
    )
    return issues
