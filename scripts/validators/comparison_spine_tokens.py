"""Comparison-spine route and contract token sets."""

from __future__ import annotations

from validators.comparison_spine_paths import (
    COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME,
    COMPARISON_SPINE_LEGACY_INDEX_NAME,
    COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME,
    COMPARISON_SPINE_MECHANIC_PARTS_NAME,
    COMPARISON_SPINE_OVERVIEW_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME,
    COMPARISON_SPINE_PROVENANCE_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME,
    COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME,
)


MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
COMPARISON_SPINE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "docs/guides/COMPARISON_SPINE_GUIDE.md",
    "docs/guides/BASELINE_COMPARISON_GUIDE.md",
    "docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
    "generated/comparison_spine.json",
    COMPARISON_SPINE_MECHANIC_PARTS_NAME,
    COMPARISON_SPINE_OVERVIEW_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_REPORT_NAME,
    COMPARISON_SPINE_FIXED_BASELINE_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_REPORT_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V1_FIXTURE_NAME,
    COMPARISON_SPINE_PEER_COMPARE_V2_FIXTURE_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V1_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_V2_REPORT_NAME,
    COMPARISON_SPINE_STRESS_RECOVERY_REPORT_NAME,
    COMPARISON_SPINE_REPEATED_WINDOW_FIXTURE_NAME,
    COMPARISON_SPINE_PROVENANCE_NAME,
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "style-only movement",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "baseline_mode",
    "comparison_surface",
    "fixtures/contract.json",
    "generated/comparison_spine.json",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/",
    "generated/comparison_spine.json",
    "comparison_surface",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "pressure-to-route maps",
)
COMPARISON_SPINE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "Parts carry comparison-spine fixture and readout surfaces",
    "Source claim meaning stays in `evals/**/EVAL.md`",
    "fixture and readout surfaces",
    "| repo-global score or broad growth proof | source bundle review plus `longitudinal-window` evidence and growth/progression owner route |",
)
COMPARISON_SPINE_PARTS_README_REQUIRED_TOKENS = (
    "spine-overview/",
    "fixed-baseline/",
    "peer-compare/",
    "longitudinal-window/",
    "AGENTS.md#validation",
)
COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
COMPARISON_SPINE_OVERVIEW_PART_REQUIRED_TOKENS = (
    "comparison-spine-proof-flow-v1.md",
    "cross-mode",
    "generated/comparison_spine.json",
    "| overview dossier as comparison result | source bundle comparison surface plus mode-specific part report |",
    "| fixed-baseline, peer-compare, and longitudinal-window collapsed into one score | mode-specific part route plus bundle-local review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_FIXED_BASELINE_PART_REQUIRED_TOKENS = (
    "frozen-same-task-v1",
    "same-task-baseline-proof-flow-v1.md",
    "fixed-baseline",
    "repo-global score",
    "baseline_target_label",
    "| one fixed-baseline result as repo-global score | source bundle review plus comparison-spine bounded read |",
    "| broad growth from same-task regression evidence | `longitudinal-window` evidence plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PEER_COMPARE_PART_REQUIRED_TOKENS = (
    "bounded-change-paired-v1",
    "bounded-change-paired-v2",
    "artifact-process-paired-proof-flow-v1.md",
    "artifact-process-paired-proof-flow-v2.md",
    "Peer-compare",
    "matched_surface",
    "| peer comparison into fixed-baseline by association | source bundle `baseline_mode` and fixed-baseline part route |",
    "| peer-compare blur as broad capability growth or repo-global score | bounded comparison read plus growth/progression owner review |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_LONGITUDINAL_PART_REQUIRED_TOKENS = (
    "repeated-window-bounded-v1",
    "repeated-window-proof-flow-v1.md",
    "repeated-window-proof-flow-v2.md",
    "stress-recovery-window-proof-flow-v1.md",
    "broad growth proof",
    "cross-window invariants",
    "| ordered-window movement as broad growth by association | source bundle claim plus growth/progression owner review |",
    "| repeated-window or stress-recovery evidence as runtime health or antifragility acceptance | `abyss-stack` runtime route or `mechanics/antifragility/` owner route |",
) + COMPARISON_SPINE_PART_README_COMMON_REQUIRED_TOKENS
COMPARISON_SPINE_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Comparison Spine Part Contract Guard",
    "mechanics/comparison-spine/parts/spine-overview/README.md",
    "mechanics/comparison-spine/parts/fixed-baseline/README.md",
    "mechanics/comparison-spine/parts/peer-compare/README.md",
    COMPARISON_SPINE_LONGITUDINAL_PART_README_NAME,
    "part-level contracts",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "stronger owner split",
    "stop-lines",
    "broad growth",
    "pressure-to-owner routes",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_REPORT_PARTS_DECISION_REQUIRED_TOKENS = (
    "mechanics/comparison-spine/parts/",
    "paired_readout_path",
    "generated `proof_artifacts`",
    "spine-overview",
    "fixed-baseline",
    "peer-compare",
    "longitudinal-window",
    "does not make a shared dossier stronger than the source proof object",
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_FIXTURE_PARTS_DECISION_REQUIRED_TOKENS = (
    "fixed-baseline/fixtures/frozen-same-task-v1/",
    "peer-compare/fixtures/bounded-change-paired-v1/",
    "peer-compare/fixtures/bounded-change-paired-v2/",
    "longitudinal-window/fixtures/repeated-window-bounded-v1/",
    "Bundle source truth stays in `evals/**/EVAL.md`",
    "does not make a fixture family stronger than the source proof object",
    COMPARISON_SPINE_PROVENANCE_NAME,
    "python scripts/build_catalog.py --check",
)
COMPARISON_SPINE_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
COMPARISON_SPINE_LEGACY_INDEX_REQUIRED_TOKENS = (
    "fixtures/frozen-same-task-v1/",
    "fixtures/bounded-change-paired-v1/",
    "fixtures/bounded-change-paired-v2/",
    "fixtures/repeated-window-bounded-v1/",
    "active fixed-baseline fixture family",
    "active peer-compare fixture family",
    "active longitudinal-window fixture family",
)


__all__ = tuple(name for name in globals() if name.endswith("_TOKENS"))
