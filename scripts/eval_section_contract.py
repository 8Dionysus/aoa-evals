from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

import eval_catalog_contract


GENERATED_DIR_NAME = eval_catalog_contract.GENERATED_DIR_NAME
SECTIONS_NAME = "eval_sections.full.json"
SECTION_VERSION = 1
SECTION_SOURCE_OF_TRUTH = {
    "eval_markdown": "bundles/*/EVAL.md",
    "sections": [
        "Intent",
        "Object under evaluation",
        "Bounded claim",
        "Trigger boundary",
        "Inputs",
        "Fixtures and case surface",
        "Scoring or verdict logic",
        "Baseline or comparison mode",
        "Execution contract",
        "Outputs",
        "Failure modes",
        "Blind spots",
        "Interpretation guidance",
        "Verification",
        "Technique traceability",
        "Skill traceability",
        "Adaptation points",
    ],
}
CANONICAL_HEADINGS = tuple(SECTION_SOURCE_OF_TRUTH["sections"])
SECTION_KEY_BY_HEADING = {
    "Intent": "intent",
    "Object under evaluation": "object_under_evaluation",
    "Bounded claim": "bounded_claim",
    "Trigger boundary": "trigger_boundary",
    "Inputs": "inputs",
    "Fixtures and case surface": "fixtures_and_case_surface",
    "Scoring or verdict logic": "scoring_or_verdict_logic",
    "Baseline or comparison mode": "baseline_or_comparison_mode",
    "Execution contract": "execution_contract",
    "Outputs": "outputs",
    "Failure modes": "failure_modes",
    "Blind spots": "blind_spots",
    "Interpretation guidance": "interpretation_guidance",
    "Verification": "verification",
    "Technique traceability": "technique_traceability",
    "Skill traceability": "skill_traceability",
    "Adaptation points": "adaptation_points",
}


def collect_section_contract_issues(
    sections: dict[str, str],
    *,
    location: str,
) -> list[eval_catalog_contract.ContractIssue]:
    issues: list[eval_catalog_contract.ContractIssue] = []
    section_pairs = list(sections.items())
    headings = [heading for heading, _content in section_pairs]
    heading_counts = Counter(headings)

    for heading in CANONICAL_HEADINGS:
        if heading_counts[heading] == 0:
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    f"missing required section '{heading}'",
                )
            )
        elif heading_counts[heading] > 1:
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    f"duplicate top-level section '{heading}'",
                )
            )

    for heading in headings:
        if heading not in SECTION_KEY_BY_HEADING:
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    f"unexpected top-level section '{heading}'",
                )
            )

    if headings != list(CANONICAL_HEADINGS):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                "top-level sections must match the canonical order exactly",
            )
        )

    for heading, content_markdown in section_pairs:
        if heading in SECTION_KEY_BY_HEADING and not content_markdown.strip():
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    f"section '{heading}' must not be empty",
                )
            )

    return issues


def build_section_entries(sections: dict[str, str]) -> list[dict[str, str]]:
    return [
        {
            "key": SECTION_KEY_BY_HEADING[heading],
            "heading": heading,
            "content_markdown": content_markdown,
        }
        for heading, content_markdown in sections.items()
        if heading in SECTION_KEY_BY_HEADING
    ]


def build_sections_entry(repo_root: Path, record: Any) -> tuple[dict[str, Any] | None, list[eval_catalog_contract.ContractIssue]]:
    location = eval_catalog_contract.relative_location(record.eval_md_path, repo_root)
    issues = collect_section_contract_issues(record.sections, location=location)
    if issues:
        return None, issues

    return (
        {
            "name": record.metadata["name"],
            "category": record.metadata["category"],
            "status": record.metadata["status"],
            "verdict_shape": record.manifest["verdict_shape"],
            "eval_path": eval_catalog_contract.relative_location(record.eval_md_path, repo_root),
            "sections": build_section_entries(record.sections),
        },
        [],
    )


def build_sections_payload(
    repo_root: Path,
    records: list[Any],
) -> tuple[dict[str, Any], list[eval_catalog_contract.ContractIssue]]:
    issues: list[eval_catalog_contract.ContractIssue] = []
    entries: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda item: item.name):
        entry, entry_issues = build_sections_entry(repo_root, record)
        issues.extend(entry_issues)
        if entry is not None:
            entries.append(entry)

    return (
        {
            "section_version": SECTION_VERSION,
            "source_of_truth": SECTION_SOURCE_OF_TRUTH,
            "evals": entries,
        },
        issues,
    )

