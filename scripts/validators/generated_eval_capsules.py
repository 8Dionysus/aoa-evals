"""Generated eval capsule projection parity."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import eval_capsule_contract
from validators.common import ValidationIssue, relative_location
from validators.generated_eval_readmodel_common import (
    CAPSULE_NAME,
    CAPSULE_SOURCE_OF_TRUTH,
    CAPSULE_VERSION,
    FULL_CATALOG_NAME,
    GENERATED_DIR_NAME,
    GeneratedReadModelContext,
    add_contract_issues,
    read_generated_object,
    validate_target_entry_parity,
    validate_versioned_source,
)


def validate_generated_capsules(
    repo_root: Path,
    records: Sequence[Any],
    *,
    context: GeneratedReadModelContext,
    target_eval_names: Sequence[str] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    full_path = repo_root / GENERATED_DIR_NAME / FULL_CATALOG_NAME
    capsule_path = repo_root / GENERATED_DIR_NAME / CAPSULE_NAME
    capsule_location = relative_location(capsule_path, repo_root)

    expected_full, _expected_min = context.build_catalog_payloads(repo_root, records)
    expected_capsules = context.build_capsule_payload(repo_root, records, expected_full)
    actual_capsules = read_generated_object(
        capsule_path,
        label="generated capsules",
        issues=issues,
        repo_root=repo_root,
        context=context,
    )
    if actual_capsules is None:
        return issues

    validate_versioned_source(
        actual_capsules,
        version_key="capsule_version",
        expected_version=CAPSULE_VERSION,
        expected_source=CAPSULE_SOURCE_OF_TRUTH,
        source_message="source_of_truth does not match the capsule contract",
        location=capsule_location,
        issues=issues,
    )

    if target_eval_names is None:
        if actual_capsules != expected_capsules:
            issues.append(
                ValidationIssue(
                    capsule_location,
                    "generated capsules are out of date; run 'python scripts/build_catalog.py'",
                )
            )
    else:
        validate_target_entry_parity(
            expected_payload=expected_capsules,
            actual_payload=actual_capsules,
            target_eval_names=target_eval_names,
            location=capsule_location,
            missing_message="generated capsules are missing eval '{eval_name}'",
            drift_message=(
                "generated capsule entry for '{eval_name}' is out of date; "
                "run 'python scripts/build_catalog.py'"
            ),
            issues=issues,
        )

    alignment_issues: list[ValidationIssue] = []
    actual_full = context.read_json_file(full_path, alignment_issues, repo_root)
    issues.extend(alignment_issues)
    if isinstance(actual_full, dict):
        contract_issues = eval_capsule_contract.validate_capsule_alignment(
            actual_full,
            actual_capsules,
            location=capsule_location,
            target_eval_names=set(target_eval_names) if target_eval_names is not None else None,
        )
        add_contract_issues(issues, contract_issues)

    return issues
