from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Callable

import eval_catalog_contract


GENERATED_DIR_NAME = eval_catalog_contract.GENERATED_DIR_NAME
CAPSULE_NAME = "eval_capsules.json"
CAPSULE_VERSION = 1
CAPSULE_SOURCE_OF_TRUTH = {
    "eval_markdown": "bundles/*/EVAL.md",
    "eval_catalog": f"{GENERATED_DIR_NAME}/{eval_catalog_contract.FULL_CATALOG_NAME}",
}
CAPSULE_ENTRY_KEYS = (
    "name",
    "category",
    "status",
    "summary",
    "bounded_claim_short",
    "use_when_short",
    "do_not_use_short",
    "verdict_shape",
    "blind_spot_short",
    "what_this_does_not_prove",
    "proof_artifact_short",
    "technique_dependencies",
    "skill_dependencies",
    "eval_path",
)
REQUIRED_SOURCE_HEADINGS = (
    "Bounded claim",
    "Trigger boundary",
    "Blind spots",
    "Interpretation guidance",
)


def normalize_markdown_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n")
    normalized = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", normalized)
    normalized = re.sub(r"`([^`]+)`", r"\1", normalized)
    normalized = normalized.replace("**", "")
    normalized = normalized.replace("__", "")
    normalized = normalized.replace("*", "")
    normalized = normalized.replace("_", "")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def split_paragraphs(text: str) -> list[str]:
    return [
        normalize_markdown_text(paragraph)
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]


def trim_summary(
    text: str,
    *,
    max_words: int,
    max_chars: int,
) -> str:
    words = text.split()
    trimmed = " ".join(words[:max_words])
    if len(trimmed) > max_chars:
        trimmed = trimmed[: max_chars + 1].rsplit(" ", 1)[0].rstrip(" ,;:")
    if len(words) > max_words or len(text) > len(trimmed):
        return f"{trimmed}..."
    return trimmed


def collect_bullets_after_label(
    text: str,
    *,
    label_matcher: Callable[[str], bool],
) -> list[str]:
    lines = text.splitlines()
    collecting = False
    bullets: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not collecting:
            if label_matcher(stripped):
                collecting = True
            continue

        if stripped.startswith("- "):
            bullets.append(normalize_markdown_text(stripped[2:]))
            continue
        if not stripped:
            if bullets:
                break
            continue
        if bullets:
            break
    return bullets


def extract_claim_paragraph(section_text: str) -> str:
    paragraphs = split_paragraphs(section_text)
    for paragraph in paragraphs:
        lower = paragraph.lower()
        if lower.startswith("this eval is designed to support a claim like"):
            continue
        if lower.startswith("this eval does not support claims such as"):
            continue
        cleaned = re.sub(r"\s-\s", "; ", paragraph)
        cleaned = cleaned.replace(": ;", ":")
        cleaned = cleaned.replace(":;", ":")
        return cleaned
    return ""


def extract_trigger_boundary_groups(section_text: str) -> tuple[list[str], list[str]]:
    use_when = collect_bullets_after_label(
        section_text,
        label_matcher=lambda line: line == "Use this eval when:",
    )
    do_not_use = collect_bullets_after_label(
        section_text,
        label_matcher=lambda line: line == "Do not use this eval when:",
    )
    return use_when, do_not_use


def extract_blind_spot_bullets(section_text: str) -> list[str]:
    return collect_bullets_after_label(
        section_text,
        label_matcher=lambda line: line == "This eval does not prove:",
    )


def extract_interpretation_limit_bullets(section_text: str) -> list[str]:
    return collect_bullets_after_label(
        section_text,
        label_matcher=lambda line: line.startswith("Do not treat ") and line.endswith(":"),
    )


def validate_capsule_source_sections(
    sections: dict[str, str],
    eval_md_path: Path,
    repo_root: Path,
) -> list[eval_catalog_contract.ContractIssue]:
    issues: list[eval_catalog_contract.ContractIssue] = []
    location = eval_catalog_contract.relative_location(eval_md_path, repo_root)
    for heading in REQUIRED_SOURCE_HEADINGS:
        content = sections.get(heading, "")
        if not content.strip():
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    f"missing capsule source section '{heading}'",
                )
            )

    bounded_claim = sections.get("Bounded claim", "")
    if bounded_claim.strip() and not extract_claim_paragraph(bounded_claim):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                "section 'Bounded claim' must contain a derivable bounded claim paragraph",
            )
        )

    trigger_boundary = sections.get("Trigger boundary", "")
    if trigger_boundary.strip():
        use_when, do_not_use = extract_trigger_boundary_groups(trigger_boundary)
        if not use_when:
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    "section 'Trigger boundary' must include a 'Use this eval when:' bullet list",
                )
            )
        if not do_not_use:
            issues.append(
                eval_catalog_contract.ContractIssue(
                    location,
                    "section 'Trigger boundary' must include a 'Do not use this eval when:' bullet list",
                )
            )

    blind_spots = sections.get("Blind spots", "")
    if blind_spots.strip() and not extract_blind_spot_bullets(blind_spots):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                "section 'Blind spots' must include a 'This eval does not prove:' bullet list",
            )
        )

    interpretation = sections.get("Interpretation guidance", "")
    if interpretation.strip() and not extract_interpretation_limit_bullets(interpretation):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                "section 'Interpretation guidance' must include a 'Do not treat ... as:' bullet list",
            )
        )
    return issues


def summarize_bounded_claim(section_text: str) -> str:
    claim = extract_claim_paragraph(section_text)
    return trim_summary(claim, max_words=28, max_chars=190)


def summarize_use_when(section_text: str) -> str:
    use_when, _do_not_use = extract_trigger_boundary_groups(section_text)
    return trim_summary("; ".join(use_when[:2]), max_words=24, max_chars=170)


def summarize_do_not_use(section_text: str) -> str:
    _use_when, do_not_use = extract_trigger_boundary_groups(section_text)
    return trim_summary("; ".join(do_not_use[:2]), max_words=24, max_chars=170)


def summarize_blind_spots(section_text: str) -> str:
    blind_spots = extract_blind_spot_bullets(section_text)
    return trim_summary("; ".join(blind_spots[:3]), max_words=24, max_chars=170)


def summarize_interpretation_limits(section_text: str) -> str:
    limits = extract_interpretation_limit_bullets(section_text)
    return trim_summary("; ".join(limits[:3]), max_words=28, max_chars=190)


def summarize_proof_artifacts(catalog_entry: dict[str, Any]) -> str:
    proof_artifacts = catalog_entry.get("proof_artifacts", {})
    if not isinstance(proof_artifacts, dict):
        return "bundle-local notes and examples only"

    labels: list[str] = []
    if proof_artifacts.get("shared_fixture_family_path"):
        labels.append("shared fixture family")
    if proof_artifacts.get("runner_contract_path"):
        labels.append("runner contract")
    if proof_artifacts.get("scorer_helper_paths"):
        labels.append("shared scorer helper")
    if proof_artifacts.get("report_schema_path"):
        labels.append("schema-backed report")

    if not labels:
        return "bundle-local notes and examples only"

    return "; ".join(labels)


def capsule_entry(
    repo_root: Path,
    record: Any,
    catalog_entry: dict[str, Any],
) -> dict[str, Any]:
    sections = record.sections
    return {
        "name": record.metadata["name"],
        "category": record.metadata["category"],
        "status": record.metadata["status"],
        "summary": record.metadata["summary"],
        "bounded_claim_short": summarize_bounded_claim(sections["Bounded claim"]),
        "use_when_short": summarize_use_when(sections["Trigger boundary"]),
        "do_not_use_short": summarize_do_not_use(sections["Trigger boundary"]),
        "verdict_shape": catalog_entry["verdict_shape"],
        "blind_spot_short": summarize_blind_spots(sections["Blind spots"]),
        "what_this_does_not_prove": summarize_interpretation_limits(
            sections["Interpretation guidance"]
        ),
        "proof_artifact_short": summarize_proof_artifacts(catalog_entry),
        "technique_dependencies": list(record.metadata["technique_dependencies"]),
        "skill_dependencies": list(record.metadata["skill_dependencies"]),
        "eval_path": eval_catalog_contract.relative_location(record.eval_md_path, repo_root),
    }


def build_capsule_payload(
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
    return {
        "capsule_version": CAPSULE_VERSION,
        "source_of_truth": CAPSULE_SOURCE_OF_TRUTH,
        "evals": [
            capsule_entry(repo_root, record, catalog_entries[record.name])
            for record in sorted_records
        ],
    }


def validate_capsule_alignment(
    full_catalog: dict[str, Any],
    capsules: dict[str, Any],
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
    capsule_entries, capsule_entry_issues = eval_catalog_contract.catalog_entries_by_name(
        capsules,
        array_key="evals",
        key_name="name",
        location=location,
    )
    issues.extend(catalog_entry_issues)
    issues.extend(capsule_entry_issues)
    if issues:
        return issues

    catalog_names = set(catalog_entries)
    capsule_names = set(capsule_entries)
    if target_eval_names is not None:
        catalog_names = catalog_names & target_eval_names
        capsule_names = capsule_names & target_eval_names
    for missing in sorted(catalog_names - capsule_names):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                f"capsules are missing eval '{missing}' from generated/eval_catalog.json",
            )
        )
    for extra in sorted(capsule_names - catalog_names):
        issues.append(
            eval_catalog_contract.ContractIssue(
                location,
                f"capsules contain unknown eval '{extra}'",
            )
        )
    shared_fields = (
        "name",
        "category",
        "status",
        "summary",
        "verdict_shape",
        "technique_dependencies",
        "skill_dependencies",
        "eval_path",
    )
    for name in sorted(catalog_names & capsule_names):
        catalog_entry = catalog_entries[name]
        capsule_entry_data = capsule_entries[name]
        for field_name in shared_fields:
            if capsule_entry_data.get(field_name) != catalog_entry.get(field_name):
                issues.append(
                    eval_catalog_contract.ContractIssue(
                        location,
                        f"capsule field '{field_name}' for '{name}' does not align with generated/eval_catalog.json",
                    )
                )
    return issues
