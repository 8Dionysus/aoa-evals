from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import jsonschema
import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DRY_REVIEW_PATH = REPO_ROOT / "reports" / "eval-result-receipt-intake-dry-review-v1.json"
SOURCE_REPORT_PATH = (
    REPO_ROOT
    / "bundles"
    / "aoa-verification-honesty"
    / "reports"
    / "aoa-evals-slice-19-lifecycle-contract.report.json"
)
SOURCE_MANIFEST_PATH = REPO_ROOT / "bundles" / "aoa-verification-honesty" / "eval.yaml"


def load_script(script_name: str):
    path = REPO_ROOT / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publish_live_receipts = load_script("publish_live_receipts.py")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_receipt_intake_dry_review_payload_preview_is_valid_but_not_publishable() -> None:
    artifact = load_json(DRY_REVIEW_PATH)
    preview = artifact["candidate_payload_preview"]
    schema = load_json(REPO_ROOT / "schemas" / "eval-result-receipt.schema.json")

    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(preview)

    assert artifact["publication_boundary"]["receipt_status"] == "not_published"
    assert artifact["publication_boundary"]["event_envelope_status"] == "not_created"
    assert artifact["publication_boundary"]["live_log_append_status"] == "not_attempted"
    assert artifact["publication_boundary"]["publisher_execution_status"] == "not_attempted"
    for field in (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    ):
        assert field not in artifact

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="event_kind"):
        publish_live_receipts.validate_receipt(artifact, location="dry-review")


def test_receipt_intake_dry_review_matches_first_bundle_local_report() -> None:
    artifact = load_json(DRY_REVIEW_PATH)
    source_report = load_json(SOURCE_REPORT_PATH)
    manifest = yaml.safe_load(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))
    preview = artifact["candidate_payload_preview"]

    assert artifact["source_report_ref"] == (
        "repo:aoa-evals/bundles/aoa-verification-honesty/reports/"
        "aoa-evals-slice-19-lifecycle-contract.report.json"
    )
    assert preview["eval_name"] == source_report["eval_name"] == manifest["name"]
    assert preview["bundle_status"] == source_report["bundle_status"] == manifest["status"]
    assert preview["report_format"] == manifest["report_format"]
    assert preview["verdict"] == source_report["verdict"]
    assert preview["claim_scope"] == "bundle_scoped"
    assert preview["comparison_mode"] == "none"
    assert preview["case_count"] == len(source_report["per_case_breakdown"])
    assert "does not publish an eval result receipt" in preview["interpretation_bound"]
    assert "complete the aoa-evals strategic refactor" in artifact["claim_limit"]
