from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    BUNDLE_ROOT / "runners" / "run_phase13_participation_codex_lane.py"
)


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_participation_codex_lane",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runner():
    return load_runner()


def digest(character: str = "1") -> str:
    return "sha256:" + (character * 64)


def synthetic_observations(runner) -> tuple[dict, list[dict]]:
    fixture = runner.load_json(runner.CASES_PATH)
    cases = runner.validate_fixture(fixture)
    observations: list[dict] = []
    for case in cases:
        for arm_id in case["arm_order"]:
            selected_skills: list[str] = []
            mcp_calls: list[dict[str, str]] = []
            family = case["case_family"]
            if family == "explicit_orientation":
                selected_skills = ["aoa-memo"]
                tool = "aoa_memo_brief" if arm_id == "P1" else "aoa_memo_search"
                mcp_calls = [
                    {
                        "server": "aoa_memo",
                        "tool": tool,
                        "status": "completed",
                    }
                ]
            elif family == "indirect_continuity":
                if arm_id == "P1":
                    selected_skills = ["aoa-memo"]
                    mcp_calls = [
                        {
                            "server": "aoa_memo",
                            "tool": "aoa_memo_brief",
                            "status": "completed",
                        }
                    ]
                else:
                    selected_skills = ["aoa-decision"]
                    mcp_calls = [
                        {
                            "server": "aoa_decisions",
                            "tool": "aoa_decisions_search",
                            "status": "failed",
                        }
                    ]
            elif family == "raw_session_sibling":
                selected_skills = ["aoa-session-memory-global-route"]
            memo_tool_calls = [
                call["tool"]
                for call in mcp_calls
                if call["server"] == "aoa_memo"
            ]
            observation = {
                "attempt_index": len(observations),
                "case_id": case["case_id"],
                "case_family": family,
                "arm_id": arm_id,
                "prompt_sha256": runner.text_digest(case["prompt"]),
                "status": "complete",
                "exit_code": 0,
                "latency_ms": 1000.0 + len(observations),
                "thread_started": True,
                "turn_completed": True,
                "selected_skills": selected_skills,
                "mcp_calls": mcp_calls,
                "memo_selected": "aoa-memo" in selected_skills,
                "memo_tool_calls": memo_tool_calls,
                "locator_call_count": len(mcp_calls),
                "usage": {
                    "input_tokens": 100,
                    "cached_input_tokens": 80,
                    "output_tokens": 10,
                    "reasoning_output_tokens": 5,
                },
                "expectation_passed": False,
                "expectation_failures": [],
                "raw_jsonl_digest": digest("2"),
                "stderr_digest": digest("3"),
            }
            failures = runner.score_expectation(
                observation,
                case["expectations"][arm_id],
            )
            observation["expectation_failures"] = failures
            observation["expectation_passed"] = not failures
            observations.append(observation)
    return fixture, observations


def test_fixture_is_paired_and_alternates_first_arm(runner) -> None:
    fixture = runner.load_json(runner.CASES_PATH)
    cases = runner.validate_fixture(fixture)
    assert len(cases) == 4
    assert [case["arm_order"][0] for case in cases] == [
        "P0",
        "P1",
        "P0",
        "P1",
    ]
    assert {case["case_family"] for case in cases} == {
        "explicit_orientation",
        "indirect_continuity",
        "current_source_negative",
        "raw_session_sibling",
    }


def test_event_parser_records_routes_without_message_content(runner) -> None:
    stream = "\n".join(
        [
            json.dumps({"type": "thread.started", "thread_id": "thread-1"}),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "command_execution",
                        "command": (
                            "sed -n 1,240p "
                            "/candidate/skills/aoa-memo/SKILL.md"
                        ),
                    },
                }
            ),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "mcp_tool_call",
                        "server": "aoa_memo",
                        "tool": "aoa_memo_brief",
                        "status": "completed",
                        "arguments": {"private": "must not be copied"},
                        "result": {"private": "must not be copied"},
                    },
                }
            ),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "agent_message",
                        "text": "private answer must not be copied",
                    },
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 10,
                        "cached_input_tokens": 8,
                        "output_tokens": 2,
                        "reasoning_output_tokens": 1,
                    },
                }
            ),
        ]
    )
    parsed, error = runner.parse_event_stream(stream)
    assert error is None
    assert parsed["selected_skills"] == ["aoa-memo"]
    assert parsed["mcp_calls"] == [
        {
            "server": "aoa_memo",
            "tool": "aoa_memo_brief",
            "status": "completed",
        }
    ]
    assert "private" not in json.dumps(parsed)


def test_expectation_scoring_enforces_silence_and_sibling_boundary(runner) -> None:
    observation = {
        "status": "complete",
        "memo_selected": True,
        "memo_tool_calls": ["aoa_memo_brief"],
        "selected_skills": ["aoa-memo"],
        "locator_call_count": 1,
    }
    expectation = {
        "memo_route": "forbidden",
        "required_selected_skill": "aoa-session-memory-global-route",
        "required_memo_tool": None,
        "max_locator_calls": 0,
    }
    assert runner.score_expectation(observation, expectation) == [
        "memo_route_unexpected",
        "required_skill_missing",
        "locator_budget_exceeded",
    ]


def test_synthetic_report_passes_schema_and_locks_authority(runner) -> None:
    fixture, observations = synthetic_observations(runner)
    source_pins = {
        f"source_{index}": digest(str((index % 9) + 1))
        for index in range(9)
    }
    report = runner.build_report(
        fixture=fixture,
        observations=observations,
        source_pins=source_pins,
        codex_version="codex-cli 0.145.0",
        model="gpt-5.6-sol",
        execution_fingerprint=digest("4"),
    )
    schema = runner.load_json(runner.REPORT_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    runner.validate_report(report)
    assert report["exit_gate_passed"] is True
    assert report["metrics"]["paired_route_delta_count"] == 2
    assert report["metrics"]["p1_false_positive_count"] == 0
    assert report["metrics"]["sibling_takeover_count"] == 0

    widened = json.loads(json.dumps(report))
    widened["authority"]["live_activation"] = True
    widened["report_digest"] = runner.normalized_report_digest(widened)
    with pytest.raises(runner.CodexParticipationError, match="live_activation"):
        runner.validate_report(widened)
