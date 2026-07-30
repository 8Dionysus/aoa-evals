from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_phase13_participation_lab.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_participation_lab",
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


def report(runner) -> dict:
    observations = [
        {
            "case_id": f"PART-{index:02d}",
            "case_family": (
                "direct",
                "indirect",
                "incomplete",
                "negative",
                "edge",
            )[(index - 1) % 5],
            "expected_route": "none",
            "observed_route": "none",
            "expected_opportunity_state": "not_applicable",
            "observed_opportunity_state": "not_applicable",
            "passed": True,
            "latency_ms": 10.0,
            "receipt_digest": digest("2"),
        }
        for index in range(1, 11)
    ]
    payload = {
        "schema_version": "aoa_memo_phase13_participation_lab_v0",
        "report_id": "aoa-memo-phase13-participation-mechanism-20260729",
        "generated_at": "2026-07-29T12:00:00Z",
        "posture": "source_local_shadow_mechanism_no_live_activation",
        "source_pins": {
            f"source_{index}": digest(str((index % 9) + 1))
            for index in range(10)
        },
        "variants": {
            "P0": "named_baseline_not_executed_in_mechanism_lab",
            "P1": "two_speed_skill_source_validated",
            "P2": "shadow_hook_and_composition_executed_disposably",
            "P3": "selective_route_only_cue_closed_not_executed",
        },
        "skill_contract": {
            "bundle_version": "0.1.22",
            "materiality_trigger_present": True,
            "fast_lane_present": True,
            "one_brief_budget_present": True,
            "silence_present": True,
            "deep_gate_present": True,
            "sibling_handoffs_present": True,
            "session_memory_dependency": False,
            "prompt_visibility_checked": False,
            "fresh_session_selection_checked": False,
        },
        "trigger_corpus": {
            "case_count": 10,
            "families": [
                "direct",
                "edge",
                "incomplete",
                "indirect",
                "negative",
            ],
            "exact_match_count": 10,
            "false_positive_count": 0,
            "false_negative_count": 0,
            "observations": observations,
        },
        "lifecycle": {
            "events_seen": [
                "SessionStart",
                "UserPromptSubmit",
                "PostToolUse",
                "PreCompact",
                "PostCompact",
                "Stop",
                "SessionEnd",
            ],
            "receipt_count": 17,
            "receipt_logs_valid": True,
            "hash_chains_valid": True,
            "hook_stdout_empty": True,
            "hook_stderr_empty": True,
            "hook_failure_count": 0,
        },
        "composition": {
            "native_source_digest": digest("3"),
            "memo_fragment_digest": digest("4"),
            "output_digest": digest("5"),
            "composition_receipt_digest": digest("6"),
            "fragment_order": [
                "native-config:0",
                "aoa-memo:participation-shadow:v0",
            ],
            "event_count": 7,
            "native_handler_count": 5,
            "combined_handler_count": 12,
            "standalone_native_preserved": True,
            "owner_metadata_removed": True,
            "unresolved_binding_count": 0,
            "disposable_atomic_write": True,
            "backup_created": True,
            "live_config_touched": False,
            "codex_trust_established": False,
        },
        "privacy": {
            "raw_prompt_persisted": False,
            "transcript_path_persisted": False,
            "cwd_persisted": False,
            "tool_input_persisted": False,
            "tool_response_persisted": False,
            "assistant_message_persisted": False,
            "case_marker_leak_count": 0,
            "raw_binding_value_in_composition_receipt": False,
        },
        "evidence_ladder": {
            "opportunity": "synthetic_corpus_observed",
            "noticed": "unknown",
            "invocation": "synthetic_posttool_observed",
            "result_returned": "synthetic_posttool_observed",
            "used_or_rejected": "unknown",
            "action_change": "unknown",
            "outcome": "unknown",
            "benefit_claim_allowed": False,
        },
        "performance": {
            "prompt_hook_observation_count": 10,
            "p50_hook_latency_ms": 10.0,
            "p95_hook_latency_ms": 12.0,
            "max_hook_latency_ms": 15.0,
            "receipt_state_bytes": 1000,
            "composed_config_bytes": 2000,
        },
        "gates": {
            f"gate_{index}": True
            for index in range(8)
        },
        "exit_gate_passed": True,
        "verdict": "supports source-local H0 participation mechanism continuation",
        "authority": {
            "live_activation": False,
            "codex_trust": False,
            "skill_admission": False,
            "policy_promotion": False,
            "memory_write": False,
            "production": False,
            "landing": False,
            "benefit_verdict": False,
        },
        "limitations": [
            "Synthetic trigger matches do not prove selection.",
            "Synthetic PostToolUse does not prove natural invocation.",
            "Disposable composition is not live trust.",
            "No context was injected.",
            "No benefit is established.",
        ],
        "report_digest": "",
    }
    payload["report_digest"] = runner.normalized_report_digest(payload)
    return payload


def test_trigger_corpus_covers_all_families_and_separate_variants(runner) -> None:
    fixture = runner.load_json(runner.CASES_PATH)
    cases = runner.validate_trigger_fixture(fixture)
    assert len(cases) == 14
    assert {case["case_family"] for case in cases} == {
        "direct",
        "indirect",
        "incomplete",
        "negative",
        "edge",
    }
    assert fixture["variant_labels"]["P0"].startswith("current")
    assert fixture["variant_labels"]["P3"].endswith("closed in this corpus")


def test_report_schema_is_valid_and_self_digesting(runner) -> None:
    schema = runner.load_json(runner.REPORT_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    payload = report(runner)
    runner.validate_report(payload)
    assert payload["report_digest"] == runner.normalized_report_digest(payload)


def test_report_rejects_authority_and_benefit_widening(runner) -> None:
    widened = report(runner)
    widened["authority"]["live_activation"] = True
    widened["report_digest"] = runner.normalized_report_digest(widened)
    with pytest.raises(runner.ParticipationLabError, match="live_activation"):
        runner.validate_report(widened)

    benefit = report(runner)
    benefit["evidence_ladder"]["benefit_claim_allowed"] = True
    benefit["report_digest"] = runner.normalized_report_digest(benefit)
    with pytest.raises(runner.ParticipationLabError, match="benefit_claim_allowed"):
        runner.validate_report(benefit)


def test_handler_identity_preserves_event_and_matcher(runner) -> None:
    hooks = {
        "PostToolUse": [
            {
                "matcher": "^mcp__aoa_memo__.*$",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 memo.py",
                    }
                ],
            }
        ],
        "UserPromptSubmit": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 memo.py",
                    }
                ]
            }
        ],
    }
    assert runner.handler_keys(hooks) == [
        (
            "PostToolUse",
            "^mcp__aoa_memo__.*$",
            "python3 memo.py",
            "",
        ),
        (
            "UserPromptSubmit",
            "",
            "python3 memo.py",
            "",
        ),
    ]


def test_runner_has_no_fixed_session_memory_repo_dependency() -> None:
    source = RUNNER_PATH.read_text(encoding="utf-8")
    assert "/aoa-session-memory" not in source
    assert "import aoa_session_memory" not in source
    assert "--native-hooks" in source
