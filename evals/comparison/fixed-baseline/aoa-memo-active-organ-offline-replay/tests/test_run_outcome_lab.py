from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_outcome_lab.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "active_organ_outcome_lab",
        RUNNER_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runner():
    return load_runner()


def _digest(character: str = "1") -> str:
    return "sha256:" + (character * 64)


def _consumer_report() -> dict:
    pins = {
        key: _digest(str((index % 8) + 1))
        for index, key in enumerate(
            (
                "sdk_registry",
                "sdk_plan_schema",
                "memo_profile",
                "memo_policy",
                "stack_delivery_core",
                "sdk_dependency_manifest",
            )
        )
    }
    return {
        "created_at": "2026-07-29T09:00:00Z",
        "pins": pins,
        "case_fixture": {"sha256": _digest("9")},
        "seeds": [17, 29, 43],
        "paired_observations": [{} for _ in range(36)],
    }


def test_randomized_assignment_is_deterministic_and_balanced(runner):
    assignments = [
        runner.randomized_assigned_arm(
            f"CO-{case_number:02d}",
            seed,
            (17, 29, 43),
        )
        for seed in (17, 29, 43)
        for case_number in range(1, 13)
    ]

    assert assignments.count("A") == 18
    assert assignments.count("B") == 18
    assert assignments == [
        runner.randomized_assigned_arm(
            f"CO-{case_number:02d}",
            seed,
            (17, 29, 43),
        )
        for seed in (17, 29, 43)
        for case_number in range(1, 13)
    ]


def test_phase6_c21_and_c22_are_owner_contract_valid(runner):
    consumer_report = _consumer_report()
    validator = runner.load_module(
        "active_organ_outcome_contract_test",
        runner.EXPERIMENT_VALIDATOR_PATH,
    )
    c21 = runner.build_c21(consumer_report)
    validator.validate_payload(c21)

    c22 = runner.build_c22(
        consumer_report,
        c21=c21,
        c21_file_digest=_digest("a"),
    )
    c22["preregistration"][
        "manifest_sha256"
    ] = validator.normalized_c22_manifest_sha256(c22)
    validator.validate_payload(c22)

    assert c22["execution"]["randomized"] is True
    assert c22["arms"][0]["memory_treatment"] == "memory_disabled"
    assert c22["arms"][1]["memory_treatment"] == "explicit_pull_only"
    assert c22["arms"][2]["memory_treatment"] == "active_organ_policy_gated"
    assert c22["authority"]["verdict_authority"] is False


def test_outcome_report_schema_forbids_authority_widening(runner):
    schema = runner.load_json(runner.REPORT_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)

    authority = schema["properties"]["authority"]["properties"]
    assert all(
        property_schema["const"] is False
        for property_schema in authority.values()
    )
