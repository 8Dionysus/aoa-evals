from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "bundles" / "aoa-memo-contradiction-integrity" / "reports"
REPORT_PATH = REPORT_DIR / "phase-alpha-memo-contradiction-rerun.report.json"
SCHEMA_PATH = REPORT_DIR / "summary.schema.json"
SELECTION_PATH = (
    REPO_ROOT
    / "examples"
    / "runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json"
)
EVAL_MANIFEST_PATH = REPO_ROOT / "bundles" / "aoa-memo-contradiction-integrity" / "eval.yaml"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase_alpha_memo_contradiction_rerun_report_matches_bundle_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report = load_json(REPORT_PATH)

    Draft202012Validator(schema).validate(report)


def test_phase_alpha_memo_contradiction_rerun_report_stays_bounded_and_non_exportable() -> None:
    report = load_json(REPORT_PATH)
    selection = load_json(SELECTION_PATH)
    manifest_text = EVAL_MANIFEST_PATH.read_text(encoding="utf-8")

    assert report["bundle_status"] == "draft"
    assert report["verdict"] == "supports bounded claim"
    assert "export_ready: true" in manifest_text
    assert selection["selection_id"] in report["case_family"]
    assert "runtime sidecar consumed" in report["claim_boundary"]

    limitations = " ".join(report["limitations"])
    for bounded_limit in (
        "not broad memo readiness",
        "does not prove contradiction resolution",
        "does not prove permission or authority safety",
    ):
        assert bounded_limit in limitations
    assert "does not make aoa-memo-contradiction-integrity export-ready" not in limitations


def test_phase_alpha_memo_contradiction_rerun_report_names_key_evidence_and_breakdown() -> None:
    report = load_json(REPORT_PATH)
    report_text = json.dumps(report, sort_keys=True)

    for artifact_name in (
        "runtime_evidence_selection.phase-alpha-memo-contradiction-rerun.example.json",
        "memory_object_catalog.min.json",
        "memory_object_sections.full.json",
        "memo.claim.2026-04-03.phase-alpha-closure-with-residual-runtime-history",
        "memo.claim.2026-04-03.phase-alpha-rerun-pending-handoff",
        "memo.claim.2026-04-03.phase-alpha-runtime-history-fully-retired",
        "memo.claim.2026-04-03.phase-alpha-runtime-history-later-infra-track",
        "contradiction_map.json",
        "handoff_record.json",
    ):
        assert artifact_name in report_text

    assert report["breakdown"]["lifecycle_visibility"] == "strong"
    assert report["breakdown"]["current_recall_honesty"] == "strong"
    assert report["breakdown"]["contradiction_linkage"] == "strong"
    assert report["breakdown"]["replacement_vs_withdrawal_clarity"] == "strong"
    assert report["breakdown"]["audit_trace_visibility"] == "strong"

    readings = {case_note["contradiction_reading"] for case_note in report["case_notes"]}
    assert "supports bounded claim" in readings
    assert "mixed support" not in readings
