from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_eval_readiness_dashboard as readiness


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_repo(workspace: Path, relative_path: str) -> Path:
    repo_root = workspace / relative_path
    git_dir = repo_root / ".git"
    git_dir.mkdir(parents=True)
    write_text(git_dir / "HEAD", "ref: refs/heads/main\n")
    return repo_root


def make_port(repo_root: Path, *, status: str = "active") -> None:
    write_text(
        repo_root / "evals" / "PORT.yaml",
        f"""
        schema_version: local_eval_port_v1
        owner_repo: {repo_root.name}
        status: {status}
        proof_owner_repo: aoa-evals
        default_intake_schema: eval_need_v1
        local_role: repo-local eval pressure, fixtures, suites, and reports
        central_boundary: no verdict, scoring, regression, or proof doctrine authority
        """,
    )
    write_text(
        repo_root / "evals" / "README.md",
        """
        # Local Eval Port

        `aoa-evals` owns central verdict, scoring, regression, and proof doctrine
        authority.
        """,
    )
    write_text(
        repo_root / "evals" / "AGENTS.md",
        """
        # AGENTS.md

        Route verdict, scoring, regression, and proof doctrine authority to `aoa-evals`.
        """,
    )
    write_text(repo_root / "evals" / "intake" / "README.md", "# Intake\n")
    write_text(repo_root / "evals" / "suites" / "README.md", "# Suites\n")
    write_text(repo_root / "evals" / "reports" / "README.md", "# Reports\n")


def write_valid_intake(repo_root: Path) -> None:
    payload = {
        "schema_version": "eval_need_v1",
        "name": "aoa-readiness-route-pressure",
        "proof_question": "Does local pressure route before central proof adoption?",
        "origin_need": "A repo-local eval pressure packet needs a route.",
        "summary": "Checks whether local pressure stays below proof authority.",
        "object_under_evaluation": "local eval readiness route",
        "category": "boundary",
        "claim_type": "bounded",
        "baseline_mode": "none",
        "report_format": "summary-with-breakdown",
        "verdict_shape": "categorical",
        "authoring_route": "candidate_evidence_packet",
        "expected_use_when": ["local eval pressure appears"],
        "blind_spot_notes": ["does not accept a central proof verdict"],
        "candidate_evidence_refs": ["evals/README.md"],
        "source_refs": ["evals/README.md"],
    }
    write_text(
        repo_root / "evals" / "intake" / "aoa-readiness-route-pressure.eval_need.json",
        json.dumps(payload, indent=2) + "\n",
    )


def test_dashboard_builds_living_readmodel_without_live_checks(tmp_path: Path) -> None:
    workspace = tmp_path / "AbyssOS"
    repo = make_repo(workspace, "aoa-routing")
    make_port(repo)
    write_valid_intake(repo)

    dashboard, support = readiness.build_dashboard(
        evals_root=REPO_ROOT,
        workspace_root=workspace,
        aoa_root=tmp_path / ".aoa",
        skills_source_root=tmp_path / "aoa-skills",
        installed_skills_root=tmp_path / "skills",
        stack_root=None,
        include_live_checks=False,
        live_timeout=1,
        observed_at_utc="2026-06-25T00:00:00Z",
    )

    assert dashboard["schema_version"] == readiness.SCHEMA_VERSION
    assert dashboard["read_model_posture"] == {
        "can_route": True,
        "can_score": False,
        "can_accept_proof": False,
        "can_promote_candidates": False,
        "can_mutate_sibling_repos": False,
    }
    assert dashboard["local_eval_ports"]["summary"]["active"] == 1
    assert dashboard["mcp_runtime_status"]["status"] == "skipped"
    assert dashboard["aoa_session_memory_freshness"]["status"] == "skipped"
    assert dashboard["repo_readiness"]["summary"]["actionable_repos"] == 1
    routing_repo = {
        item["repo_id"]: item for item in dashboard["repo_readiness"]["repos"]
    }["aoa-routing"]
    assert routing_repo["route_state"] == "needs_local_design_or_owner_review"
    assert routing_repo["pressure_severity"] == "low"
    assert "build_local_eval_port_inventory.py" in routing_repo["exact_next_command"]
    assert len(dashboard["trigger_criteria"]["taxonomy"]) >= 8
    assert "central_proof_promotion" in dashboard["trigger_criteria"]["sample_packet_schema"]["forbidden_effects"]
    session_status = dashboard["trigger_criteria"]["session_mining_status"]
    assert session_status["status"] == "manual_review_packetized"
    assert session_status["reviewed_count"] >= 20
    assert "candidate evidence only" in session_status["candidate_only_boundary"]
    assert dashboard["candidate_queue"]["summary"]["entries"] >= 2
    assert dashboard["candidate_queue"]["summary"]["packet_count"] >= 5
    assert dashboard["candidate_queue"]["summary"]["session_packet_count"] >= 5
    assert {
        "local-port:aoa-routing",
        "packet:session:aoa-eval-keyword-mining-blindspot",
    }.issubset({entry["candidate_id"] for entry in dashboard["candidate_queue"]["entries"]})
    forge = dashboard["eval_forge_readiness"]
    assert forge["schema_version"] == "os_abyss_eval_forge_readiness_v1"
    assert forge["registry_validation"]["valid"] is True
    assert forge["archetype_count"] >= 18
    assert "aoa-skills-trigger-eval" in forge["archetype_ids"]
    keyword_hint = {
        item["candidate_id"]: item for item in forge["candidate_archetype_hints"]
    }["packet:session:aoa-eval-keyword-mining-blindspot"]
    assert keyword_hint["selected_archetype_id"] == "aoa-skills-trigger-eval"
    assert keyword_hint["promotion_allowed"] is False
    assert dashboard["local_to_central_promotion_path"]["forbidden_shortcuts"]
    assert dashboard["freshness_sentinel"]["tracked_dimensions"]
    assert [item["phase"] for item in dashboard["phase_coverage"]] == list(range(1, 11))

    assert support["schema_version"] == readiness.SUPPORT_REGISTRY_SCHEMA_VERSION
    assert support["summary"]["total_surfaces"] > 0
    assert support["summary"]["eval_lane_relevant"] > 0
    assert "by_semantic_class" in support["summary"]
    assert "by_review_status" in support["summary"]


def test_aoa_freshness_extracts_actionable_json_summary(monkeypatch, tmp_path: Path) -> None:
    script = tmp_path / ".aoa" / "scripts" / "aoa_session_memory.py"
    script.parent.mkdir(parents=True)
    script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    payload = {
        "ok": True,
        "recommendation": "run_live_catchup",
        "exact_next_command": "python3 scripts/aoa_session_memory.py index-maintenance target",
        "route": {"status": "current"},
        "agent_route": {
            "action": "run_live_catchup_for_recent_live",
            "can_use_graph_search": True,
            "maintenance_required": True,
            "live_catchup_pending": True,
        },
        "live_tail": {
            "status": "ready_for_catchup",
            "ready_count": 1,
            "waiting_count": 1,
            "next_ready_at": "2026-06-25T22:22:53Z",
        },
        "next_actions": [
            {"id": "run_live_catchup", "reason": "deferred_live_ready_for_bounded_catchup"}
        ],
        "diagnostics": [],
    }

    monkeypatch.setattr(
        readiness,
        "run_command",
        lambda *args, **kwargs: {
            "status": "ok",
            "returncode": 0,
            "stdout": json.dumps(payload),
            "stderr": "",
        },
    )

    result = readiness.build_aoa_freshness(script.parents[1], include_live_checks=True, timeout=1)

    assert result["status"] == "ok"
    assert result["next_route"] == payload["exact_next_command"]
    assert result["json_summary"]["recommendation"] == "run_live_catchup"
    assert result["json_summary"]["next_action_id"] == "run_live_catchup"
    assert result["json_summary"]["live_tail_status"] == "ready_for_catchup"


def test_skill_pack_profile_verification_summarizes_installed_foundation(tmp_path: Path) -> None:
    skills_source_root = tmp_path / "aoa-skills"
    installed_skills_root = tmp_path / "skills"
    verifier = skills_source_root / "scripts" / "verify_skill_pack.py"
    verifier.parent.mkdir(parents=True)
    write_text(
        verifier,
        """
        import json

        print(json.dumps({
            "verified": True,
            "profile_revision": "rev-1",
            "expected_skill_count": 36,
            "verified_skill_count": 36,
            "missing_skills": [],
            "mismatched_skills": [],
            "extra_skill_dirs": [".system"],
            "release_identity": {"has_unreleased_changes": True},
            "skills": [
                {
                    "name": "aoa-eval",
                    "install_state": "ok",
                    "is_symlink": True,
                    "source_digest": "src",
                    "target_digest": "src"
                }
            ]
        }))
        """,
    )

    result = readiness.build_skill_pack_profile_verification(
        skills_source_root,
        installed_skills_root,
        timeout=1,
    )

    assert result["status"] == "ok"
    assert result["verified"] is True
    assert result["expected_skill_count"] == 36
    assert result["verified_skill_count"] == 36
    assert result["missing_skill_count"] == 0
    assert result["mismatched_skill_count"] == 0
    assert result["aoa_eval_install_state"] == "ok"
    assert result["aoa_eval_is_symlink"] is True
    assert result["authority_boundary"].startswith("aoa-skills owns")


def test_support_registry_maps_readiness_builder_after_inventory_registration() -> None:
    support = readiness.build_support_registry(REPO_ROOT)
    entries = {entry["path"]: entry for entry in support["surfaces"]}

    entry = entries["scripts/build_eval_readiness_dashboard.py"]
    assert entry["classification"] == "builder_with_check_mode"
    assert entry["eval_lane_relevant"] is True
    assert entry["recommended_route"] == "run_check_mode_before_eval_support"
    assert entry["semantic_class"] == "generated_parity_check"
    assert entry["safe_to_apply_directly"] is False
    assert entry["lane"] == "advisory"


def test_support_registry_marks_write_script_without_guard_as_not_eval_apply() -> None:
    raw = {
        "path": "scripts/mutate_everything.py",
        "family": "maintenance_script",
        "owner_surface": "scripts/AGENTS.md",
        "side_effects": "writes tracked state",
        "writes": ["generated/state.json"],
        "validation_lane": "advisory",
    }

    semantic = readiness.semantic_support_classification("script", raw, relevant=True)

    assert semantic["semantic_class"] == "unsafe_side_effect_script"
    assert semantic["review_status"] == "reviewed_forbidden"
    assert semantic["recommended_route"] == "forbidden_as_eval_apply_until_manual_owner_review"
    assert semantic["safe_to_apply_directly"] is False
    assert "apply_as_deterministic_eval_support" in semantic["forbidden_interpretations"]
    assert "direct eval application is forbidden" in semantic["review_reason"]


def test_support_registry_has_no_unresolved_eval_relevant_manual_review() -> None:
    support = readiness.build_support_registry(REPO_ROOT)
    unresolved = [
        entry
        for entry in support["surfaces"]
        if entry["eval_lane_relevant"] and entry["review_status"] == "manual_review_required"
    ]

    assert unresolved == []
    assert support["summary"]["by_review_status"].get("manual_review_required", 0) == 0
    assert support["summary"]["by_review_status"]["reviewed_forbidden"] >= 1


def test_support_registry_routes_validator_helpers_through_owner_command() -> None:
    raw = {
        "path": "scripts/validators/example_route_tokens.py",
        "family": "validator_helper",
        "owner_surface": "scripts/AGENTS.md",
        "side_effects": "helper import only; shared route token checks",
        "validation_lane": "source_fast",
    }

    semantic = readiness.semantic_support_classification("script", raw, relevant=True)

    assert semantic["semantic_class"] == "deterministic_validator"
    assert semantic["classification_rule"] == "read_only_validator_helper_component"
    assert semantic["review_status"] == "rule_reviewed"
    assert semantic["recommended_route"] == "component_only_use_owning_validator_or_lane_command"
    assert semantic["safe_to_apply_directly"] is False
    assert "owning validator or lane command" in semantic["review_reason"]


def test_session_mining_status_exposes_manual_review_packetization() -> None:
    status = readiness.SESSION_MINING_STATUS
    schema = readiness.SAMPLE_PACKET_SCHEMA

    assert status["status"] == "manual_review_packetized"
    assert status["reviewed_count"] >= 20
    assert status["packetized_count"] >= 5
    assert status["report_refs"]
    assert "candidate evidence only" in status["candidate_only_boundary"]
    assert "candidate_state_reason" in schema["required_fields"]
    assert "promotion_forbidden_until" in schema["required_fields"]


def test_candidate_queue_imports_packet_routes_without_promotion() -> None:
    packet = {
        "path": "mechanics/audit/parts/candidate-readers/packets/session-mining/example.eval_candidate.json",
        "payload": {
            "packet_id": "session:example",
            "source_kind": "session_episode",
            "source_ref": ".aoa:session/example",
            "trigger_class_id": "session_episode_candidate_for_eval_design",
            "expected_aoa_eval_route": "session_candidate",
            "candidate_state": "needs_owner_review",
            "candidate_state_reason": "route break with owner refs",
            "owner_surface_refs": ["docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md"],
            "evidence_refs": [".aoa:session/example"],
            "freshness_refs": ["checked_at:2026-06-25"],
            "promotion_forbidden_until": ["human owner acceptance"],
            "evaluator_fit": "trace_trajectory_eval",
            "next_step": "manual owner review",
        },
    }

    queue = readiness.build_candidate_queue(
        {"repos": []},
        {"count": 0},
        {"total_evals": 39},
        {
            "packet_count": 1,
            "issue_count": 0,
            "packet_root": "mechanics/audit/parts/candidate-readers/packets",
            "summary": {"session_episode_packets": 1},
            "packets": [packet],
        },
    )

    ids = {entry["candidate_id"] for entry in queue["entries"]}
    imported = queue["entries"][0]
    assert "packet:session:example" in ids
    assert "session-mining:criteria-gated" not in ids
    assert imported["promotion_allowed"] is False
    assert imported["packet_ref"].endswith("example.eval_candidate.json")


def test_dashboard_shape_check_rejects_proof_promoting_posture(tmp_path: Path) -> None:
    dashboard = {
        "schema_version": readiness.SCHEMA_VERSION,
        "authority_boundary": readiness.AUTHORITY_BOUNDARY,
        "external_research_grounding": readiness.EXTERNAL_RESEARCH_GROUNDING,
        "owner_boundaries": [],
        "local_eval_ports": {},
        "central_catalog": {},
        "mcp_runtime_status": {},
        "runtime_candidate_exports": {},
        "aoa_session_memory_freshness": {},
        "workspace_git_drift": {},
        "eval_support_registry": {},
        "repo_readiness": {"schema_version": "os_abyss_eval_repo_readiness_v1", "repos": []},
        "aoa_eval_runtime_adoption": {},
        "trigger_criteria": {
            "taxonomy": readiness.TRIGGER_CLASSES,
            "sample_packet_schema": readiness.SAMPLE_PACKET_SCHEMA,
            "session_mining_status": readiness.SESSION_MINING_STATUS,
        },
        "trajectory_eval_slice": {},
        "candidate_queue": {"allowed_states": list(readiness.CANDIDATE_QUEUE_STATES)},
        "eval_forge_readiness": {
            "schema_version": "os_abyss_eval_forge_readiness_v1",
            "registry_validation": {"valid": True, "errors": [], "archetype_count": 18},
            "archetype_count": 18,
            "router_command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --json",
            "candidate_archetype_hints": [],
        },
        "local_to_central_promotion_path": {},
        "freshness_sentinel": {},
        "phase_coverage": [],
        "read_model_posture": {
            "can_score": False,
            "can_accept_proof": True,
            "can_promote_candidates": False,
            "can_mutate_sibling_repos": False,
        },
    }
    support = {"schema_version": readiness.SUPPORT_REGISTRY_SCHEMA_VERSION}

    issues = readiness.validate_dashboard_shape(dashboard, support)

    assert "read_model_posture.can_accept_proof must be false" in issues
