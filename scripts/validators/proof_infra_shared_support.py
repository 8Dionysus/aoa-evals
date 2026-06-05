"""Shared proof-infra guide and support-contract exercise checks."""

from __future__ import annotations

from pathlib import Path

import eval_catalog_contract
import eval_proof_contract_helpers

from validators import proof_infra_common as common
from validators.common import ValidationIssue, read_text_or_issue


def validate_shared_proof_infra_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    fixture_relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
    }
    runner_relevant_names = fixture_relevant_names | {
        "aoa-longitudinal-growth-snapshot",
    }
    relevant_names = fixture_relevant_names | runner_relevant_names
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(repo_root / common.SHARED_PROOF_INFRA_GUIDE_NAME, issues, root=repo_root)
    docs_readme_text = read_text_or_issue(repo_root / "docs" / "README.md", issues, root=repo_root)
    fixtures_agents_text = read_text_or_issue(repo_root / "fixtures" / "AGENTS.md", issues, root=repo_root)
    reports_agents_text = read_text_or_issue(repo_root / "reports" / "AGENTS.md", issues, root=repo_root)
    runner_surface_text = read_text_or_issue(
        repo_root / common.PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
        issues,
        root=repo_root,
    )

    if "Shared Proof Infra Guide" not in docs_readme_text:
        issues.append(ValidationIssue("docs/README.md", "docs/README.md must list Shared Proof Infra Guide"))
    for phrase in (
        "additional_shared_fixture_family_paths",
        "additional_paired_readout_paths",
        "shared_fixture_family_path",
        "paired_readout_path",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(common.SHARED_PROOF_INFRA_GUIDE_NAME, f"shared proof infra guide must mention '{phrase}'")
            )

    if "additional_shared_fixture_family_paths" not in fixtures_agents_text:
        issues.append(
            ValidationIssue(
                "fixtures/AGENTS.md",
                "fixtures/AGENTS.md must describe additional_shared_fixture_family_paths",
            )
        )
    if "additional_paired_readout_paths" not in reports_agents_text:
        issues.append(
            ValidationIssue(
                "reports/AGENTS.md",
                "reports/AGENTS.md must describe additional_paired_readout_paths",
            )
        )
    if "additional_paired_readout_paths" not in runner_surface_text:
        issues.append(
            ValidationIssue(
                common.PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME,
                (
                    f"{common.PROOF_INFRA_REPORTABLE_CONTRACTS_RUNNER_SURFACE_NAME} "
                    "must describe additional_paired_readout_paths"
                ),
            )
        )

    fixture_bundle_names = (
        selected_evals.intersection(fixture_relevant_names)
        if selected_evals is not None
        else fixture_relevant_names
    )
    runner_bundle_names = (
        selected_evals.intersection(runner_relevant_names)
        if selected_evals is not None
        else runner_relevant_names
    )
    fixture_contracts_with_additional = 0
    runner_contracts_with_additional = 0
    for name in fixture_bundle_names:
        fixture_payload = eval_catalog_contract.load_optional_json(
            common.source_eval_dir(repo_root, name) / "fixtures" / "contract.json"
        )
        fixture_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            fixture_payload if isinstance(fixture_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_FIXTURE_FAMILY_PATHS_KEY,
        )
        if fixture_paths:
            fixture_contracts_with_additional += 1
    for name in runner_bundle_names:
        runner_payload = eval_catalog_contract.load_optional_json(
            common.source_eval_dir(repo_root, name) / "runners" / "contract.json"
        )
        runner_paths = eval_proof_contract_helpers.normalize_repo_relative_path_list(
            runner_payload if isinstance(runner_payload, dict) else {},
            eval_proof_contract_helpers.ADDITIONAL_PAIRED_READOUT_PATHS_KEY,
        )
        if runner_paths:
            runner_contracts_with_additional += 1

    minimum_fixture_count = 1 if selected_evals is not None and fixture_bundle_names else 2
    minimum_runner_count = 1 if selected_evals is not None and runner_bundle_names else 2
    if fixture_bundle_names and fixture_contracts_with_additional < minimum_fixture_count:
        issues.append(
            ValidationIssue(
                "fixtures/README.md",
                "shared proof infra must be exercised by fixture contracts in more than one bundle family",
            )
        )
    if runner_bundle_names and runner_contracts_with_additional < minimum_runner_count:
        issues.append(
            ValidationIssue(
                "reports/README.md",
                "shared proof infra must be exercised by runner contracts in more than one bundle family",
            )
        )
    return issues
