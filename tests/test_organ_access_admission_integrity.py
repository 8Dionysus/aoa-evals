from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = (
    REPO_ROOT
    / "evals"
    / "boundary"
    / "aoa-organ-access-admission-integrity"
)
RUNNER = BUNDLE_ROOT / "runners" / "run_scenarios.py"


def run_runner(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_checked_in_scenarios_match_bounded_expectations() -> None:
    completed = run_runner("run-scenarios")
    assert completed.returncode == 0, completed.stderr or completed.stdout
    report = json.loads(completed.stdout)
    assert report["scenario_count"] == 11
    assert report["passed_count"] == 11
    assert report["failed_count"] == 0
    assert report["verdict"] == "supports bounded claim"

    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)


def test_valid_packet_and_honest_insufficient_evidence_are_accepted() -> None:
    for name in ("valid-read.json", "insufficient-read.json"):
        completed = run_runner(
            "validate-packet", str(BUNDLE_ROOT / "fixtures" / "packets" / name)
        )
        assert completed.returncode == 0, completed.stderr or completed.stdout
        payload = json.loads(completed.stdout)
        assert payload["accepted_by_source_contract"] is True
        assert payload["issues"] == []


def test_example_report_matches_report_contract() -> None:
    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(
            encoding="utf-8"
        )
    )
    example = json.loads(
        (BUNDLE_ROOT / "reports" / "example-report.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator(schema).validate(example)
    assert example["limitations"]
    assert example["failed_count"] == 0


@pytest.mark.parametrize(
    "mutation",
    [
        "failed_count",
        "passed_count",
        "scenario_count",
        "failed_outcome",
    ],
)
def test_positive_report_rejects_self_contradictory_counts_and_outcomes(
    mutation: str,
) -> None:
    schema = json.loads(
        (BUNDLE_ROOT / "reports" / "summary.schema.json").read_text(
            encoding="utf-8"
        )
    )
    example = json.loads(
        (BUNDLE_ROOT / "reports" / "example-report.json").read_text(
            encoding="utf-8"
        )
    )
    payload = deepcopy(example)
    if mutation == "failed_count":
        payload["failed_count"] = 1
    elif mutation == "passed_count":
        payload["passed_count"] = 10
    elif mutation == "scenario_count":
        payload["scenario_count"] = 10
    else:
        payload["per_scenario_breakdown"][0]["outcome"] = "fail"

    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)


def test_negative_scenarios_cover_forbidden_admission_inferences() -> None:
    expected_codes = set()
    for scenario_path in sorted(
        (BUNDLE_ROOT / "fixtures" / "scenarios").glob("*.json")
    ):
        scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
        expected_codes.update(scenario["expected_codes"])

    assert "endpoint_ready_does_not_imply_result_grounded" in expected_codes
    assert "central_eval_does_not_imply_owner_accepted" in expected_codes
    assert "read_or_candidate_plane_cannot_authorize_effect" in expected_codes
    assert "admission_change_not_authorized_by_central_proof" in expected_codes
    assert (
        "axis_evidence_expired_within_observation_window:freshness_satisfied"
        in expected_codes
    )
    assert "positive_verdict_requires_asserted_evidence" in expected_codes
    assert "axis_revision_slot_mismatch:deployed" in expected_codes
    assert "observation_window_invalid" in expected_codes
