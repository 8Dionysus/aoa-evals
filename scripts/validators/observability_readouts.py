"""Receipt, report-index, and release-support readout validation routes."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    publication_receipts_intake_artifact as publication_receipts_intake_artifact_validator,
    publication_receipts_intake_boundary as publication_receipts_intake_boundary_validator,
    publication_receipts_intake_preview as publication_receipts_intake_preview_validator,
    publication_receipts_intake_route as publication_receipts_intake_route_validator,
    publication_receipts_live as publication_receipts_live_validator,
    publication_receipts_payload as publication_receipts_payload_validator,
    release_support_pr_handoff_report as release_support_pr_handoff_report_validator,
    release_support_readiness_report as release_support_readiness_report_validator,
    release_support_strategic_closeout_report as release_support_strategic_closeout_report_validator,
    report_index as report_index_validator,
    root_context,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def validate_observability_readout_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    repo_ref_roots = root_context.REPO_REF_ROOTS
    strict_sibling_compat = root_context.strict_sibling_compat_checks_enabled()

    issues.extend(
        _module_issues(
            publication_receipts_payload_validator.validate_eval_result_receipt_surfaces(
                repo_root,
                aoa_stats_root=root_context.AOA_STATS_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_intake_route_validator.validate_receipt_intake_route_surfaces(repo_root)
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_intake_artifact_validator.validate_receipt_intake_artifact_surface(repo_root)
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_intake_preview_validator.validate_receipt_intake_candidate_preview_surface(
                repo_root, fallback_repo_root=root_context.REPO_ROOT
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_intake_boundary_validator.validate_receipt_intake_boundary_surface(repo_root)
        )
    )
    issues.extend(
        _module_issues(
            release_support_readiness_report_validator.validate_release_support_readiness_audit_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            release_support_strategic_closeout_report_validator.validate_strategic_closeout_audit_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            release_support_pr_handoff_report_validator.validate_release_prep_pr_handoff_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_live_validator.validate_live_receipt_log(
                repo_root,
                fallback_repo_root=root_context.REPO_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            report_index_validator.validate_eval_report_index(
                repo_root,
                builder_loader=report_index_validator.load_eval_report_index_builder,
            )
        )
    )
    return issues
