#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = REPO_ROOT / "examples" / "phase_alpha_eval_matrix.example.json"
PLAYBOOKS_ROOT = Path(
    os.environ.get("AOA_PLAYBOOKS_ROOT", REPO_ROOT.parent / "aoa-playbooks")
).expanduser().resolve()
PLAYBOOK_MATRIX_PATH = PLAYBOOKS_ROOT / "generated" / "phase_alpha_run_matrix.min.json"
OUTPUT_PATH = REPO_ROOT / "generated" / "phase_alpha_eval_matrix.min.json"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"[error] missing required file: {path}")


def read_json(path: Path) -> object:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[error] invalid JSON in {path}: {exc}")


def ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def build_phase_alpha_eval_matrix_payload() -> dict[str, object]:
    example_payload = read_json(EXAMPLE_PATH)
    playbook_payload = read_json(PLAYBOOK_MATRIX_PATH)
    if not isinstance(example_payload, dict):
        raise SystemExit("[error] examples/phase_alpha_eval_matrix.example.json must contain an object")
    if not isinstance(playbook_payload, dict):
        raise SystemExit("[error] aoa-playbooks/generated/phase_alpha_run_matrix.min.json must contain an object")

    example_runs = example_payload.get("runs")
    playbook_runs = playbook_payload.get("runs")
    if not isinstance(example_runs, list):
        raise SystemExit("[error] examples/phase_alpha_eval_matrix.example.json must contain runs")
    if not isinstance(playbook_runs, list):
        raise SystemExit("[error] aoa-playbooks/generated/phase_alpha_run_matrix.min.json must contain runs")

    example_by_run_id: dict[str, dict[str, object]] = {}
    for item in example_runs:
        if not isinstance(item, dict):
            raise SystemExit("[error] phase alpha eval example runs must be objects")
        run_id = item.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise SystemExit("[error] phase alpha eval example runs must expose a non-empty run_id")
        if run_id in example_by_run_id:
            raise SystemExit(f"[error] duplicate phase alpha eval example run_id: {run_id}")
        example_by_run_id[run_id] = item

    playbook_by_run_id: dict[str, dict[str, object]] = {}
    for item in playbook_runs:
        if not isinstance(item, dict):
            raise SystemExit("[error] aoa-playbooks phase alpha runs must be objects")
        run_id = item.get("run_id")
        if not isinstance(run_id, str) or not run_id:
            raise SystemExit("[error] aoa-playbooks phase alpha runs must expose a non-empty run_id")
        if run_id in playbook_by_run_id:
            raise SystemExit(f"[error] duplicate aoa-playbooks phase alpha run_id: {run_id}")
        playbook_by_run_id[run_id] = item

    if set(example_by_run_id) != set(playbook_by_run_id):
        missing = sorted(set(playbook_by_run_id) - set(example_by_run_id))
        extra = sorted(set(example_by_run_id) - set(playbook_by_run_id))
        raise SystemExit(
            "[error] phase alpha eval example run ids must match aoa-playbooks phase alpha run ids "
            f"(missing={missing}, extra={extra})"
        )

    entries: list[dict[str, object]] = []
    for run in sorted(playbook_runs, key=lambda item: int(item.get("sequence", 0))):
        run_id = str(run["run_id"])
        example_run = example_by_run_id[run_id]
        eval_surfaces = example_run.get("eval_surfaces")
        if not isinstance(eval_surfaces, list):
            raise SystemExit(f"[error] {run_id} must define eval_surfaces")

        surfaces_by_eval: dict[str, list[str]] = {}
        for surface in eval_surfaces:
            if not isinstance(surface, dict):
                raise SystemExit(f"[error] {run_id} eval_surfaces entries must be objects")
            eval_anchor = surface.get("eval_anchor")
            if not isinstance(eval_anchor, str) or not eval_anchor:
                raise SystemExit(f"[error] {run_id} eval_surfaces entries must define eval_anchor")
            if eval_anchor in surfaces_by_eval:
                raise SystemExit(f"[error] {run_id} duplicates eval surface for {eval_anchor}")
            support_refs = surface.get("support_refs", [])
            if not isinstance(support_refs, list):
                raise SystemExit(f"[error] {run_id} support_refs for {eval_anchor} must be a list")
            normalized_support_refs = [ref for ref in support_refs if isinstance(ref, str) and ref]
            if len(normalized_support_refs) != len(support_refs):
                raise SystemExit(f"[error] {run_id} support_refs for {eval_anchor} must be non-empty strings")
            surfaces_by_eval[eval_anchor] = normalized_support_refs

        run_eval_anchors = run.get("eval_anchors")
        if not isinstance(run_eval_anchors, list):
            raise SystemExit(f"[error] {run_id} must expose eval_anchors in aoa-playbooks phase alpha matrix")
        if set(surfaces_by_eval) != set(anchor for anchor in run_eval_anchors if isinstance(anchor, str)):
            missing = sorted(set(run_eval_anchors) - set(surfaces_by_eval))
            extra = sorted(set(surfaces_by_eval) - set(run_eval_anchors))
            raise SystemExit(
                f"[error] {run_id} eval surface anchors must match aoa-playbooks eval_anchors "
                f"(missing={missing}, extra={extra})"
            )

        reviewed_run_ref = run.get("reviewed_run_ref")
        if not isinstance(reviewed_run_ref, str) or not reviewed_run_ref:
            raise SystemExit(f"[error] {run_id} must expose reviewed_run_ref in aoa-playbooks phase alpha matrix")
        reviewed_run_repo_ref = f"repo:aoa-playbooks/{reviewed_run_ref}"

        required_evals: list[dict[str, object]] = []
        for eval_anchor in run_eval_anchors:
            refs = ordered_unique(surfaces_by_eval[eval_anchor] + [reviewed_run_repo_ref])
            required_evals.append(
                {
                    "eval_anchor": eval_anchor,
                    "evidence_refs": refs,
                }
            )

        entries.append(
            {
                "run_id": run_id,
                "sequence": run.get("sequence"),
                "playbook_id": run.get("playbook_id"),
                "playbook_name": run.get("playbook_name"),
                "runtime_lane": run.get("runtime_path_key"),
                "optional_control_path_rerun": bool(example_run.get("optional_control_path_rerun")),
                "required_evals": required_evals,
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-evals",
        "phase": "alpha",
        "source_of_truth": {
            "phase_alpha_eval_plan": "examples/phase_alpha_eval_matrix.example.json",
            "phase_alpha_run_matrix": "repo:aoa-playbooks/generated/phase_alpha_run_matrix.min.json",
            "trace_eval_hooks": "examples/artifact_to_verdict_hook.*.example.json",
            "runtime_evidence_selection_examples": "examples/runtime_evidence_selection.*.example.json",
        },
        "runtime_lanes": example_payload.get("runtime_lanes"),
        "verdict_interpretation": example_payload.get("verdict_interpretation"),
        "runs": entries,
    }


def write_output(payload: dict[str, object]) -> None:
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the Phase Alpha eval matrix.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated output without writing files.",
    )
    args = parser.parse_args(argv)

    payload = build_phase_alpha_eval_matrix_payload()
    if args.check:
        current = read_json(OUTPUT_PATH)
        if current != payload:
            raise SystemExit(
                "[error] generated/phase_alpha_eval_matrix.min.json is out of date; "
                "run scripts/generate_phase_alpha_eval_matrix.py"
            )
        print("[ok] generated/phase_alpha_eval_matrix.min.json is current")
        return 0

    write_output(payload)
    print("[ok] wrote generated/phase_alpha_eval_matrix.min.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
