from __future__ import annotations

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SDK_FIXTURE_PATH = (
    WORKSPACE_ROOT / "aoa-sdk" / "examples" / "a2a" / "summon_return_checkpoint_e2e.fixture.json"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_a2a_eval_fixture_contract_points_to_shared_family() -> None:
    contract = load_json(
        REPO_ROOT
        / "bundles"
        / "aoa-a2a-summon-return-checkpoint"
        / "fixtures"
        / "contract.json"
    )
    shared_family_path = REPO_ROOT / contract["shared_fixture_family_path"]
    family_text = shared_family_path.read_text(encoding="utf-8")

    assert shared_family_path.exists()
    assert "A2A Summon Return Checkpoint V1" in family_text
    assert "dry_run=true" in family_text
    assert "live_automation=false" in family_text


def test_a2a_eval_hook_references_sdk_e2e_fixture() -> None:
    hook = load_json(
        REPO_ROOT
        / "examples"
        / "artifact_to_verdict_hook.a2a-summon-return-checkpoint.example.json"
    )

    assert "repo:aoa-sdk/examples/a2a/summon_return_checkpoint_e2e.fixture.json" in hook[
        "artifact_contract_refs"
    ]


def test_sdk_e2e_fixture_keeps_eval_contract_inputs_visible() -> None:
    if not SDK_FIXTURE_PATH.exists():
        pytest.skip("live aoa-sdk E2E fixture is unavailable")

    fixture = load_json(SDK_FIXTURE_PATH)

    assert fixture["eval_anchor"] == "aoa-a2a-summon-return-checkpoint"
    assert fixture["a2a_return_eval_packet"]["hook_id"] == (
        "aoa-p-0031-a2a-summon-return-checkpoint-hook"
    )
    assert fixture["a2a_return_eval_packet"]["review_required"] is True
    assert fixture["runtime_closeout_dry_run_receipt_contract"]["dry_run"] is True
    assert fixture["runtime_closeout_dry_run_receipt_contract"]["live_automation"] is False
