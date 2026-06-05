from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import release_support_report_constants as release_support_report_constants_validator
from validators import release_support_strategic_closeout_report as release_support_strategic_closeout_report_validator

REPO_REF_ROOTS = {
    "aoa-evals": REPO_ROOT,
    "aoa-techniques": REPO_ROOT.parent / "aoa-techniques",
    "aoa-skills": REPO_ROOT.parent / "aoa-skills",
    "aoa-agents": REPO_ROOT.parent / "aoa-agents",
    "aoa-playbooks": REPO_ROOT.parent / "aoa-playbooks",
    "aoa-memo": REPO_ROOT.parent / "aoa-memo",
    "aoa-routing": REPO_ROOT.parent / "aoa-routing",
    "aoa-kag": REPO_ROOT.parent / "aoa-kag",
    "aoa-sdk": REPO_ROOT.parent / "aoa-sdk",
    "aoa-stats": REPO_ROOT.parent / "aoa-stats",
    "abyss-stack": REPO_ROOT.parent / "abyss-stack",
}

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


def write_json_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def make_strategic_closeout_audit_surface(repo_root: Path) -> Path:
    copy_repo_text(repo_root, release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME)
    return repo_root / release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME


def validate_strategic_closeout_audit_surface(repo_root: Path):
    return release_support_strategic_closeout_report_validator.validate_strategic_closeout_audit_surface(
        repo_root,
        repo_ref_roots=REPO_REF_ROOTS,
        strict_sibling_compat=False,
    )


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

    assert "repo:aoa-evals/docs/architecture/PROOF_TOPOLOGY.md" in requirements["phase_4_proof_topology"]["evidence_refs"]
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
        "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py",
        "python -m pytest -q tests/test_generated_route_residue.py",
        "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_readme_contract",
        "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory",
        "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command",
        "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync",
        "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge",
        "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture",
        "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language",
        "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording",
        "python -m pytest -q tests/test_validate_repo.py -k mechanic_provenance_entry",
        "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon",
        "python -m pytest -q tests/test_mechanics_topology.py",
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

    assert "payload coverage anchors" in commands["python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command"]["claim_limit"]
    assert "not receipt or verdict authority" in commands["python scripts/generate_eval_report_index.py --check"]["claim_limit"]


def test_strategic_closeout_audit_surface_validates_current_route() -> None:
    assert validate_strategic_closeout_audit_surface(REPO_ROOT) == []


def test_strategic_closeout_audit_rejects_goal_completion_claim(
    tmp_path: Path,
) -> None:
    audit_path = make_strategic_closeout_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["goal_completion_status"] = "complete"
    write_json_payload(audit_path, payload)

    issues = validate_strategic_closeout_audit_surface(tmp_path)

    assert any(
        issue.location == release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME
        and "goal_completion_status must be 'not_complete_pending_requirement_audit_and_landing_route'"
        in issue.message
        for issue in issues
    )


def test_strategic_closeout_audit_rejects_missing_requirement_id(
    tmp_path: Path,
) -> None:
    audit_path = make_strategic_closeout_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["requirements_review"] = [
        entry
        for entry in payload["requirements_review"]
        if entry["requirement_id"] != "phase_8_active_proof_loop"
    ]
    write_json_payload(audit_path, payload)

    issues = validate_strategic_closeout_audit_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME}.requirements_review"
        and "phase_8_active_proof_loop" in issue.message
        for issue in issues
    )


def test_strategic_closeout_audit_rejects_missing_focused_gate(
    tmp_path: Path,
) -> None:
    audit_path = make_strategic_closeout_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["verification_snapshot"] = [
        entry
        for entry in payload["verification_snapshot"]
        if entry["command"]
        != "python -m pytest -q mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py"
    ]
    write_json_payload(audit_path, payload)

    issues = validate_strategic_closeout_audit_surface(tmp_path)

    assert any(
        issue.location == f"{release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME}.verification_snapshot"
        and "mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py"
        in issue.message
        for issue in issues
    )


def test_strategic_closeout_audit_rejects_absolute_plan_path(
    tmp_path: Path,
) -> None:
    audit_path = make_strategic_closeout_audit_surface(tmp_path)
    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    payload["source_plan_ref"] = "/home/dionysus/private-note.md"
    write_json_payload(audit_path, payload)

    issues = validate_strategic_closeout_audit_surface(tmp_path)

    assert any(
        issue.location == release_support_report_constants_validator.STRATEGIC_CLOSEOUT_AUDIT_NAME
        and "must not expose an absolute host path" in issue.message
        for issue in issues
    )
