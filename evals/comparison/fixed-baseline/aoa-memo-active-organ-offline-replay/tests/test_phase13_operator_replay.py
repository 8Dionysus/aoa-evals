from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = (
    BUNDLE_ROOT / "runners" / "run_phase13_operator_replay.py"
)
SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-operator-replay.schema.json"
)


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_operator_replay",
        RUNNER_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_operator_replay_is_pinned_retrospective_and_refs_only() -> None:
    runner = load_runner()
    contract, source, source_digest = runner.load_inputs()
    prompts = runner.build_prompts(contract, source)

    assert contract["source_fixture"]["sha256"] == source_digest
    assert contract["experiment_posture"] == (
        "retrospective_sanitized_counterfactual_upper_bound"
    )
    assert len(prompts) == 24
    assert {prompt["arm_id"] for prompt in prompts} == {"0", "A"}
    assert sum(
        prompt["arm_id"] == "A"
        and prompt["expected_influence"] == "silence"
        for prompt in prompts
    ) == 2
    assert all("raw:line:" not in prompt["prompt"] for prompt in prompts)
    assert all(
        "raw/blocks/" not in prompt["prompt"] for prompt in prompts
    )
    assert all(value is False for value in contract["authority"].values())


def test_v2_prompt_protocol_uses_exact_enum_and_short_owner_token() -> None:
    runner = load_runner()
    contract_path = (
        BUNDLE_ROOT
        / "fixtures"
        / "phase13-operator-replay-contract-v2.json"
    )
    contract, source, _ = runner.load_inputs(contract_path)
    prompts = runner.build_prompts(contract, source)
    eligible_active = next(
        prompt
        for prompt in prompts
        if prompt["arm_id"] == "A"
        and prompt["orientation_eligible"]
    )

    assert "DECLARED_MEMORY_INFLUENCE_ENUM: used" in eligible_active["prompt"]
    assert "OWNER_ROUTE_OPTIONS:" in eligible_active["prompt"]
    assert "Copy memory_influence exactly as the single enum" in (
        eligible_active["prompt"]
    )
    assert contract["predecessor_run"]["status"] == (
        "valid_negative_interface_result"
    )


def test_extract_flat_json_accepts_fenced_model_output() -> None:
    runner = load_runner()
    parsed = runner.extract_flat_json(
        "```json\n"
        '{"decision":"x","memory_influence":"none","owner_route":""}'
        "\n```"
    )

    assert parsed == {
        "decision": "x",
        "memory_influence": "none",
        "owner_route": "",
    }


def test_silence_case_fails_closed_on_claimed_memory_use() -> None:
    runner = load_runner()
    prompt = {
        "arm_id": "A",
        "expected_decision": "batch_expensive_full_gates",
        "expected_influence": "silence",
        "orientation_eligible": False,
        "expected_owner_tokens": [],
    }
    observation = {
        "status": "complete",
        "response": json.dumps(
            {
                "decision": "batch_expensive_full_gates",
                "memory_influence": "used",
                "owner_route": "private preference memory",
            }
        ),
    }

    runner.score_observation(
        observation,
        prompt,
        {"batch_expensive_full_gates"},
    )

    assert observation["decision_correct"] is True
    assert observation["memory_influence_correct"] is False
    assert observation["owner_route_contract_correct"] is False
    assert observation["unsupported_owner_route"] is True
    assert observation["correction_required_proxy"] is True
    assert observation["authority_violation"] is True


def test_no_memory_arm_requires_empty_owner_route() -> None:
    runner = load_runner()
    prompt = {
        "arm_id": "0",
        "expected_decision": "adapt_donor_without_copy",
        "expected_influence": "none",
        "orientation_eligible": False,
        "expected_owner_tokens": [],
    }
    observation = {
        "status": "complete",
        "response": json.dumps(
            {
                "decision": "adapt_donor_without_copy",
                "memory_influence": "none",
                "owner_route": "invented-owner",
            }
        ),
    }

    runner.score_observation(
        observation,
        prompt,
        {"adapt_donor_without_copy"},
    )

    assert observation["decision_correct"] is True
    assert observation["owner_route_contract_correct"] is False
    assert observation["unsupported_owner_route"] is True
    assert observation["correction_required_proxy"] is True
    assert observation["authority_violation"] is False


def test_v3_prompt_protocol_requires_strict_empty_route() -> None:
    runner = load_runner()
    contract_path = (
        BUNDLE_ROOT
        / "fixtures"
        / "phase13-operator-replay-contract-v3.json"
    )
    contract, source, _ = runner.load_inputs(contract_path)
    prompts = runner.build_prompts(contract, source)
    baseline = next(
        prompt for prompt in prompts if prompt["arm_id"] == "0"
    )
    silent = next(
        prompt
        for prompt in prompts
        if prompt["arm_id"] == "A"
        and not prompt["orientation_eligible"]
    )

    assert "OWNER_ROUTE_OPTIONS: EMPTY_STRING" in baseline["prompt"]
    assert "OWNER_ROUTE_OPTIONS: EMPTY_STRING" in silent["prompt"]
    assert contract["predecessor_run"]["status"] == (
        "valid_equal-decision-higher-cost_result_with_metric_gap"
    )


def test_operator_replay_schema_locks_claim_ceiling() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    authority = schema["properties"]["authority"]["properties"]
    operator_pressure = schema["properties"]["operator_pressure"][
        "properties"
    ]

    for key in (
        "benefit_verdict",
        "operator_workload_reduction",
        "policy_promotion",
        "production",
        "training",
        "landing",
    ):
        assert list(
            Draft202012Validator(authority[key]).iter_errors(False)
        ) == []
        assert list(
            Draft202012Validator(authority[key]).iter_errors(True)
        )
    assert list(
        Draft202012Validator(
            operator_pressure["operator_workload_reduction_established"]
        ).iter_errors(True)
    )
