#!/usr/bin/env python3
"""Generate docs/decisions lookup indexes from decision-note metadata."""

from __future__ import annotations

import argparse
from pathlib import Path

from validators import docs_decisions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated indexes are stale")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    records, issues = docs_decisions.collect_decision_records(repo_root)
    issues.extend(docs_decisions.load_index_contract(repo_root)[1])
    if issues:
        for location, message in issues:
            print(f"- {location}: {message}")
        return 1

    rendered = docs_decisions.render_index_files(records)
    stale: list[str] = []
    for relative_path, expected_text in rendered.items():
        path = repo_root / relative_path
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != expected_text:
                stale.append(relative_path.as_posix())
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected_text, encoding="utf-8")

    if stale:
        print("Stale decision indexes:")
        for path_name in stale:
            print(f"- {path_name}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
