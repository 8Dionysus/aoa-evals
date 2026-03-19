#!/usr/bin/env python3
"""Build derived eval catalog artifacts for aoa-evals."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import eval_catalog_contract
from validate_repo import (
    collect_catalog_records,
    format_issues,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


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
    parse_issues = []
    full_path = repo_root / eval_catalog_contract.GENERATED_DIR_NAME / eval_catalog_contract.FULL_CATALOG_NAME
    min_path = repo_root / eval_catalog_contract.GENERATED_DIR_NAME / eval_catalog_contract.MIN_CATALOG_NAME
    actual_full, full_parse_issues = eval_catalog_contract.read_json_file(full_path, repo_root)
    actual_min, min_parse_issues = eval_catalog_contract.read_json_file(min_path, repo_root)
    parse_issues.extend(full_parse_issues)
    parse_issues.extend(min_parse_issues)
    if parse_issues:
        return [issue.message for issue in parse_issues]

    problems: list[str] = []
    if actual_full != expected_full:
        problems.append(f"stale {full_path.relative_to(repo_root).as_posix()}")
    if actual_min != expected_min:
        problems.append(f"stale {min_path.relative_to(repo_root).as_posix()}")
    return problems


def write_catalogs(repo_root: Path) -> tuple[Path, Path]:
    issues, records = collect_catalog_records(repo_root)
    if issues:
        raise ValueError(format_issues(issues))

    full_catalog, min_catalog = eval_catalog_contract.build_catalog_payloads(repo_root, records)
    generated_dir = repo_root / eval_catalog_contract.GENERATED_DIR_NAME
    generated_dir.mkdir(exist_ok=True)
    full_path = generated_dir / eval_catalog_contract.FULL_CATALOG_NAME
    min_path = generated_dir / eval_catalog_contract.MIN_CATALOG_NAME
    eval_catalog_contract.write_json_file(full_path, full_catalog, compact=False)
    eval_catalog_contract.write_json_file(min_path, min_catalog, compact=True)
    return full_path, min_path


def main(argv: Sequence[str] | None = None, repo_root: Path | None = None) -> int:
    repo_root = repo_root or REPO_ROOT
    try:
        args = parse_args(argv)
        if args.check:
            problems = check_catalogs(repo_root)
            if problems:
                print("Catalog check failed.")
                for problem in problems:
                    print(f"- {problem}")
                return 1
            print("Catalog check passed.")
            return 0

        full_path, min_path = write_catalogs(repo_root)
    except ValueError as exc:
        print("Catalog build failed because source bundles are invalid.")
        print(str(exc))
        return 1
    except Exception as exc:  # pragma: no cover
        print(f"Runtime error: {exc}", file=sys.stderr)
        return 2

    print(f"[ok] wrote {full_path.relative_to(repo_root).as_posix()}")
    print(f"[ok] wrote {min_path.relative_to(repo_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
