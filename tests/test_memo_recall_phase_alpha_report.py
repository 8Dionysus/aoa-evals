from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "bundles" / "aoa-memo-recall-integrity" / "reports"
REPORT_PATH = REPORT_DIR / "phase-alpha-memo-recall-rerun.report.json"
SCHEMA_PATH = REPORT_DIR / "summary.schema.json"
SELECTION_PATH = (
    REPO_ROOT
    / "examples"
    / "runtime_evidence_selection.phase-alpha-memo-recall-rerun.example.json"
)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase_alpha_memo_recall_report_matches_bundle_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report = load_json(REPORT_PATH)

    Draft202012Validator(schema).validate(report)


def test_phase_alpha_memo_recall_report_stays_bounded_to_runtime_selection() -> None:
    report = load_json(REPORT_PATH)
    selection = load_json(SELECTION_PATH)

    assert report["bundle_status"] == "draft"
    assert report["verdict"] == "supports bounded claim"
    assert selection["selection_id"] in report["case_family"]
    assert "general memo readiness" in report["claim_boundary"]

    limitations = " ".join(report["limitations"])
    for forbidden_overread in selection["do_not_overread"]:
        assert forbidden_overread in limitations

    report_text = json.dumps(report, sort_keys=True)
    for selected_evidence in selection["selected_evidence"]:
        artifact_name = str(selected_evidence["artifact_ref"]).rsplit("/", maxsplit=1)[-1]
        assert artifact_name in report_text


def test_phase_alpha_memo_recall_report_keeps_staleness_gap_visible() -> None:
    report = load_json(REPORT_PATH)

    assert report["breakdown"]["staleness_honesty"] == "mixed"
    assert "stale, superseded, or retracted" in report["strongest_recall_risk"]
    assert any(
        case_note["recall_reading"] == "mixed support"
        for case_note in report["case_notes"]
    )
