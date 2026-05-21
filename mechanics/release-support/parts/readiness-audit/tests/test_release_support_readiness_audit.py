from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
AUDIT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "readiness-audit"
    / "reports"
    / "release-support-readiness-audit-v1.json"
)


def load_audit() -> dict:
    return json.loads(AUDIT_PATH.read_text(encoding="utf-8"))


def test_release_support_readiness_audit_keeps_publication_open() -> None:
    audit = load_audit()
    boundary = audit["publication_boundary"]

    assert audit["readiness_verdict"] == "local_release_prep_review_ready_with_open_landing"
    assert boundary["release_publication_status"] == "not_published"
    assert boundary["tag_status"] == "not_created"
    assert boundary["github_release_status"] == "not_published"
    assert boundary["github_pr_status"] == "not_opened"
    assert boundary["github_repo_validation_status"] == "not_observed_for_this_uncommitted_diff"
    assert boundary["goal_completion_status"] == "not_complete"
    assert boundary["live_receipt_publication_status"] == "not_attempted"
    assert "not a release" in boundary["boundary"]
    assert "not goal completion" in boundary["boundary"]


def test_release_support_readiness_audit_maps_required_strategic_surfaces() -> None:
    audit = load_audit()
    requirements = {
        entry["requirement_id"]: entry for entry in audit["requirements_review"]
    }

    assert set(requirements) == {
        "root_design_spine",
        "decision_memory",
        "roadmap_quest_and_lifecycle_route",
        "proof_topology_legacy_and_mechanics",
        "proof_loop_materialization",
        "generated_reader_freshness",
        "local_release_gate_coverage",
        "sibling_boundary_and_canary",
    }
    for entry in requirements.values():
        assert entry["status"] == "ready_for_release_prep_review"
        assert entry["evidence_refs"]
        assert "claim_limit" in entry

    proof_loop_refs = requirements["proof_loop_materialization"]["evidence_refs"]
    assert "repo:aoa-evals/mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json" in proof_loop_refs
    assert "repo:aoa-evals/generated/eval_report_index.min.json" in proof_loop_refs


def test_release_support_readiness_audit_lists_local_gates_and_limits() -> None:
    audit = load_audit()
    commands = {entry["command"]: entry for entry in audit["verification_snapshot"]}

    for command in (
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
        "python scripts/build_catalog.py --check",
        "python scripts/generate_eval_report_index.py --check",
        "python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json",
        "python -m pytest -q",
        "python scripts/release_check.py",
        "git diff --check",
    ):
        assert commands[command]["result"] == "passed"

    assert "does not publish a release" in audit["claim_limit"]
    assert "mark the aoa-evals strategic goal complete" in audit["claim_limit"]
