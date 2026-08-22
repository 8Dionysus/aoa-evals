from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


PART_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_PATH = PART_ROOT / "scripts" / "run_validation_routing_comparison.py"
CONTRACT_PATH = PART_ROOT / "schemas" / "validation-routing-comparison-v1.contract.json"
REPORT_SCHEMA_PATH = PART_ROOT / "schemas" / "validation-routing-comparison-report-v1.schema.json"
CASES_PATH = PART_ROOT / "fixtures" / "validation-routing-bounded-v1" / "cases.json"
EXAMPLE_PATH = PART_ROOT / "examples" / "validation-routing-comparison.example.json"

if str(SCRIPT_PATH.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PATH.parent))

import run_validation_routing_comparison as comparison  # noqa: E402


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def report() -> dict:
    return comparison.build_report(load_json(CONTRACT_PATH), load_json(CASES_PATH))


def method(report: dict, method_id: str) -> dict:
    return next(entry for entry in report["methods"] if entry["method_id"] == method_id)


def scenario_result(report: dict, method_id: str, scenario_id: str) -> dict:
    entry = method(report, method_id)
    return next(result for result in entry["scenario_results"] if result["scenario_id"] == scenario_id)


def test_report_is_measurement_only_and_covers_required_adversarial_classes(report: dict) -> None:
    assert report["schema_version"] == "validation_routing_comparison_report_v1"
    assert report["claim_posture"] == "measurement_only"
    assert report["policy_verdict"] is None
    assert report["selection_status"] == "deferred_pending_bound_external_campaign"
    assert {
        "stale_graph",
        "unknown_dependency",
        "wrong_candidate_environment_receipt",
        "malformed_receipt",
        "unexplained_miss",
    }.issubset(report["adversarial_classes_covered"])
    assert report["real_case_count"] == 0
    assert report["seeded_case_count"] == 7


def test_peer_identity_is_constant_for_each_scenario(report: dict) -> None:
    for method_entry in report["methods"]:
        for result in method_entry["scenario_results"]:
            assert result["identity"]["candidate_set_id"] == report["comparison_identity"]["candidate_set_id"]
            assert result["identity"]["environment_id"] == report["comparison_identity"]["environment_id"]
            assert set(result["identity"]) == {
                "workload_id",
                "candidate_set_id",
                "environment_id",
                "source_ref",
            }


def test_unsupported_candidate_families_are_explicit_missing_candidates(report: dict) -> None:
    missing = {
        entry["method_id"]: entry
        for entry in report["methods"]
        if entry["implementation_status"] == "unsupported_missing_candidate"
    }
    assert set(missing) == {
        "api_abi",
        "coverage",
        "mutation",
        "kag_relations",
        "llm_proposed_additions",
    }
    assert all(entry["measurements"] is None for entry in missing.values())
    assert all(entry["reason"] for entry in missing.values())


def test_stale_unknown_wrong_and_malformed_states_are_preserved(report: dict) -> None:
    stale = scenario_result(report, "dependency_graph", "RVC-002-stale-graph")
    unknown = scenario_result(report, "dependency_graph", "RVC-003-unknown-dependency")
    wrong = scenario_result(report, "owner_contracts", "RVC-004-wrong-receipt")
    malformed = scenario_result(report, "owner_contracts", "RVC-005-malformed-receipt")

    assert stale["state_counts"]["stale"] == 1
    assert stale["stale_unknown_behavior"] == "preserved_as_incomplete"
    assert unknown["state_counts"]["unknown"] == 1
    assert wrong["state_counts"]["wrong_identity"] == 1
    assert malformed["state_counts"]["malformed"] == 1
    assert all(result["first_failure_latency_ms"] is not None for result in (stale, unknown, wrong, malformed))


def test_hybrid_escalates_without_declaring_a_winner(report: dict) -> None:
    hybrid = method(report, "hybrid_fail_closed")
    by_id = {result["scenario_id"]: result for result in hybrid["scenario_results"]}
    for scenario_id in (
        "RVC-002-stale-graph",
        "RVC-003-unknown-dependency",
        "RVC-004-wrong-receipt",
        "RVC-005-malformed-receipt",
        "RVC-007-unbound-owner",
    ):
        escalation = by_id[scenario_id]["fail_closed_escalation"]
        assert escalation["triggered"] is True
        assert escalation["fallback"] == "full_owner_proof"
        assert escalation["policy_verdict"] is None
    assert hybrid["measurements"]["fail_closed_escalation_count"] == 5


def test_unexplained_miss_and_excess_activation_are_reported(report: dict) -> None:
    static_miss = scenario_result(report, "static_paths", "RVC-006-unexplained-miss")
    claim_summary = method(report, "claim_risk")["measurements"]
    assert static_miss["missing_nodes"] == ["source_fast", "owner_external_kag"]
    assert static_miss["unexplained_miss_nodes"] == ["source_fast", "owner_external_kag"]
    assert claim_summary["excess_node_count"] >= 1


def test_precision_recall_are_null_when_oracle_denominator_is_incomplete(report: dict) -> None:
    unbound = scenario_result(report, "hybrid_fail_closed", "RVC-007-unbound-owner")
    assert unbound["precision_recall_denominator_valid"] is False
    assert unbound["precision"] is None
    assert unbound["recall"] is None
    assert method(report, "hybrid_fail_closed")["measurements"]["precision"] is not None
    assert method(report, "hybrid_fail_closed")["measurements"]["precision"] < 1.0


def test_example_preserves_runner_measurements_and_unsupported_candidates(report: dict) -> None:
    example = load_json(EXAMPLE_PATH)
    assert example["fixture_id"] == report["fixture_id"]
    assert example["claim_posture"] == report["claim_posture"]
    assert example["selection_status"] == report["selection_status"]
    assert example["real_miss_count"] is None

    methods = {entry["method_id"]: entry for entry in report["methods"]}
    for measurement in example["example_measurements"]:
        actual = methods[measurement["method_id"]]["measurements"]
        for key, value in measurement.items():
            if key != "method_id":
                assert actual[key] == value

    unsupported = {
        entry["method_id"]
        for entry in report["methods"]
        if entry["implementation_status"] == "unsupported_missing_candidate"
    }
    assert set(example["unsupported_candidates"]) == unsupported


def test_report_schema_declares_required_measurements() -> None:
    schema = load_json(REPORT_SCHEMA_PATH)
    required = set(schema["required"])
    assert {
        "policy_verdict",
        "candidate_catalog",
        "adversarial_classes_covered",
        "methods",
        "oracle_rule",
    }.issubset(required)


def test_runner_cli_emits_json(tmp_path: Path) -> None:
    output_path = tmp_path / "validation-routing-report.json"
    process = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "--format",
            "json",
            "--output",
            str(output_path),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    parsed_stdout = json.loads(process.stdout)
    parsed_output = load_json(output_path)
    assert parsed_stdout["comparison_identity_digest"] == parsed_output["comparison_identity_digest"]
    assert parsed_output["claim_posture"] == "measurement_only"
