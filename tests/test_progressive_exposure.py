from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "evals/boundary/aoa-organ-access-admission-integrity"


def _runner_module():
    path = BUNDLE / "runners/review_exposure.py"
    spec = importlib.util.spec_from_file_location("review_exposure", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_progressive_exposure_matched_fixtures_and_report_contract() -> None:
    generator = BUNDLE / "runners/generate_exposure_fixtures.py"
    generated = subprocess.run(
        [sys.executable, str(generator), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert generated.returncode == 0, generated.stdout + generated.stderr

    runner = BUNDLE / "runners/review_exposure.py"
    result = subprocess.run(
        [sys.executable, str(runner), "run-scenarios"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    schema = json.loads(
        (BUNDLE / "reports/progressive-exposure.schema.json").read_text(
            encoding="utf-8"
        )
    )
    errors = sorted(Draft202012Validator(schema).iter_errors(report), key=str)
    assert not errors
    assert report["integrity_verdict"] == "supports_bounded_claim"
    assert report["economy"]["status"] == "not_run_baseline_admission_missing"
    assert report["activation_authorized"] is False
    assert report["execution_authorized"] is False
    assert report["matched_selection"]["same_selection"] is True
    assert report["visibility_comparison"]["candidate_minus_default_tokens"] is None
    assert {
        item["mode"] for item in report["fixture_breakdown"]
    } == {
        "default_off",
        "explicit_candidate",
        "feature_disabled_baseline_ready",
        "feature_enabled_baseline_missing",
    }


def test_progressive_exposure_rejects_malformed_and_unmatched_inputs() -> None:
    runner = _runner_module()
    malformed = {
        "schema_version": "aoa_progressive_exposure_fixture_v1",
        "fixture_id": "malformed",
        "mode": "default_off",
        "source_selection_digest": None,
        "plan": {"capability": {}, "visible_tools": []},
        "expected": {},
    }
    issues = runner.review_fixture(malformed)
    assert "selection_identity_missing" in issues
    assert "plan_binding_missing" in issues

    fixture = json.loads(
        (BUNDLE / "fixtures/exposure/02-explicit-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    fixture["plan"]["requested_primitive_ids"] = ["different-primitive"]
    issues = runner.review_fixture(fixture)
    assert "source_selection_digest_invalid" in issues
    assert "visible_tool_selection_mismatch" in issues


def _rehash_plan(runner, fixture: dict) -> None:
    snapshot = fixture["plan"]["rendered_snapshot"]
    snapshot["snapshot_id"] = runner.digest(
        {key: value for key, value in snapshot.items() if key != "snapshot_id"}
    )
    plan = fixture["plan"]
    plan["plan_id"] = runner.digest(
        {key: value for key, value in plan.items() if key not in {"plan_id", "claim_limit"}}
    )


def test_progressive_exposure_binds_immutable_identity_and_nested_versions() -> None:
    runner = _runner_module()
    fixture = json.loads(
        (BUNDLE / "fixtures/exposure/02-explicit-candidate.json").read_text(
            encoding="utf-8"
        )
    )

    changed_identity = copy.deepcopy(fixture)
    changed_identity["plan"]["capability"]["schema_digest"] = "sha256:" + "e" * 64
    changed_identity["plan"]["visible_tools"][0]["schema_digest"] = "sha256:" + "e" * 64
    changed_identity["plan"]["rendered_snapshot"]["tools"][0]["schema_digest"] = (
        "sha256:" + "e" * 64
    )
    tools = changed_identity["plan"]["visible_tools"]
    snapshot = changed_identity["plan"]["rendered_snapshot"]
    snapshot["rendered_schema_digest"] = runner.digest(tools)
    snapshot["rendered_bytes"] = len(runner.canonical(tools))
    snapshot["rendered_tokens"] = max(1, (snapshot["rendered_bytes"] + 3) // 4)
    _rehash_plan(runner, changed_identity)
    assert "source_selection_digest_invalid" in runner.review_fixture(changed_identity)

    unknown_versions = copy.deepcopy(fixture)
    unknown_versions["plan"]["schema_version"] = "aoa_organ_exposure_plan_v2"
    unknown_versions["plan"]["rendered_snapshot"]["schema_version"] = (
        "aoa_organ_exposure_snapshot_v2"
    )
    _rehash_plan(runner, unknown_versions)
    issues = runner.review_fixture(unknown_versions)
    assert "plan_schema_version_invalid" in issues
    assert "snapshot_schema_version_invalid" in issues


def test_progressive_exposure_rejects_candidate_refusal_reasons() -> None:
    runner = _runner_module()
    fixture = json.loads(
        (BUNDLE / "fixtures/exposure/02-explicit-candidate.json").read_text(
            encoding="utf-8"
        )
    )
    fixture["plan"]["refusal_reasons"] = ["baseline_not_ready"]
    _rehash_plan(runner, fixture)
    assert "candidate_refusal_reasons_present" in runner.review_fixture(fixture)
