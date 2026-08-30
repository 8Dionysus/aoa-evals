from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest
from jsonschema import Draft202012Validator

BUNDLE_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = BUNDLE_ROOT / "runners/run_continuity_capsule_compaction.py"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports/summary.schema.json"
EXAMPLE_REPORT_PATH = BUNDLE_ROOT / "reports/example-report.json"


def _load_runner() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "continuity_capsule_eval_runner", RUNNER_PATH
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUNNER = _load_runner()


def _digest(value: dict[str, object]) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _packet() -> dict[str, object]:
    tail = "protected tail"
    posture = {
        "mode": "verbatim_private_tail",
        "portable_tail_policy": "omitted",
        "private_tail_digest": "sha256:" + hashlib.sha256(tail.encode()).hexdigest(),
        "private_tail_bytes": len(tail.encode()),
    }
    content = {
        "capsule_id": "case-001",
        "goal": {
            "goal_id": "goal-001",
            "title": "continuity",
            "source_ref": "goal-source:001",
            "digest": "sha256:" + "2" * 64,
            "content": "Preserve exact continuity across compaction.",
        },
        "constraints": ["default off"],
        "completed": ["contract"],
        "current_work": ["validation"],
        "blockers": [],
        "exact_decisions": ["tail private"],
        "open_obligations": ["baseline"],
        "evidence_refs": [{"ref": "evidence:001", "position": 1}],
        "omissions_uncertainty": {"omitted": []},
    }
    source_watermark = {
        "source_ref": "session:001",
        "source_digest": "sha256:" + "1" * 64,
        "generation": 1,
        "observed_at": "2026-08-26T18:30:48Z",
    }
    compaction_event = {
        "event_ref": "event:001",
        "session_id": "session-001",
        "sequence": 1,
        "occurred_at": "2026-08-26T18:30:48Z",
        "kind": "compaction",
    }
    capsule_payload = {
        "schema_version": "continuity_capsule_v1",
        **content,
        "source_watermark": source_watermark,
        "compaction_event": compaction_event,
        "protected_tail_posture": posture,
    }
    capsule_digest = _digest(capsule_payload)
    capsule_ref = {
        "object_id": "continuity-capsule:case-001",
        "owner_repo": "aoa-session-memory",
        "schema_version": "continuity_capsule_v1",
        "digest": capsule_digest,
    }
    baseline = {
        **capsule_payload,
        "capsule_ref": capsule_ref,
        "capsule_digest": capsule_digest,
    }

    def view(kind: str) -> dict[str, object]:
        result: dict[str, object] = {
            "schema_version": "continuity_capsule_materialization_v1",
            "view": kind,
            "capsule_ref": capsule_ref,
            "capsule_digest": capsule_digest,
            "content": json.loads(json.dumps(content)),
            "source_watermark": source_watermark,
            "compaction_event": compaction_event,
            "protected_tail_posture": posture,
        }
        if kind == "private":
            result["protected_tail"] = tail
        result["view_digest"] = _digest(result)
        return result

    return {
        "schema_version": "aoa_continuity_capsule_compaction_input_v1",
        "case_family": "continuity-capsule-paired-v1",
        "cases": [
            {
                "case_id": "CC-01",
                "baseline_capsule": baseline,
                "portable_view": view("portable"),
                "private_view": view("private"),
            }
        ],
    }


def test_runner_emits_schema_valid_field_preservation_report() -> None:
    report = RUNNER.build_report(_packet())
    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))

    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert report["verdict"] == "no material regression"
    assert report["admission"]["real_session_evidence"] is False
    assert report["admission"]["baseline_ready"] is False


def test_example_report_covers_every_preservation_field() -> None:
    report = json.loads(EXAMPLE_REPORT_PATH.read_text(encoding="utf-8"))
    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))

    assert list(Draft202012Validator(schema).iter_errors(report)) == []
    assert report["preservation_fields"] == list(RUNNER.PRESERVATION_FIELDS)
    for comparison in report["per_case_comparisons"]:
        assert [item["field"] for item in comparison["field_checks"]] == list(
            RUNNER.PRESERVATION_FIELDS
        )


def test_runner_keeps_content_drift_as_a_regression_signal() -> None:
    packet = _packet()
    case = packet["cases"][0]
    assert isinstance(case, dict)
    portable = case["portable_view"]
    assert isinstance(portable, dict)
    content = portable["content"]
    assert isinstance(content, dict)
    content["open_obligations"] = ["drifted"]
    portable["view_digest"] = _digest(
        {key: value for key, value in portable.items() if key != "view_digest"}
    )
    report = RUNNER.build_report(packet)

    assert report["verdict"] == "mixed regression signal"
    comparison = report["per_case_comparisons"][0]
    assert comparison["comparative_reading"] == "mixed regression signal"
    obligation_check = next(
        item
        for item in comparison["field_checks"]
        if item["field"] == "open_obligations"
    )
    assert obligation_check["preserved"] is False
    assert obligation_check["reason"] == (
        "canonical content differs across materializations"
    )


def test_runner_distinguishes_boolean_from_numeric_json_drift() -> None:
    packet = _packet()
    case = packet["cases"][0]
    assert isinstance(case, dict)
    portable = case["portable_view"]
    assert isinstance(portable, dict)
    content = portable["content"]
    assert isinstance(content, dict)
    evidence_refs = content["evidence_refs"]
    assert isinstance(evidence_refs, list)
    evidence_refs[0]["position"] = True
    portable["view_digest"] = _digest(
        {key: value for key, value in portable.items() if key != "view_digest"}
    )

    report = RUNNER.build_report(packet)

    assert report["verdict"] == "mixed regression signal"
    evidence_check = next(
        item
        for item in report["per_case_comparisons"][0]["field_checks"]
        if item["field"] == "evidence_refs"
    )
    assert evidence_check["preserved"] is False


def test_runner_describes_metadata_drift_as_a_mismatch() -> None:
    packet = _packet()
    case = packet["cases"][0]
    assert isinstance(case, dict)
    portable = case["portable_view"]
    assert isinstance(portable, dict)
    watermark = portable["source_watermark"]
    assert isinstance(watermark, dict)
    portable["source_watermark"] = {**watermark, "generation": 2}
    portable["view_digest"] = _digest(
        {key: value for key, value in portable.items() if key != "view_digest"}
    )

    report = RUNNER.build_report(packet)

    watermark_check = next(
        item
        for item in report["per_case_comparisons"][0]["field_checks"]
        if item["field"] == "source_watermark"
    )
    assert watermark_check["preserved"] is False
    assert watermark_check["reason"] == (
        "metadata differs from the canonical capsule across views"
    )


def test_runner_rejects_private_tail_and_capsule_identity_drift() -> None:
    tail_packet = _packet()
    tail_case = tail_packet["cases"][0]
    assert isinstance(tail_case, dict)
    private = tail_case["private_view"]
    assert isinstance(private, dict)
    private["protected_tail"] = "changed"
    private_posture = private["protected_tail_posture"]
    assert isinstance(private_posture, dict)
    private["protected_tail_posture"] = {
        **private_posture,
        "private_tail_digest": "sha256:" + hashlib.sha256(b"changed").hexdigest(),
        "private_tail_bytes": len(b"changed"),
    }
    private["view_digest"] = _digest(
        {key: value for key, value in private.items() if key != "view_digest"}
    )
    tail_report = RUNNER.build_report(tail_packet)
    assert tail_report["verdict"] == "mixed regression signal"
    tail_checks = {
        item["field"]: item
        for item in tail_report["per_case_comparisons"][0]["field_checks"]
    }
    assert tail_checks["private_tail_digest"]["reason"] == (
        "private view differs from the protected-tail digest"
    )
    assert tail_checks["private_tail_bytes"]["reason"] == (
        "private view differs from the protected-tail byte count"
    )

    identity_packet = _packet()
    identity_case = identity_packet["cases"][0]
    assert isinstance(identity_case, dict)
    portable = identity_case["portable_view"]
    assert isinstance(portable, dict)
    ref = portable["capsule_ref"]
    assert isinstance(ref, dict)
    ref["object_id"] = "continuity-capsule:other"
    portable["view_digest"] = _digest(
        {key: value for key, value in portable.items() if key != "view_digest"}
    )
    identity_report = RUNNER.build_report(identity_packet)
    assert identity_report["verdict"] == "regression present"


def test_runner_rejects_boolean_counters_and_noncanonical_numbers() -> None:
    packet = _packet()
    case = packet["cases"][0]
    assert isinstance(case, dict)
    baseline = case["baseline_capsule"]
    assert isinstance(baseline, dict)
    watermark = baseline["source_watermark"]
    assert isinstance(watermark, dict)
    watermark["generation"] = True
    baseline_payload = {
        key: value
        for key, value in baseline.items()
        if key not in {"capsule_ref", "capsule_digest"}
    }
    digest = _digest(baseline_payload)
    baseline["capsule_digest"] = digest
    ref = baseline["capsule_ref"]
    assert isinstance(ref, dict)
    ref["digest"] = digest
    report = RUNNER.build_report(packet)
    assert report["verdict"] == "regression present"

    with pytest.raises(RUNNER.ContinuityCapsuleInputError, match="canonical JSON"):
        RUNNER._canonical_digest({"value": float("nan")})


@pytest.mark.parametrize(
    ("field", "value"),
    [("case_family", "tiny"), ("case_id", "x")],
)
def test_runner_enforces_report_identifier_lengths(field: str, value: str) -> None:
    packet = _packet()
    if field == "case_family":
        packet[field] = value
    else:
        packet["cases"][0][field] = value

    with pytest.raises(RUNNER.ContinuityCapsuleInputError, match="at least"):
        RUNNER.build_report(packet)
