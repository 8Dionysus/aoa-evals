"""Comparison-spine path constants."""

from __future__ import annotations

from pathlib import Path


DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)

COMPARISON_SPINE_MECHANIC_README_NAME = "mechanics/comparison-spine/README.md"
COMPARISON_SPINE_MECHANIC_AGENTS_NAME = "mechanics/comparison-spine/AGENTS.md"
COMPARISON_SPINE_MECHANIC_PARTS_NAME = "mechanics/comparison-spine/PARTS.md"
COMPARISON_SPINE_PARTS_README_NAME = "mechanics/comparison-spine/parts/README.md"
COMPARISON_SPINE_OVERVIEW_PART_README_NAME = "mechanics/comparison-spine/parts/spine-overview/README.md"
COMPARISON_SPINE_FIXED_BASELINE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_PART_README_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/README.md"
)
COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/README.md"
)
COMPARISON_SPINE_OVERVIEW_REPORT_NAME = (
    "mechanics/comparison-spine/parts/spine-overview/reports/"
    "comparison-spine-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/reports/"
    "same-task-baseline-proof-flow-v1.md"
)
COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/fixed-baseline/fixtures/"
    "frozen-same-task-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v1.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/reports/"
    "artifact-process-paired-proof-flow-v2.md"
)
COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v1/README.md"
)
COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/peer-compare/fixtures/"
    "bounded-change-paired-v2/README.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "repeated-window-proof-flow-v2.md"
)
COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/reports/"
    "stress-recovery-window-proof-flow-v1.md"
)
COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME = (
    "mechanics/comparison-spine/parts/longitudinal-window/fixtures/"
    "repeated-window-bounded-v1/README.md"
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0029-comparison-spine-report-parts.md"
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0040-comparison-spine-fixture-parts.md"
)
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0059-comparison-spine-part-contract-guard.md"
)
COMPARISON_SPINE_PROVENANCE_NAME = "mechanics/comparison-spine/PROVENANCE.md"
COMPARISON_SPINE_LEGACY_INDEX_NAME = "mechanics/comparison-spine/legacy/INDEX.md"
COMPARISON_SPINE_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0011-comparison-spine-mechanic-package.md"
)


__all__ = tuple(name for name in globals() if name.endswith("_NAME") or name == "DECISION_INDEX_PATHS")
