#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


PART_ROOT = Path(__file__).resolve().parents[1]


def resolve_repo_root() -> Path:
    if len(PART_ROOT.parents) >= 4:
        expected_repo_root = PART_ROOT.parents[3]
        if (expected_repo_root / "mechanics").is_dir():
            return expected_repo_root
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "bundles").is_dir() and (candidate / "AGENTS.md").is_file():
            return candidate
    raise SystemExit("[error] unable to locate aoa-evals repository root")


REPO_ROOT = resolve_repo_root()
EXAMPLE_PATH = PART_ROOT / "examples" / "phase_alpha_eval_matrix.example.json"


def candidate_playbooks_roots() -> list[Path]:
    candidates = [REPO_ROOT.parent / "aoa-playbooks"]
    for ancestor in REPO_ROOT.parents:
        candidate = ancestor / "aoa-playbooks"
        if candidate not in candidates:
            candidates.append(candidate)
    return candidates


def resolve_playbooks_root() -> Path:
    env_root = os.environ.get("AOA_PLAYBOOKS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    for candidate in candidate_playbooks_roots():
        if (candidate / "generated" / "phase_alpha_run_matrix.min.json").is_file():
            return candidate.resolve()
    return candidate_playbooks_roots()[0].expanduser().resolve()


PLAYBOOKS_ROOT = resolve_playbooks_root()
PLAYBOOK_MATRIX_PATH = PLAYBOOKS_ROOT / "generated" / "phase_alpha_run_matrix.min.json"
OUTPUT_PATH = PART_ROOT / "generated" / "phase_alpha_eval_matrix.min.json"


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
        raise SystemExit(
            "[error] mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
            "examples/phase_alpha_eval_matrix.example.json must contain an object"
        )
    if not isinstance(playbook_payload, dict):
        raise SystemExit("[error] aoa-playbooks/generated/phase_alpha_run_matrix.min.json must contain an object")

    example_runs = example_payload.get("runs")
    playbook_runs = playbook_payload.get("runs")
    if not isinstance(example_runs, list):
        raise SystemExit(
            "[error] mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
            "examples/phase_alpha_eval_matrix.example.json must contain runs"
        )
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

        optional_control_path_rerun = example_run.get("optional_control_path_rerun", False)
        if not isinstance(optional_control_path_rerun, bool):
            raise SystemExit(
                f"[error] {run_id} optional_control_path_rerun must be a boolean when present"
            )

        entries.append(
            {
                "run_id": run_id,
                "sequence": run.get("sequence"),
                "playbook_id": run.get("playbook_id"),
                "playbook_name": run.get("playbook_name"),
                "runtime_lane": run.get("runtime_path_key"),
                "optional_control_path_rerun": optional_control_path_rerun,
                "required_evals": required_evals,
            }
        )

    return {
        "schema_version": 1,
        "layer": "aoa-evals",
        "phase": "alpha",
        "source_of_truth": {
            "phase_alpha_eval_plan": (
                "mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
                "examples/phase_alpha_eval_matrix.example.json"
            ),
            "phase_alpha_run_matrix": "repo:aoa-playbooks/generated/phase_alpha_run_matrix.min.json",
            "trace_eval_hooks": "mechanics/audit/parts/artifact-verdict-hooks/examples/artifact_to_verdict_hook.*.example.json",
            "runtime_evidence_selection_examples": "mechanics/audit/parts/selected-evidence-packets/examples/runtime_evidence_selection.*.example.json",
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
                "[error] mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
                "generated/phase_alpha_eval_matrix.min.json is out of date; "
                "run mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
                "scripts/generate_phase_alpha_eval_matrix.py"
            )
        print(
            "[ok] mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
            "generated/phase_alpha_eval_matrix.min.json is current"
        )
        return 0

    write_output(payload)
    print(
        "[ok] wrote mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/"
        "generated/phase_alpha_eval_matrix.min.json"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
