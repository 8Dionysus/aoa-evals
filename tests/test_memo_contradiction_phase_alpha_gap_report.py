from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "bundles" / "aoa-memo-contradiction-integrity" / "reports"
REPORT_PATH = REPORT_DIR / "phase-alpha-memo-contradiction-gap.report.json"
SCHEMA_PATH = REPORT_DIR / "summary.schema.json"
SELECTION_PATH = (
    REPO_ROOT
    / "examples"
    / "runtime_evidence_selection.phase-alpha-memo-contradiction-gap.example.json"
)
EVAL_MANIFEST_PATH = REPO_ROOT / "bundles" / "aoa-memo-contradiction-integrity" / "eval.yaml"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase_alpha_memo_contradiction_gap_report_matches_bundle_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report = load_json(REPORT_PATH)

    Draft202012Validator(schema).validate(report)


def test_phase_alpha_memo_contradiction_gap_report_stays_negative() -> None:
    report = load_json(REPORT_PATH)
    selection = load_json(SELECTION_PATH)
    manifest_text = EVAL_MANIFEST_PATH.read_text(encoding="utf-8")

    assert report["bundle_status"] == "draft"
    assert report["verdict"] == "does not support bounded claim"
    assert "export_ready: false" in manifest_text
    assert selection["selection_id"] in report["case_family"]
    assert "no lifecycle-aware object recall rerun" in report["claim_boundary"]

    limitations = " ".join(report["limitations"])
    for forbidden_overread in selection["do_not_overread"]:
        assert forbidden_overread in limitations


def test_phase_alpha_memo_contradiction_gap_report_names_selected_evidence() -> None:
    report = load_json(REPORT_PATH)
    selection = load_json(SELECTION_PATH)

    report_text = json.dumps(report, sort_keys=True)
    for selected_evidence in selection["selected_evidence"]:
        artifact_name = str(selected_evidence["artifact_ref"]).rsplit("/", maxsplit=1)[-1]
        assert artifact_name in report_text

    assert report["breakdown"]["lifecycle_visibility"] == "weak"
    assert report["breakdown"]["current_recall_honesty"] == "weak"
    assert report["breakdown"]["contradiction_linkage"] == "mixed"
    assert all(
        case_note["contradiction_reading"] == "does not support bounded claim"
        for case_note in report["case_notes"]
    )
