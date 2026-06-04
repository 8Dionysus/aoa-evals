"""Source-bundle doctrine and guide alignment validators."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


SOURCE_EVALS_DIR_NAME = "evals"
EVAL_SELECTION_NAME = "EVAL_SELECTION.md"
EVAL_INDEX_NAME = "EVAL_INDEX.md"
ARTIFACT_PROCESS_GUIDE_NAME = "docs/guides/ARTIFACT_PROCESS_SEPARATION_GUIDE.md"
REPEATED_WINDOW_GUIDE_NAME = "docs/guides/REPEATED_WINDOW_DISCIPLINE_GUIDE.md"
COMPARISON_SPINE_GUIDE_NAME = "docs/guides/COMPARISON_SPINE_GUIDE.md"
INTEGRITY_RISK_CLASSES = (
    "style-over-substance",
    "artifact/process collapse",
    "baseline by association",
    "growth by association",
    "peer-compare blur",
    "fixed-baseline drift",
    "longitudinal overclaim",
    "schema-clean but claim-overstated",
    "routing overreach",
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        return {}

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_dirs.setdefault(eval_dir.name, eval_dir)
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    return discover_eval_dirs(repo_root).get(
        eval_name,
        repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
    )


def validate_comparison_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    comparison_records = [
        record for record in records if record.manifest.get("baseline_mode") != "none"
    ]
    if selected_evals is not None:
        comparison_records = [
            record for record in comparison_records if record.name in selected_evals
        ]
    if not comparison_records:
        return []

    issues: list[ValidationIssue] = []
    doctrine_path = repo_root / COMPARISON_SPINE_GUIDE_NAME
    readme_path = repo_root / "README.md"
    docs_readme_path = repo_root / "docs" / "README.md"
    selection_path = repo_root / EVAL_SELECTION_NAME
    index_path = repo_root / EVAL_INDEX_NAME

    try:
        doctrine_text = doctrine_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [ValidationIssue(COMPARISON_SPINE_GUIDE_NAME, "file is missing")]

    try:
        readme_text = readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        readme_text = ""
        issues.append(ValidationIssue("README.md", "file is missing"))

    try:
        docs_readme_text = docs_readme_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        docs_readme_text = ""
        issues.append(ValidationIssue("docs/README.md", "file is missing"))

    try:
        selection_text = selection_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        selection_text = ""
        issues.append(ValidationIssue(EVAL_SELECTION_NAME, "file is missing"))

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        index_text = ""
        issues.append(ValidationIssue(EVAL_INDEX_NAME, "file is missing"))

    if "generated reader index" not in readme_text:
        issues.append(
            ValidationIssue(
                "README.md",
                "README.md must route generated comparison readers through the generated reader index",
            )
        )

    if "Comparison Spine Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Comparison Spine Guide",
            )
        )
    if "generated/comparison_spine.json" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must reference generated/comparison_spine.json",
            )
        )

    if "## Pick Comparison Surface" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must include a 'Pick Comparison Surface' chooser section",
            )
        )

    if "comparison spine" not in index_text.lower():
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the comparison spine as a public program layer",
            )
        )

    doctrine_names = {record.name for record in comparison_records}
    doctrine_names.add("aoa-eval-integrity-check")
    for name in sorted(doctrine_names):
        if name not in doctrine_text:
            issues.append(
                ValidationIssue(
                    COMPARISON_SPINE_GUIDE_NAME,
                    f"comparison doctrine must mention '{name}'",
                )
            )

    for record in comparison_records:
        comparison_surface = record.manifest.get("comparison_surface")
        if not isinstance(comparison_surface, dict):
            continue
        selection_question = comparison_surface.get("selection_question")
        if isinstance(selection_question, str) and selection_question not in selection_text:
            issues.append(
                ValidationIssue(
                    EVAL_SELECTION_NAME,
                    f"EVAL_SELECTION.md must include the comparison selector question for '{record.name}'",
                )
            )

    return issues


def validate_artifact_process_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / ARTIFACT_PROCESS_GUIDE_NAME,
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    selection_text = read_text_or_issue(
        repo_root / EVAL_SELECTION_NAME,
        issues,
        root=repo_root,
    )
    index_text = read_text_or_issue(
        repo_root / EVAL_INDEX_NAME,
        issues,
        root=repo_root,
    )

    if "Artifact Process Separation Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Artifact Process Separation Guide",
            )
        )
    if "## Artifact Process Layer" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must describe the artifact/process layer as a bounded program layer",
            )
        )
    if "standalone artifact and workflow surfaces" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must say that the artifact/process bridge is read only after the standalone artifact and workflow surfaces",
            )
        )

    for phrase in (
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
        "aoa-output-vs-process-gap",
        "aoa-witness-trace-integrity",
        "aoa-compost-provenance-preservation",
        "matched conditions",
        "style-over-substance",
        "mechanics/comparison-spine/parts/peer-compare/fixtures/bounded-change-paired-v2/README.md",
        "mechanics/comparison-spine/parts/peer-compare/reports/artifact-process-paired-proof-flow-v2.md",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    ARTIFACT_PROCESS_GUIDE_NAME,
                    f"artifact/process doctrine must mention '{phrase}'",
                )
            )

    record_map = {record.name: record for record in records}
    bundle_phrase_checks = {
        "aoa-artifact-review-rubric": ("artifact-side reading",),
        "aoa-bounded-change-quality": ("process-side reading",),
        "aoa-output-vs-process-gap": ("matched-condition", "side_by_side_note"),
        "aoa-witness-trace-integrity": ("adjacent witness context",),
        "aoa-compost-provenance-preservation": ("adjacent compost context",),
    }
    for name, phrases in bundle_phrase_checks.items():
        record = record_map.get(name)
        if record is None:
            continue
        bundle_text = "\n".join(record.sections.values())
        for phrase in phrases:
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"artifact/process distinctness wording must mention '{phrase}'",
                    )
                )
    return issues


def validate_repeated_window_doctrine_surfaces(
    repo_root: Path,
    records: Sequence[Any],
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    if selected_evals is not None and "aoa-longitudinal-growth-snapshot" not in selected_evals:
        return []

    issues: list[ValidationIssue] = []
    guide_text = read_text_or_issue(
        repo_root / REPEATED_WINDOW_GUIDE_NAME,
        issues,
        root=repo_root,
    )
    docs_readme_text = read_text_or_issue(
        repo_root / "docs" / "README.md",
        issues,
        root=repo_root,
    )
    selection_text = read_text_or_issue(
        repo_root / EVAL_SELECTION_NAME,
        issues,
        root=repo_root,
    )
    index_text = read_text_or_issue(
        repo_root / EVAL_INDEX_NAME,
        issues,
        root=repo_root,
    )

    if "Repeated Window Discipline Guide" not in docs_readme_text:
        issues.append(
            ValidationIssue(
                "docs/README.md",
                "docs/README.md must list Repeated Window Discipline Guide",
            )
        )
    for phrase in (
        "aoa-longitudinal-growth-snapshot",
        "context_note",
        "transition_note",
        "after",
    ):
        if phrase not in guide_text:
            issues.append(
                ValidationIssue(
                    REPEATED_WINDOW_GUIDE_NAME,
                    f"repeated-window doctrine must mention '{phrase}'",
                )
            )

    if "context_note" not in selection_text or "transition_note" not in selection_text:
        issues.append(
            ValidationIssue(
                EVAL_SELECTION_NAME,
                "EVAL_SELECTION.md must explain context_note and transition_note for repeated-window reading",
            )
        )
    if "mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md" not in index_text:
        issues.append(
            ValidationIssue(
                EVAL_INDEX_NAME,
                "EVAL_INDEX.md must reference mechanics/comparison-spine/parts/longitudinal-window/reports/repeated-window-proof-flow-v2.md for repeated-window discipline",
            )
        )

    record_map = {record.name: record for record in records}
    record = record_map.get("aoa-longitudinal-growth-snapshot")
    if record is not None:
        bundle_text = "\n".join(record.sections.values())
        for phrase in ("context_note", "transition_note"):
            if phrase not in bundle_text:
                issues.append(
                    ValidationIssue(
                        relative_location(record.eval_md_path, repo_root),
                        f"longitudinal bundle wording must mention '{phrase}'",
                    )
                )
    return issues


def validate_integrity_taxonomy_surfaces(
    repo_root: Path,
    selected_evals: set[str] | None = None,
) -> list[ValidationIssue]:
    relevant_names = {
        "aoa-eval-integrity-check",
        "aoa-regression-same-task",
        "aoa-output-vs-process-gap",
        "aoa-longitudinal-growth-snapshot",
        "aoa-artifact-review-rubric",
        "aoa-bounded-change-quality",
    }
    if selected_evals is not None and not relevant_names.intersection(selected_evals):
        return []

    issues: list[ValidationIssue] = []
    eval_dir = source_eval_dir(repo_root, "aoa-eval-integrity-check")
    eval_text = read_text_or_issue(
        eval_dir / "EVAL.md",
        issues,
        root=repo_root,
    )
    review_text = read_text_or_issue(
        eval_dir / "notes" / "review-contract.md",
        issues,
        root=repo_root,
    )
    example_report_location = "evals/capability/aoa-eval-integrity-check/examples/example-report.md"
    example_report_text = read_text_or_issue(
        eval_dir / "examples" / "example-report.md",
        issues,
        root=repo_root,
    )
    schema_location = "evals/capability/aoa-eval-integrity-check/reports/summary.schema.json"
    schema_payload = load_json_payload(
        eval_dir / "reports" / "summary.schema.json",
        issues,
        root=repo_root,
    )
    schema_enum: list[str] = []
    if isinstance(schema_payload, dict):
        properties = schema_payload.get("properties", {})
        if isinstance(properties, dict):
            per_target_breakdown = properties.get("per_target_breakdown", {})
            if isinstance(per_target_breakdown, dict):
                items = per_target_breakdown.get("items", {})
                if isinstance(items, dict):
                    item_properties = items.get("properties", {})
                    if isinstance(item_properties, dict):
                        risk_schema = item_properties.get("integrity_risk_class", {})
                        if isinstance(risk_schema, dict):
                            raw_enum = risk_schema.get("enum", [])
                            if isinstance(raw_enum, list):
                                schema_enum = [
                                    item
                                    for item in raw_enum
                                    if isinstance(item, str)
                                ]
    if tuple(schema_enum) != INTEGRITY_RISK_CLASSES:
        issues.append(
            ValidationIssue(
                schema_location,
                "integrity_risk_class enum must match the public integrity risk taxonomy",
            )
        )

    for phrase in INTEGRITY_RISK_CLASSES:
        if phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/notes/review-contract.md",
                    f"integrity review contract must mention '{phrase}'",
                )
            )
        if phrase not in eval_text and phrase not in review_text:
            issues.append(
                ValidationIssue(
                    "evals/capability/aoa-eval-integrity-check/EVAL.md",
                    f"integrity sidecar surfaces must mention '{phrase}' in EVAL.md or review-contract.md",
                )
            )
        if phrase not in example_report_text:
            issues.append(
                ValidationIssue(
                    example_report_location,
                    f"integrity example report must mention '{phrase}'",
                )
            )
    return issues
