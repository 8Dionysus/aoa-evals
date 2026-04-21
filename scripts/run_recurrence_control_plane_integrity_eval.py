#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scorers.recurrence_control_plane_integrity import (
    evaluate_dossier,
    compare_expected,
)


def main():
    ap = argparse.ArgumentParser(
        description="Run aoa-recurrence-control-plane-integrity scorer"
    )
    ap.add_argument("--case", required=True)
    ap.add_argument("--output")
    ap.add_argument("--check-expected", action="store_true")
    ap.add_argument("--json", action="store_true")
    ns = ap.parse_args()
    p = Path(ns.case)
    p = p if p.is_absolute() else Path.cwd() / p
    dossier = json.loads(p.read_text(encoding="utf-8"))
    report = evaluate_dossier(dossier)
    if ns.output:
        out = Path(ns.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    if ns.json or not ns.output:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    if ns.check_expected:
        errors = compare_expected(report, dossier.get("expected_axis_status") or {})
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 2
    return 1 if report["verdict"] == "does not support bounded claim" else 0


if __name__ == "__main__":
    raise SystemExit(main())
