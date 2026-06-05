"""Release-support PR handoff report contract."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from validators.common import ValidationIssue, load_json_payload
from validators.release_support_refs import repo_ref_roots_for_validation
from validators.release_support_report_checks import (
    require_claim_limit_tokens,
    require_joined_list_tokens,
    validate_repo_ref_list,
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
    RELEASE_PREP_PR_HANDOFF_DECISION_NAME,
    RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS,
    RELEASE_PREP_PR_HANDOFF_NAME,
    RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS,
    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
    STRATEGIC_CLOSEOUT_AUDIT_NAME,
)
from validators.release_support_route_tokens import (
    DECISION_RECORDS_README_NAME,
    require_route_tokens,
)
from validators.release_support_routes import (
    RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
    RELEASE_SUPPORT_MECHANIC_README_NAME,
    RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
)


def validate_release_prep_pr_handoff_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = repo_ref_roots_for_validation(repo_root, repo_ref_roots)
    handoff_path = repo_root / RELEASE_PREP_PR_HANDOFF_NAME
    location = RELEASE_PREP_PR_HANDOFF_NAME

    require_route_tokens(
        repo_root,
        issues,
        (
            (RELEASE_PREP_PR_HANDOFF_NAME, RELEASE_PREP_PR_HANDOFF_REQUIRED_TOKENS),
            (RELEASE_PREP_PR_HANDOFF_DECISION_NAME, RELEASE_PREP_PR_HANDOFF_DECISION_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_PR_HANDOFF_PART_README_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "branch", "GitHub evidence", "goal completion"),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    RELEASE_PREP_PR_HANDOFF_NAME,
                    "pre-PR snapshot",
                    "current git and GitHub evidence for live branch, commit, push, PR",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "Release Prep PR Handoff", "snapshot status for branch"),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_AGENTS_NAME,
                (RELEASE_PREP_PR_HANDOFF_NAME, "live PR or GitHub `Repo Validation` state"),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (RELEASE_PREP_PR_HANDOFF_NAME, "goal completion")),
            (DECISION_RECORDS_README_NAME, (RELEASE_PREP_PR_HANDOFF_DECISION_NAME, "live PR status")),
        ),
    )

    payload = load_json_payload(handoff_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "release-prep PR handoff must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "release_prep_pr_handoff",
        "schema_version": 1,
        "handoff_id": "release-prep-pr-handoff-v1",
        "prepared_at": "2026-05-19",
        "scope_kind": "accumulated_strategic_refactor_diff",
        "status_snapshot_kind": "pre_pr_handoff_snapshot",
        "pre_landing_worktree_posture": "dirty_uncommitted_local_diff",
        "source_readiness_audit_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_READINESS_AUDIT_NAME}",
        "source_strategic_closeout_audit_ref": f"repo:aoa-evals/{STRATEGIC_CLOSEOUT_AUDIT_NAME}",
        "decision_ref": f"repo:aoa-evals/{RELEASE_PREP_PR_HANDOFF_DECISION_NAME}",
        "handoff_verdict": "ready_for_owner_landing_route_with_open_pr",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    for key in ("candidate_branch_name", "candidate_commit_message", "candidate_pr_title"):
        value = payload.get(key)
        if not isinstance(value, str) or len(value) < 10:
            issues.append(ValidationIssue(location, f"{key} must be a meaningful string"))

    github_status = payload.get("pre_handoff_github_status")
    if isinstance(github_status, dict):
        for key, expected in {
            "branch_status": "not_created_by_this_handoff",
            "commit_status": "not_created_by_this_handoff",
            "push_status": "not_attempted",
            "pr_status": "not_opened",
            "repo_validation_status": "not_observed_for_this_uncommitted_diff",
            "merge_status": "not_attempted",
            "tag_status": "not_created",
            "github_release_status": "not_published",
        }.items():
            if github_status.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{location}.pre_handoff_github_status",
                        f"pre_handoff {key} must be {expected!r}",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "pre_handoff_github_status must be a JSON object"))

    changed_groups = payload.get("changed_surface_groups")
    if isinstance(changed_groups, list):
        seen_group_ids: set[str] = set()
        for index, group in enumerate(changed_groups):
            group_location = f"{location}.changed_surface_groups[{index}]"
            if not isinstance(group, dict):
                issues.append(ValidationIssue(group_location, "changed surface group must be an object"))
                continue
            group_id = group.get("group_id")
            if isinstance(group_id, str):
                seen_group_ids.add(group_id)
            else:
                issues.append(ValidationIssue(group_location, "group_id must be a string"))
            summary = group.get("summary")
            if not isinstance(summary, str) or len(summary) < 30:
                issues.append(ValidationIssue(group_location, "summary must be a meaningful string"))
            validate_repo_ref_list(
                group.get("evidence_refs"),
                location=f"{group_location}.evidence_refs",
                issues=issues,
                repo_ref_roots=refs,
                strict_sibling_compat=strict_sibling_compat,
            )
        for group_id in sorted(
            {
                "root_design_and_route",
                "decision_memory",
                "roadmap_changelog_quests",
                "proof_topology_legacy_mechanics",
                "active_proof_loop",
                "agent_lane_and_generated_readers",
                "validators_and_tests",
            }
            - seen_group_ids
        ):
            issues.append(ValidationIssue(f"{location}.changed_surface_groups", f"missing group_id {group_id!r}"))
    else:
        issues.append(ValidationIssue(location, "changed_surface_groups must be a list"))

    require_joined_list_tokens(
        payload,
        location=location,
        key="draft_pr_body",
        tokens=(
            "## Summary",
            "## Validation",
            "## Boundaries",
            "python scripts/validate_repo.py",
            "python scripts/release_check.py",
            "no tag or GitHub Release",
            "no live eval-result receipt publication",
            "no runtime evidence acceptance",
            "no sibling repository mutation",
            "goal completion remains open",
        ),
        message_name="draft PR body",
        issues=issues,
    )

    validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py",
            "python -m pytest -q tests/test_generated_route_residue.py",
            ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND,
            MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND,
            ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND,
            ACTIVE_LEGACY_PARENT_WORDING_COMMAND,
            DECISION_ROUTE_RESIDUE_COMMAND,
            REPO_CONFIG_ROUTE_RESIDUE_COMMAND,
            SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND,
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
            "python scripts/validate_repo.py",
            "python scripts/validate_semantic_agents.py",
            "python scripts/validate_nested_agents.py",
            "git diff --check",
            "python scripts/build_catalog.py --check",
            "python scripts/generate_eval_report_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_template_index.py --check",
            "python mechanics/audit/parts/candidate-readers/scripts/generate_runtime_candidate_intake.py --check",
            "python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check",
            "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
            "python -m pytest -q",
            "python scripts/release_check.py",
        },
        issues=issues,
    )

    require_joined_list_tokens(
        payload,
        location=location,
        key="landing_steps",
        tokens=(
            "create a branch",
            "commit the intended accumulated diff",
            "push the branch",
            "open a PR",
            "watch GitHub Repo Validation",
            "merge only after required checks are green",
            "worktree is clean",
            "final owner-visible completion audit",
        ),
        message_name="landing steps",
        issues=issues,
    )
    require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "At the snapshot time",
            "did not create a branch",
            "did not create a commit",
            "did not push",
            "did not open a PR",
            "did not observe GitHub Repo Validation",
            "did not merge",
            "did not publish a release",
            "did not create a tag",
            "did not publish a GitHub Release",
            "did not publish an eval result receipt",
            "did not promote any bundle",
            "did not accept runtime evidence",
            "did not mutate sibling repos",
            "did not mark the goal complete",
            "supersedes this snapshot",
        ),
        issues=issues,
    )
    return issues


__all__ = ("validate_release_prep_pr_handoff_surface",)
