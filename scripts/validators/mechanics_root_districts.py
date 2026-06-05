"""Mechanic root-district reconnaissance contracts."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue, read_text_or_issue
from validators.mechanics_common import (
    MECHANICS_AGENTS_NAME,
    MECHANICS_EVIDENCE_CLUSTERS_NAME,
    MECHANICS_README_NAME,
    PROOF_TOPOLOGY_NAME,
    ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
    ROADMAP_NAME,
    _markdown_heading_section,
    _markdown_table_rows,
    _require_tokens,
)

MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0084-mechanic-root-district-reconnaissance.md"
)
MECHANIC_ROOT_DISTRICT_RECON_COMMAND = (
    "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon"
)
MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS = (
    "Root District Reconnaissance Ledger",
    "Current root posture",
    "Mechanics relationship",
    "Validation guard",
    "root-district",
)
MECHANIC_ROOT_DISTRICT_RECON_COLUMNS = (
    "District",
    "Authority class",
    "Current root posture",
    "Mechanics relationship",
    "Validation guard",
)
MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS = (
    "docs",
    "evals",
    "fixtures",
    "schemas",
    "examples",
    "scripts",
    "tests",
    "config",
    "manifests",
    "generated",
    "reports",
    "runners",
    "scorers",
    "templates",
    "quests",
    "mechanics",
)
MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS = (
    "config",
    "examples",
    "fixtures",
    "manifests",
    "reports",
    "runners",
    "schemas",
    "scorers",
    "templates",
)
MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    "docs": ("source guidance", "mechanic-owned docs"),
    "evals": ("source proof object", "source eval packages stay out of mechanics"),
    "fixtures": ("route-card-only", "mechanics/proof-infra/parts/fixture-families/fixtures/"),
    "schemas": ("route-card-only", "mechanics/proof-object/parts/eval-contracts/schemas/"),
    "examples": ("route-card-only", "evals/**/examples/"),
    "scripts": ("repo-wide", "mechanic-owned scripts"),
    "tests": ("repo-wide", "mechanics/<mechanic>/parts/<part>/tests/"),
    "config": ("route-card-only", "mechanics/agon/parts/*/config/"),
    "manifests": ("route-card-only", "mechanics/recurrence/parts/"),
    "generated": ("derived readers", "part-local generated"),
    "reports": ("route-card-only", "mechanics/release-support/parts/"),
    "runners": ("route-card-only", "mechanics/proof-infra/parts/reportable-contracts/runners/"),
    "scorers": ("route-card-only", "mechanics/proof-infra/parts/reportable-contracts/scorers/"),
    "templates": ("route-card-only", "mechanics/proof-object/parts/eval-authoring/templates/"),
    "quests": ("source quest records", "mechanics/questbook/parts/"),
    "mechanics": ("operation atlas", "mechanics/EVIDENCE_CLUSTERS.md"),
}
MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS = (
    "Mechanic Root-district Reconnaissance",
    "Root District Reconnaissance Ledger",
    "Source Eval Tree Topology",
    "`evals/<claim-family>/<eval-name>/`",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "docs",
    "evals",
    "fixtures",
    "schemas",
    "examples",
    "scripts",
    "tests",
    "config",
    "manifests",
    "generated",
    "reports",
    "runners",
    "scorers",
    "templates",
    "quests",
    "mechanics",
    "route-card-only",
    "mechanic-owned payload",
    "mechanics/AGENTS.md#validation",
)


def validate_mechanic_root_district_recon_surfaces(
    repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = read_text_or_issue(
        repo_root / MECHANICS_EVIDENCE_CLUSTERS_NAME,
        issues,
        root=repo_root,
    )
    if not text:
        return issues

    recon_section = _markdown_heading_section(
        text, "Root District Reconnaissance Ledger"
    )
    if not recon_section:
        issues.append(
            ValidationIssue(
                MECHANICS_EVIDENCE_CLUSTERS_NAME,
                "mechanics evidence cluster map must contain section 'Root District Reconnaissance Ledger'",
            )
        )

    for token in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS:
        if token not in recon_section:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"mechanic root-district reconnaissance must mention {token!r}",
                )
            )

    recon_rows: dict[str, list[str]] = {}
    for cells in _markdown_table_rows(recon_section):
        district_cell = cells[0] if cells else ""
        district_name = district_cell.strip("`")
        if district_name not in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS:
            continue
        if district_name in recon_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` must appear only once in the reconnaissance ledger",
                )
            )
        recon_rows[district_name] = cells
        if len(cells) != len(MECHANIC_ROOT_DISTRICT_RECON_COLUMNS):
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` reconnaissance row must have {len(MECHANIC_ROOT_DISTRICT_RECON_COLUMNS)} columns",
                )
            )
            continue
        for column_name, cell in zip(
            MECHANIC_ROOT_DISTRICT_RECON_COLUMNS[1:],
            cells[1:],
            strict=True,
        ):
            if not cell or cell.lower() in {"-", "n/a", "todo", "tbd"}:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"root district `{district_name}` reconnaissance row must fill `{column_name}`",
                    )
                )
        row_text = " | ".join(cells)
        for token in MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS[district_name]:
            if token not in row_text:
                issues.append(
                    ValidationIssue(
                        MECHANICS_EVIDENCE_CLUSTERS_NAME,
                        f"root district `{district_name}` reconnaissance row must mention '{token}'",
                    )
                )
        if (
            district_name in MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS
            and "route-card-only" not in row_text
        ):
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` reconnaissance row must preserve route-card-only posture",
                )
            )

    for district_name in MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS:
        if district_name not in recon_rows:
            issues.append(
                ValidationIssue(
                    MECHANICS_EVIDENCE_CLUSTERS_NAME,
                    f"root district `{district_name}` must appear in the reconnaissance ledger",
                )
            )

    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME,
        tokens=MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_README_NAME,
        tokens=("Root District Reconnaissance Ledger", "root-district"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=MECHANICS_AGENTS_NAME,
        tokens=("Focused mechanic topology checks", MECHANIC_ROOT_DISTRICT_RECON_COMMAND),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=PROOF_TOPOLOGY_NAME,
        tokens=("Root District Reconnaissance Ledger", "mechanic-owned payload"),
        issues=issues,
    )
    _require_tokens(
        repo_root=repo_root,
        path_name=ROADMAP_NAME,
        tokens=ROADMAP_MECHANICS_EVIDENCE_DIRECTION_TOKENS,
        issues=issues,
    )

    return issues


__all__ = (
    "MECHANIC_ROOT_DISTRICT_RECON_COMMAND",
    "MECHANIC_ROOT_DISTRICT_RECON_COLUMNS",
    "MECHANIC_ROOT_DISTRICT_RECON_DECISION_NAME",
    "MECHANIC_ROOT_DISTRICT_RECON_DECISION_REQUIRED_TOKENS",
    "MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_DISTRICTS",
    "MECHANIC_ROOT_DISTRICT_RECON_REQUIRED_TOKENS",
    "MECHANIC_ROOT_DISTRICT_RECON_ROUTE_CARD_ONLY_DISTRICTS",
    "MECHANIC_ROOT_DISTRICT_RECON_ROW_REQUIRED_TOKENS",
    "validate_mechanic_root_district_recon_surfaces",
)
