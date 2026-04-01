#!/usr/bin/env python3
"""Build derived eval catalog artifacts for aoa-evals."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import eval_catalog_contract
import eval_capsule_contract
import eval_section_contract
import eval_comparison_spine_contract
from validate_repo import (
    build_capsule_payload,
    build_quest_catalog_projection,
    build_quest_dispatch_projection,
    collect_catalog_records,
    format_issues,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
QUESTBOOK_SURFACE_SENTINELS = (
    "QUESTBOOK.md",
    "docs/QUESTBOOK_EVAL_INTEGRATION.md",
    "schemas/quest.schema.json",
    "schemas/quest_dispatch.schema.json",
    "quests",
)


def has_questbook_surface(repo_root: Path) -> bool:
    return any((repo_root / relative_path).exists() for relative_path in QUESTBOOK_SURFACE_SENTINELS)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build derived reader catalogs for aoa-evals.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether generated catalogs are present and current.",
    )
    return parser.parse_args(argv)


def check_catalogs(repo_root: Path) -> list[str]:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        return [f"source validation failed:\n{format_issues(issues)}"]

    expected_full, expected_min = eval_catalog_contract.build_catalog_payloads(repo_root, records)
    expected_capsules = eval_capsule_contract.build_capsule_payload(repo_root, records, expected_full)
    expected_sections, section_issues = eval_section_contract.build_sections_payload(repo_root, records)
    expected_comparison_spine = eval_comparison_spine_contract.build_comparison_spine_payload(
        repo_root,
        records,
        expected_full,
    )
    if section_issues:
        return [f"source validation failed:\n{eval_catalog_contract.format_issues(section_issues)}"]
    parse_issues = []
    full_path = repo_root / eval_catalog_contract.GENERATED_DIR_NAME / eval_catalog_contract.FULL_CATALOG_NAME
    min_path = repo_root / eval_catalog_contract.GENERATED_DIR_NAME / eval_catalog_contract.MIN_CATALOG_NAME
    capsule_path = repo_root / eval_capsule_contract.GENERATED_DIR_NAME / eval_capsule_contract.CAPSULE_NAME
    sections_path = repo_root / eval_section_contract.GENERATED_DIR_NAME / eval_section_contract.SECTIONS_NAME
    comparison_spine_path = (
        repo_root
        / eval_comparison_spine_contract.GENERATED_DIR_NAME
        / eval_comparison_spine_contract.COMPARISON_SPINE_NAME
    )
    quest_catalog_path = repo_root / "generated" / "quest_catalog.min.json"
    quest_dispatch_path = repo_root / "generated" / "quest_dispatch.min.json"
    quest_catalog_example_path = repo_root / "generated" / "quest_catalog.min.example.json"
    quest_dispatch_example_path = repo_root / "generated" / "quest_dispatch.min.example.json"
    actual_full, full_parse_issues = eval_catalog_contract.read_json_file(full_path, repo_root)
    actual_min, min_parse_issues = eval_catalog_contract.read_json_file(min_path, repo_root)
    actual_capsules, capsule_parse_issues = eval_catalog_contract.read_json_file(capsule_path, repo_root)
    actual_sections, sections_parse_issues = eval_catalog_contract.read_json_file(sections_path, repo_root)
    actual_comparison_spine, comparison_spine_parse_issues = eval_catalog_contract.read_json_file(
        comparison_spine_path,
        repo_root,
    )
    parse_issues.extend(full_parse_issues)
    parse_issues.extend(min_parse_issues)
    parse_issues.extend(capsule_parse_issues)
    parse_issues.extend(sections_parse_issues)
    parse_issues.extend(comparison_spine_parse_issues)
    if parse_issues:
        return [issue.message for issue in parse_issues]

    problems: list[str] = []
    if actual_full != expected_full:
        problems.append(f"stale {full_path.relative_to(repo_root).as_posix()}")
    if actual_min != expected_min:
        problems.append(f"stale {min_path.relative_to(repo_root).as_posix()}")
    if actual_capsules != expected_capsules:
        problems.append(f"stale {capsule_path.relative_to(repo_root).as_posix()}")
    if actual_sections != expected_sections:
        problems.append(f"stale {sections_path.relative_to(repo_root).as_posix()}")
    if actual_comparison_spine != expected_comparison_spine:
        problems.append(f"stale {comparison_spine_path.relative_to(repo_root).as_posix()}")
    if has_questbook_surface(repo_root):
        expected_quest_catalog = build_quest_catalog_projection(repo_root)
        expected_quest_dispatch = build_quest_dispatch_projection(repo_root)
        actual_quest_catalog, quest_catalog_parse_issues = eval_catalog_contract.read_json_file(
            quest_catalog_path, repo_root
        )
        actual_quest_dispatch, quest_dispatch_parse_issues = eval_catalog_contract.read_json_file(
            quest_dispatch_path, repo_root
        )
        actual_quest_catalog_example, quest_catalog_example_parse_issues = eval_catalog_contract.read_json_file(
            quest_catalog_example_path, repo_root
        )
        actual_quest_dispatch_example, quest_dispatch_example_parse_issues = eval_catalog_contract.read_json_file(
            quest_dispatch_example_path, repo_root
        )
        parse_issues.extend(quest_catalog_parse_issues)
        parse_issues.extend(quest_dispatch_parse_issues)
        parse_issues.extend(quest_catalog_example_parse_issues)
        parse_issues.extend(quest_dispatch_example_parse_issues)
        if parse_issues:
            return [issue.message for issue in parse_issues]
        if actual_quest_catalog != expected_quest_catalog:
            problems.append(f"stale {quest_catalog_path.relative_to(repo_root).as_posix()}")
        if actual_quest_dispatch != expected_quest_dispatch:
            problems.append(f"stale {quest_dispatch_path.relative_to(repo_root).as_posix()}")
        if actual_quest_catalog_example != expected_quest_catalog:
            problems.append(f"stale {quest_catalog_example_path.relative_to(repo_root).as_posix()}")
        if actual_quest_dispatch_example != expected_quest_dispatch:
            problems.append(f"stale {quest_dispatch_example_path.relative_to(repo_root).as_posix()}")
    return problems


def write_catalogs(repo_root: Path) -> tuple[Path, Path, Path, Path, Path]:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        raise ValueError(format_issues(issues))

    full_catalog, min_catalog = eval_catalog_contract.build_catalog_payloads(repo_root, records)
    capsules = build_capsule_payload(repo_root, records, full_catalog)
    sections, section_issues = eval_section_contract.build_sections_payload(repo_root, records)
    comparison_spine = eval_comparison_spine_contract.build_comparison_spine_payload(
        repo_root,
        records,
        full_catalog,
    )
    if section_issues:
        raise ValueError(eval_catalog_contract.format_issues(section_issues))
    generated_dir = repo_root / eval_catalog_contract.GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    full_path = generated_dir / eval_catalog_contract.FULL_CATALOG_NAME
    min_path = generated_dir / eval_catalog_contract.MIN_CATALOG_NAME
    capsule_path = generated_dir / eval_capsule_contract.CAPSULE_NAME
    sections_path = generated_dir / eval_section_contract.SECTIONS_NAME
    comparison_spine_path = generated_dir / eval_comparison_spine_contract.COMPARISON_SPINE_NAME
    eval_catalog_contract.write_json_file(full_path, full_catalog, compact=False)
    eval_catalog_contract.write_json_file(min_path, min_catalog, compact=True)
    eval_catalog_contract.write_json_file(capsule_path, capsules, compact=False)
    eval_catalog_contract.write_json_file(sections_path, sections, compact=False)
    eval_catalog_contract.write_json_file(comparison_spine_path, comparison_spine, compact=False)
    if has_questbook_surface(repo_root):
        quest_catalog = build_quest_catalog_projection(repo_root)
        quest_dispatch = build_quest_dispatch_projection(repo_root)
        eval_catalog_contract.write_json_file(
            generated_dir / "quest_catalog.min.json", quest_catalog, compact=True
        )
        eval_catalog_contract.write_json_file(
            generated_dir / "quest_dispatch.min.json", quest_dispatch, compact=True
        )
        eval_catalog_contract.write_json_file(
            generated_dir / "quest_catalog.min.example.json", quest_catalog, compact=False
        )
        eval_catalog_contract.write_json_file(
            generated_dir / "quest_dispatch.min.example.json", quest_dispatch, compact=False
        )
    return full_path, min_path, capsule_path, sections_path, comparison_spine_path


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.check:
            problems = check_catalogs(repo_root)
            if problems:
                print("Generated surface check failed.")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print("Generated surface check passed.")
            return 0

        full_path, min_path, capsule_path, sections_path, comparison_spine_path = write_catalogs(repo_root)
    except ValueError as exc:
        print("Catalog build failed because source bundles are invalid.")
        print(str(exc))
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(f"[ok] wrote {full_path.relative_to(repo_root).as_posix()}")
    print(f"[ok] wrote {min_path.relative_to(repo_root).as_posix()}")
    print(f"[ok] wrote {capsule_path.relative_to(repo_root).as_posix()}")
    print(f"[ok] wrote {sections_path.relative_to(repo_root).as_posix()}")
    print(f"[ok] wrote {comparison_spine_path.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
