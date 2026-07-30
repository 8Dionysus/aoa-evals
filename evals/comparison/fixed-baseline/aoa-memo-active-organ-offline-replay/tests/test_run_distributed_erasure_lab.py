from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_distributed_erasure_lab.py"
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "distributed-erasure-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "distributed-erasure.schema.json"
EVAL_OWNER_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "erasure-owner-extension.schema.json"
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
        "aoa_active_organ_distributed_erasure_runner_test",
        RUNNER_PATH,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_phase11_fixture_covers_exact_erasure_surface_and_fault_set() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    assert [item["surface_id"] for item in fixture["surfaces"]] == [
        "ER0",
        "ER1",
        "ER2",
        "ER3",
        "ER4",
        "ER5",
        "ER6",
        "ER7",
        "ER8",
        "ER9",
    ]
    assert len({item["worker_owner"] for item in fixture["surfaces"]}) == 10
    assert fixture["fault_cases"] == [
        "missing_surface",
        "missing_receipt",
        "broken_positive_control",
        "probe_retains_subject_material",
        "rebuild_restores_material",
        "hidden_residue",
        "unlearning_obligation_residue",
        "tombstone_identity_leak",
        "missing_required_race_probe",
        "owner_extension_binding_drift",
    ]
    assert "model_checkpoint_or_unlearning_obligation" in next(
        item["material_classes"]
        for item in fixture["surfaces"]
        if item["surface_id"] == "ER8"
    )
    assert "landing" in fixture["forbidden_effects"]


def test_phase11_report_and_eval_owner_schemas_are_strict() -> None:
    runner = load_runner()
    report_schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    owner_schema = json.loads(EVAL_OWNER_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(report_schema)
    Draft202012Validator.check_schema(owner_schema)

    payload = {
        "b": 2,
        "a": 1,
        "report_digest": "sha256:" + ("0" * 64),
    }
    assert runner.canonical_digest(
        payload,
        exclude={"report_digest"},
    ) == runner.canonical_digest({"a": 1, "b": 2})
    authority = report_schema["properties"]["authority"]["properties"]
    assert authority["landing_performed"]["const"] is False
    assert authority["live_private_data_deleted"]["const"] is False
    sampling = report_schema["properties"]["sampling"]["properties"]
    assert sampling["runtime_promotion_allowed"]["const"] is False


def test_phase11_reference_lab_passes_owner_contracts(tmp_path: Path) -> None:
    runner = load_runner()
    output = tmp_path / "distributed-erasure-report.json"
    report = runner.run_lab(
        memo_root=require_owner_root("AOA_MEMO_ROOT"),
        session_memory_root=require_owner_root("AOA_SESSION_MEMORY_ROOT"),
        kag_root=require_owner_root("AOA_KAG_ROOT"),
        stack_root=require_owner_root("ABYSS_STACK_ROOT"),
        machine_root=require_owner_root("ABYSS_MACHINE_REPO_ROOT"),
        output_path=output,
    )

    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert output.exists()
    assert report["exit_gate"]["passed"] is True
    assert report["complete_closure"]["plain_complete"] is True
    assert (
        report["complete_closure"]["private_memory_deployment_allowed"] is True
    )
    assert (
        report["approved_exception_residue"][
            "private_memory_deployment_allowed"
        ]
        is False
    )
    assert all(item["detected"] for item in report["fault_results"])
    assert report["authority"]["landing_performed"] is False
    assert report["sampling"]["human_operator_sampling_status"] == "not_performed"
