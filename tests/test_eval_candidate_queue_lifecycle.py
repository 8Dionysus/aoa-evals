from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_eval_candidate_queue_lifecycle as lifecycle


def base_packet(**overrides: object) -> dict:
    packet = {
        "schema_version": "aoa_eval_candidate_packet_v1",
        "packet_id": "session:test-candidate",
        "candidate_only": True,
        "proof_authority": False,
        "promotion_allowed": False,
        "source_kind": "session_episode",
        "source_ref": ".aoa:session/test",
        "observed_at_utc": "2026-06-25T00:00:00Z",
        "trigger_class_id": "session_episode_candidate_for_eval_design",
        "task_pressure": "agent missed an eval trigger under route pressure",
        "expected_aoa_eval_route": "session_candidate",
        "actual_trajectory": "agent continued without route check",
        "first_failure": "route check skipped",
        "consequence": "eval pressure was not preserved",
        "owner_surface_refs": ["docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md"],
        "evidence_refs": [".aoa:session/test"],
        "freshness_refs": ["checked_at:2026-06-25"],
        "privacy_boundary": "raw session evidence remains outside proof",
        "existing_surface_check": "existing central and local surfaces checked",
        "routing_rubric": {
            "trigger_strength": 2,
            "owner_surface_clarity": 2,
            "consequence_severity": 1,
            "repeatability": 1,
            "freshness_dependency": 1,
            "existing_eval_fit": 0,
            "privacy_raw_evidence_boundary": 2,
        },
        "evaluator_fit": "trace_trajectory_eval",
        "candidate_state": "needs_owner_review",
        "candidate_state_reason": "candidate needs owner review before conversion",
        "promotion_forbidden_until": [
            "manual source-span review completed by owner",
            "human owner acceptance recorded",
            "candidate converted into local intake or source eval bundle by owner",
        ],
        "forbidden_effects": [
            "central_proof_promotion",
            "verdict_acceptance",
            "score_or_baseline_creation",
            "repo_mutation",
            "mcp_created_bundle",
        ],
        "next_step": "manual owner review",
    }
    packet.update(overrides)
    return packet


def write_packet(tmp_path: Path, payload: dict) -> Path:
    path = tmp_path / "candidate.eval_candidate.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_candidate_queue_lifecycle_current_packets_are_review_only() -> None:
    payload = lifecycle.build_lifecycle_payload([])

    assert payload["schema_version"] == lifecycle.SCHEMA_VERSION
    assert payload["valid"] is True
    assert payload["packet_count"] >= 5
    assert payload["summary"]["by_state"]["needs_owner_review"] >= 5
    assert payload["summary"]["next_action_count"] == payload["packet_count"]
    assert all(action["candidate_only"] is True for action in payload["next_actions"])
    assert all(action["proof_authority"] is False for action in payload["next_actions"])
    assert all(action["promotion_allowed"] is False for action in payload["next_actions"])
    assert any("do not accept proof" in line for line in payload["stop_lines"])


def test_candidate_queue_lifecycle_rejects_review_state_without_owner_gate(tmp_path: Path) -> None:
    packet_path = write_packet(
        tmp_path,
        base_packet(promotion_forbidden_until=["criteria taxonomy accepted"]),
    )

    payload = lifecycle.build_lifecycle_payload([str(packet_path)])

    assert payload["valid"] is False
    assert payload["issue_count"] == 1
    assert payload["issues"][0]["message"] == (
        "needs_owner_review candidate must keep a human owner acceptance gate"
    )


def test_candidate_queue_lifecycle_rejects_accepted_without_conversion_gate(tmp_path: Path) -> None:
    packet_path = write_packet(
        tmp_path,
        base_packet(
            candidate_state="accepted",
            candidate_state_reason="human owner accepted the candidate for later conversion",
            promotion_forbidden_until=["human owner acceptance recorded"],
        ),
    )

    payload = lifecycle.build_lifecycle_payload([str(packet_path)])

    assert payload["valid"] is False
    assert any(
        issue["message"] == "accepted candidate must name owner conversion before any proof route"
        for issue in payload["issues"]
    )
