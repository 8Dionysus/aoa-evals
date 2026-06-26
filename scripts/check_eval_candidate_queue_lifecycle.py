#!/usr/bin/env python3
"""Check eval candidate queue lifecycle routes without promoting proof."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Sequence

import validate_eval_candidate_packets as packet_validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "aoa_eval_candidate_queue_lifecycle_v1"

ACTIVE_REVIEW_STATES = {
    "needs_owner_review",
    "central_draft",
    "accepted",
}
STATE_ROUTES = {
    "observed": "inspect_owner_surface_before_packetization",
    "needs_owner_review": "manual_owner_review_then_select_apply_design_or_reject",
    "duplicate_existing_eval": "link_existing_eval_then_apply_or_reject_duplicate",
    "local_only": "repo_local_intake_or_suite_owner_route",
    "central_draft": "central_owner_draft_review_without_proof_acceptance",
    "rejected": "retain_rejection_reason_no_eval_work",
    "deferred": "resolve_freshness_or_owner_blocker_before_revisit",
    "accepted": "owner_conversion_only_proof_promotion_still_forbidden",
}
STOP_LINES = [
    "candidate queue lifecycle checks do not accept proof",
    "candidate queue lifecycle checks do not write packet state",
    "accepted candidate state still cannot set promotion_allowed=true",
    "session evidence remains candidate-only until owner conversion",
]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        help=(
            "Candidate packet files or directories. Directories are searched for "
            "'*.eval_candidate.json'. Defaults to the candidate-reader packets directory."
        ),
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    return parser.parse_args(argv)


def relative(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def owner_gate_present(payload: dict[str, Any]) -> bool:
    gates = payload.get("promotion_forbidden_until")
    if not isinstance(gates, list):
        return False
    gate_text = " ".join(str(item).lower() for item in gates)
    return "human" in gate_text and "owner" in gate_text


def conversion_gate_present(payload: dict[str, Any]) -> bool:
    gates = payload.get("promotion_forbidden_until")
    if not isinstance(gates, list):
        return False
    gate_text = " ".join(str(item).lower() for item in gates)
    return "converted" in gate_text or "conversion" in gate_text


def lifecycle_issues_for_payload(payload: Any, *, location: str) -> list[dict[str, str]]:
    if not isinstance(payload, dict):
        return [{"location": location, "message": "candidate packet must be an object"}]
    issues: list[dict[str, str]] = []
    state = str(payload.get("candidate_state") or "")
    if payload.get("candidate_only") is not True:
        issues.append({"location": location, "message": "candidate_only must remain true"})
    if payload.get("proof_authority") is not False:
        issues.append({"location": location, "message": "proof_authority must remain false"})
    if payload.get("promotion_allowed") is not False:
        issues.append({"location": location, "message": "promotion_allowed must remain false"})
    if state in ACTIVE_REVIEW_STATES and not owner_gate_present(payload):
        issues.append(
            {
                "location": location,
                "message": f"{state} candidate must keep a human owner acceptance gate",
            }
        )
    if state == "accepted" and not conversion_gate_present(payload):
        issues.append(
            {
                "location": location,
                "message": "accepted candidate must name owner conversion before any proof route",
            }
        )
    if state == "rejected":
        evaluator_fit = str(payload.get("evaluator_fit") or "")
        reason = str(payload.get("candidate_state_reason") or "").lower()
        if evaluator_fit != "reject_no_eval_fit" and "reject" not in reason:
            issues.append(
                {
                    "location": location,
                    "message": "rejected candidate must preserve explicit reject fit or reason",
                }
            )
    if state == "duplicate_existing_eval":
        surface_check = str(payload.get("existing_surface_check") or "").lower()
        if "existing" not in surface_check and "duplicate" not in surface_check:
            issues.append(
                {
                    "location": location,
                    "message": "duplicate candidate must name the existing surface check",
                }
            )
    return issues


def lifecycle_route(payload: dict[str, Any]) -> str:
    state = str(payload.get("candidate_state") or "")
    return STATE_ROUTES.get(state, "repair_unknown_candidate_state")


def load_packets(paths: Sequence[Path]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    packets: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    for path in paths:
        location = relative(path)
        if not path.exists():
            issues.append({"location": location, "message": "candidate packet path is missing"})
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append({"location": location, "message": f"invalid JSON: {exc}"})
            continue
        packets.append({"path": path, "location": location, "payload": payload})
    return packets, issues


def build_lifecycle_payload(targets: Sequence[str]) -> dict[str, Any]:
    paths = packet_validator.packet_paths(targets)
    schema_issues = [
        {"location": issue.location, "message": issue.message}
        for issue in packet_validator.validate_files(paths)
    ]
    packets, load_issues = load_packets(paths)
    lifecycle_issues: list[dict[str, str]] = []
    next_actions: list[dict[str, Any]] = []
    by_state: Counter[str] = Counter()
    by_route: Counter[str] = Counter()
    by_owner: Counter[str] = Counter()
    for item in packets:
        payload = item["payload"]
        location = str(item["location"])
        lifecycle_issues.extend(lifecycle_issues_for_payload(payload, location=location))
        if not isinstance(payload, dict):
            continue
        state = str(payload.get("candidate_state") or "unknown")
        route = lifecycle_route(payload)
        owner_refs = payload.get("owner_surface_refs")
        owner = str(owner_refs[0]) if isinstance(owner_refs, list) and owner_refs else "unknown"
        by_state[state] += 1
        by_route[route] += 1
        by_owner[owner] += 1
        gates = payload.get("promotion_forbidden_until")
        next_actions.append(
            {
                "packet_id": payload.get("packet_id"),
                "packet_ref": location,
                "candidate_state": state,
                "owner_hint": owner,
                "expected_aoa_eval_route": payload.get("expected_aoa_eval_route"),
                "lifecycle_route": route,
                "next_step": payload.get("next_step"),
                "promotion_allowed": payload.get("promotion_allowed"),
                "candidate_only": payload.get("candidate_only"),
                "proof_authority": payload.get("proof_authority"),
                "owner_gate_present": owner_gate_present(payload),
                "promotion_forbidden_until_count": len(gates) if isinstance(gates, list) else 0,
            }
        )
    issues = schema_issues + load_issues + lifecycle_issues
    next_actions.sort(
        key=lambda item: (
            0 if item.get("candidate_state") == "needs_owner_review" else 1,
            str(item.get("packet_id") or ""),
        )
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": "Candidate queue lifecycle checks route review work only; they do not accept proof, score candidates, promote packets, or mutate packet state.",
        "packet_root": relative(packet_validator.DEFAULT_PACKET_ROOT),
        "packet_count": len(paths),
        "valid": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "summary": {
            "by_state": dict(sorted(by_state.items())),
            "by_lifecycle_route": dict(sorted(by_route.items())),
            "by_owner_hint": dict(sorted(by_owner.items())),
            "next_action_count": len(next_actions),
        },
        "next_actions": next_actions,
        "stop_lines": STOP_LINES,
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = [
        "# Eval Candidate Queue Lifecycle",
        "",
        payload["authority_boundary"],
        "",
        f"- Packets: {payload['packet_count']}",
        f"- Valid: {payload['valid']}",
        f"- Issues: {payload['issue_count']}",
        "",
        "## Next Actions",
    ]
    for action in payload["next_actions"]:
        lines.append(
            "- {packet}: {state}; route {route}; next {next_step}".format(
                packet=action.get("packet_id"),
                state=action.get("candidate_state"),
                route=action.get("lifecycle_route"),
                next_step=action.get("next_step"),
            )
        )
    if payload["issues"]:
        lines.extend(["", "## Issues"])
        for issue in payload["issues"]:
            lines.append(f"- {issue['location']}: {issue['message']}")
    lines.extend(["", "## Stop Lines"])
    for line in payload["stop_lines"]:
        lines.append(f"- {line}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = build_lifecycle_payload(args.targets)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_text(payload), end="")
    return 0 if payload["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
