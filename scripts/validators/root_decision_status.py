"""Decision status-line shape contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue


DECISION_STATUS_DETAIL_MARKERS = (";", "superseded by")


def validate_decision_status_lines(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    decisions_root = repo_root / "docs" / "decisions"
    if not decisions_root.exists():
        return issues

    for decision_path in sorted(decisions_root.glob("AOA-EV-D-[0-9][0-9][0-9][0-9]-*.md")):
        relative_path = decision_path.relative_to(repo_root).as_posix()
        try:
            lines = decision_path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            issues.append(ValidationIssue(relative_path, f"failed to read decision: {exc}"))
            continue
        for line_number, line in enumerate(lines, start=1):
            if not line.startswith("- Status:"):
                continue
            status = line.removeprefix("- Status:").strip()
            normalized_status = status.lower()
            if any(marker in normalized_status for marker in DECISION_STATUS_DETAIL_MARKERS):
                issues.append(
                    ValidationIssue(
                        f"{relative_path}:{line_number}",
                        "decision status should stay atomic; put applicability or supersession detail in dated Current Applicability and Review Log",
                    )
                )
            break
    return issues


__all__ = (
    "DECISION_STATUS_DETAIL_MARKERS",
    "validate_decision_status_lines",
)
