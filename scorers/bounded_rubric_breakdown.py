from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def _string_list(values: Sequence[str] | None) -> list[str]:
    if not values:
        return []
    return [value for value in values if isinstance(value, str) and value.strip()]


def _axis_payload(axes: Mapping[str, str] | None) -> list[dict[str, str]]:
    if not axes:
        return []
    return [
        {"axis": axis, "reading": reading}
        for axis, reading in axes.items()
        if isinstance(axis, str) and axis.strip() and isinstance(reading, str) and reading.strip()
    ]


def build_case_breakdown(
    case_id: str,
    readout: str,
    evidence_note: str,
    *,
    signals: Sequence[str] | None = None,
    cautions: Sequence[str] | None = None,
    axes: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "case_id": case_id,
        "readout": readout,
        "evidence_note": evidence_note,
    }
    axis_payload = _axis_payload(axes)
    if axis_payload:
        payload["axes"] = axis_payload

    signal_payload = _string_list(signals)
    if signal_payload:
        payload["signals"] = signal_payload

    caution_payload = _string_list(cautions)
    if caution_payload:
        payload["cautions"] = caution_payload

    return payload


def build_comparative_case(
    case_id: str,
    artifact_side_reading: str,
    process_side_reading: str,
    gap_reading: str,
    side_by_side_note: str,
) -> dict[str, str]:
    return {
        "case_id": case_id,
        "artifact_side_reading": artifact_side_reading,
        "process_side_reading": process_side_reading,
        "gap_reading": gap_reading,
        "side_by_side_note": side_by_side_note,
    }


def build_target_risk(
    target_bundle: str,
    integrity_risk_class: str,
    target_reading: str,
    note: str,
    *,
    evidence_coverage: str | None = None,
    routing_note: str | None = None,
) -> dict[str, str]:
    payload = {
        "target_bundle": target_bundle,
        "integrity_risk_class": integrity_risk_class,
        "target_reading": target_reading,
        "note": note,
    }
    if evidence_coverage:
        payload["evidence_coverage"] = evidence_coverage
    if routing_note:
        payload["routing_note"] = routing_note
    return payload

