"""Root legacy single-bridge residue checks."""

from __future__ import annotations

import re
from pathlib import Path

from validators import root_legacy_common as common
from validators.common import ValidationIssue, read_text_or_issue


LEGACY_NAMING_NAME = common.LEGACY_NAMING_NAME
LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME = (
    common.LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME
)
LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME = common.LEGACY_NAMING_POSTURE_GUIDE_DECISION_NAME
LEGACY_NAMING_SECOND_ACTIVE_BRIDGE_RE = re.compile(
    r"(?:enter|enters|mapped)\s+through\s+`mechanics/[^`]+/PROVENANCE\.md`"
    r"\s+and\s+`mechanics/[^`]+/legacy/INDEX\.md`"
    r"|Use package\s+`PROVENANCE\.md`,\s+`legacy/INDEX\.md`",
    re.MULTILINE,
)
LEGACY_NAMING_DIRECT_MECHANIC_LEGACY_INDEX_RE = re.compile(
    r"`mechanics/[a-z0-9-]+/legacy/INDEX\.md`"
)
LEGACY_SINGLE_BRIDGE_RESIDUE_RE = re.compile(
    r"(?:enter|enters|entered|lookup starts from the active route and then enters)\s+"
    r"`PROVENANCE\.md`,\s+`legacy/INDEX\.md`"
    r"|`PROVENANCE\.md`\s+and\s+`legacy/INDEX\.md`"
    r"|`mechanics/[a-z0-9-]+/PROVENANCE\.md`\s+and\s+`mechanics/[a-z0-9-]+/legacy/INDEX\.md`"
    r"|entered through\s+`PROVENANCE\.md`\s+and\s+then\s+through\s+`legacy/INDEX\.md`",
    re.MULTILINE,
)
LEGACY_SINGLE_BRIDGE_RESIDUE_SURFACES = (
    common.DESIGN_NAME,
    common.LEGACY_NAMING_NAME,
    common.PROOF_TOPOLOGY_NAME,
    common.MECHANICS_EVIDENCE_CLUSTERS_NAME,
    "mechanics/README.md",
    common.ROADMAP_NAME,
    "CHANGELOG.md",
    "schemas/README.md",
    "schemas/AGENTS.md",
    "manifests/README.md",
    "manifests/AGENTS.md",
    "config/README.md",
    "config/AGENTS.md",
    "examples/README.md",
    "examples/AGENTS.md",
    "fixtures/README.md",
    "fixtures/AGENTS.md",
    "reports/README.md",
    "reports/AGENTS.md",
    "runners/README.md",
    "runners/AGENTS.md",
    "scorers/README.md",
    "scorers/AGENTS.md",
    "templates/README.md",
    "templates/AGENTS.md",
    "docs/decisions/AOA-EV-D-0071-mechanic-legacy-skeleton-contract.md",
    "docs/decisions/AOA-EV-D-0075-mechanic-provenance-entry-contract.md",
    "docs/decisions/AOA-EV-D-0082-mechanic-parent-direction-contract.md",
    "docs/decisions/AOA-EV-D-0089-mechanic-legacy-single-bridge.md",
    "docs/decisions/AOA-EV-D-0090-mechanic-provenance-bridge-posture.md",
    LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_DECISION_NAME,
)


def validate_legacy_single_bridge_residue_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    text = read_text_or_issue(repo_root / LEGACY_NAMING_NAME, issues, root=repo_root)
    if text:
        for match in LEGACY_NAMING_SECOND_ACTIVE_BRIDGE_RE.finditer(text):
            issues.append(
                ValidationIssue(
                    LEGACY_NAMING_NAME,
                    "legacy naming map must keep `PROVENANCE.md` as the single controlled bridge from active mechanic surfaces; `legacy/INDEX.md` may appear only as archive-internal detail after that bridge",
                )
            )
        for match in LEGACY_NAMING_DIRECT_MECHANIC_LEGACY_INDEX_RE.finditer(text):
            issues.append(
                ValidationIssue(
                    LEGACY_NAMING_NAME,
                    "legacy naming posture guide must not carry direct mechanic legacy index paths; route to the active mechanic and package PROVENANCE.md",
                )
            )
    for path_name in LEGACY_SINGLE_BRIDGE_RESIDUE_SURFACES:
        surface_path = repo_root / path_name
        if not surface_path.exists():
            continue
        surface_text = read_text_or_issue(surface_path, issues, root=repo_root)
        if not surface_text:
            continue
        if LEGACY_SINGLE_BRIDGE_RESIDUE_RE.search(surface_text):
            issues.append(
                ValidationIssue(
                    path_name,
                    "legacy route wording must cross only through PROVENANCE.md; archive index, distillation log, and raw lineage are archive-internal after that bridge",
                )
            )
    return issues
