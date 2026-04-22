from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
BUNDLE_NAME = "aoa-stats-regrounding-boundary-integrity"


def test_stats_regrounding_boundary_eval_is_cataloged() -> None:
    catalog = json.loads(
        (REPO_ROOT / "generated" / "eval_catalog.min.json").read_text(encoding="utf-8")
    )
    entry = next(item for item in catalog["evals"] if item["name"] == BUNDLE_NAME)

    assert entry["category"] == "boundary"
    assert entry["claim_type"] == "bounded"
    assert entry["verdict_shape"] == "mixed"
    assert entry["report_format"] == "summary-with-breakdown"
    assert entry["object_under_evaluation"] == (
        "stats-driven re-grounding consumer boundary across aoa-stats, "
        "aoa-sdk, aoa-routing, and aoa-evals"
    )
    assert "stats" in entry["summary"]
    assert "proof" in entry["summary"]


def test_stats_regrounding_boundary_report_example_matches_schema() -> None:
    report_dir = REPO_ROOT / "bundles" / BUNDLE_NAME / "reports"
    schema = json.loads((report_dir / "summary.schema.json").read_text(encoding="utf-8"))
    example = json.loads((report_dir / "example-report.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(example)
    assert example["verdict"] == "mixed support"
    assert "aoa-stats.summary_surface_catalog.min" in example["stats_signals_observed"]
    assert "aoa-skills owner-local receipts" in example["owner_truth_targets"]
