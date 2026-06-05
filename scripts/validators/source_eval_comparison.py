"""Source eval comparison-surface contract validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_catalog_contract
import eval_proof_contract_helpers

from validators.common import ValidationIssue
from validators.source_eval_common import relative_location


COMPARISON_SURFACE_COMMON_KEYS = (
    "shared_family_path",
    "paired_readout_path",
    "integrity_sidecar",
    "selection_question",
)
COMPARISON_SURFACE_ALLOWED_KEYS = {
    "fixed-baseline": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "previous-version": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "baseline_target_label")
    ),
    "peer-compare": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("peer_surfaces", "matched_surface")
    ),
    "longitudinal-window": set(
        COMPARISON_SURFACE_COMMON_KEYS + ("anchor_surface", "window_family_label")
    ),
}


def ensure_repo_relative_path(
    raw_path: str,
    location: str,
    issues: list[ValidationIssue],
) -> str:
    value, contract_issues = eval_catalog_contract.ensure_repo_relative_path(
        raw_path,
        location,
    )
    issues.extend(
        ValidationIssue(issue.location, issue.message)
        for issue in contract_issues
    )
    return value


def validate_repo_relative_contract_path(
    repo_root: Path,
    raw_path: str,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> str | None:
    normalized_path = ensure_repo_relative_path(raw_path, location, issues)
    if not normalized_path:
        return None
    resolved_path = repo_root / normalized_path
    if not resolved_path.exists():
        issues.append(
            ValidationIssue(
                location,
                f"path '{normalized_path}' does not exist",
            )
        )
        return None
    return normalized_path


def validate_comparison_eval_target(
    raw_name: Any,
    *,
    location: str,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> str | None:
    if not isinstance(raw_name, str) or not raw_name:
        issues.append(
            ValidationIssue(location, "comparison target must be a non-empty eval name")
        )
        return None
    if raw_name not in known_eval_names:
        issues.append(
            ValidationIssue(location, f"comparison target '{raw_name}' does not exist")
        )
        return None
    return raw_name


def validate_comparison_surface_contract(
    repo_root: Path,
    bundle_dir: Path,
    manifest: dict[str, Any],
    *,
    known_eval_names: set[str],
    issues: list[ValidationIssue],
) -> None:
    baseline_mode = manifest.get("baseline_mode")
    if baseline_mode == "none":
        return

    location = relative_location(bundle_dir / "eval.yaml", repo_root)
    comparison_surface = manifest.get("comparison_surface")
    if not isinstance(comparison_surface, dict):
        issues.append(
            ValidationIssue(
                location,
                "comparison bundle must define comparison_surface in eval.yaml",
            )
        )
        return

    allowed_keys = COMPARISON_SURFACE_ALLOWED_KEYS.get(baseline_mode, set())
    unexpected_keys = sorted(set(comparison_surface) - allowed_keys)
    if unexpected_keys:
        issues.append(
            ValidationIssue(
                location,
                f"comparison_surface has unexpected keys for baseline_mode '{baseline_mode}': {', '.join(unexpected_keys)}",
            )
        )

    shared_family_path = comparison_surface.get("shared_family_path")
    normalized_shared_family_path = None
    if isinstance(shared_family_path, str):
        normalized_shared_family_path = validate_repo_relative_contract_path(
            repo_root,
            shared_family_path,
            location=f"{location}.comparison_surface.shared_family_path",
            issues=issues,
        )

    paired_readout_path = comparison_surface.get("paired_readout_path")
    normalized_paired_readout_path = None
    if isinstance(paired_readout_path, str):
        normalized_paired_readout_path = validate_repo_relative_contract_path(
            repo_root,
            paired_readout_path,
            location=f"{location}.comparison_surface.paired_readout_path",
            issues=issues,
        )

    integrity_sidecar = comparison_surface.get("integrity_sidecar")
    validate_comparison_eval_target(
        integrity_sidecar,
        location=f"{location}.comparison_surface.integrity_sidecar",
        known_eval_names=known_eval_names,
        issues=issues,
    )

    if baseline_mode in {"fixed-baseline", "previous-version", "longitudinal-window"}:
        validate_comparison_eval_target(
            comparison_surface.get("anchor_surface"),
            location=f"{location}.comparison_surface.anchor_surface",
            known_eval_names=known_eval_names,
            issues=issues,
        )

    if baseline_mode == "peer-compare":
        raw_peer_surfaces = comparison_surface.get("peer_surfaces")
        if not isinstance(raw_peer_surfaces, list):
            issues.append(
                ValidationIssue(
                    f"{location}.comparison_surface.peer_surfaces",
                    "peer_surfaces must be a list",
                )
            )
        else:
            for index, raw_name in enumerate(raw_peer_surfaces):
                validate_comparison_eval_target(
                    raw_name,
                    location=f"{location}.comparison_surface.peer_surfaces[{index}]",
                    known_eval_names=known_eval_names,
                    issues=issues,
                )

    fixture_contract_path = bundle_dir / "fixtures" / "contract.json"
    fixture_contract = eval_catalog_contract.load_optional_json(fixture_contract_path)
    if isinstance(fixture_contract, dict):
        fixture_family_paths = eval_proof_contract_helpers.collect_fixture_family_paths(
            fixture_contract
        )
        fixture_family_path = fixture_family_paths[0] if fixture_family_paths else None
        if (
            isinstance(fixture_family_path, str)
            and normalized_shared_family_path is not None
            and fixture_family_path.replace("\\", "/") != normalized_shared_family_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.shared_family_path must match fixtures/contract.json shared_fixture_family_path",
                )
            )

    runner_contract_path = bundle_dir / "runners" / "contract.json"
    runner_contract = eval_catalog_contract.load_optional_json(runner_contract_path)
    if isinstance(runner_contract, dict):
        paired_readout_paths = eval_proof_contract_helpers.collect_paired_readout_paths(
            runner_contract
        )
        runner_paired_readout_path = (
            paired_readout_paths[0] if paired_readout_paths else None
        )
        if (
            isinstance(runner_paired_readout_path, str)
            and normalized_paired_readout_path is not None
            and runner_paired_readout_path.replace("\\", "/")
            != normalized_paired_readout_path
        ):
            issues.append(
                ValidationIssue(
                    location,
                    "comparison_surface.paired_readout_path must match runners/contract.json paired_readout_path",
                )
            )


__all__ = (
    "COMPARISON_SURFACE_COMMON_KEYS",
    "COMPARISON_SURFACE_ALLOWED_KEYS",
    "ensure_repo_relative_path",
    "validate_repo_relative_contract_path",
    "validate_comparison_eval_target",
    "validate_comparison_surface_contract",
)
