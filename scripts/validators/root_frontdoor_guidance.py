"""Root README and docs route-map validation."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.root_guidance_common import markdown_python_commands, reject_tokens, require_tokens

ROOT_README_SURFACE_REQUIRED_TOKENS = (
    "# aoa-evals Bounded Proof Canon",
    "AoA proof canon",
    "bounded proof surface",
    "repo to authority class",
    "docs/architecture/AGENT_INDEX.md",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "mechanics/README.md",
    "Eval Bundle Selection Chooser",
    "Eval Bundle Index",
    "public proof-organ entry",
    "Agent route law and local checks",
    "Executable validation routes live in",
    "practice canon -> workflow canon -> proof canon",
)
ROOT_README_SURFACE_FORBIDDEN_TOKENS = (
    "Which comparison, artifact/process, repeated-window, or shared-infra guide applies?",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "generated/eval_report_index.min.json",
    "generated/comparison_spine.json",
)

DOCS_README_ROUTE_MAP_REQUIRED_TOKENS = (
    "# Documentation Map",
    "human and agent entrypoint",
    "Operational edit law belongs in the nearest `AGENTS.md`",
    "aoa-evals Bounded Proof Canon",
    "Mechanics Operation Atlas",
    "Decision Records Index",
    "Eval Bundle Selection Chooser",
    "Eval Bundle Index",
    "Folder Map",
    "docs/architecture/",
    "docs/guides/",
    "docs/operations/",
    "guides/COMPARISON_SPINE_GUIDE.md",
    "guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md",
    "guides/SHARED_PROOF_INFRA_GUIDE.md",
    "guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
    "Route Residue Guards",
    "Recommended Reading Paths",
    "Mechanics Refactor Path",
    "Validation Route",
    "docs/AGENTS.md#validation",
)
DOCS_README_ROUTE_MAP_FORBIDDEN_TOKENS = (
    "[Mechanics](../mechanics/README.md)",
    "[Decisions](decisions/README.md)",
    "[README](../README.md)",
    "[EVAL_SELECTION]",
    "[EVAL_INDEX]",
    "Verify Current Surfaces",
)


def validate_root_readme_surface_role(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root,
        "README.md",
        ROOT_README_SURFACE_REQUIRED_TOKENS,
        issues,
    )
    if text:
        reject_tokens(
            text=text,
            path_name="README.md",
            tokens=ROOT_README_SURFACE_FORBIDDEN_TOKENS,
            message_template=(
                "root README Proof Check should stay compact; detailed proof-guide catalogs route to docs/README.md"
            ),
            issues=issues,
        )
    require_tokens(
        repo_root,
        "docs/README.md",
        (
            "aoa-evals Bounded Proof Canon",
            "Eval Bundle Selection Chooser",
            "Eval Bundle Index",
        ),
        issues,
    )

    return issues


def validate_docs_readme_route_map(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    text = require_tokens(
        repo_root,
        "docs/README.md",
        DOCS_README_ROUTE_MAP_REQUIRED_TOKENS,
        issues,
    )
    if not text:
        return issues

    reject_tokens(
        text=text,
        path_name="docs/README.md",
        tokens=DOCS_README_ROUTE_MAP_FORBIDDEN_TOKENS,
        message_template="docs route map must use role labels and keep validation route out of reader paths; found '{token}'",
        issues=issues,
    )
    if markdown_python_commands(text):
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs route map must route executable validation commands to docs/AGENTS.md instead of carrying command blocks",
            )
        )

    recommended_pos = text.find("## Recommended Reading Paths")
    validation_pos = text.find("## Validation Route")
    if validation_pos != -1 and recommended_pos != -1 and validation_pos < recommended_pos:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "Validation Route must stay after Recommended Reading Paths so reader paths remain contiguous",
            )
        )

    return issues
