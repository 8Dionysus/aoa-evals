from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_eval_candidate_packets as packets


def valid_packet() -> dict:
    return {
        "schema_version": "aoa_eval_candidate_packet_v1",
        "packet_id": "session:test-route-break",
        "candidate_only": True,
        "proof_authority": False,
        "promotion_allowed": False,
        "source_kind": "session_episode",
        "source_ref": ".aoa/session/test-segment",
        "observed_at_utc": "2026-06-25T00:00:00Z",
        "trigger_class_id": "agent_route_miss_or_tool_trajectory_pressure",
        "task_pressure": "Agent route behavior needs candidate-only review.",
        "expected_aoa_eval_route": "session_candidate",
        "actual_trajectory": "Agent skipped route inspection before changing source.",
        "first_failure": "Route owner was not inspected before mutation.",
        "consequence": "A generated or local surface could be treated as proof.",
        "owner_surface_refs": [
            "docs/guides/AGENT_TRACE_EVAL_CANDIDATE_DISCOVERY.md"
        ],
        "evidence_refs": [".aoa/session/test-segment"],
        "freshness_refs": ["checked_at:2026-06-25"],
        "privacy_boundary": "Only bounded refs are recorded; no raw transcript body.",
        "existing_surface_check": "Existing eval overlap not yet found.",
        "routing_rubric": {
            "trigger_strength": 2,
            "owner_surface_clarity": 2,
            "consequence_severity": 1,
            "repeatability": 2,
            "freshness_dependency": 1,
            "existing_eval_fit": 0,
            "privacy_raw_evidence_boundary": 2,
        },
        "evaluator_fit": "trace_trajectory_eval",
        "candidate_state": "needs_owner_review",
        "candidate_state_reason": "Expected route, break, consequence, owner, and repeatability are present.",
        "promotion_forbidden_until": [
            "local owner review",
            "central overlap check",
            "human owner acceptance",
        ],
        "forbidden_effects": [
            "central_proof_promotion",
            "verdict_acceptance",
            "score_or_baseline_creation",
            "repo_mutation",
            "mcp_created_bundle",
        ],
        "next_step": "Review bounded source refs manually before queue import.",
    }


def test_candidate_packet_schema_accepts_candidate_only_packet() -> None:
    validator = packets.schema_validator()
    payload = valid_packet()

    assert packets.validate_payload(
        payload,
        location="example.eval_candidate.json",
        validator=validator,
    ) == []


def test_candidate_packet_schema_rejects_proof_promotion_fields() -> None:
    validator = packets.schema_validator()
    payload = valid_packet()
    payload["verdict"] = "supports bounded claim"

    issues = packets.validate_payload(
        payload,
        location="bad.eval_candidate.json",
        validator=validator,
    )

    assert any("must not carry proof-promotion fields" in issue.message for issue in issues)


def test_candidate_packet_requires_base_forbidden_effects() -> None:
    validator = packets.schema_validator()
    payload = valid_packet()
    payload["forbidden_effects"] = ["central_proof_promotion"]

    issues = packets.validate_payload(
        payload,
        location="bad.eval_candidate.json",
        validator=validator,
    )

    assert any("forbidden_effects must include" in issue.message for issue in issues)


def test_candidate_packet_schema_only_validates_bundled_example() -> None:
    schema = json.loads(packets.PACKET_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    example = json.loads(packets.EXAMPLE_PACKET.read_text(encoding="utf-8"))
    issues = packets.validate_files([packets.EXAMPLE_PACKET])

    assert example["candidate_only"] is True
    assert issues == []


def test_real_candidate_packet_queue_validates() -> None:
    paths = packets.packet_paths([str(packets.DEFAULT_PACKET_ROOT)])
    session_packets = [path for path in paths if "session-mining" in path.parts]

    assert len(session_packets) >= 5
    assert packets.validate_files(session_packets) == []
