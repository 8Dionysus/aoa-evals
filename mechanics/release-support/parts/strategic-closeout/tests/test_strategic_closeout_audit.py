from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
AUDIT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "strategic-closeout"
    / "reports"
    / "strategic-closeout-audit-v1.json"
)


def load_audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_strategic_closeout_audit_keeps_goal_open() -> None:
    audit = load_audit()

    assert audit["completion_verdict"] == "current_objective_audit_and_landing_route_in_progress_after_mechanics_validation_hardening"
    assert audit["goal_completion_status"] == "not_complete_pending_requirement_audit_and_landing_route"
    assert "does not mark the goal complete" in audit["claim_limit"]
    assert "does not treat PR or GitHub landing alone as objective completion" in audit["claim_limit"]
    assert "does not publish an eval result receipt" in audit["claim_limit"]
    assert "does not mutate sibling repos" in audit["claim_limit"]

    open_items = "\n".join(audit["open_items_before_goal_completion"])
    assert "requirement-by-requirement mechanics objective audit" in open_items
    assert "cross-root evidence clusters" in open_items
    assert "payload coverage anchors" in open_items
    assert "PROVENANCE.md" in open_items
    assert "complete the requested landing route" in open_items
    assert "GitHub Repo Validation" in open_items
    assert "clean worktree" in open_items


def test_strategic_closeout_audit_maps_original_plan_requirements() -> None:
    audit = load_audit()
    requirements = {
        entry["requirement_id"]: entry for entry in audit["requirements_review"]
    }

    assert set(requirements) == {
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
    }
    for entry in requirements.values():
        assert entry["status"] == "satisfied_for_local_refactor"
        assert entry["evidence_refs"]
        assert "claim_limit" in entry

    assert "repo:aoa-evals/docs/PROOF_TOPOLOGY.md" in requirements["phase_4_proof_topology"]["evidence_refs"]
    assert "repo:aoa-evals/mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json" in requirements["release_readiness"]["evidence_refs"]
    assert "repo:aoa-evals/.agents/spark/AGENTS.md" in requirements["spark_agent_lane_cleanup"]["evidence_refs"]


def test_strategic_closeout_audit_names_traps_and_mitigations() -> None:
    audit = load_audit()
    traps = {entry["trap_id"]: entry for entry in audit["trap_review"]}

    assert {
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
    }.issubset(traps)
    assert "candidate-only" in traps["machine_gravity"]["mitigation"]
    assert "provenance" in traps["legacy_permanence"]["mitigation"]


def test_strategic_closeout_audit_lists_verification_snapshot() -> None:
    audit = load_audit()
    commands = {entry["command"]: entry for entry in audit["verification_snapshot"]}

    for command in (
        "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py tests/test_validate_repo.py -k strategic_closeout",
        "python -m pytest -q tests/test_validate_repo.py -k generated_route_residue",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_readme_contract",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_payload_inventory",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_part_validation_command",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_parts_index_sync",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_legacy_single_bridge",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_bridge_posture",
        "python -m pytest -q tests/test_validate_repo.py -k legacy_naming_single_bridge_language",
        "python -m pytest -q tests/test_validate_repo.py -k active_legacy_parent_wording",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_root_district_recon",
        "python -m pytest -q tests/test_validate_repo.py -k root_authored_surface_classification",
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
    ):
        assert commands[command]["result"] == "passed"

    assert "payload coverage anchors" in commands["python -m pytest -q tests/test_validate_repo.py -k mechanic_part_validation_command"]["claim_limit"]
    assert "not receipt or verdict authority" in commands["python scripts/generate_eval_report_index.py --check"]["claim_limit"]
