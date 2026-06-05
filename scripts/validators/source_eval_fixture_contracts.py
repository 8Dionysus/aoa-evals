"""Bundle-local source eval fixture contract validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_proof_contract_helpers
from validators import proof_infra_common as proof_infra_validator
from validators.common import ValidationIssue
from validators.source_eval_artifact_common import (
    requires_materialized_comparison_artifacts,
    validate_raw_repo_relative_path,
    validate_raw_repo_relative_path_list,
    validate_repo_relative_contract_path,
)
from validators.source_eval_common import load_json_payload, relative_location, validate_against_schema


def validate_bundle_fixture_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "fixtures" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship fixtures/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, proof_infra_validator.FIXTURE_CONTRACT_SCHEMA_NAME, location, issues):
        return

    validate_raw_repo_relative_path(
        payload.get("shared_fixture_family_path"),
        location=f"{location}.shared_fixture_family_path",
        issues=issues,
    )
    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        location=location,
        issues=issues,
    )
    fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(payload)
    for index, shared_fixture_family_path in enumerate(fixture_family_paths):
        field_name = (
            "shared_fixture_family_path"
            if index == 0
            else f"{eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY}[{index - 1}]"
        )
        validate_repo_relative_contract_path(
            repo_root,
            shared_fixture_family_path,
            location=f"{location}.{field_name}",
            issues=issues,
        )


__all__ = ("validate_bundle_fixture_contract",)
