from __future__ import annotations

import sys
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SCORER_PATH = (
    REPO_ROOT
    / "mechanics"
    / "proof-infra"
    / "parts"
    / "reportable-contracts"
    / "scorers"
    / "bounded_rubric_breakdown.py"
)
SCORER_SPEC = importlib.util.spec_from_file_location(
    "aoa_evals_proof_infra_bounded_rubric_breakdown",
    SCORER_PATH,
)
assert SCORER_SPEC is not None
assert SCORER_SPEC.loader is not None
bounded_rubric_breakdown = importlib.util.module_from_spec(SCORER_SPEC)
SCORER_SPEC.loader.exec_module(bounded_rubric_breakdown)

build_case_breakdown = bounded_rubric_breakdown.build_case_breakdown
build_comparative_case = bounded_rubric_breakdown.build_comparative_case
build_target_risk = bounded_rubric_breakdown.build_target_risk


def test_build_case_breakdown_keeps_axes_signals_and_cautions() -> None:
    payload = build_case_breakdown(
        "BCQ-01",
        "supports bounded claim",
        "The workflow stayed scoped and named verification clearly.",
        signals=["scoped", "verified"],
        cautions=["still bounded"],
        axes={"scope discipline": "strong", "verification honesty": "strong"},
    )

    assert payload["case_id"] == "BCQ-01"
    assert payload["axes"] == [
        {"axis": "scope discipline", "reading": "strong"},
        {"axis": "verification honesty", "reading": "strong"},
    ]
    assert payload["signals"] == ["scoped", "verified"]
    assert payload["cautions"] == ["still bounded"]


def test_shared_helper_formats_comparative_and_integrity_entries() -> None:
    comparative = build_comparative_case(
        "OP-01",
        "supports bounded claim",
        "mixed support",
        "artifact outruns process",
        "Polish looked stronger than workflow evidence.",
    )
    integrity = build_target_risk(
        "aoa-output-vs-process-gap",
        "baseline by association risk",
        "mixed support",
        "The bridge still must not be read as baseline-default.",
        evidence_coverage="comparison contract and runner contract are present",
        routing_note="chooser keeps the bridge separate from same-task regression",
    )

    assert comparative["gap_reading"] == "artifact outruns process"
    assert comparative["side_by_side_note"] == "Polish looked stronger than workflow evidence."
    assert integrity["target_bundle"] == "aoa-output-vs-process-gap"
    assert integrity["integrity_risk_class"] == "baseline by association risk"
    assert integrity["routing_note"] == "chooser keeps the bridge separate from same-task regression"
