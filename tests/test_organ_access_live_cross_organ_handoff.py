from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import stat

import jsonschema
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_ROOT = (
    REPO_ROOT
    / "evals"
    / "boundary"
    / "aoa-organ-access-live-cross-organ-handoff"
)
RUNNER_PATH = BUNDLE_ROOT / "runners" / "run_live_handoff.py"
SCHEMA_PATH = BUNDLE_ROOT / "reports" / "summary.schema.json"


def _runner():
    spec = importlib.util.spec_from_file_location("live_cross_organ_runner", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_handoff_bundle_source_contract_is_explicit() -> None:
    eval_text = (BUNDLE_ROOT / "EVAL.md").read_text(encoding="utf-8")
    manifest = (BUNDLE_ROOT / "eval.yaml").read_text(encoding="utf-8")
    assert "status: bounded" in eval_text
    assert "status: bounded" in manifest
    assert "aoa-memo" in eval_text
    assert "cannot close the chain itself" in eval_text
    assert "runtime effects" in eval_text
    assert "private" in eval_text


def test_synthetic_positive_report_is_content_bound_and_private(tmp_path: Path) -> None:
    module = _runner()
    os.chmod(tmp_path, 0o700)
    paths = module.build_synthetic_case(tmp_path)
    reviewed_at = module.datetime(2026, 1, 1, 0, 30, tzinfo=module.timezone.utc)
    report = module._review_case(paths, reviewed_at)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(report)
    assert report["verdict"] == "supported_bounded"
    assert report["next_owner"] == "aoa-memo"
    assert report["checks"]["acceptance_absent"] is True
    assert report["authority_boundary"] == {
        "proof_owner": "aoa-evals",
        "acceptance_owner": "aoa-memo",
        "owner_tools_executed_by_evals": False,
        "durable_memory_written": False,
        "owner_acceptance_inferred": False,
        "admission_authorized": False,
        "runtime_execution_authorized": False,
    }
    assert report["result_digest"] == module.digest(
        module._without(report, "result_digest")
    )

    output = tmp_path / "proof-result.json"
    module.write_private_json(output, report)
    assert stat.S_IMODE(output.stat().st_mode) == 0o600


def test_offline_scenario_lane_rejects_every_negative() -> None:
    result = _runner().run_scenarios()
    assert result["verdict"] == "supports bounded claim"
    assert result["cases"][0] == {
        "case": "valid_direct_owner_chain",
        "accepted": True,
        "issue_code": None,
    }
    assert all(not item["accepted"] for item in result["cases"][1:])
    assert all(
        item["issue_code"] == item["expected_issue_code"]
        for item in result["cases"][1:]
    )


def test_secret_material_and_public_permissions_fail_before_review(tmp_path: Path) -> None:
    module = _runner()
    os.chmod(tmp_path, 0o700)
    paths = module.build_synthetic_case(tmp_path)
    memo_call = json.loads(paths["memo_call"].read_text(encoding="utf-8"))
    memo_call["access_token"] = "not-a-real-token"
    paths["memo_call"].write_text(json.dumps(memo_call), encoding="utf-8")
    os.chmod(paths["memo_call"], 0o600)
    with pytest.raises(module.ReviewError, match="secret_material"):
        module._review_case(
            paths,
            module.datetime(2026, 1, 1, 0, 30, tzinfo=module.timezone.utc),
        )

    public_root = tmp_path / "public-mode"
    public_root.mkdir(mode=0o700)
    paths = module.build_synthetic_case(public_root)
    os.chmod(paths["kag_call"], 0o644)
    with pytest.raises(module.ReviewError, match="unsafe_permissions"):
        module._review_case(
            paths,
            module.datetime(2026, 1, 1, 0, 30, tzinfo=module.timezone.utc),
        )
