"""Generated read-model parity validation routes."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    generated_eval_capsules as generated_capsules,
    generated_eval_catalogs as generated_catalogs,
    generated_eval_comparison_spine as generated_comparison_spine,
    generated_eval_readmodel_common as generated_readmodel_common,
    generated_eval_sections as generated_sections,
    readout_contexts,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def validate_generated_readout_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: generated_readmodel_common.GeneratedReadModelContext | None = None,
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    generated_context = context or readout_contexts.generated_read_model_context()

    issues.extend(
        _module_issues(
            generated_catalogs.validate_generated_catalogs(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_eval_names,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_capsules.validate_generated_capsules(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_eval_names,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_sections.validate_generated_sections(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_eval_names,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_comparison_spine.validate_generated_comparison_spine(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_eval_names,
            )
        )
    )
    return issues
