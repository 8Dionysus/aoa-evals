from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys

import pytest
from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_identity_bound_method_comparison.py"
APPLY_SCHEMA_PATH = BUNDLE_ROOT / "fixtures" / "apply-packet.schema.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "summary.schema.json"
MANUAL_CASE_PATH = BUNDLE_ROOT / "fixtures" / "manual-case-trace.json"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "identity_bound_method_comparison",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def digest(character: str = "1") -> str:
    return "sha256:" + (character * 64)


def posture(identifier: str, status: str = "known") -> dict:
    return {"status": status, "id": identifier if status == "known" else None}


def measurement(value: float, unit: str) -> dict:
    return {"status": "known", "value": value, "unit": unit}


def state(status: str, unit: str) -> dict:
    return {"status": status, "value": None, "unit": unit}


def identity(source_digest: str, route: str = "treatment-A", cache_status: str = "known", resource_status: str = "known") -> dict:
    return {
        "workload_id": "workload-identity-contract-01",
        "candidate_or_source_identity": digest("2"),
        "source_ref_or_digest": source_digest,
        "environment_id": "env-class-A",
        "route_or_treatment_identity": route,
        "evidence_class": "reviewed-owner-packet",
        "acceptance_target": "owner-local-observation-only",
        "cache_posture": posture("cache-disabled", cache_status),
        "resource_posture": posture("resource-class-A", resource_status),
    }


def observation(runner, unit_id: str, method_id: str, *, origin: str = "observed", review_status: str = "reviewed", route: str = "treatment-A", cache_status: str = "known", resource_status: str = "known") -> dict:
    metrics = {
        "wall_seconds": measurement(10.0 if method_id == runner.METHOD_IDS[0] else 8.0, "seconds"),
        "cpu_ms": measurement(100.0, "milliseconds"),
        "peak_rss_kib": measurement(2048.0, "kibibytes"),
        "io_read_bytes": measurement(1000.0, "bytes"),
        "io_write_bytes": measurement(200.0, "bytes"),
        "setup_startup_seconds": measurement(1.0, "seconds"),
        "first_failure_latency_seconds": state("null", "seconds"),
        "retry_amplification": state("unobservable", "ratio"),
    }
    return {
        "unit_id": unit_id,
        "method_id": method_id,
        "identity": identity(digest("1"), route, cache_status, resource_status),
        "review_status": review_status,
        "measurement_origin": origin,
        "evidence_refs": [f"owner-packet:{unit_id}:{method_id}"],
        "metrics": metrics,
    }


def packet(runner, *, origin: str = "observed") -> dict:
    observations = [
        observation(runner, "unit-01", "legacy_serial_full_release", origin=origin),
        observation(runner, "unit-01", "owner_focused_affected_only", origin=origin),
    ]
    observation_artifacts = [
        {
            "ref": row["evidence_refs"][0],
            "digest": digest("3"),
            "kind": "public-safe-observation",
            "evidence_class": "reviewed-owner-packet",
        }
        for row in observations
    ]
    return {
        "schema_version": "identity_bound_method_comparison_apply_v1",
        "eval_name": "aoa-identity-bound-method-comparison",
        "verdict": "exact_fit",
        "owner": "aoa-evals",
        "source_ref": "owner-packet:source",
        "source_digest": digest("1"),
        "environment": {
            "environment_id": "env-class-A",
            "runtime_id": "runtime-contract-v1",
            "source_ref": "owner-packet:source",
            "source_digest": digest("1"),
            "cache_posture": posture("cache-disabled"),
            "resource_posture": posture("resource-class-A"),
        },
        "command": {
            "argv": ["owner-declared", "future-apply"],
            "cwd": "/isolated/owner-worktree",
            "timeout_seconds": 30,
            "accepted_exit_codes": [0],
        },
        "prerequisites": [
            {"id": "source-bound", "required": True, "status": "known", "evidence_ref": "owner-packet:source"}
        ],
        "artifacts": [
            {"ref": "artifact:apply-contract", "digest": digest("2"), "kind": "public-safe-contract", "evidence_class": "public-safe-contract"},
            *observation_artifacts,
        ],
        "pass_criteria": ["identity tuple matches", "unknown is not zero"],
        "effect_authority": "owner-local-observation-only",
        "expected_effect": "report observation disposition only",
        "proof_authority": False,
        "proof_limit": "no central proof, causal, policy, winner, or acceptance claim",
        "comparison": {
            "mode": "fixed-baseline",
            "baseline_method_id": "legacy_serial_full_release",
            "method_ids": list(runner.METHOD_IDS),
            "manual_case_ids": ["positive_exact_identity_match"],
        },
        "observations": observations,
    }


@pytest.fixture(scope="module")
def runner():
    return load_runner()


def test_source_schemas_and_manual_cases_are_valid(runner) -> None:
    apply_schema = json.loads(APPLY_SCHEMA_PATH.read_text(encoding="utf-8"))
    report_schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(apply_schema)
    Draft202012Validator.check_schema(report_schema)
    manual = json.loads(MANUAL_CASE_PATH.read_text(encoding="utf-8"))
    assert manual["method_ids"] == list(runner.METHOD_IDS)
    assert {case["kind"] for case in manual["cases"]} == {"positive", "negative", "collision", "regression"}


def test_observed_identity_match_is_narrow_and_deterministic(runner) -> None:
    payload = packet(runner)
    first = runner.build_report(payload)
    second = runner.build_report(copy.deepcopy(payload))
    assert first == second
    assert first["verdict"] == "matched_observation_only"
    assert first["policy_verdict"] is None
    assert first["admission"]["eligible_real_pairs"] == 1
    assert first["admission"]["matched_pair_count"] == 1
    assert first["comparison_units"][0]["observed_pair_count"] == 1
    assert first["admission"]["method_effect_admitted"] is False
    assert first["comparison_units"][0]["disposition"] == "matched_observation_only"
    assert [item["value"] for item in first["comparison_units"][0]["metric_coverage"]["wall_seconds"]["observed_values"]] == [10.0, 8.0]
    assert first["comparison_units"][0]["metric_coverage"]["first_failure_latency_seconds"]["state_counts"]["null"] == 2
    assert first["comparison_units"][0]["metric_coverage"]["retry_amplification"]["state_counts"]["unobservable"] == 2
    Draft202012Validator(json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))).validate(first)


def test_report_preserves_matched_identity_and_evidence_provenance(runner) -> None:
    payload = packet(runner)
    report = runner.build_report(payload)
    binding = report["comparison_units"][0]["matched_identity_bindings"][0]

    assert binding["method_ids"] == [
        "legacy_serial_full_release",
        "owner_focused_affected_only",
    ]
    assert binding["identity"]["candidate_or_source_identity"] == digest("2")
    assert binding["identity"]["source_ref_or_digest"] == digest("1")
    assert binding["identity"]["environment_id"] == "env-class-A"
    assert {item["method_id"] for item in binding["evidence_provenance"]} == {
        "legacy_serial_full_release",
        "owner_focused_affected_only",
    }
    assert {item["digest"] for item in binding["evidence_provenance"]} == {digest("3")}

    changed = copy.deepcopy(payload)
    for row in changed["observations"]:
        row["identity"]["candidate_or_source_identity"] = digest("9")
    assert runner.build_report(changed) != report


def test_report_schema_requires_provenance_binding_for_positive_unit(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_identity_bindings"] = []
    errors = list(
        Draft202012Validator(json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))).iter_errors(report)
    )
    assert any(
        list(error.absolute_path)[-1:] == ["matched_identity_bindings"]
        for error in errors
    )


def test_report_schema_requires_binding_cardinality_parity(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_pair_count"] = 2
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_a_matched_unit_for_positive_verdict(runner) -> None:
    report = runner.build_report(packet(runner))
    report["verdict"] = "matched_observation_only"
    report["admission"]["matched_unit_count"] = 0
    report["admission"]["matched_pair_count"] = 0
    report["admission"]["eligible_real_pairs"] = 0
    report["comparison_units"][0]["disposition"] = "unmatched"
    report["comparison_units"][0]["matched_pair_count"] = 0
    report["comparison_units"][0]["observed_pair_count"] = 0
    report["comparison_units"][0]["matched_identity_bindings"] = []
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_identity_match_for_admitted_unit(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["identity_match"] = False
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_observed_metric_coverage_for_positive_unit(runner) -> None:
    report = runner.build_report(packet(runner))
    for coverage in report["comparison_units"][0]["metric_coverage"].values():
        coverage["observed_values"] = []
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_baseline_and_candidate_metric_methods(runner) -> None:
    report = runner.build_report(packet(runner))
    for coverage in report["comparison_units"][0]["metric_coverage"].values():
        for observed_value in coverage["observed_values"]:
            observed_value["method_id"] = runner.METHOD_IDS[0]
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_provenance_for_both_binding_methods(runner) -> None:
    report = runner.build_report(packet(runner))
    binding = report["comparison_units"][0]["matched_identity_bindings"][0]
    for provenance in binding["evidence_provenance"]:
        provenance["method_id"] = runner.METHOD_IDS[2]
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_measured_candidate_in_admitted_binding(runner) -> None:
    report = runner.build_report(packet(runner))
    unit = report["comparison_units"][0]
    unit["method_ids"].append(runner.METHOD_IDS[2])
    for coverage in unit["metric_coverage"].values():
        for observed_value in coverage["observed_values"]:
            observed_value["method_id"] = runner.METHOD_IDS[2]
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_unmatched_pair_counts_and_bindings_zero(runner) -> None:
    report = runner.build_report(packet(runner))
    unit = report["comparison_units"][0]
    unit["disposition"] = "unmatched"
    unit["identity_match"] = False
    unit["matched_pair_count"] = 1
    unit["observed_pair_count"] = 0
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_canonical_metric_units(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["metric_coverage"]["wall_seconds"]["observed_values"][0]["unit"] = "milliseconds"
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_baseline_in_matched_binding(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_identity_bindings"][0]["method_ids"] = [
        runner.METHOD_IDS[1],
        runner.METHOD_IDS[2],
    ]
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_requires_binding_methods_in_enclosing_unit(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_identity_bindings"][0]["method_ids"] = [
        runner.METHOD_IDS[0],
        runner.METHOD_IDS[2],
    ]
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_restricts_binding_identity_evidence_class(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_identity_bindings"][0]["identity"]["evidence_class"] = "generated-reader"
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_schema_matches_binding_identity_and_provenance_class(runner) -> None:
    report = runner.build_report(packet(runner))
    report["comparison_units"][0]["matched_identity_bindings"][0]["identity"]["evidence_class"] = "public-safe-contract"
    errors = list(
        Draft202012Validator(
            json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
        ).iter_errors(report)
    )
    assert errors


def test_report_order_is_independent_of_observation_order(runner) -> None:
    payload = packet(runner)
    extra_rows = [
        observation(runner, "unit-00", method_id)
        for method_id in ("owner_focused_affected_only", "legacy_serial_full_release")
    ]
    payload["observations"].extend(extra_rows)
    payload["artifacts"].extend(
        {
            "ref": row["evidence_refs"][0],
            "digest": digest(str(index + 5)),
            "kind": "public-safe-observation",
            "evidence_class": "reviewed-owner-packet",
        }
        for index, row in enumerate(extra_rows)
    )

    reordered = copy.deepcopy(payload)
    reordered["observations"].reverse()

    assert runner.build_report(reordered) == runner.build_report(payload)
    assert [unit["unit_id"] for unit in runner.build_report(reordered)["comparison_units"]] == [
        "unit-00",
        "unit-01",
    ]


def test_identity_mismatch_is_unmatched_and_visible(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["identity"]["route_or_treatment_identity"] = "treatment-B"
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert report["verdict"] == "not_admitted"
    assert unit["disposition"] == "unmatched"
    assert "identity.route_or_treatment_identity" in unit["mismatched_fields"]
    assert report["unmatched_cases"][0]["mismatched_fields"]


def test_mutable_source_ref_is_not_an_observation_binding(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["identity"]["source_ref_or_digest"] = payload["source_ref"]
    with pytest.raises(runner.ContractError, match="source_ref_or_digest"):
        runner.build_report(payload)


def test_candidate_identity_must_be_digest_pinned(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["identity"]["candidate_or_source_identity"] = "candidate-A"
    with pytest.raises(runner.ContractError, match="candidate_or_source_identity"):
        runner.build_report(payload)


def test_unmatched_observed_rows_do_not_enter_observed_values(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["review_status"] = "provisional"
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "unmatched"
    assert unit["metric_coverage"]["wall_seconds"]["observed_values"] == []


def test_unmatched_controlled_candidate_does_not_hide_observed_pair(runner) -> None:
    payload = packet(runner)
    extra = observation(
        runner,
        "unit-01",
        "claim_evidence_activated_subgraph_or_tiered",
        origin="controlled",
        route="treatment-B",
    )
    payload["observations"].append(extra)
    payload["artifacts"].append(
        {
            "ref": extra["evidence_refs"][0],
            "digest": digest("4"),
            "kind": "public-safe-observation",
            "evidence_class": "reviewed-owner-packet",
        }
    )
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "matched_observation_only"
    assert [item["value"] for item in unit["metric_coverage"]["wall_seconds"]["observed_values"]] == [10.0, 8.0]
    assert unit["metric_coverage"]["wall_seconds"]["controlled_values"] == []


def test_eligible_real_pairs_count_only_observed_pairs(runner) -> None:
    payload = packet(runner)
    extra = observation(
        runner,
        "unit-01",
        "claim_evidence_activated_subgraph_or_tiered",
        origin="controlled",
    )
    payload["observations"].append(extra)
    payload["artifacts"].append(
        {
            "ref": extra["evidence_refs"][0],
            "digest": digest("4"),
            "kind": "public-safe-observation",
            "evidence_class": "reviewed-owner-packet",
        }
    )
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "matched_observation_only"
    assert unit["matched_pair_count"] == 2
    assert unit["observed_pair_count"] == 1
    assert report["admission"]["matched_pair_count"] == 2
    assert report["admission"]["eligible_real_pairs"] == 1


def test_eligible_controlled_pair_populates_controlled_values(runner) -> None:
    report = runner.build_report(packet(runner, origin="controlled"))
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "controlled_accounting_only"
    assert [item["value"] for item in unit["metric_coverage"]["wall_seconds"]["controlled_values"]] == [10.0, 8.0]


def test_observed_pair_requires_jointly_known_metric(runner) -> None:
    payload = packet(runner)
    payload["observations"] = [
        {
            **row,
            "metrics": {
                metric_name: state("unknown", unit)
                for metric_name, unit in runner.CANONICAL_METRIC_UNITS.items()
            },
        }
        for row in payload["observations"]
    ]
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert report["verdict"] == "not_admitted"
    assert unit["disposition"] == "unmatched"
    assert "metric_coverage.no_jointly_known_metric" in unit["mismatched_fields"]
    assert report["admission"]["eligible_real_pairs"] == 0


def test_metric_units_are_canonical_before_admission(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["metrics"]["wall_seconds"]["unit"] = "milliseconds"
    with pytest.raises(runner.ContractError, match="wall_seconds"):
        runner.build_report(payload)


def test_non_finite_metric_values_and_json_literals_are_rejected(runner, tmp_path) -> None:
    payload = packet(runner)
    payload["observations"][1]["metrics"]["wall_seconds"]["value"] = float("nan")
    with pytest.raises(runner.ContractError, match="must be finite"):
        runner.build_report(payload)

    input_path = tmp_path / "non-finite.json"
    input_path.write_text("{\"value\": NaN}\n", encoding="utf-8")
    with pytest.raises(runner.ContractError, match="non-finite JSON"):
        runner._load_json(input_path)


def test_timeout_seconds_overflow_is_rejected(runner, tmp_path) -> None:
    input_path = tmp_path / "overflow-timeout.json"
    serialized = json.dumps(packet(runner), indent=2).replace(
        '"timeout_seconds": 30', '"timeout_seconds": 1e999'
    )
    input_path.write_text(serialized, encoding="utf-8")
    loaded = runner._load_json(input_path)
    assert loaded["command"]["timeout_seconds"] == float("inf")
    with pytest.raises(runner.ContractError, match="timeout_seconds"):
        runner.build_report(loaded)


def test_observation_evidence_must_be_declared_and_digest_pinned(runner) -> None:
    payload = packet(runner)
    payload["observations"][1]["evidence_refs"] = ["owner-packet:missing-evidence"]
    with pytest.raises(runner.ContractError, match="evidence_ref"):
        runner.build_report(payload)


def test_disallowed_observation_evidence_class_is_rejected(runner) -> None:
    payload = packet(runner)
    evidence_ref = payload["observations"][1]["evidence_refs"][0]
    artifact = next(item for item in payload["artifacts"] if item["ref"] == evidence_ref)
    artifact["evidence_class"] = "generated-reader"
    with pytest.raises(runner.ContractError, match="disallowed evidence class"):
        runner.build_report(payload)


def test_derived_observation_artifact_kind_is_rejected(runner) -> None:
    payload = packet(runner)
    evidence_ref = payload["observations"][1]["evidence_refs"][0]
    artifact = next(item for item in payload["artifacts"] if item["ref"] == evidence_ref)
    artifact["kind"] = "generated-reader"
    artifact["evidence_class"] = "public-safe-contract"
    with pytest.raises(runner.ContractError, match="disallowed artifact kind"):
        runner.build_report(payload)


def test_observed_origin_requires_reviewed_status(runner) -> None:
    payload = packet(runner)
    for row in payload["observations"]:
        row["review_status"] = "controlled"
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert report["verdict"] == "not_admitted"
    assert unit["disposition"] == "unmatched"
    assert "review_status.baseline_observed_requires_reviewed" in unit["mismatched_fields"]
    assert "review_status.owner_focused_affected_only_observed_requires_reviewed" in unit["mismatched_fields"]


def test_report_publishes_canonical_evidence_class_allowlist(runner) -> None:
    report = runner.build_report(packet(runner))
    assert report["identity_contract"]["allowed_evidence_classes"] == sorted(
        runner.ALLOWED_OBSERVATION_EVIDENCE_CLASSES
    )


def test_unobservable_origin_is_unmatched(runner) -> None:
    payload = packet(runner, origin="unobservable")
    for row in payload["observations"]:
        row["metrics"] = {
            metric_name: state("unobservable", runner.CANONICAL_METRIC_UNITS[metric_name])
            for metric_name in runner.METRIC_NAMES
        }
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "unmatched"
    assert "measurement_origin.baseline" in unit["mismatched_fields"]
    assert report["admission"]["eligible_real_pairs"] == 0


def test_unobservable_origin_cannot_carry_known_metric(runner) -> None:
    with pytest.raises(runner.ContractError, match="measurement_origin=unobservable"):
        runner.build_report(packet(runner, origin="unobservable"))


def test_unknown_cache_or_resource_is_not_zero(runner) -> None:
    payload = packet(runner)
    payload["observations"][0]["identity"]["cache_posture"] = posture("cache-disabled", "unknown")
    payload["observations"][1]["identity"]["cache_posture"] = posture("cache-disabled", "unknown")
    report = runner.build_report(payload)
    unit = report["comparison_units"][0]
    assert unit["disposition"] == "unmatched"
    assert "identity.cache_posture.status" in unit["mismatched_fields"]
    assert report["admission"]["unknown_is_not_zero"] is True


def test_source_digest_mismatch_fails_closed(runner) -> None:
    payload = packet(runner)
    payload["environment"]["source_digest"] = digest("9")
    with pytest.raises(runner.ContractError, match="source_digest"):
        runner.build_report(payload)


def test_duplicate_unit_method_collision_fails_before_report(runner) -> None:
    payload = packet(runner)
    payload["observations"].append(copy.deepcopy(payload["observations"][0]))
    with pytest.raises(runner.ContractError, match="duplicate observation collision"):
        runner.build_report(payload)


def test_synthetic_latency_is_controlled_accounting_only(runner) -> None:
    report = runner.build_report(packet(runner, origin="synthetic"))
    unit = report["comparison_units"][0]
    coverage = unit["metric_coverage"]["wall_seconds"]
    assert report["verdict"] == "not_admitted"
    assert unit["disposition"] == "controlled_accounting_only"
    assert coverage["observed_values"] == []
    assert coverage["synthetic_count"] == 2
    assert report["policy_verdict"] is None


def test_partial_fit_is_rejected_and_all_methods_are_declared(runner) -> None:
    payload = packet(runner)
    payload["verdict"] = "partial_fit"
    with pytest.raises(runner.ContractError, match="verdict"):
        runner.build_report(payload)
    assert set(runner.METHOD_IDS) == set(json.loads(MANUAL_CASE_PATH.read_text(encoding="utf-8"))["method_ids"])


def test_synthetic_manual_case_keeps_baseline_visible(runner) -> None:
    manual = json.loads(MANUAL_CASE_PATH.read_text(encoding="utf-8"))
    case = next(item for item in manual["cases"] if item["case_id"] == "synthetic_latency_accounting_seal")
    assert runner.METHOD_IDS[0] in case["methods"]
    assert "controlled_same_candidate_seeded_fault" in case["methods"]
