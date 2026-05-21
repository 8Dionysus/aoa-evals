#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "generated" / "eval_report_index.min.json"
REPORT_SUFFIX = ".report.json"
SOURCE_EVALS_DIR_NAME = "evals"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"[error] missing required file: {path.relative_to(REPO_ROOT).as_posix()}")


def read_json(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[error] invalid JSON in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def read_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(read_text(path))
    except yaml.YAMLError as exc:
        raise SystemExit(f"[error] invalid YAML in {path.relative_to(REPO_ROOT).as_posix()}: {exc}")


def repo_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def report_id(report_path: Path) -> str:
    name = report_path.name
    if not name.endswith(REPORT_SUFFIX):
        raise SystemExit(f"[error] actual report must end with {REPORT_SUFFIX}: {repo_path(report_path)}")
    return name[: -len(REPORT_SUFFIX)]


def string_value(payload: dict[str, Any], key: str, *, location: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise SystemExit(f"[error] {location} must expose non-empty string field '{key}'")
    return value


def build_report_entry(report_path: Path) -> dict[str, object]:
    bundle_dir = report_path.parents[1]
    manifest_path = bundle_dir / "eval.yaml"
    report_schema_path = bundle_dir / "reports" / "summary.schema.json"
    report_payload = read_json(report_path)
    manifest = read_yaml(manifest_path)
    location = repo_path(report_path)

    if not isinstance(report_payload, dict):
        raise SystemExit(f"[error] {location} must contain a JSON object")
    if not isinstance(manifest, dict):
        raise SystemExit(f"[error] {repo_path(manifest_path)} must contain a YAML object")

    eval_name = string_value(report_payload, "eval_name", location=location)
    bundle_status = string_value(report_payload, "bundle_status", location=location)
    manifest_name = manifest.get("name")
    manifest_status = manifest.get("status")
    if eval_name != manifest_name:
        raise SystemExit(
            f"[error] {location} eval_name '{eval_name}' does not match {repo_path(manifest_path)}"
        )
    if bundle_status != manifest_status:
        raise SystemExit(
            f"[error] {location} bundle_status '{bundle_status}' does not match {repo_path(manifest_path)}"
        )

    limitations = report_payload.get("limitations")
    limitations_count = len(limitations) if isinstance(limitations, list) else 0

    return {
        "report_id": report_id(report_path),
        "eval_name": eval_name,
        "bundle_status": bundle_status,
        "source_report_path": location,
        "source_bundle_ref": repo_path(bundle_dir / "EVAL.md"),
        "manifest_ref": repo_path(manifest_path),
        "report_schema_ref": repo_path(report_schema_path),
        "verdict": string_value(report_payload, "verdict", location=location),
        "case_family": string_value(report_payload, "case_family", location=location),
        "claim_boundary": string_value(report_payload, "claim_boundary", location=location),
        "limitations_count": limitations_count,
        "report_posture": "bounded_report_output",
        "authority_boundary": "derived index only; read the source report and bundle before interpreting",
        "receipt_status": "not_a_receipt",
    }


def build_eval_report_index_payload() -> dict[str, object]:
    report_paths = sorted((REPO_ROOT / SOURCE_EVALS_DIR_NAME).glob(f"**/reports/*{REPORT_SUFFIX}"))
    reports = [build_report_entry(path) for path in report_paths]
    reports.sort(key=lambda item: (str(item["eval_name"]), str(item["report_id"])))

    return {
        "schema_version": 1,
        "layer": "aoa-evals",
        "source_of_truth": {
            "bundle_reports": "evals/**/reports/*.report.json",
            "bundle_report_schema": "evals/**/reports/summary.schema.json",
            "bundle_manifest": "evals/**/eval.yaml",
            "eval_review_guide": "docs/EVAL_REVIEW_GUIDE.md",
        },
        "interpretation_boundary": (
            "This generated reader routes to bounded report artifacts. It is not a receipt, "
            "promotion signal, runtime acceptance, or verdict authority."
        ),
        "reports": reports,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact eval report index.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_eval_report_index_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/eval_report_index.min.json is out of date; "
                "run scripts/generate_eval_report_index.py"
            )
        print("[ok] generated/eval_report_index.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/eval_report_index.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
