"""Release-support readiness audit report contract."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from validators.common import ValidationIssue, load_json_payload
from validators.release_support_refs import repo_ref_roots_for_validation
from validators.release_support_report_checks import (
    require_claim_limit_tokens,
    require_joined_list_tokens,
    validate_required_object_ids,
    validate_verification_snapshot,
)
from validators.release_support_report_commands import (
    ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
    ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
    DECISION_ROUTE_RESIDUE_COMMAND,
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
    MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
    MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
    MECHANIC_PARENT_DIRECTION_COMMAND,
    MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
    MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
    MECHANIC_PARTS_INDEX_SYNC_COMMAND,
    MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
    MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
    MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
    REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
    ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
    ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
    SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
)
from validators.release_support_report_constants import (
    RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME,
    RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS,
    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
    RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS,
)
from validators.release_support_route_tokens import (
    DECISION_RECORDS_README_NAME,
    require_route_tokens,
)
from validators.release_support_routes import (
    RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
    RELEASE_SUPPORT_MECHANIC_README_NAME,
    RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
)


def validate_release_support_readiness_audit_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = repo_ref_roots_for_validation(repo_root, repo_ref_roots)
    audit_path = repo_root / RELEASE_SUPPORT_READINESS_AUDIT_NAME
    location = RELEASE_SUPPORT_READINESS_AUDIT_NAME

    require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_SUPPORT_READINESS_AUDIT_NAME, RELEASE_SUPPORT_READINESS_AUDIT_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME,
                RELEASE_SUPPORT_READINESS_AUDIT_DECISION_REQUIRED_TOKENS,
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "Readiness Audit",
                    "GitHub Release evidence",
                    "GitHub `Repo Validation`",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
                (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "readiness audits", "GitHub `Repo Validation`"),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "local release-prep reviewability evidence",
                    "current git, GitHub, tag, release, PR, and objective evidence",
                ),
            ),
            (
                RELEASE_SUPPORT_READINESS_AUDIT_PART_README_NAME,
                (
                    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
                    "GitHub PR approval and Repo Validation",
                    "current goal review",
                ),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (RELEASE_SUPPORT_READINESS_AUDIT_NAME, "goal completion")),
            (
                DECISION_RECORDS_README_NAME,
                (RELEASE_SUPPORT_READINESS_AUDIT_DECISION_NAME, "release-prep PR handoff"),
            ),
        ),
    )

    payload = load_json_payload(audit_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "release-support readiness audit must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "release_support_readiness_audit",
        "schema_version": 1,
        "audit_id": "release-support-readiness-audit-v1",
        "audited_at": "2026-05-19",
        "scope_kind": "accumulated_strategic_refactor_diff",
        "readiness_verdict": "local_release_prep_review_ready_with_open_landing",
        "changelog_anchor_ref": "repo:aoa-evals/CHANGELOG.md",
        "release_support_mechanic_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_MECHANIC_README_NAME}",
        "release_check_ref": "repo:aoa-evals/scripts/release_check.py",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    release_scope = payload.get("release_scope")
    if not isinstance(release_scope, str):
        issues.append(ValidationIssue(location, "release_scope must be a string"))
    else:
        for token in (
            "Unreleased",
            "strategic refactor",
            "root design",
            "proof topology",
            "proof-loop reports",
            "receipt-intake dry review",
            "validators",
        ):
            if token not in release_scope:
                issues.append(ValidationIssue(location, f"release_scope must mention '{token}'"))

    validate_required_object_ids(
        payload.get("requirements_review"),
        location=f"{location}.requirements_review",
        id_key="requirement_id",
        required_ids={
            "root_design_spine",
            "decision_memory",
            "roadmap_quest_and_lifecycle_route",
            "proof_topology_legacy_and_mechanics",
            "proof_loop_materialization",
            "generated_reader_freshness",
            "local_release_gate_coverage",
            "sibling_boundary_and_canary",
        },
        status_value="ready_for_release_prep_review",
        min_claim_limit_length=20,
        issues=issues,
        repo_ref_roots=refs,
        strict_sibling_compat=strict_sibling_compat,
    )

    validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
            MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND,
            MECHANIC_PART_VALIDATION_COMMAND_COMMAND,
            MECHANIC_PARTS_INDEX_SYNC_COMMAND,
            MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND,
            MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND,
            LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND,
            "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
            MECHANIC_PARENT_DIRECTION_COMMAND,
            MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND,
            MECHANIC_ROOT_DISTRICT_RECON_COMMAND,
            ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND,
            ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
            ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
            ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
            DECISION_ROUTE_RESIDUE_COMMAND,
            REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
            SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python scripts/validate_nested_agents.py",
            "python scripts/build_catalog.py --check",
            "python scripts/generate_eval_report_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
            "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
            "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
            "python -m pytest -q",
            "python scripts/release_check.py",
            "git diff --check",
        },
        issues=issues,
    )

    publication_boundary = payload.get("publication_boundary")
    if isinstance(publication_boundary, dict):
        expected_boundary_values = {
            "release_publication_status": "not_published",
            "tag_status": "not_created",
            "github_release_status": "not_published",
            "github_pr_status": "not_opened",
            "github_repo_validation_status": "not_observed_for_this_uncommitted_diff",
            "goal_completion_status": "not_complete",
            "live_receipt_publication_status": "not_attempted",
        }
        for key, expected in expected_boundary_values.items():
            if publication_boundary.get(key) != expected:
                issues.append(ValidationIssue(f"{location}.publication_boundary", f"{key} must be {expected!r}"))
        boundary = publication_boundary.get("boundary")
        if not isinstance(boundary, str):
            issues.append(ValidationIssue(f"{location}.publication_boundary", "boundary must be a string"))
        else:
            for token in (
                "not a release",
                "not a tag",
                "not GitHub Repo Validation",
                "not a GitHub Release",
                "not PR approval",
                "not an eval result receipt",
                "not goal completion",
            ):
                if token not in boundary:
                    issues.append(
                        ValidationIssue(
                            f"{location}.publication_boundary.boundary",
                            f"boundary must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(location, "publication_boundary must be a JSON object"))

    require_joined_list_tokens(
        payload,
        location=location,
        key="open_requirements_before_publication",
        tokens=(
            "review the accumulated diff",
            "open a PR",
            "observe GitHub Repo Validation",
            "merge only after required checks are green",
            "create any tag or GitHub Release only after",
            "goal completion audit",
        ),
        message_name="open requirements",
        issues=issues,
    )
    require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "does not publish a release",
            "create a tag",
            "open or approve a PR",
            "observe GitHub Repo Validation",
            "publish an eval result receipt",
            "mutate sibling repos",
            "mark the aoa-evals strategic goal complete",
        ),
        issues=issues,
    )
    return issues


__all__ = ("validate_release_support_readiness_audit_surface",)
