from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_agent_local_federation_lab.py"
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "agent-local-federation-cases.json"
REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "agent-local-federation.schema.json"
)
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
        "aoa_active_organ_agent_local_federation_runner_test",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase12_fixture_covers_namespaces_promotions_models_and_faults() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    assert len(fixture["namespaces"]) == 4
    assert len({item["agent_id"] for item in fixture["namespaces"]}) == 4
    assert len({item["role"] for item in fixture["namespaces"]}) == 4
    assert len({item["tenant_id"] for item in fixture["namespaces"]}) == 2
    assert len(fixture["local_cases"]) == 12
    assert len(fixture["promotion_cases"]) == 8
    assert len(fixture["model_pins"]) == 3
    assert fixture["fault_cases"] == [
        "cross_agent_lookup",
        "cross_tenant_lookup",
        "unbounded_weight_delta",
        "access_count_as_utility",
        "namespace_fault_propagation",
        "private_auto_share",
        "direct_local_kag_projection",
        "local_rollback_mutates_shared",
        "consumer_zero_residual",
        "model_specific_hidden_policy",
    ]
    assert sum(
        item["result"] == "memo_candidate"
        for item in fixture["promotion_cases"]
    ) == 3


def test_phase12_report_schema_is_strict_and_non_live() -> None:
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
    authority = schema["properties"]["authority"]["properties"]
    assert authority["live_private_memory_written"]["const"] is False
    assert authority["live_namespace_deployed"]["const"] is False
    assert authority["runtime_promotion_allowed"]["const"] is False
    assert authority["policy_promotion_allowed"]["const"] is False
    assert authority["landing_performed"]["const"] is False


def test_phase12_reference_lab_passes_owner_contracts(tmp_path: Path) -> None:
    runner = load_runner()
    output = tmp_path / "agent-local-federation-report.json"
    report = runner.run_lab(
        agents_root=require_owner_root("AOA_AGENTS_ROOT"),
        sdk_root=require_owner_root("AOA_SDK_ROOT"),
        memo_root=require_owner_root("AOA_MEMO_ROOT"),
        stack_root=require_owner_root("ABYSS_STACK_ROOT"),
        kag_root=require_owner_root("AOA_KAG_ROOT"),
        stats_root=require_owner_root("AOA_STATS_ROOT"),
        output_path=output,
    )

    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert output.exists()
    assert all(report["exit_gate"].values())
    assert all(
        item["detected"] and item["blocked"]
        for item in report["fault_results"]
    )
    arms = {item["arm"]: item for item in report["abcd_comparison"]}
    assert arms["D_reviewed_agent_local"]["safe"] is True
    assert arms["B_unisolated_local"]["safe"] is False
    assert arms["C_auto_shared_local"]["safe"] is False
    assert report["stats_aggregate"]["isolation"]["cross_tenant_leak_count"] == 0
    assert report["stats_aggregate"]["promotion"][
        "silent_shared_truth_count"
    ] == 0
    assert report["cost_quality_speed_result"]["cost"][
        "net_operator_minutes_saved"
    ] > 0
    assert report["authority"]["landing_performed"] is False
