#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PART_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
SCORER_DIR = PART_ROOT / "scorers"
if str(SCORER_DIR) not in sys.path:
    sys.path.insert(0, str(SCORER_DIR))

from recursor_readiness_boundary import check_expected, score  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run recursor readiness boundary eval case.")
    parser.add_argument("--case", required=True, help="Path to fixture case JSON.")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    case_path = Path(args.case)
    if not case_path.is_absolute():
        repo_relative = REPO_ROOT / case_path
        part_relative = PART_ROOT / case_path
        case_path = repo_relative if repo_relative.exists() else part_relative
    case = json.loads(case_path.read_text(encoding="utf-8"))
    result = score(case.get("input", {}))
    ok = True
    errors = []
    if args.check_expected:
        ok, errors = check_expected(result, case.get("expected", {}))
    report = {
        "schema_version": "recursor-readiness-boundary-run-report/v1",
        "case_id": case.get("case_id"),
        "case_name": case.get("name"),
        "result": result,
        "expected_check": {"ok": ok, "errors": errors},
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"{case.get('case_id')}: {result['verdict']} expected_check={ok}")
        for err in errors:
            print(f"- {err}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
