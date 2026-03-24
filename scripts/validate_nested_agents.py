#!/usr/bin/env python3
"""Validate nested AGENTS.md coverage for aoa-evals."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]

Issue = tuple[str, str]

REQUIRED_AGENTS: dict[str, tuple[str, ...]] = {
    "bundles/AGENTS.md": (
        "EVAL.md",
        "eval.yaml",
        "bounded claim",
        "technique_dependencies",
        "skill_dependencies",
        "Do not add bundle-local AGENTS.md by default",
    ),
    "generated/AGENTS.md": (
        "generated/eval_catalog.json",
        "generated/eval_catalog.min.json",
        "generated/eval_capsules.json",
        "generated/comparison_spine.json",
        "generated/eval_sections.full.json",
        "Do not hand-edit",
        "python scripts/build_catalog.py",
    ),
    "fixtures/AGENTS.md": (
        "public-safe",
        "shared_fixture_family_path",
        "additional_shared_fixture_family_paths",
        "bounded-change-paired-v1",
        "frozen-same-task-v1",
        "repeated-window-bounded-v1",
        "bundle-local EVAL.md",
    ),
    "runners/AGENTS.md": (
        "reportable_proof_contract.md",
        "bounded inputs",
        "shared fixture replacement",
        "report schema validation",
        "paired_readout_path",
        "additional_paired_readout_paths",
    ),
    "scorers/AGENTS.md": (
        "bounded_rubric_breakdown.py",
        "bundle-local meaning in EVAL.md",
        "generic score",
        "transition-note",
        "integrity-risk",
    ),
    "templates/AGENTS.md": (
        "EVAL.template.md",
        "frontmatter",
        "comparison_surface",
        "shared_family_path",
        "paired_readout_path",
        "integrity_sidecar",
        "comparison_mode",
        "placeholders",
    ),
}


def normalize(text: str) -> str:
    return " ".join(text.lower().split())


def run_validation(repo_root: Path | None = None) -> list[Issue]:
    repo_root = repo_root or REPO_ROOT
    issues: list[Issue] = []

    for relative_path, required_phrases in REQUIRED_AGENTS.items():
        path = repo_root / relative_path
        if not path.is_file():
            issues.append((relative_path, "missing required nested AGENTS.md"))
            continue

        text = normalize(path.read_text(encoding="utf-8"))
        for phrase in required_phrases:
            if normalize(phrase) not in text:
                issues.append((relative_path, f"missing required phrase: {phrase}"))

    return issues


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    del argv
    issues = run_validation(repo_root or REPO_ROOT)
    if issues:
        print("Nested AGENTS docs check failed.")
        for location, message in issues:
            print(f"- {location}: {message}")
        return 1

    print(f"Nested AGENTS docs check passed for {len(REQUIRED_AGENTS)} directories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
