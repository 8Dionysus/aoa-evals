from __future__ import annotations

import json
import textwrap
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_catalog
import eval_section_contract
from validate_repo import (
    NO_ADDITIONAL_STARTER_BUNDLES_TEXT,
    build_capsule_payload,
    build_catalog_payloads,
    build_comparison_spine_payload,
    collect_catalog_records,
    run_validation,
    validate_eval_index,
    write_json_file,
)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def ensure_support_bundle(repo_root: Path, name: str, *, category: str = "workflow") -> None:
    bundle_dir = repo_root / "bundles" / name
    if bundle_dir.exists():
        return

    write_text(
        bundle_dir / "EVAL.md",
        f"""
        ---
        name: {name}
        category: {category}
        status: draft
        summary: Minimal support bundle for validation.
        object_under_evaluation: bounded support surface
        claim_type: bounded
        baseline_mode: none
        report_format: summary
        technique_dependencies: []
        skill_dependencies: []
        ---

        # {name}

        ## Intent
        Minimal support intent.

        ## Object under evaluation
        Minimal support object.

        ## Bounded claim
        This eval is designed to support a claim like:

        under these conditions, the bounded support claim holds on this surface.

        This eval does not support claims such as:
        - broad general strength
        - total safety

        ## Trigger boundary
        Use this eval when:
        - bounded review matters
        - the support surface is the real question

        Do not use this eval when:
        - the task is unbounded
        - the main question is something else

        ## Inputs
        - input

        ## Fixtures and case surface
        - fixture

        ## Scoring or verdict logic
        - logic

        ## Baseline or comparison mode
        - none

        ## Execution contract
        - contract

        ## Outputs
        - output

        ## Failure modes
        - failure

        ## Blind spots
        This eval does not prove:
        - broad general strength
        - stable behavior across time
        - downstream artifact excellence

        ## Interpretation guidance
        Treat a positive result as support for one bounded claim:
        the bounded support claim holds on this surface.

        Do not treat a positive result as:
        - proof of general capability
        - proof of total safety
        - proof that every nearby surface is strong

        ## Verification
        - verify

        ## Technique traceability
        - none

        ## Skill traceability
        - none

        ## Adaptation points
        - point
        """,
    )
    write_text(
        bundle_dir / "eval.yaml",
        yaml.safe_dump(
            {
                "name": name,
                "category": category,
                "status": "draft",
                "object_under_evaluation": "bounded support surface",
                "claim_type": "bounded",
                "baseline_mode": "none",
                "verdict_shape": "categorical",
                "report_format": "summary",
                "maturity_score": 1,
                "rigor_level": "bounded",
                "repeatability": "moderate",
                "portability_level": "local-shaped",
                "review_required": True,
                "validation_strength": "baseline",
                "export_ready": True,
                "blind_spot_disclosure": "required-and-present",
                "score_interpretation_bound": "explicit",
                "technique_dependencies": [],
                "skill_dependencies": [],
                "relations": [],
                "evidence": [
                    {"kind": "origin_need", "path": "notes/origin-need.md"},
                    {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
                ],
            },
            sort_keys=False,
        ),
    )
    write_text(bundle_dir / "notes" / "origin-need.md", "# Origin Need\n")
    write_text(bundle_dir / "examples" / "example-report.md", "# Example Report\n")
    write_text(bundle_dir / "checks" / "eval-integrity-check.md", "# Eval Integrity Check\n")


def build_default_comparison_surface(
    repo_root: Path,
    *,
    bundle_name: str,
    baseline_mode: str,
) -> dict[str, object] | None:
    if baseline_mode == "none":
        return None

    ensure_support_bundle(repo_root, "aoa-eval-integrity-check", category="capability")

    if baseline_mode in {"fixed-baseline", "previous-version"}:
        ensure_support_bundle(repo_root, "aoa-anchor-surface")
        write_text(repo_root / "fixtures" / "frozen-same-task-v1" / "README.md", "# Shared Fixture Family\n")
        write_text(repo_root / "reports" / "same-task-baseline-proof-flow-v1.md", "# Paired Proof\n")
        return {
            "shared_family_path": "fixtures/frozen-same-task-v1/README.md",
            "paired_readout_path": "reports/same-task-baseline-proof-flow-v1.md",
            "integrity_sidecar": "aoa-eval-integrity-check",
            "selection_question": "Do you need a frozen-baseline comparison on the same bounded task family?",
            "anchor_surface": "aoa-anchor-surface",
            "baseline_target_label": "RS-v1 frozen bounded workflow reference",
        }

    if baseline_mode == "peer-compare":
        ensure_support_bundle(repo_root, "aoa-peer-left")
        ensure_support_bundle(repo_root, "aoa-peer-right")
        write_text(repo_root / "fixtures" / "bounded-change-paired-v1" / "README.md", "# Shared Fixture Family\n")
        write_text(repo_root / "reports" / "artifact-process-paired-proof-flow-v1.md", "# Paired Proof\n")
        return {
            "shared_family_path": "fixtures/bounded-change-paired-v1/README.md",
            "paired_readout_path": "reports/artifact-process-paired-proof-flow-v1.md",
            "integrity_sidecar": "aoa-eval-integrity-check",
            "selection_question": "Do you need a side-by-side peer compare between artifact quality and workflow discipline on the same bounded cases?",
            "peer_surfaces": ["aoa-peer-left", "aoa-peer-right"],
            "matched_surface": "same bounded case family under matched peer conditions",
        }

    ensure_support_bundle(repo_root, "aoa-anchor-surface")
    write_text(repo_root / "fixtures" / "repeated-window-bounded-v1" / "README.md", "# Shared Fixture Family\n")
    write_text(repo_root / "reports" / "repeated-window-proof-flow-v1.md", "# Paired Proof\n")
    return {
        "shared_family_path": "fixtures/repeated-window-bounded-v1/README.md",
        "paired_readout_path": "reports/repeated-window-proof-flow-v1.md",
        "integrity_sidecar": "aoa-eval-integrity-check",
        "selection_question": "Do you need ordered repeated-window movement on one named bounded workflow surface?",
        "anchor_surface": "aoa-anchor-surface",
        "window_family_label": "repeated-window-bounded-v1 validation family",
    }


def make_repo_docs(
    repo_root: Path,
    *,
    starter_names: list[str],
    comparison_entries: list[tuple[str, str]] | None = None,
) -> None:
    comparison_entries = comparison_entries or []
    comparison_lines = "\n".join(f"- `{name}`" for _question, name in comparison_entries)
    comparison_questions = "\n".join(
        f"### {question}\n- `{name}`"
        for question, name in comparison_entries
    )
    if not comparison_questions:
        comparison_questions = "### Do you need a frozen-baseline comparison on the same bounded task family?\n- `aoa-regression-same-task`"
    doctrine_names = starter_names + [name for _question, name in comparison_entries] + ["aoa-eval-integrity-check"]
    doctrine_block = "\n".join(f"- `{name}`" for name in sorted(set(doctrine_names)))

    write_text(
        repo_root / "README.md",
        """
        # aoa-evals

        See `docs/COMPARISON_SPINE_GUIDE.md` when you need the comparison ladder.
        See `docs/ARTIFACT_PROCESS_SEPARATION_GUIDE.md` when you need the artifact/process layer.
        Generated comparison routing lives in `generated/comparison_spine.json`.
        """,
    )
    write_text(
        repo_root / "docs" / "README.md",
        """
        # Documentation Map

        - [Comparison Spine Guide](COMPARISON_SPINE_GUIDE.md)
        - [Artifact Process Separation Guide](ARTIFACT_PROCESS_SEPARATION_GUIDE.md)
        - `generated/comparison_spine.json`
        """,
    )
    write_text(
        repo_root / "docs" / "COMPARISON_SPINE_GUIDE.md",
        f"""
        # Comparison Spine Guide

        Current comparison doctrine:
        {doctrine_block}
        """,
    )
    write_text(
        repo_root / "docs" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md",
        """
        # Artifact Process Separation Guide

        `aoa-artifact-review-rubric`
        `aoa-bounded-change-quality`
        `aoa-output-vs-process-gap`
        `aoa-witness-trace-integrity`
        `aoa-compost-provenance-preservation`
        matched conditions
        style-over-substance
        fixtures/bounded-change-paired-v2/README.md
        reports/artifact-process-paired-proof-flow-v2.md
        """,
    )
    write_text(
        repo_root / "EVAL_SELECTION.md",
        f"""
        # Eval Selection

        Current starter posture:
        {"".join(f"- `{name}`\n" for name in starter_names)}

        The artifact/process bridge is read only after the standalone artifact and workflow surfaces are already visible.

        ## Pick Comparison Surface

        {comparison_questions}
        """,
    )


def make_index(
    repo_root: Path,
    name: str,
    category: str,
    *,
    include_comparison_spine: bool = False,
) -> None:
    comparison_spine_block = ""
    if include_comparison_spine:
        comparison_spine_block = """

        ## Comparison Spine

        The comparison spine is a bounded program layer.
        """
    artifact_process_block = """

        ## Artifact Process Layer

        The artifact/process layer is a bounded program layer.
        """
    write_text(
        repo_root / "EVAL_INDEX.md",
        f"""
        # EVAL_INDEX

        ## Starter eval bundles

        | name | category | status | summary |
        |---|---|---|---|
        | {name} | {category} | draft | Minimal summary for validation. |

        ## Planned starter bundles

        {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}
        {comparison_spine_block}
        {artifact_process_block}
        """,
    )


def make_selection(
    repo_root: Path,
    names: list[str],
    comparison_entries: list[tuple[str, str]] | None = None,
) -> None:
    lines = "\n".join(f"- `{name}`" for name in names)
    comparison_entries = comparison_entries or []
    comparison_block = ""
    if comparison_entries:
        comparison_block = "\n## Pick Comparison Surface\n\n" + "\n".join(
            f"### {question}\n- `{name}`"
            for question, name in comparison_entries
        )
    write_text(
        repo_root / "EVAL_SELECTION.md",
        f"""
        # Eval Selection

        Current starter posture:
        {lines}
        The artifact/process bridge is read only after the standalone artifact and workflow surfaces are already visible.
        {comparison_block}
        """,
    )


def make_roadmap(
    repo_root: Path,
    current_public_surface_names: list[str] | None = None,
    *,
    include_absence_note: bool = True,
) -> None:
    current_public_surface_names = current_public_surface_names or []
    current_surface_block = ""
    if current_public_surface_names:
        surface_lines = "\n".join(
            f"- `{name}` as the current public surface for validation."
            for name in current_public_surface_names
        )
        current_surface_block = f"\nCurrent public surface:\n{surface_lines}\n"

    next_candidate_line = (
        f"- {NO_ADDITIONAL_STARTER_BUNDLES_TEXT}"
        if include_absence_note
        else "- placeholder next candidate"
    )

    write_text(
        repo_root / "docs" / "ROADMAP.md",
        f"""
        # Roadmap

        ## What should happen next

        Highest-priority additions:
        - placeholder

        Next likely cross-surface candidate after the current public starter set:
        {next_candidate_line}
        {current_surface_block}
        """,
    )


def make_eval_bundle(
    repo_root: Path,
    *,
    name: str,
    category: str = "workflow",
    status: str = "draft",
    claim_type: str = "bounded",
    baseline_mode: str = "none",
    verdict_shape: str = "categorical",
    report_format: str = "summary",
    portability_level: str | None = None,
    technique_dependencies: list[dict[str, str]] | None = None,
    skill_dependencies: list[dict[str, str]] | None = None,
    relations: list[dict[str, str]] | None = None,
    evidence_entries: list[dict[str, str]] | None = None,
    support_files: dict[str, str] | None = None,
    section_overrides: dict[str, str] | None = None,
    comparison_surface: dict[str, object] | None = None,
) -> None:
    bundle_dir = repo_root / "bundles" / name
    support_files = dict(support_files or {
        "notes/origin-need.md": "# Origin Need\n",
        "examples/example-report.md": "# Example Report\n",
        "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
    })
    technique_dependencies = technique_dependencies or [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        }
    ]
    skill_dependencies = skill_dependencies or [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/aoa-change-protocol/SKILL.md",
        }
    ]
    relations = relations or []
    if comparison_surface is None:
        comparison_surface = build_default_comparison_surface(
            repo_root,
            bundle_name=name,
            baseline_mode=baseline_mode,
        )
    if evidence_entries is None:
        evidence_entries = [
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ]
        if status == "bounded":
            evidence_entries.append(
                {"kind": "support_note", "path": "notes/bounded-promotion-review.md"}
            )
            support_files.setdefault(
                "notes/bounded-promotion-review.md",
                textwrap.dedent(
                    """\
                    # Bounded Review

                    approve for bounded promotion
                    readout distinctions stay explicit
                    failure signals stay visible
                    """
                ),
            )
        if status in {"portable", "baseline", "canonical"}:
            evidence_entries.append(
                {"kind": "portable_review", "path": "notes/portable-review.md"}
            )
            support_files.setdefault("notes/portable-review.md", "# Portable Review\n")
        if status == "canonical":
            evidence_entries.append(
                {"kind": "canonical_readiness", "path": "notes/canonical-readiness.md"}
            )
            support_files.setdefault(
                "notes/canonical-readiness.md",
                "# Canonical Readiness\n",
            )
        if baseline_mode != "none":
            evidence_entries.append(
                {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"}
            )
            support_files.setdefault(
                "notes/baseline-readiness.md",
                "# Baseline Readiness\n",
            )
        if report_format == "comparative-summary":
            if baseline_mode == "longitudinal-window":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/window-contract.md"}
                )
                support_files.setdefault(
                    "notes/window-contract.md",
                    textwrap.dedent(
                        """\
                        # Window Contract

                        ordered window sequence
                        anchor workflow surface
                        no clear directional movement
                        """
                    ),
                )
            elif baseline_mode == "peer-compare":
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        matched conditions
                        side-by-side interpretation
                        """
                    ),
                )
            else:
                evidence_entries.append(
                    {"kind": "support_note", "path": "notes/comparison-contract.md"}
                )
                support_files.setdefault(
                    "notes/comparison-contract.md",
                    textwrap.dedent(
                        """\
                        # Comparison Contract

                        baseline target
                        noisy variation
                        style-only overread
                        """
                    ),
                )
    frontmatter = {
        "name": name,
        "category": category,
        "status": status,
        "summary": "Minimal summary for validation.",
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "report_format": report_format,
        "technique_dependencies": [entry["id"] for entry in technique_dependencies],
        "skill_dependencies": [entry["name"] for entry in skill_dependencies],
    }
    if comparison_surface is not None:
        frontmatter["comparison_surface"] = comparison_surface
    section_bodies = {
        "Intent": "Minimal intent.",
        "Object under evaluation": "Minimal object.",
        "Bounded claim": textwrap.dedent(
            """\
            This eval is designed to support a claim like:

            under these conditions, the bounded claim holds on this surface.

            This eval does not support claims such as:
            - broad general strength
            - total safety
            """
        ).strip(),
        "Trigger boundary": textwrap.dedent(
            """\
            Use this eval when:
            - bounded review matters
            - the workflow claim is the real question

            Do not use this eval when:
            - the task is unbounded
            - the main question is something else
            """
        ).strip(),
        "Inputs": "- input",
        "Fixtures and case surface": "- fixture",
        "Scoring or verdict logic": "- logic",
        "Baseline or comparison mode": "- mode",
        "Execution contract": "- contract",
        "Outputs": "- output",
        "Failure modes": "- failure",
        "Blind spots": textwrap.dedent(
            """\
            This eval does not prove:
            - broad general strength
            - stable behavior across time
            - downstream artifact excellence
            """
        ).strip(),
        "Interpretation guidance": textwrap.dedent(
            """\
            Treat a positive result as support for one bounded claim:
            the bounded claim holds on this surface.

            Do not treat a positive result as:
            - proof of general capability
            - proof of total safety
            - proof that every nearby surface is strong
            """
        ).strip(),
        "Verification": "- verify",
        "Technique traceability": "- " + (technique_dependencies[0]["id"] if technique_dependencies else "none"),
        "Skill traceability": "- " + (skill_dependencies[0]["name"] if skill_dependencies else "none"),
        "Adaptation points": "- point",
    }
    if section_overrides:
        section_bodies.update(section_overrides)

    default_portability_by_status = {
        "draft": "local-shaped",
        "bounded": "local-shaped",
        "portable": "portable",
        "baseline": "portable",
        "canonical": "broad",
    }
    if portability_level is None:
        portability_level = default_portability_by_status.get(status, "local-shaped")

    body_sections = [f"# {name}"]
    for heading in (
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
    ):
        body_sections.append(f"## {heading}\n{section_bodies[heading]}")
    body = "\n\n".join(body_sections) + "\n"
    write_text(
        bundle_dir / "EVAL.md",
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False)
        + "---\n\n"
        + body,
    )

    manifest = {
        "name": name,
        "category": category,
        "status": status,
        "object_under_evaluation": "bounded test surface",
        "claim_type": claim_type,
        "baseline_mode": baseline_mode,
        "verdict_shape": verdict_shape,
        "report_format": report_format,
        "maturity_score": 2,
        "rigor_level": "bounded",
        "repeatability": "moderate",
        "portability_level": portability_level,
        "review_required": True,
        "validation_strength": "baseline",
        "export_ready": True,
        "blind_spot_disclosure": "required-and-present",
        "score_interpretation_bound": "explicit",
        "technique_dependencies": technique_dependencies,
        "skill_dependencies": skill_dependencies,
        "comparison_surface": comparison_surface,
        "relations": relations,
        "evidence": evidence_entries,
    }
    write_text(bundle_dir / "eval.yaml", yaml.safe_dump(manifest, sort_keys=False))

    for relative_path, content in support_files.items():
        write_text(bundle_dir / relative_path, content)

    comparison_entries = []
    if isinstance(comparison_surface, dict):
        raw_question = comparison_surface.get("selection_question")
        if isinstance(raw_question, str):
            comparison_entries.append((raw_question, name))

    make_index(
        repo_root,
        name,
        category,
        include_comparison_spine=baseline_mode != "none",
    )
    make_selection(repo_root, [name], comparison_entries=comparison_entries)
    make_roadmap(repo_root, [name])
    make_repo_docs(repo_root, starter_names=[name], comparison_entries=comparison_entries)


def write_catalogs(repo_root: Path) -> None:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        return
    full_catalog, min_catalog = build_catalog_payloads(repo_root, records)
    capsules = build_capsule_payload(repo_root, records, full_catalog)
    comparison_spine = build_comparison_spine_payload(repo_root, records, full_catalog)
    sections, section_issues = eval_section_contract.build_sections_payload(repo_root, records)
    if section_issues:
        return
    write_json_file(repo_root / "generated" / "eval_catalog.json", full_catalog, compact=False)
    write_json_file(repo_root / "generated" / "eval_catalog.min.json", min_catalog, compact=True)
    write_json_file(repo_root / "generated" / "eval_capsules.json", capsules, compact=False)
    write_json_file(repo_root / "generated" / "comparison_spine.json", comparison_spine, compact=False)
    write_json_file(repo_root / "generated" / "eval_sections.full.json", sections, compact=False)


def add_materialized_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    report_schema: dict[str, object],
    report_example: dict[str, object],
    comparison_mode: str | None = None,
    include_fixture_contract: bool = True,
    include_paired_readout: bool = False,
    include_runner_contract: bool = True,
    fixture_family_path: str = "fixtures/shared-bounded-family/README.md",
    shared_case_surface: str = "shared bounded case family for validation",
    bounded_replacement_rule: str = "replace only with the same bounded case class and public-safe evidence surface",
    public_safe_requirements: list[str] | None = None,
    runner_inputs: list[str] | None = None,
    paired_readout_path: str = "reports/paired-proof.md",
    additional_fixture_family_paths: list[str] | None = None,
    additional_paired_readout_paths: list[str] | None = None,
) -> None:
    write_text(repo_root / "runners" / "reportable_proof_contract.md", "# Runner Contract\n")
    write_text(repo_root / "scorers" / "bounded_rubric_breakdown.py", "def helper():\n    return {'ok': True}\n")
    if include_paired_readout:
        write_text(repo_root / Path(paired_readout_path), "# Paired Proof\n")
    for extra_path in additional_paired_readout_paths or []:
        write_text(repo_root / Path(extra_path), "# Paired Proof\n")

    if include_fixture_contract:
        public_safe_requirements = public_safe_requirements or [
            "outside reviewers can inspect the surface",
        ]
        write_text(repo_root / Path(fixture_family_path), "# Shared Fixture Family\n")
        for extra_path in additional_fixture_family_paths or []:
            write_text(repo_root / Path(extra_path), "# Shared Fixture Family\n")
        write_text(
            repo_root / "bundles" / bundle_name / "fixtures" / "contract.json",
            json.dumps(
                {
                    "contract_version": 1,
                    "shared_fixture_family_path": fixture_family_path,
                    "additional_shared_fixture_family_paths": additional_fixture_family_paths or [],
                    "shared_case_surface": shared_case_surface,
                    "bounded_replacement_rule": bounded_replacement_rule,
                    "public_safe_requirements": public_safe_requirements,
                },
                indent=2,
            ),
        )

    schema_path = f"bundles/{bundle_name}/reports/summary.schema.json"
    example_path = f"bundles/{bundle_name}/reports/example-report.json"
    if comparison_mode is not None:
        schema_required = list(report_schema.get("required", []))
        if "comparison_mode" not in schema_required:
            insert_at = 3 if len(schema_required) >= 3 else len(schema_required)
            schema_required.insert(insert_at, "comparison_mode")
            report_schema["required"] = schema_required
        schema_properties = dict(report_schema.get("properties", {}))
        schema_properties["comparison_mode"] = {"const": comparison_mode}
        report_schema["properties"] = schema_properties
        report_example["comparison_mode"] = comparison_mode
    write_text(
        repo_root / "bundles" / bundle_name / "reports" / "summary.schema.json",
        json.dumps(report_schema, indent=2),
    )
    write_text(
        repo_root / "bundles" / bundle_name / "reports" / "example-report.json",
        json.dumps(report_example, indent=2),
    )

    if include_runner_contract:
        runner_contract: dict[str, object] = {
            "contract_version": 1,
            "runner_surface_path": "runners/reportable_proof_contract.md",
            "inputs": runner_inputs or ["bounded case dossier"],
            "scorer_helper_paths": ["scorers/bounded_rubric_breakdown.py"],
            "report_schema_path": schema_path,
            "report_example_path": example_path,
        }
        if include_fixture_contract:
            runner_contract["fixture_contract_paths"] = [
                f"bundles/{bundle_name}/fixtures/contract.json"
            ]
        if include_paired_readout:
            runner_contract["paired_readout_path"] = paired_readout_path
        if additional_paired_readout_paths:
            runner_contract["additional_paired_readout_paths"] = additional_paired_readout_paths

        write_text(
            repo_root / "bundles" / bundle_name / "runners" / "contract.json",
            json.dumps(runner_contract, indent=2),
        )


def add_fixed_baseline_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    status: str = "draft",
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
) -> None:
    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="fixed-baseline",
        include_paired_readout=True,
        fixture_family_path="fixtures/frozen-same-task-v1/README.md",
        shared_case_surface="shared frozen same-task case family for validation",
        bounded_replacement_rule="replace only with the same bounded task family, the same named frozen baseline target, and the same visible evidence surface",
        public_safe_requirements=[
            "the frozen baseline target stays visible and inspectable",
            "baseline and candidate stay on the same bounded case family",
        ],
        runner_inputs=[
            "frozen baseline target",
            "candidate run family on the same bounded cases",
            "per-case comparison notes",
        ],
        paired_readout_path="reports/same-task-baseline-proof-flow-v1.md",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "baseline_target",
                "case_family",
                "per_case_comparisons",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": status},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "no material regression",
                        "mixed regression signal",
                        "regression present",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "baseline_target": {"type": "string"},
                "case_family": {"type": "string"},
                "per_case_comparisons": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "case_id",
                            "baseline_note",
                            "candidate_note",
                            "comparative_reading",
                            "comparison_note",
                        ],
                        "properties": {
                            "case_id": {"type": "string"},
                            "baseline_note": {"type": "string"},
                            "candidate_note": {"type": "string"},
                            "comparative_reading": {
                                "type": "string",
                                "enum": [
                                    "no material regression",
                                    "bounded improvement present",
                                    "noisy variation",
                                    "regression present",
                                ],
                            },
                            "comparison_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": bundle_name,
            "bundle_status": status,
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed regression signal",
            "claim_boundary": "bounded same-task regression example for validation",
            "limitations": ["still bounded"],
            "baseline_target": "RS-v1 frozen bounded workflow reference",
            "case_family": "frozen-same-task-v1",
            "per_case_comparisons": [
                {
                    "case_id": "RS-01",
                    "baseline_note": "baseline note",
                    "candidate_note": "candidate note",
                    "comparative_reading": "no material regression",
                    "comparison_note": "comparison note",
                }
            ],
        },
    )


def add_longitudinal_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
    report_example_override: dict[str, object] | None = None,
) -> None:
    report_example = {
        "eval_name": bundle_name,
        "bundle_status": "draft",
        "object_under_evaluation": "bounded test surface",
        "verdict": "mixed or unstable movement",
        "claim_boundary": "bounded repeated-window movement example for validation",
        "limitations": ["still bounded"],
        "anchor_surface": "aoa-bounded-change-quality",
        "window_family": "repeated-window-bounded-v1",
        "windows": [
            {
                "window_id": "LG-01",
                "window_order": 1,
                "workflow_note": "workflow note",
                "movement_reading": "no clear directional movement",
                "context_note": "context note",
            },
            {
                "window_id": "LG-02",
                "window_order": 2,
                "workflow_note": "workflow note later",
                "movement_reading": "bounded improvement signal",
                "context_note": "context note later",
            },
        ],
    }
    if report_example_override:
        report_example.update(report_example_override)

    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="longitudinal-window",
        include_paired_readout=True,
        fixture_family_path="fixtures/repeated-window-bounded-v1/README.md",
        shared_case_surface="shared repeated-window workflow family for validation",
        bounded_replacement_rule="replace only with the same ordered named windows on one bounded workflow surface and explicit context notes",
        public_safe_requirements=[
            "the anchor workflow surface stays explicit across the window sequence",
            "each window has a public report or summary artifact",
        ],
        runner_inputs=[
            "ordered named windows",
            "one public report or summary artifact per window",
            "context-shift notes",
        ],
        paired_readout_path="reports/repeated-window-proof-flow-v1.md",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "anchor_surface",
                "window_family",
                "windows",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "bounded improvement signal",
                        "no clear directional movement",
                        "mixed or unstable movement",
                        "bounded regression signal",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "anchor_surface": {"type": "string"},
                "window_family": {"type": "string"},
                "windows": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "window_id",
                            "window_order",
                            "workflow_note",
                            "movement_reading",
                            "context_note",
                        ],
                        "properties": {
                            "window_id": {"type": "string"},
                            "window_order": {"type": "integer", "minimum": 1},
                            "workflow_note": {"type": "string"},
                            "movement_reading": {
                                "type": "string",
                                "enum": [
                                    "bounded improvement signal",
                                    "no clear directional movement",
                                    "mixed or unstable movement",
                                    "bounded regression signal",
                                ],
                            },
                            "context_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example=report_example,
    )


def add_peer_compare_proof_artifacts(
    repo_root: Path,
    *,
    bundle_name: str,
    include_fixture_contract: bool = True,
    include_runner_contract: bool = True,
) -> None:
    add_materialized_proof_artifacts(
        repo_root,
        bundle_name=bundle_name,
        include_fixture_contract=include_fixture_contract,
        include_runner_contract=include_runner_contract,
        comparison_mode="peer-compare",
        include_paired_readout=True,
        fixture_family_path="fixtures/bounded-change-paired-v1/README.md",
        shared_case_surface="shared bounded change case family for validation",
        bounded_replacement_rule="replace only with the same bounded case family under matched artifact and workflow review conditions",
        public_safe_requirements=[
            "the shared case family stays explicit",
            "the side-by-side artifact and workflow surfaces stay reviewable",
        ],
        runner_inputs=[
            "shared bounded case family",
            "artifact-side readings",
            "process-side readings",
            "matched-condition evidence",
            "paired divergence summary",
        ],
        paired_readout_path="reports/artifact-process-paired-proof-flow-v1.md",
        additional_fixture_family_paths=["fixtures/bounded-change-paired-v2/README.md"],
        additional_paired_readout_paths=["reports/artifact-process-paired-proof-flow-v2.md"],
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
                "case_family",
                "paired_surfaces",
                "per_case_comparisons",
            ],
            "properties": {
                "eval_name": {"const": bundle_name},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {
                    "type": "string",
                    "enum": [
                        "artifact outruns process",
                        "process outruns artifact",
                        "artifact and process are broadly aligned",
                        "mixed comparison signal",
                    ],
                },
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "case_family": {"type": "string"},
                "paired_surfaces": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 2,
                },
                "per_case_comparisons": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": [
                            "case_id",
                            "artifact_side_reading",
                            "process_side_reading",
                            "gap_reading",
                            "side_by_side_note",
                        ],
                        "properties": {
                            "case_id": {"type": "string"},
                            "artifact_side_reading": {"type": "string"},
                            "process_side_reading": {"type": "string"},
                            "gap_reading": {"type": "string"},
                            "side_by_side_note": {"type": "string"},
                        },
                    },
                },
            },
        },
        report_example={
            "eval_name": bundle_name,
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "mixed comparison signal",
            "claim_boundary": "bounded peer-compare example for validation",
            "limitations": ["still bounded"],
            "case_family": "bounded-change-paired-v1",
            "paired_surfaces": ["aoa-peer-left", "aoa-peer-right"],
            "per_case_comparisons": [
                {
                    "case_id": "PC-01",
                    "artifact_side_reading": "supports bounded claim",
                    "process_side_reading": "mixed support",
                    "gap_reading": "artifact outruns process",
                    "side_by_side_note": "paired note",
                }
            ],
        },
    )


def test_build_catalog_preserves_same_kind_relations_in_full_catalog(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-alpha",
        relations=[{"type": "complements", "target": "aoa-beta"}],
    )
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha", "aoa-beta"])

    assert build_catalog.main(argv=[], repo_root=tmp_path) == 0

    full_catalog = json.loads((tmp_path / "generated" / "eval_catalog.json").read_text(encoding="utf-8"))
    alpha_entry = next(entry for entry in full_catalog["evals"] if entry["name"] == "aoa-alpha")

    assert alpha_entry["relations"] == [{"type": "complements", "target": "aoa-beta"}]
    assert alpha_entry["technique_refs"][0]["repo"] == "aoa-techniques"
    assert alpha_entry["skill_refs"][0]["repo"] == "aoa-skills"


def test_build_catalog_records_materialized_proof_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-materialized-proof")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-materialized-proof",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-materialized-proof"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-materialized-proof",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "bounded machine-readable proof artifact for validation",
            "limitations": ["still bounded"],
        },
        include_paired_readout=True,
    )

    assert build_catalog.main(argv=[], repo_root=tmp_path) == 0

    full_catalog = json.loads((tmp_path / "generated" / "eval_catalog.json").read_text(encoding="utf-8"))
    entry = next(item for item in full_catalog["evals"] if item["name"] == "aoa-materialized-proof")

    assert entry["proof_artifacts"]["shared_fixture_family_path"] == "fixtures/shared-bounded-family/README.md"
    assert entry["proof_artifacts"]["runner_surface_path"] == "runners/reportable_proof_contract.md"
    assert entry["proof_artifacts"]["report_schema_path"] == "bundles/aoa-materialized-proof/reports/summary.schema.json"


def test_validate_repo_rejects_missing_evidence_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-evidence-path",
        evidence_entries=[{"kind": "origin_need", "path": "notes/missing.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("evidence path 'notes/missing.md' does not exist" in issue.message for issue in issues)


def test_validate_repo_requires_origin_need_for_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-origin-need",
        evidence_entries=[{"kind": "integrity_check", "path": "checks/eval-integrity-check.md"}],
        support_files={
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("starter bundle must include an evidence entry with kind 'origin_need'" in issue.message for issue in issues)


def test_validate_repo_requires_baseline_readiness_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-readiness",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[{"kind": "origin_need", "path": "notes/origin-need.md"}],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("baseline_readiness" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_portable_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-portable-review",
        status="portable",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'portable' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_portable_review_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-baseline-portable-review",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'baseline' requires an evidence entry with kind 'portable_review'" in issue.message for issue in issues)


def test_validate_repo_requires_local_shaped_portability_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-bounded-portability-drift",
        status="bounded",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'bounded' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_local_shaped_portability_for_draft_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-draft-portability-drift",
        status="draft",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'draft' requires portability_level 'local-shaped' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_portable_portability_for_baseline_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-baseline-portability-drift",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        portability_level="local-shaped",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'baseline' requires portability_level 'portable' but found 'local-shaped'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_broad_portability_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-canonical-portability-drift",
        status="canonical",
        portability_level="portable",
    )

    issues = run_validation(tmp_path)

    assert any(
        "status 'canonical' requires portability_level 'broad' but found 'portable'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_support_note_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_bounded_review_language_for_bounded_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-bounded-review-note",
        status="bounded",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/bounded-promotion-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/bounded-promotion-review.md": "# Bounded Review\nA useful note, but no explicit promotion language.\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'bounded' requires a support_note that records approve-for-bounded outcome plus failure and readout distinctions" in issue.message for issue in issues)


def test_validate_repo_requires_canonical_readiness_for_canonical_status(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-canonical-readiness",
        status="canonical",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "portable_review", "path": "notes/portable-review.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/portable-review.md": "# Portable Review\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("status 'canonical' requires an evidence entry with kind 'canonical_readiness'" in issue.message for issue in issues)


def test_validate_repo_requires_support_note_for_comparative_summary(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("report_format 'comparative-summary' requires an evidence entry with kind 'support_note'" in issue.message for issue in issues)


def test_validate_repo_requires_fixed_baseline_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-fixed-baseline-contract",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state the baseline target, noisy variation, and style-only overread limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_requires_materialized_report_artifacts_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-report-artifacts",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("reports/summary.schema.json" in issue.message for issue in issues)
    assert any("reports/example-report.json" in issue.message for issue in issues)


def test_validate_repo_requires_runner_contract_for_fixed_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-fixed-baseline-runner",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-fixed-baseline-runner",
        include_runner_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_requires_peer_compare_contract_phrases(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-weak-peer-compare-contract",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nmatched conditions only\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "must state matched conditions and side-by-side interpretation limits in a support note"
        in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_fixed_baseline_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-fixed-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-fixed-baseline")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-fixed-baseline")

    assert issues == []


def test_validate_repo_accepts_valid_peer_compare_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-peer-compare",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-valid-peer-compare")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-peer-compare")

    assert issues == []


def test_validate_repo_accepts_valid_longitudinal_comparison_surface(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-valid-longitudinal-window")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-valid-longitudinal-window")

    assert issues == []


def test_validate_repo_requires_comparison_surface_for_non_none_baseline(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-surface",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = tmp_path / "bundles" / "aoa-missing-comparison-surface" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest.pop("comparison_surface", None)
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("comparison_surface" in issue.message for issue in issues)


def test_validate_repo_requires_comparison_mode_in_comparative_report_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-comparison-mode",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-missing-comparison-mode")
    schema_path = tmp_path / "bundles" / "aoa-missing-comparison-mode" / "reports" / "summary.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    schema["required"] = [item for item in schema["required"] if item != "comparison_mode"]
    schema["properties"].pop("comparison_mode", None)
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    example_path = tmp_path / "bundles" / "aoa-missing-comparison-mode" / "reports" / "example-report.json"
    example = json.loads(example_path.read_text(encoding="utf-8"))
    example.pop("comparison_mode", None)
    example_path.write_text(json.dumps(example, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("comparison_mode" in issue.message for issue in issues)


def test_validate_repo_rejects_peer_compare_with_wrong_peer_surface_count(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-invalid-peer-surface-count",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    manifest_path = tmp_path / "bundles" / "aoa-invalid-peer-surface-count" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["peer_surfaces"] = ["aoa-peer-left"]
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("peer_surfaces" in issue.location or "peer_surfaces" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_shared_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-shared-family",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-shared-family")
    write_text(tmp_path / "fixtures" / "alt-family" / "README.md", "# Shared Fixture Family\n")
    manifest_path = tmp_path / "bundles" / "aoa-mismatched-shared-family" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["shared_family_path"] = "fixtures/alt-family/README.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("shared_family_path must match fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_mismatched_comparison_surface_paired_readout_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-mismatched-paired-readout",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(tmp_path, bundle_name="aoa-mismatched-paired-readout")
    write_text(tmp_path / "reports" / "alt-proof-flow.md", "# Paired Proof\n")
    manifest_path = tmp_path / "bundles" / "aoa-mismatched-paired-readout" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["comparison_surface"]["paired_readout_path"] = "reports/alt-proof-flow.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("paired_readout_path must match runners/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_invalid_additional_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-output-vs-process-gap",
        category="comparative",
        claim_type="comparative",
        baseline_mode="peer-compare",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_peer_compare_proof_artifacts(tmp_path, bundle_name="aoa-output-vs-process-gap")
    contract_path = tmp_path / "bundles" / "aoa-output-vs-process-gap" / "fixtures" / "contract.json"
    payload = json.loads(contract_path.read_text(encoding="utf-8"))
    payload["additional_shared_fixture_family_paths"] = ["fixtures/missing-v2/README.md"]
    contract_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path, eval_name="aoa-output-vs-process-gap")

    assert any("additional_shared_fixture_family_paths" in issue.location for issue in issues)


def test_validate_repo_requires_comparison_doctrine_selection_parity(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-selection-drift",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-selection-drift")
    write_catalogs(tmp_path)
    write_text(
        tmp_path / "EVAL_SELECTION.md",
        """
        # Eval Selection

        Current starter posture:
        - `aoa-selection-drift`
        """,
    )

    issues = run_validation(tmp_path)

    assert any("Pick Comparison Surface" in issue.message or "comparison selector question" in issue.message for issue in issues)


def test_validate_repo_requires_artifact_process_doctrine_guide(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-artifact-review-rubric", category="artifact")
    write_catalogs(tmp_path)
    (tmp_path / "docs" / "ARTIFACT_PROCESS_SEPARATION_GUIDE.md").unlink()

    issues = run_validation(tmp_path, eval_name="aoa-artifact-review-rubric")

    assert any("ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.location or "ARTIFACT_PROCESS_SEPARATION_GUIDE.md" in issue.message for issue in issues)


def test_validate_repo_requires_fixture_contract_for_longitudinal_window(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-longitudinal-fixture",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/window-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/window-contract.md": "# Window Contract\nordered window\nanchor workflow surface\nno clear directional movement\nmixed or unstable movement\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-missing-longitudinal-fixture",
        include_fixture_contract=False,
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("fixtures/contract.json" in issue.message for issue in issues)


def test_validate_repo_rejects_missing_shared_fixture_family_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-shared-fixture")
    write_catalogs(tmp_path)
    write_text(
        tmp_path / "bundles" / "aoa-missing-shared-fixture" / "fixtures" / "contract.json",
        json.dumps(
            {
                "contract_version": 1,
                "shared_fixture_family_path": "fixtures/does-not-exist/README.md",
                "shared_case_surface": "shared bounded case family for validation",
                "bounded_replacement_rule": "replace only with the same bounded case class and public-safe evidence surface",
                "public_safe_requirements": ["outside reviewers can inspect the surface"],
            },
            indent=2,
        ),
    )

    issues = run_validation(tmp_path)

    assert any("shared_fixture_family_path" in issue.location and "does not exist" in issue.message for issue in issues)


def test_validate_repo_rejects_report_example_that_violates_bundle_schema(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-invalid-report-example")
    write_catalogs(tmp_path)
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-invalid-report-example",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-invalid-report-example"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-invalid-report-example",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "missing limitations should fail",
        },
    )

    issues = run_validation(tmp_path)

    assert any("report violation" in issue.message and "limitations" in issue.message for issue in issues)


def test_validate_repo_rejects_longitudinal_report_with_duplicate_window_id(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-duplicate-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-duplicate-longitudinal-window",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 1,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_id 'LG-01' must be unique" in issue.message for issue in issues)


def test_validate_repo_rejects_longitudinal_report_with_non_increasing_window_order(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-out-of-order-longitudinal-window",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-out-of-order-longitudinal-window",
        report_example_override={
            "windows": [
                {
                    "window_id": "LG-01",
                    "window_order": 2,
                    "workflow_note": "workflow note",
                    "movement_reading": "no clear directional movement",
                    "context_note": "context note",
                },
                {
                    "window_id": "LG-02",
                    "window_order": 2,
                    "workflow_note": "workflow note later",
                    "movement_reading": "bounded improvement signal",
                    "context_note": "context note later",
                },
            ]
        },
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("window_order values must be strictly increasing" in issue.message for issue in issues)


def test_validate_repo_requires_roadmap_current_public_surface_to_be_a_starter_bundle(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-alpha")
    make_eval_bundle(tmp_path, name="aoa-beta")
    make_index(tmp_path, "aoa-alpha", "workflow")
    make_selection(tmp_path, ["aoa-alpha"])
    make_roadmap(tmp_path, ["aoa-beta"])
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("roadmap 'Current public surface' eval 'aoa-beta' must appear in EVAL_INDEX.md starter bundles" in issue.message for issue in issues)


def test_validate_repo_allows_public_bundle_outside_starter_surface(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-starter-alpha") == []
    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_repo_allows_targeted_non_starter_bundle_validation(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-public-draft") == []


def test_validate_eval_index_allows_targeted_non_starter_bundle_selection(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-starter-alpha")
    make_eval_bundle(tmp_path, name="aoa-public-draft")
    make_index(tmp_path, "aoa-starter-alpha", "workflow")
    make_selection(tmp_path, ["aoa-starter-alpha"])
    make_roadmap(tmp_path, ["aoa-starter-alpha"])
    write_catalogs(tmp_path)

    issues = validate_eval_index(
        tmp_path,
        starter_names=["aoa-starter-alpha"],
        selected_evals={"aoa-public-draft"},
    )

    assert issues == []


def test_validate_repo_requires_absence_note_sync_between_roadmap_and_index(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-absence-note-drift")
    make_roadmap(tmp_path, ["aoa-absence-note-drift"], include_absence_note=False)
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any("absence note" in issue.message for issue in issues)


def test_validate_repo_rejects_mirrored_field_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-field-drift")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-field-drift" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["category"] = "artifact"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("field 'category' does not match" in issue.message for issue in issues)


def test_validate_repo_rejects_technique_dependency_order_mismatch(tmp_path: Path) -> None:
    technique_dependencies = [
        {
            "id": "AOA-T-0001",
            "repo": "8Dionysus/aoa-techniques",
            "path": "techniques/agent-workflows/plan-diff-apply-verify-report/TECHNIQUE.md",
        },
        {
            "id": "AOA-T-0002",
            "repo": "aoa-techniques",
            "path": "techniques/docs/source-of-truth-layout/TECHNIQUE.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-technique-order-drift",
        technique_dependencies=technique_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-technique-order-drift" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["technique_dependencies"] = list(reversed(frontmatter["technique_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered technique refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_skill_dependency_order_mismatch(tmp_path: Path) -> None:
    skill_dependencies = [
        {
            "name": "aoa-change-protocol",
            "repo": "8Dionysus/aoa-skills",
            "path": "skills/aoa-change-protocol/SKILL.md",
        },
        {
            "name": "aoa-approval-gate-check",
            "repo": "aoa-skills",
            "path": "skills/aoa-approval-gate-check/SKILL.md",
        },
    ]
    make_eval_bundle(
        tmp_path,
        name="aoa-skill-order-drift",
        skill_dependencies=skill_dependencies,
    )
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-skill-order-drift" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    _opening, frontmatter_text, body = text.split("---", 2)
    frontmatter = yaml.safe_load(frontmatter_text)
    frontmatter["skill_dependencies"] = list(reversed(frontmatter["skill_dependencies"]))
    eval_md_path.write_text(
        f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}",
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "ordered skill refs do not match"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_repo_mismatch(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-repo-mismatch")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-repo-mismatch" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["repo"] = "example/other-repo"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("repo must resolve to 'aoa-techniques'" in issue.message for issue in issues)


def test_validate_repo_rejects_non_repo_relative_dependency_path(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-path-mismatch")
    write_catalogs(tmp_path)

    manifest_path = tmp_path / "bundles" / "aoa-path-mismatch" / "eval.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    manifest["technique_dependencies"][0]["path"] = "../techniques/test/TECHNIQUE.md"
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any("path must be a concrete repo-relative path" in issue.message for issue in issues)


def test_validate_repo_missing_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-generated")

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if "generated/" in issue.location)


def test_validate_repo_missing_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-capsules")
    write_catalogs(tmp_path)

    (tmp_path / "generated" / "eval_capsules.json").unlink()

    issues = run_validation(tmp_path)

    assert any(
        issue.location == "generated/eval_capsules.json" and "file is missing" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_catalogs_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-generated" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_validate_repo_stale_generated_capsules_fail(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-capsules")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-capsules" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim changed without rebuilding capsules.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated capsules are out of date; run 'python scripts/build_catalog.py'" in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_catalog_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-generated")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-generated" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace("Minimal summary for validation.", "Changed without rebuilding catalog.", 1),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-generated")

    assert any(
        "generated catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog entry for 'aoa-targeted-stale-generated' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_capsule_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-capsule")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-capsule" / "EVAL.md"
    text = eval_md_path.read_text(encoding="utf-8")
    eval_md_path.write_text(
        text.replace(
            "under these conditions, the bounded claim holds on this surface.",
            "under these conditions, the bounded claim drifted after generation.",
            1,
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-capsule")

    assert any(
        "generated capsule entry for 'aoa-targeted-stale-capsule' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_catalog_metadata(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-metadata-drift")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    full_catalog["catalog_version"] = 999
    min_catalog["source_of_truth"] = {"broken": True}
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path, eval_name="aoa-targeted-metadata-drift")

    assert any(
        "generated catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )
    assert any(
        "generated min catalog metadata is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_source_section_without_derivable_content(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-missing-capsule-source",
        section_overrides={"Interpretation guidance": ""},
    )
    write_catalogs(tmp_path)

    issues = run_validation(tmp_path)

    assert any(
        "missing capsule source section 'Interpretation guidance'" in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_capsule_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-capsule-alignment-drift")
    write_catalogs(tmp_path)

    capsule_path = tmp_path / "generated" / "eval_capsules.json"
    capsules = json.loads(capsule_path.read_text(encoding="utf-8"))
    capsules["evals"] = []
    capsule_path.write_text(json.dumps(capsules), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "capsules are missing eval 'aoa-capsule-alignment-drift' from generated/eval_catalog.json"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_missing_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-missing-sections-surface")
    write_catalogs(tmp_path)
    (tmp_path / "generated" / "eval_sections.full.json").unlink()

    issues = run_validation(tmp_path)

    assert any("file is missing" in issue.message for issue in issues if issue.location.endswith("eval_sections.full.json"))


def test_validate_repo_rejects_stale_generated_sections(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-stale-sections-surface")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-stale-sections-surface" / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path)

    assert any(
        "generated sections are out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_section_catalog_alignment_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-section-alignment-drift")
    write_catalogs(tmp_path)

    sections_path = tmp_path / "generated" / "eval_sections.full.json"
    sections = json.loads(sections_path.read_text(encoding="utf-8"))
    sections["evals"][0]["status"] = "promoted"
    sections_path.write_text(json.dumps(sections), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated section entry for 'aoa-section-alignment-drift' must align with full catalog field 'status'"
        in issue.message
        for issue in issues
    )


def test_targeted_validation_catches_stale_generated_section_for_selected_eval(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-targeted-stale-sections")
    write_catalogs(tmp_path)

    eval_md_path = tmp_path / "bundles" / "aoa-targeted-stale-sections" / "EVAL.md"
    eval_md_path.write_text(
        eval_md_path.read_text(encoding="utf-8").replace(
            "## Adaptation points\n- point\n",
            "## Adaptation points\n- point\n- another point\n",
        ),
        encoding="utf-8",
    )

    issues = run_validation(tmp_path, eval_name="aoa-targeted-stale-sections")

    assert any(
        "generated section entry for 'aoa-targeted-stale-sections' is out of date; run 'python scripts/build_catalog.py'"
        in issue.message
        for issue in issues
    )


def test_validate_repo_rejects_min_projection_drift(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-min-projection-drift")
    write_catalogs(tmp_path)

    min_path = tmp_path / "generated" / "eval_catalog.min.json"
    min_catalog = json.loads(min_path.read_text(encoding="utf-8"))
    min_catalog["evals"][0]["summary"] = "tampered"
    min_path.write_text(json.dumps(min_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "min catalog must stay a projection of the full catalog" in issue.message
        for issue in issues
    )


def test_validate_repo_reports_malformed_full_catalog_projection_error(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-malformed-full-catalog")
    write_catalogs(tmp_path)

    full_path = tmp_path / "generated" / "eval_catalog.json"
    full_catalog = json.loads(full_path.read_text(encoding="utf-8"))
    del full_catalog["evals"]
    full_path.write_text(json.dumps(full_catalog), encoding="utf-8")

    issues = run_validation(tmp_path)

    assert any(
        "generated catalog is malformed; min projection could not be computed" in issue.message
        for issue in issues
    )


def test_validate_repo_accepts_valid_non_baseline_bundle_without_baseline_readiness(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-non-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-non-baseline") == []


def test_validate_repo_accepts_valid_bounded_bundle_with_review_note(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-bounded", status="bounded")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-bounded") == []


def test_validate_repo_accepts_valid_baseline_bundle_with_readiness_evidence(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
        evidence_entries=[
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "support_note", "path": "notes/comparison-contract.md"},
            {"kind": "baseline_readiness", "path": "notes/baseline-readiness.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
        support_files={
            "notes/origin-need.md": "# Origin Need\n",
            "notes/comparison-contract.md": "# Comparison Contract\nbaseline target\nnoisy variation\nstyle-only overread\n",
            "notes/baseline-readiness.md": "# Baseline Readiness\n",
            "examples/example-report.md": "# Example Report\n",
            "checks/eval-integrity-check.md": "# Eval Integrity Check\n",
        },
    )
    add_fixed_baseline_proof_artifacts(tmp_path, bundle_name="aoa-valid-baseline")
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline") == []


def test_validate_repo_accepts_valid_baseline_status_bundle_with_portable_review(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-baseline-status",
        status="baseline",
        category="regression",
        claim_type="regression",
        baseline_mode="fixed-baseline",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_fixed_baseline_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-baseline-status",
        status="baseline",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-baseline-status") == []


def test_validate_repo_accepts_valid_longitudinal_bundle_with_materialized_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(
        tmp_path,
        name="aoa-valid-longitudinal-materialized",
        category="longitudinal",
        claim_type="longitudinal",
        baseline_mode="longitudinal-window",
        verdict_shape="comparative",
        report_format="comparative-summary",
    )
    add_longitudinal_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-longitudinal-materialized",
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-longitudinal-materialized") == []


def test_real_repo_has_only_one_non_local_shaped_portability_bundle() -> None:
    issues, records = collect_catalog_records(REPO_ROOT)

    assert issues == []
    non_local_shaped = {
        record.name: record.manifest["portability_level"]
        for record in records
        if record.manifest["portability_level"] != "local-shaped"
    }
    assert non_local_shaped == {"aoa-regression-same-task": "portable"}


def test_validate_repo_accepts_valid_bundle_with_materialized_proof_artifacts(tmp_path: Path) -> None:
    make_eval_bundle(tmp_path, name="aoa-valid-proof-artifacts")
    add_materialized_proof_artifacts(
        tmp_path,
        bundle_name="aoa-valid-proof-artifacts",
        report_schema={
            "type": "object",
            "additionalProperties": False,
            "required": [
                "eval_name",
                "bundle_status",
                "object_under_evaluation",
                "verdict",
                "claim_boundary",
                "limitations",
            ],
            "properties": {
                "eval_name": {"const": "aoa-valid-proof-artifacts"},
                "bundle_status": {"const": "draft"},
                "object_under_evaluation": {"const": "bounded test surface"},
                "verdict": {"type": "string"},
                "claim_boundary": {"type": "string"},
                "limitations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
        },
        report_example={
            "eval_name": "aoa-valid-proof-artifacts",
            "bundle_status": "draft",
            "object_under_evaluation": "bounded test surface",
            "verdict": "supports bounded claim",
            "claim_boundary": "bounded machine-readable proof artifact for validation",
            "limitations": ["still bounded"],
        },
    )
    write_catalogs(tmp_path)

    assert run_validation(tmp_path, eval_name="aoa-valid-proof-artifacts") == []
