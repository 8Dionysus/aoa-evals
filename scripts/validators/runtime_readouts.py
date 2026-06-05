"""Runtime readout and trace/eval bridge validation routes."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from validators import (
    readout_contexts,
    runtime_audit_common as runtime_audit_common_validator,
    runtime_candidate_intake as runtime_candidate_intake_validator,
    runtime_candidate_template_index as runtime_candidate_template_index_validator,
    runtime_evidence_selection as runtime_evidence_selection_validator,
    runtime_integrity_review_docs as runtime_integrity_review_docs_validator,
    runtime_integrity_review_example as runtime_integrity_review_example_validator,
    runtime_integrity_review_schema as runtime_integrity_review_schema_validator,
    runtime_trace_eval_bridge as runtime_trace_eval_bridge_validator,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def validate_repo_wide_runtime_readout_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: runtime_audit_common_validator.RuntimeAuditContext | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    runtime_context = context or readout_contexts.runtime_audit_context()

    issues.extend(
        _module_issues(
            runtime_trace_eval_bridge_validator.validate_trace_eval_bridge_surfaces(
                repo_root,
                records,
                context=runtime_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_integrity_review_docs_validator.validate_runtime_integrity_review_doc_surfaces(
                repo_root
            )
        )
    )
    schema_validation = runtime_integrity_review_schema_validator.runtime_integrity_review_schema_validation(
        repo_root
    )
    issues.extend(_module_issues(schema_validation.issues))
    issues.extend(
        _module_issues(
            runtime_integrity_review_example_validator.validate_runtime_integrity_review_example_surface(
                repo_root,
                context=runtime_context,
                schema_validator=schema_validation.validator,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_evidence_selection_validator.validate_runtime_evidence_selection_surfaces(
                repo_root,
                records,
                context=runtime_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_candidate_template_index_validator.validate_runtime_candidate_template_index(
                repo_root,
                builder_loader=runtime_candidate_template_index_validator.load_runtime_candidate_template_index_builder,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_candidate_intake_validator.validate_runtime_candidate_intake(
                repo_root,
                builder_loader=runtime_candidate_intake_validator.load_runtime_candidate_intake_builder,
            )
        )
    )
    return issues


def validate_target_runtime_readout_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    target_eval_names: set[str],
    context: runtime_audit_common_validator.RuntimeAuditContext | None = None,
) -> list[ValidationIssue]:
    runtime_context = context or readout_contexts.runtime_audit_context()
    return _module_issues(
        runtime_evidence_selection_validator.validate_runtime_evidence_selection_surfaces(
            repo_root,
            records,
            context=runtime_context,
            target_eval_names=target_eval_names,
        )
    )
