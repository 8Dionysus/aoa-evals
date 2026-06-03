from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import jsonschema
import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[5]
PUBLICATION_RECEIPTS_PARTS_ROOT = (
    REPO_ROOT / "mechanics" / "publication-receipts" / "parts"
)
DRY_REVIEW_PATH = (
    PUBLICATION_RECEIPTS_PARTS_ROOT
    / "intake-dry-review"
    / "reports"
    / "eval-result-receipt-intake-dry-review-v1.json"
)
PAYLOAD_SCHEMA_PATH = (
    PUBLICATION_RECEIPTS_PARTS_ROOT
    / "receipt-payload"
    / "schemas"
    / "eval-result-receipt.schema.json"
)
PUBLISHER_PATH = (
    PUBLICATION_RECEIPTS_PARTS_ROOT
    / "live-publisher"
    / "scripts"
    / "publish_live_receipts.py"
)
SOURCE_REPORT_PATH = (
    REPO_ROOT
    / "evals"
    / "workflow"
    / "aoa-verification-honesty"
    / "reports"
    / "aoa-evals-slice-19-lifecycle-contract.report.json"
)
SOURCE_MANIFEST_PATH = REPO_ROOT / "evals" / "workflow" / "aoa-verification-honesty" / "eval.yaml"
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_repo


def load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publish_live_receipts = load_script(PUBLISHER_PATH)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def copy_repo_text(repo_root: Path, relative_path: str) -> None:
    source = REPO_ROOT / relative_path
    if not source.exists():
        raise FileNotFoundError(source)
    destination = repo_root / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def make_receipt_intake_dry_review_surface(repo_root: Path) -> Path:
    copy_repo_text(repo_root, validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME)
    return repo_root / validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME


def test_receipt_intake_dry_review_payload_preview_is_valid_but_not_publishable() -> None:
    artifact = load_json(DRY_REVIEW_PATH)
    preview = artifact["candidate_payload_preview"]
    schema = load_json(PAYLOAD_SCHEMA_PATH)

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
        "repo:aoa-evals/evals/workflow/aoa-verification-honesty/reports/"
        "aoa-evals-slice-19-lifecycle-contract.report.json"
    )
    assert preview["eval_name"] == source_report["eval_name"] == manifest["name"]
    assert preview["bundle_status"] == source_report["bundle_status"] == manifest["status"]
    assert preview["report_format"] == manifest["report_format"]
    assert preview["verdict"] == source_report["verdict"]
    assert preview["claim_scope"] == "bundle_scoped"
    assert preview["comparison_mode"] == "none"
    assert preview["case_count"] == len(source_report["per_case_breakdown"])
    assert "publication pressure routes to a receipt envelope" in preview["interpretation_bound"]
    assert "strategic closeout stays with the goal owner" in artifact["claim_limit"]


def test_receipt_intake_dry_review_surface_validates_current_route() -> None:
    assert validate_repo.validate_receipt_intake_dry_review_surface(REPO_ROOT) == []


def test_receipt_intake_dry_review_rejects_published_posture(
    tmp_path: Path,
) -> None:
    review_path = make_receipt_intake_dry_review_surface(tmp_path)
    payload = json.loads(review_path.read_text(encoding="utf-8"))
    payload["publication_boundary"]["receipt_status"] = "published"
    write_json_payload(review_path, payload)

    issues = validate_repo.validate_receipt_intake_dry_review_surface(tmp_path)

    assert any(
        issue.location == f"{validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME}.publication_boundary"
        and "receipt_status must be 'not_published'" in issue.message
        for issue in issues
    )


def test_receipt_intake_dry_review_rejects_publishable_envelope_shape(
    tmp_path: Path,
) -> None:
    review_path = make_receipt_intake_dry_review_surface(tmp_path)
    payload = json.loads(review_path.read_text(encoding="utf-8"))
    payload["event_kind"] = "eval_result_receipt"
    write_json_payload(review_path, payload)

    issues = validate_repo.validate_receipt_intake_dry_review_surface(tmp_path)

    assert any(
        issue.location == validate_repo.RECEIPT_INTAKE_DRY_REVIEW_NAME
        and "must not contain publishable receipt field 'event_kind'" in issue.message
        for issue in issues
    )
