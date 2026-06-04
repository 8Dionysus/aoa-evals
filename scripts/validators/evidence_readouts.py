"""Repo-wide and target eval readout validation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import eval_catalog_contract

from validators import (
    generated_parity,
    phase_alpha_matrix as phase_alpha_matrix_validator,
    publication_receipts as publication_receipts_validator,
    release_support as release_support_validator,
    report_index as report_index_validator,
    root_context,
    runtime_audit as runtime_audit_validator,
    runtime_candidates as runtime_candidates_validator,
    source_eval_contracts as source_eval_contracts_validator,
    titan as titan_validator,
)
from validators.common import ValidationIssue


def _module_issues(module_issues: Sequence[Any]) -> list[ValidationIssue]:
    return [
        ValidationIssue(issue.location, issue.message)
        for issue in module_issues
    ]


def read_json_file(path: Path, issues: list[ValidationIssue], repo_root: Path) -> Any | None:
    payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return payload


def runtime_audit_context() -> runtime_audit_validator.RuntimeAuditContext:
    return runtime_audit_validator.RuntimeAuditContext(
        agents_of_abyss_root=root_context.AGENTS_OF_ABYSS_ROOT,
        abyss_stack_root=root_context.ABYSS_STACK_ROOT,
        aoa_playbooks_root=root_context.AOA_PLAYBOOKS_ROOT,
        repo_ref_roots=root_context.REPO_REF_ROOTS,
        strict_sibling_compat_checks_enabled=root_context.strict_sibling_compat_checks_enabled,
        parse_repo_ref=root_context.parse_repo_ref,
        parse_named_surface_ref=root_context.parse_named_surface_ref,
        validate_abyss_stack_ref=root_context.validate_abyss_stack_ref,
    )


def generated_read_model_context() -> generated_parity.GeneratedReadModelContext:
    return generated_parity.GeneratedReadModelContext(
        build_catalog_payloads=source_eval_contracts_validator.build_catalog_payloads,
        build_capsule_payload=source_eval_contracts_validator.build_capsule_payload,
        build_comparison_spine_payload=source_eval_contracts_validator.build_comparison_spine_payload,
        full_catalog_entry=source_eval_contracts_validator.full_catalog_entry,
        project_min_catalog=source_eval_contracts_validator.project_min_catalog,
        read_json_file=read_json_file,
    )


def validate_repo_wide_readout_surfaces(
    repo_root: Path,
    records: Sequence[Any],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    runtime_context = runtime_audit_context()
    generated_context = generated_read_model_context()
    repo_ref_roots = root_context.REPO_REF_ROOTS
    strict_sibling_compat = root_context.strict_sibling_compat_checks_enabled()

    issues.extend(
        _module_issues(
            runtime_audit_validator.validate_trace_eval_bridge_surfaces(
                repo_root,
                records,
                context=runtime_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_audit_validator.validate_runtime_integrity_review_surface(
                repo_root,
                context=runtime_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_validator.validate_eval_result_receipt_surfaces(
                repo_root,
                aoa_stats_root=root_context.AOA_STATS_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_validator.validate_receipt_intake_dry_review_surface(
                repo_root,
                fallback_repo_root=root_context.REPO_ROOT,
            )
        )
    )
    issues.extend(
        _module_issues(
            release_support_validator.validate_release_support_readiness_audit_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            release_support_validator.validate_strategic_closeout_audit_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            release_support_validator.validate_release_prep_pr_handoff_surface(
                repo_root,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            publication_receipts_validator.validate_live_receipt_log(
                repo_root,
                fallback_repo_root=root_context.REPO_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_audit_validator.validate_runtime_evidence_selection_surfaces(
                repo_root,
                records,
                context=runtime_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_candidates_validator.validate_runtime_candidate_template_index(
                repo_root,
                builder_loader=runtime_candidates_validator.load_runtime_candidate_template_index_builder,
            )
        )
    )
    issues.extend(
        _module_issues(
            runtime_candidates_validator.validate_runtime_candidate_intake(
                repo_root,
                builder_loader=runtime_candidates_validator.load_runtime_candidate_intake_builder,
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
    issues.extend(
        _module_issues(
            phase_alpha_matrix_validator.validate_phase_alpha_eval_matrix(
                repo_root,
                sibling_root=root_context.AOA_PLAYBOOKS_ROOT,
                repo_ref_roots=repo_ref_roots,
                strict_sibling_compat=strict_sibling_compat,
                visible_roots=root_context.VISIBLE_ROOTS,
                builder_loader=phase_alpha_matrix_validator.load_phase_alpha_eval_matrix_builder,
            )
        )
    )
    issues.extend(_module_issues(titan_validator.validate_titan_canary_surfaces(repo_root)))
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_catalogs(
                repo_root,
                records,
                context=generated_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_capsules(
                repo_root,
                records,
                context=generated_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_sections(
                repo_root,
                records,
                context=generated_context,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_comparison_spine(
                repo_root,
                records,
                context=generated_context,
            )
        )
    )
    return issues


def validate_target_eval_readout_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    *,
    target_evals: Sequence[str],
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    runtime_context = runtime_audit_context()
    generated_context = generated_read_model_context()
    issues.extend(
        _module_issues(
            runtime_audit_validator.validate_runtime_evidence_selection_surfaces(
                repo_root,
                records,
                context=runtime_context,
                target_eval_names=set(target_evals),
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_catalogs(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_capsules(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_sections(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_evals,
            )
        )
    )
    issues.extend(
        _module_issues(
            generated_parity.validate_generated_comparison_spine(
                repo_root,
                records,
                context=generated_context,
                target_eval_names=target_evals,
            )
        )
    )
    return issues
