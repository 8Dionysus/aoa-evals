from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_mechanical_lifecycle_lab.py"
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "mechanical-lifecycle-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "mechanical-lifecycle.schema.json"
STRICT_SIBLING_COMPAT_ENV = "AOA_EVALS_STRICT_SIBLING_COMPAT"


def require_owner_root(env_name: str) -> Path:
    configured = os.environ.get(env_name)
    if configured:
        root = Path(configured).expanduser().resolve()
        if root.is_dir():
            return root
        pytest.fail(f"{env_name} points to a missing owner root: {root}")

    message = (
        f"{env_name} is required for the cross-owner reference lab; "
        "supply explicit owner roots in a sibling-compatibility lane"
    )
    if os.environ.get(STRICT_SIBLING_COMPAT_ENV, "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }:
        pytest.fail(message)
    pytest.skip(message)


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "aoa_active_organ_mechanical_lifecycle_runner_test",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase10_fixture_covers_exact_lifecycle_and_failure_surface() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    assert fixture["mechanical_classes"] == [
        "projection_invalidation",
        "projection_rebuild",
        "compaction",
        "explicit_ephemeral_ttl",
        "queue_cancellation",
        "owner_approved_archive_deadline",
        "cache_expiry",
        "generation_rollover",
        "obsolete_derived_artifact_removal",
    ]
    assert fixture["semantic_proposal_classes"] == [
        "conflict",
        "merge_split",
        "narrowed_applicability",
        "supersession",
        "retraction",
        "archive",
        "temperature_salience_change",
        "retention_change",
    ]
    assert len(fixture["fault_cases"]) == 13
    assert {case["fault"] for case in fixture["fault_cases"]} == {
        "exact_duplicate",
        "idempotency_payload_mismatch",
        "stale_retry",
        "concurrent_conflict",
        "crash_before_commit_retry",
        "crash_after_commit_before_ack",
        "projection_failure_forward_repair",
        "reordered_events",
        "missed_deadline",
        "explicit_cancellation",
        "concurrent_reader_atomicity",
        "semantic_execution_refusal",
        "operator_attention_overflow",
    }
    assert fixture["operator_attention_budget"] == 3
    assert "privacy_erasure" in fixture["forgetting_taxonomy"]
    assert "model_unlearning" in fixture["forgetting_taxonomy"]


def test_phase10_report_schema_and_digest_helper_are_strict() -> None:
    runner = load_runner()
    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)

    payload = {
        "b": 2,
        "a": 1,
        "report_digest": "sha256:" + ("0" * 64),
    }
    assert runner.canonical_digest(
        payload,
        exclude={"report_digest"},
    ) == runner.canonical_digest({"a": 1, "b": 2})
    assert schema["properties"]["authority"]["properties"][
        "landing_performed"
    ]["const"] is False
    assert schema["properties"]["sampling"]["properties"][
        "runtime_promotion_allowed"
    ]["const"] is False
    assert schema["properties"]["exit_gate"]["properties"][
        "partial_projection_fail_closed"
    ]["const"] is True


def test_phase10_reference_lab_passes_owner_contracts(
    tmp_path: Path,
) -> None:
    runner = load_runner()
    memo_root = require_owner_root("AOA_MEMO_ROOT")
    kag_root = require_owner_root("AOA_KAG_ROOT")
    output = tmp_path / "mechanical-lifecycle-report.json"

    report = runner.run_lab(
        memo_root=memo_root,
        kag_root=kag_root,
        output_path=output,
    )

    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert output.exists()
    assert report["exit_gate"]["passed"] is True
    assert report["summary"] == {
        "mechanical_classes_passed": 9,
        "fault_cases_passed": 13,
        "semantic_proposals_preserved": 8,
        "semantic_effects": 0,
        "double_commits": 0,
        "mixed_active_states": 0,
        "provenance_scope_failures": 0,
        "unfinished_erase_misreported_deleted": 0,
    }
    assert report["sampling"]["human_operator_sampling_status"] == "not_performed"
    assert report["sampling"]["runtime_promotion_allowed"] is False
    assert report["authority"]["landing_performed"] is False
