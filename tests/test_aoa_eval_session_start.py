from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import aoa_eval_session_start as session_start


def test_session_start_uses_default_stack_root_resolver(monkeypatch, tmp_path) -> None:
    stack_root = tmp_path / "abyss-stack"
    stack_root.mkdir()
    monkeypatch.setattr(session_start.readiness, "selected_stack_root", lambda value: stack_root)

    assert session_start.resolve_stack_root("") == stack_root


def sample_dashboard() -> dict:
    return {
        "read_model_posture": {
            "can_route": True,
            "can_score": False,
            "can_accept_proof": False,
            "can_promote_candidates": False,
            "can_mutate_sibling_repos": False,
        },
        "repo_readiness": {
            "repos": [
                {
                    "repo_id": "aoa-routing",
                    "route_state": "needs_local_design_or_owner_review",
                    "pressure_severity": "medium",
                    "route_confidence": "high",
                    "exact_next_command": "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
                    "freshness_warnings": [],
                },
                {
                    "repo_id": "aoa-memo",
                    "route_state": "blocked_by_freshness",
                    "pressure_severity": "blocked",
                    "route_confidence": "medium",
                    "exact_next_command": "python3 scripts/aoa_session_memory.py maintenance-status --full",
                    "freshness_warnings": ["session memory freshness unknown"],
                },
                {
                    "repo_id": "dormant-repo",
                    "route_state": "dormant_no_current_eval_pressure",
                    "pressure_severity": "none",
                    "route_confidence": "high",
                    "exact_next_command": "python scripts/build_local_eval_port_inventory.py --json",
                    "freshness_warnings": [],
                },
            ]
        },
        "candidate_queue": {
            "summary": {"entries": 2, "packet_count": 1},
            "entries": [
                {
                    "candidate_id": "packet:session:example",
                    "state": "needs_owner_review",
                    "source_kind": "session_episode",
                    "owner_repo": "aoa-evals + .aoa",
                    "packet_ref": "mechanics/audit/parts/candidate-readers/packets/session-mining/example.eval_candidate.json",
                    "trigger_class_id": "session_episode_candidate_for_eval_design",
                    "expected_aoa_eval_route": "session_candidate",
                    "review_gate": "human owner acceptance",
                    "evidence_count": 2,
                    "next_route": "manual owner review",
                },
                {
                    "candidate_id": "local-port:aoa-routing",
                    "state": "deferred",
                    "source_kind": "local_eval_port",
                    "owner_repo": "aoa-routing",
                    "review_gate": "repo owner review",
                    "evidence_count": 1,
                    "next_route": "inspect local port",
                },
            ],
        },
        "eval_forge_readiness": {
            "schema_version": "os_abyss_eval_forge_readiness_v1",
            "registry_ref": "mechanics/proof-object/parts/eval-authoring/config/eval-archetypes.json",
            "worksheet_schema_ref": "mechanics/proof-object/parts/eval-authoring/schemas/eval-design-worksheet.schema.json",
            "registry_validation": {"valid": True, "errors": [], "archetype_count": 18},
            "archetype_count": 18,
            "router_command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json",
            "local_port_pressure_hint_command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --local-port-repo <repo_id> --local-port-inventory /tmp/aoa_local_eval_ports.current.json --workspace-root /srv/AbyssOS --json",
            "worksheet_write_command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --write-worksheet <worksheet-path> --json",
            "front_door_refs": {
                "operating_path_ref": "mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md",
                "session_mining_criteria_ref": "mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md",
                "local_port_decision_matrix_ref": "mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md",
                "latest_route_review_report_ref": "mechanics/proof-object/parts/eval-authoring/reports/eval-forge/2026-06-26-session-candidate-owner-review.md",
                "worksheet_example_ref": "mechanics/proof-object/parts/eval-authoring/examples/aoa_eval_criteria_before_mining.eval_design_worksheet.example.json",
                "candidate_packet_schema_ref": "mechanics/audit/parts/candidate-readers/schemas/aoa-eval-candidate-packet.schema.json",
            },
            "front_door_commands": [
                {
                    "purpose": "raise the per-session Eval Forge front door",
                    "command": "python scripts/aoa_eval_session_start.py --json",
                },
                {
                    "purpose": "check front-door readiness gates and blockers",
                    "command": "python scripts/check_eval_forge_readiness.py --json",
                },
                {
                    "purpose": "inspect active/skeleton/missing/invalid local eval ports",
                    "command": "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
                },
                {
                    "purpose": "validate imported candidate packets before review",
                    "command": "python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
                },
                {
                    "purpose": "route a session candidate packet through Eval Forge",
                    "command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json",
                },
                {
                    "purpose": "route one active local eval port through Eval Forge",
                    "command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --local-port-repo <repo_id> --local-port-inventory /tmp/aoa_local_eval_ports.current.json --workspace-root /srv/AbyssOS --json",
                },
                {
                    "purpose": "write a non-proof owner-review worksheet only after admission gates",
                    "command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --write-worksheet <worksheet-path> --json",
                },
            ],
            "front_door_surface_status": {
                "valid": True,
                "missing_refs": [],
                "proof_authority": False,
                "promotion_allowed": False,
            },
            "candidate_archetype_hints": [
                {
                    "candidate_id": "packet:session:example",
                    "packet_ref": "mechanics/audit/parts/candidate-readers/packets/session-mining/example.eval_candidate.json",
                    "decision": "keep",
                    "selected_archetype_id": "trace-trajectory-eval",
                    "owner_repo": "aoa-evals",
                    "route_key": "session_candidate_design",
                    "missing_evidence": [],
                    "exact_next_command": "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet mechanics/audit/parts/candidate-readers/packets/session-mining/example.eval_candidate.json --json",
                    "proof_authority": False,
                    "promotion_allowed": False,
                }
            ],
            "stop_lines": ["keep candidate packets non-proof"],
        },
        "mcp_runtime_status": {"status": "ok"},
        "aoa_session_memory_freshness": {"status": "skipped"},
        "aoa_eval_runtime_adoption": {
            "source_skill_exists": True,
            "installed_profile": "user-aoa-foundation",
            "installed_profile_verified": True,
            "installed_matches_source": True,
            "front_door_invoke_capable": "covered_by_aoa_skills_prompt_trigger_harness_when_command_passes",
        },
    }


def test_session_start_payload_gives_agent_actionable_front_door() -> None:
    payload = session_start.build_session_start_payload(
        sample_dashboard(),
        {"summary": {"eval_lane_relevant": 10}},
    )

    commands = {item["command"] for item in payload["session_entry_commands"]}
    assert "python scripts/aoa_eval_session_start.py --json" in commands
    assert "python scripts/build_eval_readiness_dashboard.py --check" in commands
    assert "python scripts/check_eval_support_registry.py --json" in commands
    assert "python scripts/validate_eval_candidate_packets.py --schema-only" in commands
    assert "python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets" in commands
    assert "python scripts/check_eval_candidate_queue_lifecycle.py --json" in commands
    assert "python scripts/review_eval_promotion_path.py --json" in commands
    assert any("eval_forge_route.py" in command for command in commands)
    front_door = payload["eval_forge_front_door"]
    assert front_door["surface_refs"]["operating_path_ref"].endswith("EVAL_FORGE_OPERATING_PATH.md")
    assert front_door["surface_refs"]["session_mining_criteria_ref"].endswith("SESSION_MINING_CRITERIA.md")
    assert front_door["surface_refs"]["local_port_decision_matrix_ref"].endswith("LOCAL_PORT_DECISION_MATRIX.md")
    assert front_door["surface_refs"]["latest_route_review_report_ref"].endswith("2026-06-26-session-candidate-owner-review.md")
    assert front_door["surface_refs"]["worksheet_example_ref"].endswith("aoa_eval_criteria_before_mining.eval_design_worksheet.example.json")
    assert front_door["proof_authority"] is False
    assert front_door["promotion_allowed"] is False
    front_door_commands = {item["command"] for item in front_door["exact_commands"]}
    assert "python scripts/aoa_eval_session_start.py --json" in front_door_commands
    assert any("--local-port-repo" in command and "--local-port-inventory" in command for command in front_door_commands)
    assert any("--write-worksheet" in command for command in front_door_commands)
    assert payload["candidate_packet_contract"]["candidate_only"] is True
    assert payload["candidate_packet_contract"]["proof_authority"] is False
    assert payload["eval_forge_readiness"]["registry_valid"] is True
    assert payload["eval_forge_readiness"]["archetype_count"] == 18
    assert payload["eval_forge_readiness"]["promotion_allowed"] is False
    assert payload["eval_forge_readiness"]["worksheet_write_command"].endswith("--write-worksheet <worksheet-path> --json")
    assert payload["eval_forge_readiness"]["front_door_refs"]["worksheet_example_ref"] == front_door["surface_refs"]["worksheet_example_ref"]
    assert payload["eval_forge_readiness"]["top_candidate_hints"][0]["selected_archetype_id"] == "trace-trajectory-eval"
    assert payload["promotion_review_route"]["dry_run"] is True
    assert payload["promotion_review_route"]["promotion_allowed"] is False
    assert "human_acceptance" in payload["promotion_review_route"]["gates"]
    assert payload["read_model_posture"]["can_accept_proof"] is False
    assert payload["local_suite_execution_boundary"]["execution_allowed"] is False
    assert payload["local_suite_execution_boundary"]["owner_apply_required_for_ready"] is True
    assert payload["local_suite_execution_boundary"]["readiness_scope"] == "source-contract-ready"
    assert payload["local_suite_execution_boundary"]["runtime_reproducibility_proven"] is False
    assert payload["local_suite_execution_boundary"]["jit_revalidation_required"] is True
    assert payload["local_suite_execution_boundary"]["execution_receipt_required"] is True
    assert payload["local_suite_execution_boundary"]["environment_capture_required"] is True
    assert payload["active_repo_routes"][0]["repo_id"] == "aoa-memo"
    assert payload["active_repo_routes"][0]["suite_execution"]["state"] == "absent"
    assert payload["active_repo_routes"][0]["suite_execution"]["execution_allowed"] is False
    assert payload["candidate_queue_routes"][0]["candidate_id"] == "packet:session:example"
    assert payload["candidate_queue_routes"][0]["packet_ref"].endswith("example.eval_candidate.json")
    assert payload["candidate_queue_routes"][0]["proof_authority"] is False
    assert payload["candidate_queue_routes"][0]["promotion_allowed"] is False
    assert payload["skill_route"]["runtime_adoption"]["installed_profile_verified"] is True
    assert "dormant-repo" not in {item["repo_id"] for item in payload["active_repo_routes"]}
    assert any("do not treat .aoa" in line for line in payload["stop_lines"])


def test_session_start_surfaces_aoa_live_catchup_recommendation_when_status_is_ok() -> None:
    dashboard = sample_dashboard()
    dashboard["aoa_session_memory_freshness"] = {
        "status": "ok",
        "next_route": "python3 scripts/aoa_session_memory.py index-maintenance target --apply",
        "json_summary": {
            "recommendation": "wait_live_catchup",
            "next_action_id": "wait_live_catchup",
            "live_catchup_pending": True,
            "maintenance_required": False,
            "live_tail_status": "waiting_for_quiet_window",
            "live_tail_next_ready_at": "2026-06-25T23:37:35Z",
        },
    }

    payload = session_start.build_session_start_payload(dashboard, {"summary": {}})

    aoa_blocker = {
        item["surface"]: item for item in payload["freshness_blockers"]
    }[".aoa"]
    assert aoa_blocker["status"] == "wait_live_catchup"
    assert aoa_blocker["next_route"].startswith("python3 scripts/aoa_session_memory.py")
    assert "recommendation=wait_live_catchup" in aoa_blocker["warnings"]


def test_session_start_text_names_commands_and_stop_lines() -> None:
    payload = session_start.build_session_start_payload(sample_dashboard(), {"summary": {}})
    rendered = session_start.render_text(payload)

    assert "OS Abyss Eval Session Start" in rendered
    assert "Forge Front Door" in rendered
    assert "EVAL_FORGE_OPERATING_PATH.md" in rendered
    assert "--write-worksheet" in rendered
    assert "check_eval_support_registry.py" in rendered
    assert "validate_eval_candidate_packets.py" in rendered
    assert "check_eval_candidate_queue_lifecycle.py" in rendered
    assert "review_eval_promotion_path.py" in rendered
    assert "Promotion Review" in rendered
    assert "Eval Forge" in rendered
    assert "trace-trajectory-eval" in rendered
    assert "Skill Runtime" in rendered
    assert "user-aoa-foundation" in rendered
    assert "packet:session:example" in rendered
    assert "aoa-memo" in rendered
    assert "do not import session evidence" in rendered
