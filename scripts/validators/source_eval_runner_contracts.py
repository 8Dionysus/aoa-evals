"""Bundle-local source eval runner contract validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_proof_contract_helpers
from validators import proof_infra_common as proof_infra_validator
from validators.common import ValidationIssue
from validators.source_eval_artifact_common import (
    requires_materialized_comparison_artifacts,
    validate_raw_repo_relative_path_list,
    validate_repo_relative_contract_path,
)
from validators.source_eval_common import load_json_payload, relative_location, validate_against_schema


def validate_bundle_runner_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any] | None,
    issues: list[ValidationIssue],
) -> None:
    contract_path = bundle_dir / "runners" / "contract.json"
    if not contract_path.is_file():
        if requires_materialized_comparison_artifacts(manifest):
            baseline_mode = manifest.get("baseline_mode") if isinstance(manifest, dict) else "unknown"
            issues.append(
                ValidationIssue(
                    relative_location(bundle_dir, repo_root),
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must ship runners/contract.json",
                )
            )
        return

    location = relative_location(contract_path, repo_root)
    payload = load_json_payload(contract_path, issues)
    if payload is None:
        return
    if not validate_against_schema(payload, proof_infra_validator.RUNNER_CONTRACT_SCHEMA_NAME, location, issues):
        return

    for field_name in ("runner_surface_path", "report_schema_path", "report_example_path", "paired_readout_path"):
        raw_value = payload.get(field_name)
        if isinstance(raw_value, str):
            validate_repo_relative_contract_path(
                repo_root,
                raw_value,
                location=f"{location}.{field_name}",
                issues=issues,
            )

    validate_raw_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        location=location,
        issues=issues,
    )
    additional_paired_readout_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
        payload,
        eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
    )
    for index, value in enumerate(additional_paired_readout_paths):
        validate_repo_relative_contract_path(
            repo_root,
            value,
            location=(
                f"{location}.{eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY}[{index}]"
            ),
            issues=issues,
        )

    for field_name in ("fixture_contract_paths", "scorer_helper_paths"):
        values = payload.get(field_name, [])
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            if not isinstance(value, str):
                continue
            validate_repo_relative_contract_path(
                repo_root,
                value,
                location=f"{location}.{field_name}[{index}]",
                issues=issues,
            )


__all__ = ("validate_bundle_runner_contract",)
