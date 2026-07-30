from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from jsonschema import Draft202012Validator
import pytest


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_consumer_lab.py"


def load_runner():
    spec = importlib.util.spec_from_file_location(
        "active_organ_consumer_lab",
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


def _digest() -> str:
    return "sha256:" + ("1" * 64)


def _report(runner):
    baseline = {
        "selected_object_id": "memo.expected",
        "source_ref": "repo:aoa-memo/memo/expected/object.json",
        "source_current": True,
        "estimated_context_tokens": 1000,
        "bytes_scanned": 4000,
        "filesystem_reads": 12,
        "operator_attention_units": 1,
        "latency_ms": 1.0,
        "correct": True,
        "current": True,
    }
    active = {
        "selected_object_id": "memo.expected",
        "source_route": "repo:aoa-memo/memo/expected/object.json",
        "query_digest": _digest(),
        "recall_intent_id": "intent:test",
        "recall_intent_digest": _digest(),
        "plan_digest": _digest(),
        "recall_packet_ref": "recall-packet:test",
        "recall_packet_digest": _digest(),
        "intervention_decision_ref": "intervention-decision:test",
        "intervention_decision_digest": _digest(),
        "runtime_receipt_id": "runtime-receipt:test",
        "runtime_receipt_digest": _digest(),
        "correct": True,
        "current": True,
        "source_route_correct": True,
        "estimated_context_tokens": 500,
        "bytes_scanned": 2000,
        "filesystem_reads": 2,
        "operator_attention_units": 1,
        "latency_ms": 50.0,
        "delivery_state": "delivered",
        "c20_reason": "delivery_confirmed",
        "unsafe_authority_count": 0,
    }
    summary = {
        "observation_count": 24,
        "outcome_rate": 1.0,
        "currentness_rate": 1.0,
        "source_route_rate": 1.0,
        "mean_latency_ms": 50.0,
        "p95_latency_ms": 60.0,
        "mean_estimated_context_tokens": 500.0,
        "mean_bytes_scanned": 2000.0,
        "mean_filesystem_reads": 2.0,
        "mean_operator_attention_units": 1.0,
        "unsafe_authority_count": 0,
    }
    report = {
        "schema_version": "codex_owner_orientation_consumer_report_v0",
        "created_at": "2026-07-29T09:00:00Z",
        "consumer_id": "codex_owner_orientation_v0",
        "evidence_scope": "source-local-production-like-no-deployment",
        "case_fixture": {
            "case_count": 8,
            "sha256": _digest(),
        },
        "seeds": [17, 29, 43],
        "pins": {
            key: _digest()
            for key in (
                "consumer_report_schema",
                "consumer_runner",
                "consumer_fixture",
                "sdk_plan_schema",
                "sdk_registry",
                "sdk_dependency_manifest",
                "memo_profile",
                "memo_policy",
                "memo_sdk_compatibility",
                "memo_packet_builder",
                "stack_runtime_compatibility",
                "stack_c20_schema",
                "stack_delivery_core",
                "host_contract_examples",
            )
        },
        "arms": {
            "0_verified_current_source_lexical": summary,
            "A_reviewed_explicit_pull_bounded": summary,
        },
        "paired_observations": [
            {
                "seed": (17, 29, 43)[index % 3],
                "case_id": f"CO-{(index % 8) + 1:02d}",
                "recall_mode": "semantic",
                "expected_object_id": "memo.expected",
                "baseline": baseline,
                "active": active,
            }
            for index in range(24)
        ],
        "rollback": {
            "target": "verified-current-no-memory",
            "passed": True,
            "observations": [
                {
                    "seed": seed,
                    "latency_ms": 30.0,
                    "status": "off",
                    "delivery_state": "suppressed",
                    "memory_payload_count": 0,
                    "reason": "policy_silence",
                    "passed": True,
                }
                for seed in (17, 29, 43)
            ],
        },
        "budgets": {
            "p95_latency_ms": 500.0,
            "mean_estimated_context_tokens": 900.0,
            "unsafe_authority_count": 0,
        },
        "exit_gate_passed": True,
        "verdict": "supports bounded source-local A continuation",
        "authority": {
            "production_authorized": False,
            "deployment_authorized": False,
            "policy_promotion_authorized": False,
            "landing_authorized": False,
            "memory_write_authorized": False,
            "effect_authority": "none",
        },
        "limitations": ["Source-local execution is not deployment evidence."],
    }
    report["report_digest"] = runner.normalized_report_digest(report)
    return report


def test_consumer_fixture_has_explicit_modes_and_exact_multimodal_cases(runner):
    fixture = runner.load_json(runner.CASES_PATH)
    cases = fixture["cases"]

    assert len(cases) == 12
    assert len({case["case_id"] for case in cases}) == 12
    assert all(case["recall_mode"] for case in cases)
    by_id = {case["case_id"]: case for case in cases}
    assert by_id["CO-11"]["recall_mode"] == "source_route"
    assert by_id["CO-12"]["recall_mode"] == "lineage"


def test_consumer_report_schema_is_valid_and_report_is_self_digesting(runner):
    schema = runner.load_json(runner.CONSUMER_REPORT_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    report = _report(runner)

    runner.validate_consumer_report(report)
    assert report["report_digest"] == runner.normalized_report_digest(report)


def test_consumer_report_rejects_authority_widening_and_digest_drift(runner):
    widened = _report(runner)
    widened["authority"]["landing_authorized"] = True
    widened["report_digest"] = runner.normalized_report_digest(widened)

    with pytest.raises(runner.ConsumerLabError, match="landing_authorized"):
        runner.validate_consumer_report(widened)

    drifted = _report(runner)
    drifted["report_digest"] = _digest()
    with pytest.raises(runner.ConsumerLabError, match="digest mismatch"):
        runner.validate_consumer_report(drifted)
