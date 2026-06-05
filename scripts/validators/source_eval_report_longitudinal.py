"""Longitudinal report claim-boundary validation."""

from __future__ import annotations

import re
from typing import Any

from validators.common import ValidationIssue


LONGITUDINAL_GROWTH_CLAIM_PHRASES = (
    "broad capability growth",
    "general capability growth",
)
LONGITUDINAL_GROWTH_NEGATION_CUES = (
    "does not",
    "do not",
    "did not",
    "doesn't",
    "don't",
    "cannot",
    "can't",
    "is not",
    "isn't",
    "not prove",
    "not proven",
    "not support",
    "not supported",
    "not imply",
    "not implied",
    "without proving",
    "without implying",
)
LONGITUDINAL_GROWTH_POST_NEGATION_CUES = (
    "is not proven",
    "is not supported",
    "is not implied",
    "not proven",
    "not supported",
    "not implied",
)


def claim_boundary_overclaims_longitudinal_growth(claim_boundary: str) -> bool:
    clauses = [
        clause.strip()
        for clause in re.split(r"[.;:\n]+", claim_boundary.lower())
        if clause.strip()
    ]
    for clause in clauses:
        for phrase in LONGITUDINAL_GROWTH_CLAIM_PHRASES:
            if phrase not in clause:
                continue
            if clause_negates_longitudinal_growth_phrase(clause, phrase):
                continue
            return True
    return False


def clause_negates_longitudinal_growth_phrase(clause: str, phrase: str) -> bool:
    phrase_index = clause.find(phrase)
    if phrase_index == -1:
        return False

    for cue in LONGITUDINAL_GROWTH_NEGATION_CUES:
        cue_index = clause.find(cue)
        if cue_index == -1:
            continue
        if cue_index <= phrase_index <= cue_index + len(cue) + 80:
            return True

    trailing_window = clause[phrase_index : phrase_index + len(phrase) + 80]
    return any(cue in trailing_window for cue in LONGITUDINAL_GROWTH_POST_NEGATION_CUES)


def validate_longitudinal_report_example(
    example_payload: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> None:
    if not isinstance(example_payload, dict):
        return

    claim_boundary = example_payload.get("claim_boundary")
    if isinstance(claim_boundary, str):
        if claim_boundary_overclaims_longitudinal_growth(claim_boundary):
            issues.append(
                ValidationIssue(
                    f"{location}.claim_boundary",
                    "longitudinal example report claim_boundary must stay weaker than broad or general capability growth",
                )
            )

    limitations = example_payload.get("limitations")
    if isinstance(limitations, list):
        lowered_limitations = [
            item.lower()
            for item in limitations
            if isinstance(item, str)
        ]
        if not any("general capability growth" in item for item in lowered_limitations):
            issues.append(
                ValidationIssue(
                    f"{location}.limitations",
                    "longitudinal example report limitations must name that the report does not prove general capability growth",
                )
            )

    windows = example_payload.get("windows")
    if not isinstance(windows, list):
        return

    seen_window_ids: set[str] = set()
    last_order: int | None = None
    for index, window in enumerate(windows):
        if not isinstance(window, dict):
            continue

        window_id = window.get("window_id")
        if isinstance(window_id, str):
            if window_id in seen_window_ids:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_id",
                        f"longitudinal example report window_id '{window_id}' must be unique",
                    )
                )
            seen_window_ids.add(window_id)

        window_order = window.get("window_order")
        if isinstance(window_order, int):
            if last_order is not None and window_order <= last_order:
                issues.append(
                    ValidationIssue(
                        f"{location}.windows[{index}].window_order",
                        "longitudinal example report window_order values must be strictly increasing",
                    )
                )
            last_order = window_order

        transition_note = window.get("transition_note")
        if index == 0 and transition_note is None:
            continue
        if not isinstance(transition_note, str) or not transition_note.strip():
            issues.append(
                ValidationIssue(
                    f"{location}.windows[{index}].transition_note",
                    "longitudinal example report non-initial windows must include a non-empty transition_note",
                )
            )


__all__ = (
    "LONGITUDINAL_GROWTH_CLAIM_PHRASES",
    "LONGITUDINAL_GROWTH_NEGATION_CUES",
    "LONGITUDINAL_GROWTH_POST_NEGATION_CUES",
    "claim_boundary_overclaims_longitudinal_growth",
    "clause_negates_longitudinal_growth_phrase",
    "validate_longitudinal_report_example",
)
