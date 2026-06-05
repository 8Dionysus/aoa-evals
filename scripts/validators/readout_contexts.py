"""Shared readout validator contexts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_capsule_contract
import eval_catalog_contract
import eval_comparison_spine_contract

from validators import (
    generated_eval_readmodel_common as generated_readmodel_common,
    root_context,
    runtime_audit_common as runtime_audit_common_validator,
)
from validators.common import ValidationIssue


def read_json_file(path: Path, issues: list[ValidationIssue], repo_root: Path) -> Any | None:
    payload, contract_issues = eval_catalog_contract.read_json_file(path, repo_root)
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return payload


def runtime_audit_context() -> runtime_audit_common_validator.RuntimeAuditContext:
    return runtime_audit_common_validator.RuntimeAuditContext(
        agents_of_abyss_root=root_context.AGENTS_OF_ABYSS_ROOT,
        abyss_stack_root=root_context.ABYSS_STACK_ROOT,
        aoa_playbooks_root=root_context.AOA_PLAYBOOKS_ROOT,
        repo_ref_roots=root_context.REPO_REF_ROOTS,
        strict_sibling_compat_checks_enabled=root_context.strict_sibling_compat_checks_enabled,
        parse_repo_ref=root_context.parse_repo_ref,
        parse_named_surface_ref=root_context.parse_named_surface_ref,
        validate_abyss_stack_ref=root_context.validate_abyss_stack_ref,
    )


def generated_read_model_context() -> generated_readmodel_common.GeneratedReadModelContext:
    return generated_readmodel_common.GeneratedReadModelContext(
        build_catalog_payloads=eval_catalog_contract.build_catalog_payloads,
        build_capsule_payload=eval_capsule_contract.build_capsule_payload,
        build_comparison_spine_payload=eval_comparison_spine_contract.build_comparison_spine_payload,
        full_catalog_entry=eval_catalog_contract.full_catalog_entry,
        project_min_catalog=eval_catalog_contract.project_min_catalog,
        read_json_file=read_json_file,
    )
