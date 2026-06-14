"""Release-support strategic closeout audit report contract."""

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
    RELEASE_SUPPORT_READINESS_AUDIT_NAME,
    STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME,
    STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS,
    STRATEGIC_CLOSEOUT_AUDIT_NAME,
    STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS,
)
from validators.release_support_route_tokens import (
    DECISION_RECORDS_README_NAME,
    require_route_tokens,
)
from validators.release_support_routes import (
    RELEASE_SUPPORT_MECHANIC_README_NAME,
    RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
)


def validate_strategic_closeout_audit_surface(
    repo_root: Path,
    *,
    repo_ref_roots: Mapping[str, Path] | None = None,
    strict_sibling_compat: bool = False,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    refs = repo_ref_roots_for_validation(repo_root, repo_ref_roots)
    audit_path = repo_root / STRATEGIC_CLOSEOUT_AUDIT_NAME
    location = STRATEGIC_CLOSEOUT_AUDIT_NAME

    require_route_tokens(
        repo_root,
        issues,
        (
            (STRATEGIC_CLOSEOUT_AUDIT_NAME, STRATEGIC_CLOSEOUT_AUDIT_REQUIRED_TOKENS),
            (STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME, STRATEGIC_CLOSEOUT_AUDIT_DECISION_REQUIRED_TOKENS),
            (
                RELEASE_SUPPORT_STRATEGIC_CLOSEOUT_PART_README_NAME,
                (
                    STRATEGIC_CLOSEOUT_AUDIT_NAME,
                    "goal open",
                    "GitHub `Repo Validation`",
                    "current objective audit",
                ),
            ),
            (
                "docs/operations/RELEASING.md",
                (
                    STRATEGIC_CLOSEOUT_AUDIT_NAME,
                    "requirement-by-requirement handoff evidence",
                    "current objective audit and landing evidence",
                ),
            ),
            (
                RELEASE_SUPPORT_MECHANIC_README_NAME,
                (STRATEGIC_CLOSEOUT_AUDIT_NAME, "Strategic Closeout Audit", "Goal completion routes"),
            ),
            ("ROADMAP.md", ("Release-support posture", "mechanics/release-support/README.md")),
            ("CHANGELOG.md", (STRATEGIC_CLOSEOUT_AUDIT_NAME, "goal completion")),
            (DECISION_RECORDS_README_NAME, (STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME, "Goal completion")),
        ),
    )

    payload = load_json_payload(audit_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "strategic closeout audit must be a JSON object"))
        return issues

    expected_top_level = {
        "artifact_kind": "strategic_closeout_audit",
        "schema_version": 1,
        "audit_id": "strategic-closeout-audit-v1",
        "audited_at": "2026-05-19",
        "scope_kind": "local_strategic_refactor_diff",
        "completion_verdict": "current_objective_audit_and_landing_route_in_progress_after_mechanics_validation_hardening",
        "goal_completion_status": "not_complete_pending_requirement_audit_and_landing_route",
        "release_support_readiness_audit_ref": f"repo:aoa-evals/{RELEASE_SUPPORT_READINESS_AUDIT_NAME}",
        "decision_ref": f"repo:aoa-evals/{STRATEGIC_CLOSEOUT_AUDIT_DECISION_NAME}",
        "current_objective_ref": (
            "thread goal: deep mechanics refactor as proof-side organ with evidence-derived parent map, "
            "part contracts, active-first legacy, and source-of-truth validation"
        ),
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    source_plan_ref = payload.get("source_plan_ref")
    if not isinstance(source_plan_ref, str):
        issues.append(ValidationIssue(location, "source_plan_ref must be a string"))
    else:
        for token in ("operator working note", "outside the repository"):
            if token not in source_plan_ref:
                issues.append(ValidationIssue(location, f"source_plan_ref must mention '{token}'"))
        if "/home/" in source_plan_ref:
            issues.append(ValidationIssue(location, "source_plan_ref must not expose an absolute host path"))

    validate_required_object_ids(
        payload.get("requirements_review"),
        location=f"{location}.requirements_review",
        id_key="requirement_id",
        required_ids={
            "meta_truth_and_positive_boundary",
            "codex_maxxing_durable_loop",
            "aoa_law_and_sibling_meta_examples",
            "phase_0_truth_map",
            "phase_1_root_design_spine",
            "phase_2_decision_lane",
            "phase_3_roadmap_changelog_questbook_quests",
            "phase_4_proof_topology",
            "phase_5_mechanics_atlas_and_packages",
            "phase_6_legacy_provenance",
            "phase_7_validator_invariants",
            "phase_8_active_proof_loop",
            "runtime_machine_boundary",
            "spark_agent_lane_cleanup",
            "release_readiness",
            "trap_audit_and_completion_boundary",
        },
        status_value="satisfied_for_local_refactor",
        min_claim_limit_length=40,
        issues=issues,
        repo_ref_roots=refs,
        strict_sibling_compat=strict_sibling_compat,
    )

    trap_review = payload.get("trap_review")
    if isinstance(trap_review, list):
        seen_trap_ids: set[str] = set()
        for index, trap in enumerate(trap_review):
            trap_location = f"{location}.trap_review[{index}]"
            if not isinstance(trap, dict):
                issues.append(ValidationIssue(trap_location, "trap entry must be an object"))
                continue
            trap_id = trap.get("trap_id")
            if isinstance(trap_id, str):
                seen_trap_ids.add(trap_id)
            else:
                issues.append(ValidationIssue(trap_location, "trap_id must be a string"))
            mitigation = trap.get("mitigation")
            if not isinstance(mitigation, str) or len(mitigation) < 40:
                issues.append(ValidationIssue(trap_location, "mitigation must be a meaningful string"))
        for trap_id in sorted(
            {
                "durable_note_trap",
                "root_design_overreach",
                "decision_lane_ceremony",
                "questbook_gravity",
                "mechanics_explosion",
                "sibling_compatibility_swamp",
                "machine_gravity",
                "positive_boundary_erosion",
                "legacy_permanence",
                "validation_theatre",
                "release_check_spiral",
                "active_use_premature_connection",
            }
            - seen_trap_ids
        ):
            issues.append(ValidationIssue(f"{location}.trap_review", f"missing trap_id {trap_id!r}"))
    else:
        issues.append(ValidationIssue(location, "trap_review must be a list"))

    validate_verification_snapshot(
        payload,
        location=location,
        required_commands={
            "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py",
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
        key="open_items_before_goal_completion",
        tokens=(
            "requirement-by-requirement mechanics objective audit",
            "cross-root evidence clusters",
            "payload coverage anchors",
            "PROVENANCE.md",
            "old names",
            "full local validation battery",
            "requested landing route",
            "GitHub Repo Validation",
            "clean worktree",
        ),
        message_name="open items",
        issues=issues,
    )
    require_claim_limit_tokens(
        payload,
        location=location,
        tokens=(
            "does not mark the goal complete",
            "does not treat PR or GitHub landing alone as objective completion",
            "does not publish a release",
            "does not create a tag",
            "does not publish a GitHub Release",
            "does not publish an eval result receipt",
            "does not promote any bundle",
            "does not accept runtime evidence",
            "does not mutate sibling repos",
        ),
        issues=issues,
    )
    return issues


__all__ = ("validate_strategic_closeout_audit_surface",)
