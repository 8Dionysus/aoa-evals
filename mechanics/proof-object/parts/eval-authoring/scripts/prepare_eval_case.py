#!/usr/bin/env python3
"""Prepare a route-first eval_need_v1 case kit for future eval authoring."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import scaffold_eval_bundle as scaffold
import eval_forge_route as forge


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPT_RELATIVE_PATH = (
    "mechanics/proof-object/parts/eval-authoring/scripts/scaffold_eval_bundle.py"
)
SCHEMA_VERSION = "eval_case_preparation_v1"
AUTHORITY_BOUNDARY = (
    "This helper prepares an eval_need_v1 proposal and route kit only. "
    "It does not create source eval bundles, accept proof, score evidence, "
    "mint baselines, publish reports, or promote candidate evidence."
)
COLLECTION_ROUTES = {
    "existing_eval_route": "inspect_existing_source_eval_before_new_authoring",
    "candidate_evidence_packet": "keep_candidate_only_and_route_through_candidate_readers",
    "quest_record": "record_or_update_quest_before_eval_authoring",
    "new_draft_bundle": "review_existing_matches_then_scaffold_draft_if_still_needed",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help="aoa-evals repo root.")
    parser.add_argument(
        "--proposal",
        help="Existing eval_need_v1 JSON proposal to route. When provided, field flags are ignored.",
    )
    parser.add_argument("--write-proposal", help="Optional path to write the prepared eval_need_v1 JSON.")
    parser.add_argument("--force", action="store_true", help="Overwrite --write-proposal if it already exists.")

    parser.add_argument("--name", help="Eval name, e.g. aoa-route-discipline.")
    parser.add_argument("--proof-question", help="Bounded proof question.")
    parser.add_argument("--origin-need", help="Origin need or pressure that created the case.")
    parser.add_argument("--summary", help="Short bounded claim summary.")
    parser.add_argument("--object-under-evaluation", help="Object under evaluation.")
    parser.add_argument(
        "--category",
        default="workflow",
        choices=["capability", "workflow", "boundary", "artifact", "regression", "comparative", "longitudinal", "stress"],
    )
    parser.add_argument(
        "--claim-type",
        default="bounded",
        choices=["bounded", "comparative", "regression", "longitudinal"],
    )
    parser.add_argument(
        "--baseline-mode",
        default="none",
        choices=["none", "fixed-baseline", "previous-version", "peer-compare", "longitudinal-window"],
    )
    parser.add_argument(
        "--report-format",
        default="summary-with-breakdown",
        choices=["summary", "summary-with-breakdown", "comparative-summary"],
    )
    parser.add_argument(
        "--verdict-shape",
        default="categorical",
        choices=["pass-fail", "categorical", "scalar-with-interpretation", "comparative", "mixed"],
    )
    parser.add_argument(
        "--authoring-route",
        default="new_draft_bundle",
        choices=["existing_eval_route", "candidate_evidence_packet", "quest_record", "new_draft_bundle"],
    )
    parser.add_argument("--expected-use-when", action="append", default=[], help="Repeatable expected-use condition.")
    parser.add_argument("--blind-spot", action="append", default=[], help="Repeatable blind-spot note.")
    parser.add_argument("--related-eval-ref", action="append", default=[], help="Existing eval name to check first.")
    parser.add_argument("--candidate-evidence-ref", action="append", default=[], help="Candidate evidence ref.")
    parser.add_argument("--quest-ref", action="append", default=[], help="Quest ref, e.g. AOA-EV-Q-0010.")
    parser.add_argument("--source-ref", action="append", default=[], help="Source route/evidence ref.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser.parse_args(argv)


def load_json_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise scaffold.ScaffoldError(f"{path}: invalid proposal JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise scaffold.ScaffoldError(f"{path}: proposal must be a JSON object")
    return payload


def proposal_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema_version": "eval_need_v1",
        "name": args.name,
        "proof_question": args.proof_question,
        "origin_need": args.origin_need,
        "summary": args.summary,
        "object_under_evaluation": args.object_under_evaluation,
        "category": args.category,
        "claim_type": args.claim_type,
        "baseline_mode": args.baseline_mode,
        "report_format": args.report_format,
        "verdict_shape": args.verdict_shape,
        "authoring_route": args.authoring_route,
        "expected_use_when": args.expected_use_when,
        "blind_spot_notes": args.blind_spot,
        "related_eval_refs": args.related_eval_ref,
        "candidate_evidence_refs": args.candidate_evidence_ref,
        "quest_refs": args.quest_ref,
        "source_refs": args.source_ref,
        "technique_dependencies": [],
        "skill_dependencies": [],
        "capability_dependencies": [],
    }


def resolve_path(path_value: str, *, base: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else base / path


def write_proposal(path: Path, proposal: dict[str, Any], *, force: bool) -> dict[str, Any]:
    if path.exists() and not force:
        return {
            "status": "blocked",
            "path": path.as_posix(),
            "reason": "target exists; pass --force to overwrite the proposal file",
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(proposal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": "written", "path": path.as_posix()}


def command_for(proposal_path: str, *, allow_new: bool = False, write: bool = False) -> str:
    parts = ["python", SCRIPT_RELATIVE_PATH, "--proposal", proposal_path, "--json"]
    if allow_new:
        parts.append("--allow-new")
    if write:
        parts.append("--write")
    return " ".join(parts)


def recommended_next_step(route_result: dict[str, Any], proposal: dict[str, Any]) -> str:
    outcome = str(route_result.get("outcome") or "")
    if outcome == "invalid_proposal":
        return "fix_eval_need_fields_before_authoring"
    if outcome == "existing_route_required":
        return "inspect_existing_matches_before_scaffolding_parallel_eval"
    if outcome == "new_draft_requires_allow_new":
        return "review_existing_matches_then_run_scaffold_dry_run_with_allow_new"
    if outcome in {"existing_eval_route", "candidate_evidence_packet", "quest_record"}:
        return COLLECTION_ROUTES[outcome]
    if proposal.get("authoring_route") != "new_draft_bundle":
        return COLLECTION_ROUTES.get(str(proposal.get("authoring_route")), "follow_declared_authoring_route")
    return "run_scaffold_dry_run_then_request_human_review_before_write"


def forge_route_for(
    *,
    proposal: dict[str, Any],
    repo_root: Path,
    proposal_ref: str,
    validation_errors: list[str],
) -> dict[str, Any]:
    if validation_errors:
        return {
            "schema_version": forge.SCHEMA_VERSION,
            "authority_boundary": forge.AUTHORITY_BOUNDARY,
            "input_kind": "eval_need_v1",
            "case_id": str(proposal.get("name") or "proposal:unknown"),
            "status": "blocked",
            "reason": "proposal validation failed before forge routing",
            "errors": validation_errors,
            "proof_authority": False,
            "promotion_allowed": False,
        }
    case = forge.proposal_case(proposal, proposal_path=proposal_ref)
    return forge.build_forge_route(case=case, repo_root=repo_root)


def build_case_kit(
    *,
    proposal: dict[str, Any],
    repo_root: Path,
    proposal_output_path: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    route_check = scaffold.route_result(
        proposal=proposal,
        repo_root=repo_root,
        allow_new=False,
        write=False,
    )
    draft_plan = scaffold.route_result(
        proposal=proposal,
        repo_root=repo_root,
        allow_new=True,
        write=False,
    )
    validation_errors = route_check.get("errors", [])
    write_result: dict[str, Any] = {"status": "not_requested"}
    proposal_ref = proposal_output_path or "<write-proposal-path>"
    if proposal_output_path:
        if validation_errors:
            write_result = {
                "status": "blocked",
                "reason": "proposal validation failed; no file written",
            }
        else:
            output_path = resolve_path(proposal_output_path, base=repo_root)
            write_result = write_proposal(output_path, proposal, force=force)
            proposal_ref = output_path.as_posix()
    scaffold_commands = {
        "route_check": command_for(proposal_ref),
        "draft_dry_run_after_review": command_for(proposal_ref, allow_new=True),
        "write_draft_after_human_acceptance": command_for(proposal_ref, allow_new=True, write=True),
    }
    if write_result.get("status") == "blocked":
        validation_errors = [*validation_errors, str(write_result.get("reason"))]
    forge_route = forge_route_for(
        proposal=proposal,
        repo_root=repo_root,
        proposal_ref=proposal_ref,
        validation_errors=validation_errors,
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "valid": not validation_errors,
        "proposal": proposal,
        "proposal_write": write_result,
        "route_check": route_check,
        "draft_plan": draft_plan,
        "forge_route": forge_route,
        "recommended_next_step": recommended_next_step(route_check, proposal),
        "scaffold_commands": scaffold_commands,
        "collection_checklist": [
            "bounded proof question is explicit",
            "existing central eval matches inspected before new draft",
            "candidate evidence refs stay candidate-only",
            "owner/source refs are named",
            "blind spots are named before report or verdict work",
            "human acceptance is required before --write creates bundle files",
        ],
        "stop_lines": [
            "proposal file is not an eval verdict",
            "draft dry-run is not proof acceptance",
            "candidate evidence refs do not become source truth",
            "do not run scaffold --write before existing-match review and human acceptance",
        ],
        "errors": validation_errors,
    }


def render_text(payload: dict[str, Any]) -> str:
    proposal = payload.get("proposal", {})
    route_check = payload.get("route_check", {})
    lines = [
        "# Eval Case Preparation",
        "",
        str(payload["authority_boundary"]),
        "",
        f"- name: `{proposal.get('name')}`",
        f"- valid: {payload.get('valid')}",
        f"- route outcome: `{route_check.get('outcome')}`",
        f"- next: `{payload.get('recommended_next_step')}`",
    ]
    target = route_check.get("target_path")
    if target:
        lines.append(f"- target path: `{target}`")
    write_status = payload.get("proposal_write", {})
    lines.append(f"- proposal write: `{write_status.get('status')}`")
    if write_status.get("path"):
        lines.append(f"- proposal path: `{write_status.get('path')}`")
    forge_route = payload.get("forge_route") or {}
    if forge_route:
        decision = (forge_route.get("candidate_admissibility") or {}).get("decision")
        selected = forge_route.get("selected_archetype_id")
        if decision or selected:
            lines.extend(
                [
                    f"- forge decision: `{decision}`",
                    f"- forge archetype: `{selected}`",
                ]
            )
    matches = route_check.get("existing_matches") or []
    if matches:
        lines.extend(["", "## Existing Matches", ""])
        for match in matches:
            lines.append(f"- `{match.get('name')}` score={match.get('score')} path `{match.get('eval_path')}`")
    lines.extend(["", "## Commands", ""])
    for key, command in payload["scaffold_commands"].items():
        lines.append(f"- {key}: `{command}`")
    if payload.get("errors"):
        lines.extend(["", "## Errors", ""])
        for error in payload["errors"]:
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        if args.proposal:
            proposal_path = resolve_path(args.proposal, base=Path.cwd())
            proposal = load_json_mapping(proposal_path)
        else:
            proposal = proposal_from_args(args)
        payload = build_case_kit(
            proposal=proposal,
            repo_root=repo_root,
            proposal_output_path=args.write_proposal,
            force=args.force,
        )
    except scaffold.ScaffoldError as exc:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "authority_boundary": AUTHORITY_BOUNDARY,
            "valid": False,
            "errors": [str(exc)],
        }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return 0 if payload.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
