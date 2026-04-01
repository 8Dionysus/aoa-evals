#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_CATALOG_PATH = REPO_ROOT / "generated" / "eval_catalog.min.json"
EXAMPLES_ROOT = REPO_ROOT / "examples"
OUTPUT_PATH = REPO_ROOT / "generated" / "runtime_candidate_template_index.min.json"


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


def _eval_bundle_refs() -> dict[str, str]:
    payload = read_json(EVAL_CATALOG_PATH)
    if not isinstance(payload, dict) or not isinstance(payload.get("evals"), list):
        raise SystemExit("[error] generated/eval_catalog.min.json must contain an evals list")
    bundle_refs: dict[str, str] = {}
    for entry in payload["evals"]:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        eval_path = entry.get("eval_path")
        if isinstance(name, str) and isinstance(eval_path, str):
            bundle_refs[name] = f"repo:aoa-evals/{eval_path}"
    return bundle_refs


def _ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def build_runtime_candidate_template_index_payload() -> dict[str, object]:
    bundle_refs = _eval_bundle_refs()
    entries: list[dict[str, object]] = []

    for path in sorted(EXAMPLES_ROOT.glob("runtime_evidence_selection.*.example.json")):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise SystemExit(f"[error] {path.relative_to(REPO_ROOT).as_posix()} must contain an object")
        target_eval = payload.get("target_eval")
        selected_evidence = payload.get("selected_evidence")
        required_runtime_artifacts: list[str] = []
        if isinstance(selected_evidence, list):
            required_runtime_artifacts = _ordered_unique(
                [
                    item.get("evidence_role")
                    for item in selected_evidence
                    if isinstance(item, dict) and isinstance(item.get("evidence_role"), str)
                ]
            )
        review_posture = payload.get("review_posture")
        entries.append(
            {
                "template_kind": "runtime_evidence_selection",
                "template_name": payload.get("selection_id"),
                "playbook_id": None,
                "eval_anchor": target_eval if isinstance(target_eval, str) else None,
                "verdict_bundle_ref": bundle_refs.get(target_eval) if isinstance(target_eval, str) else None,
                "required_runtime_artifacts": required_runtime_artifacts,
                "review_required": bool(
                    isinstance(review_posture, dict) and review_posture.get("human_review_required") is True
                ),
                "source_example_ref": path.relative_to(REPO_ROOT).as_posix(),
            }
        )

    for path in sorted(EXAMPLES_ROOT.glob("artifact_to_verdict_hook.*.example.json")):
        payload = read_json(path)
        if not isinstance(payload, dict):
            raise SystemExit(f"[error] {path.relative_to(REPO_ROOT).as_posix()} must contain an object")
        artifact_inputs = payload.get("artifact_inputs")
        required_runtime_artifacts = [
            item for item in artifact_inputs if isinstance(item, str)
        ] if isinstance(artifact_inputs, list) else []
        report_expectation = payload.get("report_expectation")
        entries.append(
            {
                "template_kind": "artifact_to_verdict_hook",
                "template_name": payload.get("hook_id"),
                "playbook_id": payload.get("playbook_id") if isinstance(payload.get("playbook_id"), str) else None,
                "eval_anchor": payload.get("eval_anchor") if isinstance(payload.get("eval_anchor"), str) else None,
                "verdict_bundle_ref": payload.get("verdict_bundle_ref")
                if isinstance(payload.get("verdict_bundle_ref"), str)
                else None,
                "required_runtime_artifacts": required_runtime_artifacts,
                "review_required": bool(
                    isinstance(report_expectation, dict) and report_expectation.get("review_required") is True
                ),
                "source_example_ref": path.relative_to(REPO_ROOT).as_posix(),
            }
        )

    entries.sort(key=lambda item: (str(item["template_kind"]), str(item["template_name"])))
    return {
        "schema_version": 1,
        "layer": "aoa-evals",
        "source_of_truth": {
            "eval_catalog": "generated/eval_catalog.min.json",
            "runtime_evidence_selection_examples": "examples/runtime_evidence_selection.*.example.json",
            "artifact_to_verdict_hook_examples": "examples/artifact_to_verdict_hook.*.example.json",
        },
        "templates": entries,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact runtime candidate template index.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_runtime_candidate_template_index_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/runtime_candidate_template_index.min.json is out of date; "
                "run scripts/generate_runtime_candidate_template_index.py"
            )
        print("[ok] generated/runtime_candidate_template_index.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/runtime_candidate_template_index.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
