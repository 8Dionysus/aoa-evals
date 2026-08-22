from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import jsonschema
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
        "unbound_external_owner",
    }.issubset(report["adversarial_classes_covered"])
    assert report["real_case_count"] == 0
    assert report["seeded_case_count"] == 7


def test_contract_rejects_full_owner_proof_rule_drift() -> None:
    contract = load_json(CONTRACT_PATH)
    contract["oracle_rule"]["oracle"] = "heuristic"

    with pytest.raises(comparison.ContractError, match="oracle_rule"):
        comparison.validate_contract(contract)


def test_contract_rejects_non_v1_fixture_identity() -> None:
    contract = load_json(CONTRACT_PATH)
    cases = load_json(CASES_PATH)
    contract["fixture_id"] = "custom-fixture"
    cases["fixture_id"] = "custom-fixture"

    with pytest.raises(comparison.ContractError, match="fixture_id"):
        comparison.build_report(contract, cases)


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
    assert all(
        result["first_failure_latency_ms_synthetic_proxy"] is not None
        for result in (stale, unknown, wrong, malformed)
    )


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


def test_generic_method_rationale_cannot_explain_a_missing_node(report: dict) -> None:
    static_miss = scenario_result(report, "static_paths", "RVC-006-unexplained-miss")
    assert static_miss["explanation"]
    assert static_miss["unexplained_miss_nodes"] == static_miss["missing_nodes"]


def test_unknown_and_real_evidence_kinds_are_not_admitted_in_seeded_v1() -> None:
    cases = load_json(CASES_PATH)
    unknown = copy.deepcopy(cases)
    unknown["scenarios"][0]["evidence_kind"] = "observed_runtime"
    with pytest.raises(comparison.ContractError, match="evidence_kind"):
        comparison.build_report(load_json(CONTRACT_PATH), unknown)

    real = copy.deepcopy(cases)
    real["scenarios"][0]["evidence_kind"] = "real_session"
    with pytest.raises(comparison.ContractError, match="evidence_kind"):
        comparison.build_report(load_json(CONTRACT_PATH), real)


def test_unrecognized_signal_state_is_normalized_to_blocked_and_escalated() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["signals"]["dependency_graph"]["state"] = "currnt"
    report = comparison.build_report(load_json(CONTRACT_PATH), cases)
    result = scenario_result(report, "hybrid_fail_closed", "RVC-001-source-only-control")

    assert result["state_counts"]["blocked"] == 1
    assert result["fail_closed_escalation"]["triggered"] is True
    assert result["fail_closed_escalation"]["reasons"] == ["blocked"]
    assert result["fail_closed_escalation"]["fallback"] == "full_owner_proof"
    assert result["stale_unknown_behavior"] == "preserved_and_escalated"


def test_successful_signal_states_do_not_look_stale_or_incomplete(report: dict) -> None:
    result = scenario_result(report, "dependency_graph", "RVC-001-source-only-control")
    assert result["state_counts"] == {
        "stale": 0,
        "unknown": 0,
        "malformed": 0,
        "wrong_identity": 0,
        "blocked": 0,
    }
    assert result["stale_unknown_behavior"] == "not_observed"


def test_adversarial_coverage_is_deduplicated_and_schema_valid() -> None:
    cases = load_json(CASES_PATH)
    duplicate = copy.deepcopy(cases["scenarios"][1])
    duplicate["scenario_id"] = "RVC-008-duplicate-stale-class"
    cases["scenarios"].append(duplicate)
    report = comparison.build_report(load_json(CONTRACT_PATH), cases)

    jsonschema.Draft202012Validator(load_json(REPORT_SCHEMA_PATH)).validate(report)
    assert len(report["adversarial_classes_covered"]) == len(set(report["adversarial_classes_covered"]))


def test_latency_weights_are_declared_by_fixture_and_used() -> None:
    cases = load_json(CASES_PATH)
    weights = cases["latency_event_weights_ms_synthetic_proxy"]
    assert weights == {
        "static_paths": 1.5,
        "dependency_graph": 3.5,
        "owner_contracts": 4.0,
        "history_correlation": 5.0,
        "claim_risk": 2.0,
    }
    cases["latency_event_weights_ms_synthetic_proxy"]["static_paths"] = 7.25

    report = comparison.build_report(load_json(CONTRACT_PATH), cases)
    result = scenario_result(report, "static_paths", "RVC-001-source-only-control")

    assert {event["latency_ms_synthetic_proxy"] for event in result["events"]} == {7.25}


def test_static_events_are_deduplicated_by_target() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["changed_paths"] = ["scripts/a.py", "scripts/b.py"]

    report = comparison.build_report(load_json(CONTRACT_PATH), cases)
    result = scenario_result(report, "static_paths", "RVC-001-source-only-control")

    assert [(event["target"], event["attempt"]) for event in result["events"]] == [("source_fast", 1)]
    assert result["unique_attempt_targets"] == 1
    jsonschema.Draft202012Validator(load_json(REPORT_SCHEMA_PATH)).validate(report)


def test_static_activation_overrides_are_rejected_as_unsynchronized() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["method_overrides"] = {
        "static_paths": {"activated_nodes": ["source_fast"]}
    }

    with pytest.raises(comparison.ContractError, match="activated_nodes.*not admitted"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("full_local_release_check_seconds", -1),
        ("targeted_local_route_proxy_seconds", [-1, 4.9]),
    ],
)
def test_negative_wall_clock_proxies_are_rejected(field: str, value: object) -> None:
    cases = load_json(CASES_PATH)
    cases["input_evidence"]["observed_wall_clock_proxies"][field] = value

    with pytest.raises(comparison.ContractError, match="finite non-negative"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


def test_implemented_candidates_cannot_be_marked_missing() -> None:
    contract = load_json(CONTRACT_PATH)
    candidate = next(entry for entry in contract["candidate_catalog"] if entry["method_id"] == "static_paths")
    candidate["status"] = comparison.UNSUPPORTED_METHOD_STATUS
    candidate["reason"] = "custom contract attempts to hide a built-in runner"

    with pytest.raises(comparison.ContractError, match="must remain implemented"):
        comparison.build_report(contract, load_json(CASES_PATH))


def test_empty_owner_proof_oracle_nodes_are_rejected() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["oracle"]["required_nodes"] = []
    cases["scenarios"][0]["oracle"]["owner_proof_nodes"] = []

    with pytest.raises(comparison.ContractError, match="must contain at least one node"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


def test_unknown_owner_proof_cannot_be_scored_as_complete() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][-1]["oracle"]["complete"] = True

    with pytest.raises(comparison.ContractError, match="cannot be complete"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


def test_adversarial_class_requires_its_class_specific_condition() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["adversarial_class"] = "stale_graph"

    with pytest.raises(comparison.ContractError, match="does not match"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


def test_duplicate_signal_nodes_are_rejected_before_event_measurement() -> None:
    cases = load_json(CASES_PATH)
    cases["scenarios"][0]["signals"]["dependency_graph"]["nodes"].append("source_fast")

    with pytest.raises(comparison.ContractError, match="nodes must not contain duplicates"):
        comparison.build_report(load_json(CONTRACT_PATH), cases)


@pytest.mark.parametrize("field", ["family", "description"])
def test_implemented_candidate_strings_are_required(field: str) -> None:
    contract = load_json(CONTRACT_PATH)
    candidate = next(entry for entry in contract["candidate_catalog"] if entry["method_id"] == "static_paths")
    candidate.pop(field)

    with pytest.raises(comparison.ContractError, match="non-empty"):
        comparison.build_report(contract, load_json(CASES_PATH))


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
    assert example["evidence_posture"] == report["evidence_posture"]
    assert example["latency_posture"] == report["latency_posture"]
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
        "evidence_posture",
        "latency_posture",
        "candidate_catalog",
        "adversarial_classes_covered",
        "methods",
        "oracle_rule",
    }.issubset(required)


def test_emitted_report_matches_closed_schema_and_nested_mutations_fail(report: dict) -> None:
    schema = load_json(REPORT_SCHEMA_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    validator.validate(report)

    mutations = {
        "identity": lambda payload: payload["methods"][0]["scenario_results"][0]["identity"].pop("workload_id"),
        "method": lambda payload: payload["methods"][0].__setitem__("method_id", 7),
        "measurement": lambda payload: payload["methods"][0]["measurements"].__setitem__("precision", "one"),
        "scenario": lambda payload: payload["methods"][0]["scenario_results"][0]["oracle"].pop("required_nodes"),
        "event": lambda payload: payload["methods"][1]["scenario_results"][1]["events"][0].__setitem__(
            "latency_ms_synthetic_proxy", "fast"
        ),
        "escalation": lambda payload: payload["methods"][5]["scenario_results"][1][
            "fail_closed_escalation"
        ].pop("fallback"),
        "oracle": lambda payload: payload["methods"][5]["scenario_results"][1]["oracle"].__setitem__(
            "owner_proof_status", "green"
        ),
    }
    for _label, mutate in mutations.items():
        malformed = copy.deepcopy(report)
        mutate(malformed)
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(malformed)


def test_text_rendering_names_seeded_counts_and_synthetic_latency(report: dict) -> None:
    rendered = comparison.render_text(report)
    assert "seeded_fixture=7" in rendered
    assert "real_session=0" in rendered
    assert "synthetic_fixture_proxy" in rendered
    assert "not observed runtime latency" in rendered


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
