#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_INDEX_PATH = REPO_ROOT / "generated" / "runtime_candidate_template_index.min.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "runtime_candidate_intake.min.json"
REVIEW_GUIDE_BY_KIND = {
    "artifact_to_verdict_hook": "docs/TRACE_EVAL_BRIDGE.md",
    "runtime_evidence_selection": "docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
}
OWNER_REVIEW_FALLBACK = "docs/EVAL_REVIEW_GUIDE.md"


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


def _owner_review_refs(template: dict[str, object], *, review_guide_ref: str) -> list[str]:
    refs: list[str] = [review_guide_ref, OWNER_REVIEW_FALLBACK]
    source_example_ref = template.get("source_example_ref")
    if isinstance(source_example_ref, str):
        refs.append(source_example_ref)
    deduped: list[str] = []
    for ref in refs:
        if ref not in deduped:
            deduped.append(ref)
    return deduped


def build_runtime_candidate_intake_payload() -> dict[str, object]:
    payload = read_json(TEMPLATE_INDEX_PATH)
    if not isinstance(payload, dict) or not isinstance(payload.get("templates"), list):
        raise SystemExit("[error] generated/runtime_candidate_template_index.min.json must contain a templates list")

    entries: list[dict[str, object]] = []
    for template in payload["templates"]:
        if not isinstance(template, dict):
            continue
        template_kind = template.get("template_kind")
        template_name = template.get("template_name")
        if not isinstance(template_kind, str) or not isinstance(template_name, str):
            continue
        review_guide_ref = REVIEW_GUIDE_BY_KIND.get(template_kind, OWNER_REVIEW_FALLBACK)
        entries.append(
            {
                "template_kind": template_kind,
                "template_name": template_name,
                "playbook_id": template.get("playbook_id") if isinstance(template.get("playbook_id"), str) else None,
                "eval_anchor": template.get("eval_anchor") if isinstance(template.get("eval_anchor"), str) else None,
                "verdict_bundle_ref": template.get("verdict_bundle_ref")
                if isinstance(template.get("verdict_bundle_ref"), str)
                else None,
                "required_runtime_artifacts": [
                    item for item in template.get("required_runtime_artifacts", []) if isinstance(item, str)
                ],
                "review_required": bool(template.get("review_required")),
                "review_guide_ref": review_guide_ref,
                "owner_review_refs": _owner_review_refs(template, review_guide_ref=review_guide_ref),
                "candidate_acceptance_posture": "candidate_until_eval_review",
            }
        )

    entries.sort(key=lambda item: (str(item["template_kind"]), str(item["template_name"])))
    return {
        "schema_version": 1,
        "layer": "aoa-evals",
        "source_of_truth": {
            "runtime_candidate_template_index": "generated/runtime_candidate_template_index.min.json",
            "eval_review_guide": "docs/EVAL_REVIEW_GUIDE.md",
            "trace_eval_bridge": "docs/TRACE_EVAL_BRIDGE.md",
            "runtime_bench_promotion_guide": "docs/RUNTIME_BENCH_PROMOTION_GUIDE.md",
        },
        "templates": entries,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact runtime candidate intake surface.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_runtime_candidate_intake_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/runtime_candidate_intake.min.json is out of date; "
                "run scripts/generate_runtime_candidate_intake.py"
            )
        print("[ok] generated/runtime_candidate_intake.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/runtime_candidate_intake.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
