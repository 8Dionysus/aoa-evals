"""Source eval evidence and review-policy contract validation."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any, Sequence

from validators.common import ValidationIssue
from validators.source_eval_common import relative_location


def resolve_manifest_path(bundle_dir: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return bundle_dir / candidate


def has_evidence_kind(evidence: Sequence[dict[str, Any]], kind: str) -> bool:
    return any(item.get("kind") == kind for item in evidence)


def load_evidence_texts(
    bundle_dir: Path,
    evidence: Sequence[dict[str, Any]],
    *,
    kind: str,
) -> list[str]:
    texts: list[str] = []
    for item in evidence:
        if item.get("kind") != kind:
            continue
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.is_file():
            continue
        try:
            texts.append(resolved_path.read_text(encoding="utf-8").lower())
        except OSError:
            continue
    return texts


def contains_phrase_group(text: str, phrases: Sequence[str]) -> bool:
    return any(phrase in text for phrase in phrases)


def validate_status_specific_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    required_evidence_by_status = {
        "portable": ("portable_review",),
        "baseline": ("portable_review",),
        "canonical": ("portable_review", "canonical_readiness"),
    }
    status = manifest.get("status")
    for kind in required_evidence_by_status.get(status, ()):
        if not has_evidence_kind(evidence, kind):
            issues.append(
                ValidationIssue(
                    location,
                    f"status '{status}' requires an evidence entry with kind '{kind}'",
                )
            )

    if status == "bounded":
        support_note_text = "\n".join(
            load_evidence_texts(bundle_dir, evidence, kind="support_note")
        )
        if not support_note_text:
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires an evidence entry with kind 'support_note'",
                )
            )
            return

        phrase_groups = (
            ("approve for bounded", "approve for bounded promotion"),
            ("readout",),
            ("failure",),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions",
                )
            )


def validate_status_portability_monotonicity(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    required_portability_by_status = {
        "draft": "local-shaped",
        "bounded": "local-shaped",
        "portable": "portable",
        "baseline": "portable",
        "canonical": "broad",
    }
    status = manifest.get("status")
    portability_level = manifest.get("portability_level")
    required_portability = required_portability_by_status.get(status)
    if required_portability is None:
        return
    if portability_level != required_portability:
        issues.append(
            ValidationIssue(
                location,
                f"status '{status}' requires portability_level '{required_portability}' but found '{portability_level}'",
            )
        )


def validate_public_safety_reviewed_at(
    manifest: dict[str, Any],
    location: str,
    issues: list[ValidationIssue],
) -> None:
    status = manifest.get("status")
    raw_value = manifest.get("public_safety_reviewed_at")
    if raw_value is None:
        if status == "canonical":
            issues.append(
                ValidationIssue(
                    location,
                    "status 'canonical' requires public_safety_reviewed_at with a fresh YYYY-MM-DD review date",
                )
            )
        return

    if not isinstance(raw_value, str) or not raw_value:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a non-empty string",
            )
        )
        return

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_value):
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must use YYYY-MM-DD format",
            )
        )
        return

    try:
        reviewed_date = date.fromisoformat(raw_value)
    except ValueError:
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must be a valid calendar date",
            )
        )
        return
    if reviewed_date > date.today():
        issues.append(
            ValidationIssue(
                location,
                "public_safety_reviewed_at must not be in the future",
            )
        )


def validate_comparative_summary_contract(
    manifest: dict[str, Any],
    bundle_dir: Path,
    location: str,
    evidence: Sequence[dict[str, Any]],
    issues: list[ValidationIssue],
) -> None:
    if manifest.get("report_format") != "comparative-summary":
        return

    if not has_evidence_kind(evidence, "support_note"):
        issues.append(
            ValidationIssue(
                location,
                "report_format 'comparative-summary' requires an evidence entry with kind 'support_note'",
            )
        )
        return

    support_note_text = "\n".join(
        load_evidence_texts(bundle_dir, evidence, kind="support_note")
    )
    baseline_mode = manifest.get("baseline_mode")

    if baseline_mode in {"fixed-baseline", "previous-version"}:
        phrase_groups = (
            ("baseline",),
            ("noisy variation",),
            ("style-only", "style only"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    f"comparative-summary bundle with baseline_mode '{baseline_mode}' must state the baseline target, noisy variation, and style-only overread limits in a support note",
                )
            )
    elif baseline_mode == "peer-compare":
        phrase_groups = (
            ("matched",),
            ("side-by-side", "side by side"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'peer-compare' must state matched conditions and side-by-side interpretation limits in a support note",
                )
            )
    elif baseline_mode == "longitudinal-window":
        phrase_groups = (
            ("ordered",),
            ("window",),
            ("same bounded workflow surface", "anchor workflow surface"),
            ("no clear directional movement", "mixed or unstable movement"),
        )
        if not all(contains_phrase_group(support_note_text, group) for group in phrase_groups):
            issues.append(
                ValidationIssue(
                    location,
                    "comparative-summary bundle with baseline_mode 'longitudinal-window' must state ordered windows, cross-window invariants, and cautious movement interpretation in a support note",
                )
            )


def validate_manifest_evidence(
    manifest: dict[str, Any],
    bundle_dir: Path,
    eval_yaml_path: Path,
    issues: list[ValidationIssue],
) -> None:
    location = relative_location(eval_yaml_path)
    evidence = manifest.get("evidence", [])

    for item in evidence:
        raw_path = item.get("path")
        if not isinstance(raw_path, str):
            continue
        resolved_path = resolve_manifest_path(bundle_dir, raw_path)
        if not resolved_path.exists():
            issues.append(
                ValidationIssue(
                    location,
                    f"evidence path '{raw_path}' does not exist",
                )
            )

    if manifest.get("baseline_mode") != "none":
        has_baseline_readiness = any(
            item.get("kind") == "baseline_readiness" for item in evidence
        )
        if not has_baseline_readiness:
            issues.append(
                ValidationIssue(
                    location,
                    "baseline_mode is not 'none' but no evidence entry with kind 'baseline_readiness' is present",
                )
            )

    validate_status_portability_monotonicity(manifest, location, issues)
    validate_status_specific_evidence(manifest, bundle_dir, location, evidence, issues)
    validate_public_safety_reviewed_at(manifest, location, issues)
    validate_comparative_summary_contract(
        manifest,
        bundle_dir,
        location,
        evidence,
        issues,
    )
