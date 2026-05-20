from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = REPO_ROOT / "bundles" / "aoa-verification-honesty" / "reports"
REPORT_PATH = REPORT_DIR / "aoa-evals-slice-19-lifecycle-contract.report.json"
SCHEMA_PATH = REPORT_DIR / "summary.schema.json"


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_verification_honesty_local_report_matches_bundle_schema() -> None:
    schema = load_json(SCHEMA_PATH)
    report = load_json(REPORT_PATH)

    Draft202012Validator(schema).validate(report)


def test_verification_honesty_local_report_keeps_boundaries_visible() -> None:
    report = load_json(REPORT_PATH)
    report_text = json.dumps(report, sort_keys=True)

    assert report["eval_name"] == "aoa-verification-honesty"
    assert report["bundle_status"] == "portable"
    assert report["verdict"] == "supports bounded claim"
    assert "does not publish an eval result receipt" in report_text
    assert "No receipt publisher run was attempted" in report_text
    assert "No runtime mutation or machine maintenance check was attempted" in report_text
    assert "goal completion separate from this bounded pass" in report_text
