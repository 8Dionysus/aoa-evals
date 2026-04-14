from __future__ import annotations

import json
import os
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
AOA_MEMO_ROOT = Path(os.environ.get("AOA_MEMO_ROOT", REPO_ROOT.parent / "aoa-memo"))
AOA_PLAYBOOKS_ROOT = Path(
    os.environ.get("AOA_PLAYBOOKS_ROOT", REPO_ROOT.parent / "aoa-playbooks")
)
REPORT_DIR = REPO_ROOT / "bundles" / "aoa-memo-writeback-act-integrity" / "reports"
REPORT_PATH = REPORT_DIR / "phase-alpha-memo-writeback-act.report.json"
SCHEMA_PATH = REPORT_DIR / "summary.schema.json"
SELECTION_PATH = (
    REPO_ROOT
    / "examples"
    / "runtime_evidence_selection.phase-alpha-memo-writeback-act.example.json"
)
DECISION_PATH = (
    AOA_MEMO_ROOT
    / "examples"
    / "decision.phase-alpha-validation-remediation-rerun.example.json"
)
CATALOG_PATH = AOA_MEMO_ROOT / "generated" / "memory_object_catalog.min.json"
SECTIONS_PATH = AOA_MEMO_ROOT / "generated" / "memory_object_sections.full.json"
RECEIPT_FIXTURE_PATH = (
    AOA_MEMO_ROOT / "tests" / "fixtures" / "memo_writeback_receipts.example.jsonl"
)
REVIEWED_RUN_PATH = (
    AOA_PLAYBOOKS_ROOT
    / "docs"
    / "alpha-reviewed-runs"
    / "2026-04-02.validation-driven-remediation-recall-rerun.md"
)
PUBLISHER_RUN_PATH = (
    AOA_PLAYBOOKS_ROOT
    / "docs"
    / "real-runs"
    / "2026-04-07.federated-live-publisher-activation.md"
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl_first(path: Path) -> dict[str, object]:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    return json.loads(first_line)


def test_phase_alpha_memo_writeback_act_report_matches_bundle_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report = load_json(REPORT_PATH)

    Draft202012Validator(schema).validate(report)


def test_phase_alpha_memo_writeback_act_report_stays_bounded_to_selected_path() -> None:
    report = load_json(REPORT_PATH)
    selection = load_json(SELECTION_PATH)

    assert report["bundle_status"] == "draft"
    assert report["verdict"] == "supports bounded claim"
    assert selection["selection_id"] in report["case_family"]
    assert "memo_surviving_event decision path" in report["claim_boundary"]

    limitations = " ".join(report["limitations"])
    for bounded_limit in selection["do_not_overread"]:
        assert bounded_limit in limitations

    report_text = json.dumps(report, sort_keys=True)
    for selected_evidence in selection["selected_evidence"]:
        artifact_name = str(selected_evidence["artifact_ref"]).rsplit("/", maxsplit=1)[-1]
        assert artifact_name in report_text

    for required_name in (
        "decision.phase-alpha-validation-remediation-rerun.example.json",
        "memory_object_catalog.min.json",
        "memory_object_sections.full.json",
        "memo_writeback_receipts.example.jsonl",
        "federated-live-publisher-activation.md",
    ):
        assert required_name in report_text


def test_phase_alpha_memo_writeback_act_report_keeps_adoption_and_receipt_chain_visible() -> None:
    report = load_json(REPORT_PATH)
    decision = load_json(DECISION_PATH)
    catalog = load_json(CATALOG_PATH)
    sections = load_json(SECTIONS_PATH)
    receipt = load_jsonl_first(RECEIPT_FIXTURE_PATH)
    reviewed_run_text = REVIEWED_RUN_PATH.read_text(encoding="utf-8")
    publisher_run_text = PUBLISHER_RUN_PATH.read_text(encoding="utf-8")

    assert report["breakdown"]["runtime_boundary_honesty"] == "strong"
    assert report["breakdown"]["review_to_adoption_alignment"] == "strong"
    assert report["breakdown"]["receipt_visibility"] == "strong"
    assert report["breakdown"]["recall_surface_alignment"] == "strong"

    assert decision["id"] == "memo.decision.2026-04-02.alpha-validation-remediation-rerun"
    assert "## Memo Writeback" in reviewed_run_text
    assert "owner_change_set" in publisher_run_text
    assert "publication_verification_pack" in publisher_run_text

    assert receipt["object_ref"]["id"] == decision["id"]
    assert receipt["payload"]["review_state"] == decision["lifecycle"]["review_state"]
    assert receipt["payload"]["target_kind"] == decision["kind"]
    assert receipt["payload"]["writeback_class"] == "memo_surviving_event"

    catalog_ids = {entry["id"] for entry in catalog["memory_objects"]}
    section_ids = {entry["id"] for entry in sections["memory_objects"]}
    assert decision["id"] in catalog_ids
    assert decision["id"] in section_ids
