from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]
BUNDLE_ROOT = (
    REPO_ROOT
    / "evals"
    / "comparison"
    / "longitudinal-window"
    / "aoa-stress-recovery-window"
)

EXPECTED_INPUTS = {
    "source_receipt_refs": [
        "repo:ATM10-Agent/examples/stressor_receipt.retrieval_only_fallback.example.json"
    ],
    "handoff_refs": [
        "repo:aoa-agents/mechanics/antifragility/parts/stress-posture/examples/stress-handoff-envelope.example.json"
    ],
    "playbook_lane_refs": [
        "repo:aoa-playbooks/mechanics/antifragility/parts/stress-lanes/examples/playbook_stress_lane.example.json"
    ],
    "reentry_gate_refs": [
        "repo:aoa-playbooks/mechanics/antifragility/parts/reentry-gates/examples/playbook_reentry_gate.example.json"
    ],
    "projection_health_refs": [
        "repo:aoa-kag/mechanics/antifragility/parts/projection-health/examples/projection_health_receipt.example.json"
    ],
    "regrounding_ticket_refs": [
        "repo:aoa-kag/mechanics/antifragility/parts/"
        "retrieval-outage-regrounding/examples/regrounding_ticket.example.json"
    ],
    "route_hint_refs": [
        "repo:aoa-routing/mechanics/antifragility/parts/"
        "composite-stress-routing/examples/composite_stress_route_hint.example.json"
    ],
    "memo_context_refs": [
        "repo:aoa-memo/mechanics/antifragility/parts/recovery-pattern-memory/examples/recovery_pattern_memory.example.json"
    ],
}


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_manifest_and_report_use_current_sibling_owner_refs() -> None:
    manifest = load_json(BUNDLE_ROOT / "input_manifest.example.json")
    report = load_json(BUNDLE_ROOT / "reports" / "example-report.json")
    report_inputs = report["inputs"]
    assert isinstance(report_inputs, dict)

    for field, expected_refs in EXPECTED_INPUTS.items():
        assert manifest[field] == expected_refs
        assert report_inputs[field] == expected_refs

    assert report_inputs["adaptation_delta_refs"] == [
        "repo:ATM10-Agent/examples/adaptation_delta.retrieval_only_fallback.example.json"
    ]


def test_active_surfaces_have_no_wave_or_suggested_axis_scaffold() -> None:
    active_texts = [
        (
            REPO_ROOT
            / "mechanics"
            / "antifragility"
            / "parts"
            / "stress-recovery-window"
            / "docs"
            / "STRESS_RECOVERY_WINDOW_EVALS.md"
        ).read_text(encoding="utf-8"),
        (BUNDLE_ROOT / "EVAL.md").read_text(encoding="utf-8"),
        (BUNDLE_ROOT / "runners" / "contract.json").read_text(encoding="utf-8"),
    ]

    for text in active_texts:
        assert "Wave 4" not in text
        assert "wave-4" not in text
        assert "wave-3" not in text
        assert "Suggested Axes" not in text
