from __future__ import annotations

from pathlib import Path
from typing import Any

import eval_capsule_contract
import eval_catalog_contract


GENERATED_DIR_NAME = eval_catalog_contract.GENERATED_DIR_NAME
COMPARISON_SPINE_NAME = "comparison_spine.json"
COMPARISON_SPINE_VERSION = 1
COMPARISON_SPINE_SOURCE_OF_TRUTH = {
    "eval_markdown": "bundles/*/EVAL.md",
    "eval_manifest": "bundles/*/eval.yaml",
    "eval_catalog": f"{GENERATED_DIR_NAME}/{eval_catalog_contract.FULL_CATALOG_NAME}",
}


def is_comparison_bundle(catalog_entry: dict[str, Any]) -> bool:
    return catalog_entry.get("baseline_mode") != "none"


def build_comparison_spine_entry(
    repo_root: Path,
    record: Any,
    catalog_entry: dict[str, Any],
) -> dict[str, Any]:
    comparison_surface = catalog_entry.get("comparison_surface")
    selection_summary = catalog_entry.get("selection_summary", "")
    if not isinstance(selection_summary, str):
        selection_summary = ""
    if not selection_summary and isinstance(comparison_surface, dict):
        raw_question = comparison_surface.get("selection_question")
        if isinstance(raw_question, str):
            selection_summary = raw_question

    interpretation_boundary = catalog_entry.get("interpretation_boundary", "")
    if not isinstance(interpretation_boundary, str):
        interpretation_boundary = ""
    if not interpretation_boundary:
        interpretation_boundary = eval_capsule_contract.summarize_interpretation_limits(
            record.sections["Interpretation guidance"]
        )

    return {
        "name": record.metadata["name"],
        "status": record.metadata["status"],
        "baseline_mode": record.metadata["baseline_mode"],
        "comparison_surface": comparison_surface,
        "proof_artifacts": catalog_entry["proof_artifacts"],
        "relations": catalog_entry["relations"],
        "selection_summary": selection_summary,
        "interpretation_boundary": interpretation_boundary,
        "eval_path": eval_catalog_contract.relative_location(record.eval_md_path, repo_root),
    }


def build_comparison_spine_payload(
    repo_root: Path,
    records: list[Any],
    full_catalog: dict[str, Any],
) -> dict[str, Any]:
    catalog_entries, issues = eval_catalog_contract.catalog_entries_by_name(
        full_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_contract.FULL_CATALOG_NAME,
    )
    if issues:
        raise ValueError(eval_catalog_contract.format_issues(issues))

    sorted_records = sorted(records, key=lambda record: record.name)
    entries = [
        build_comparison_spine_entry(repo_root, record, catalog_entries[record.name])
        for record in sorted_records
        if is_comparison_bundle(catalog_entries[record.name])
    ]
    return {
        "comparison_spine_version": COMPARISON_SPINE_VERSION,
        "source_of_truth": COMPARISON_SPINE_SOURCE_OF_TRUTH,
        "evals": entries,
    }


def validate_comparison_spine_alignment(
    full_catalog: dict[str, Any],
    comparison_spine: dict[str, Any],
    *,
    location: str,
    target_eval_names: set[str] | None = None,
) -> list[eval_catalog_contract.ContractIssue]:
    issues: list[eval_catalog_contract.ContractIssue] = []
    catalog_entries, catalog_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        full_catalog,
        array_key="evals",
        key_name="name",
        location=eval_catalog_contract.FULL_CATALOG_NAME,
    )
    spine_entries, spine_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        comparison_spine,
        array_key="evals",
        key_name="name",
        location=location,
    )
    issues.extend(catalog_entry_issues)
    issues.extend(spine_entry_issues)
    if issues:
        return issues

    comparison_catalog_names = {
        name for name, entry in catalog_entries.items() if is_comparison_bundle(entry)
    }
    spine_names = set(spine_entries)
    if target_eval_names is not None:
        comparison_catalog_names &= target_eval_names
        spine_names &= target_eval_names

    for missing in sorted(comparison_catalog_names - spine_names):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                f"comparison spine is missing eval '{missing}' from generated/eval_catalog.json",
            )
        )
    for extra in sorted(spine_names - comparison_catalog_names):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                f"comparison spine contains unknown or non-comparison eval '{extra}'",
            )
        )

    shared_fields = (
        "name",
        "status",
        "baseline_mode",
        "comparison_surface",
        "proof_artifacts",
        "relations",
        "selection_summary",
        "interpretation_boundary",
        "eval_path",
    )
    for name in sorted(comparison_catalog_names & spine_names):
        catalog_entry = catalog_entries[name]
        spine_entry = spine_entries[name]
        for field_name in shared_fields:
            if spine_entry.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    eval_catalog_contract.ContractIssue(
                        location,
                        f"comparison spine field '{field_name}' for '{name}' does not align with generated/eval_catalog.json",
                    )
                )
    return issues
