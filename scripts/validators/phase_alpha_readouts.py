"""Phase Alpha matrix projection and sibling-compat readout validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    phase_alpha_matrix_projection as phase_alpha_matrix_projection_validator,
    phase_alpha_matrix_sibling_compat as phase_alpha_matrix_sibling_compat_validator,
    root_context,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def validate_phase_alpha_readout_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    repo_ref_roots = root_context.REPO_REF_ROOTS
    strict_sibling_compat = root_context.strict_sibling_compat_checks_enabled()

    issues.extend(
        _module_issues(
            phase_alpha_matrix_projection_validator.validate_phase_alpha_matrix_projection(
                repo_root
            )
        )
    )
    issues.extend(
        _module_issues(
            phase_alpha_matrix_sibling_compat_validator.validate_phase_alpha_matrix_sibling_compat(
                repo_root,
                sibling_root=root_context.AOA_PLAYBOOKS_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
                visible_roots=root_context.VISIBLE_ROOTS,
                builder_loader=phase_alpha_matrix_sibling_compat_validator.load_phase_alpha_eval_matrix_builder,
            )
        )
    )
    return issues
