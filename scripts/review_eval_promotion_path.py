#!/usr/bin/env python3
"""Dry-run local-to-central eval promotion review for OS Abyss."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence

import build_local_eval_port_inventory


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = build_local_eval_port_inventory.DEFAULT_WORKSPACE_ROOT
SCHEMA_VERSION = "os_abyss_eval_promotion_review_v1"
PROMOTION_GATES = [
    "local_owner_review",
    "central_overlap_check",
    "source_bundle_draft",
    "fixture_runner_report_contract_review",
    "human_acceptance",
    "catalog_report_regeneration",
    "release_advisory_validation",
]
AUTHORITY_BOUNDARY = (
    "This dry-run review routes local eval pressure toward owner review. "
    "It cannot promote a candidate, create a central bundle, accept proof, "
    "score a run, mint a baseline, publish a release artifact, or execute "
    "local suite runner argv."
)
FORBIDDEN_TRUE_FIELDS = {
    "promotion_allowed",
    "mcp_promotion_allowed",
    "proof_authority",
    "can_accept_proof",
    "can_promote_candidates",
    "can_score",
    "central_bundle_created",
    "release_artifact_created",
    "execution_allowed",
    "promotion_review_executed_runner",
}
FORBIDDEN_ANY_FIELDS = {
    "verdict",
    "score",
    "baseline",
    "accepted_proof",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-root",
        default=str(DEFAULT_WORKSPACE_ROOT),
        help="Workspace root containing OS Abyss repositories.",
    )
    parser.add_argument(
        "--repo-id",
        default="",
        help="Optional local repo id to dry-run. Defaults to the highest active pressure repo.",
    )
    parser.add_argument(
        "--review-payload",
        default="",
        help="Validate an existing promotion review JSON payload instead of building one.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args(argv)


def read_json_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def load_central_catalog(repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    return read_json_mapping(repo_root / "generated" / "eval_catalog.min.json")


def catalog_records(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    records = catalog.get("evals")
    return [record for record in records if isinstance(record, dict)] if isinstance(records, list) else []


def pressure_total(repo: dict[str, Any]) -> int:
    counts = repo.get("pressure_counts")
    if not isinstance(counts, dict):
        return 0
    return int(counts.get("active_total") or 0)


def severity_for_repo(repo: dict[str, Any]) -> str:
    if repo.get("inventory_status") == "invalid" or repo.get("validator_ok") is False:
        return "blocked"
    total = pressure_total(repo)
    if total >= 5:
        return "high"
    if total >= 2:
        return "medium"
    if total == 1:
        return "low"
    return "none"


def select_repo_for_review(
    inventory_payload: dict[str, Any],
    *,
    repo_id: str = "",
) -> tuple[dict[str, Any] | None, list[dict[str, str]]]:
    repos = inventory_payload.get("repos")
    if not isinstance(repos, list):
        return None, [{"code": "inventory_missing_repos", "message": "inventory payload has no repos list"}]

    candidates = [repo for repo in repos if isinstance(repo, dict)]
    if repo_id:
        for repo in candidates:
            if repo.get("repo_id") == repo_id:
                return repo, []
        return None, [{"code": "repo_not_found", "message": f"repo_id not found in local eval inventory: {repo_id}"}]

    active = [repo for repo in candidates if pressure_total(repo) > 0]
    if not active:
        return None, [{"code": "no_active_local_pressure", "message": "no local eval port with active pressure found"}]

    severity_order = {"blocked": 0, "high": 1, "medium": 2, "low": 3, "none": 4}
    return sorted(
        active,
        key=lambda repo: (
            severity_order.get(severity_for_repo(repo), 9),
            -pressure_total(repo),
            str(repo.get("repo_id") or repo.get("repo") or ""),
        ),
    )[0], []


def tokenize(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if len(token) > 1}


def compact_eval_record(record: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "name": record.get("name"),
        "category": record.get("category"),
        "status": record.get("status"),
        "eval_path": record.get("eval_path"),
        "reason": reason,
    }


def exact_catalog_matches(repo: dict[str, Any], records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    names = {
        str(name)
        for name in repo.get("central_eval_name_matches", [])
        if isinstance(name, str) and name
    }
    if not names:
        return []
    return [compact_eval_record(record, "exact local eval name match") for record in records if record.get("name") in names]


def adjacent_catalog_matches(repo: dict[str, Any], records: list[dict[str, Any]], *, limit: int = 8) -> list[dict[str, Any]]:
    repo_id = str(repo.get("repo_id") or repo.get("repo") or "")
    repo_name = str(repo.get("repo") or "")
    repo_tokens = tokenize(repo_id) | tokenize(repo_name)
    route_key = ""
    if isinstance(repo.get("route_recommendation"), dict):
        route_key = str(repo["route_recommendation"].get("route_key") or "")
    pressure_tokens = repo_tokens | tokenize(route_key)
    matches: list[tuple[int, str, dict[str, Any]]] = []
    exact_names = {item.get("name") for item in exact_catalog_matches(repo, records)}

    for record in records:
        if record.get("name") in exact_names:
            continue
        reasons: list[str] = []
        score = 0
        for skill_ref in record.get("skill_refs", []) or []:
            if not isinstance(skill_ref, dict):
                continue
            if skill_ref.get("repo") == repo_name or skill_ref.get("repo") == repo_id:
                score += 5
                reasons.append(f"skill_ref repo={skill_ref.get('repo')}")
        record_tokens = tokenize(str(record.get("name") or ""))
        record_tokens |= tokenize(str(record.get("summary") or ""))
        overlap = sorted((record_tokens & pressure_tokens) - {"aoa"})
        if overlap:
            score += len(overlap)
            reasons.append("token overlap: " + ", ".join(overlap[:5]))
        if score:
            matches.append((score, str(record.get("name") or ""), compact_eval_record(record, "; ".join(reasons))))

    matches.sort(key=lambda item: (-item[0], item[1]))
    return [record for _score, _name, record in matches[:limit]]


def route_key(repo: dict[str, Any]) -> str:
    route = repo.get("route_recommendation")
    if not isinstance(route, dict):
        return "inspect_local_port"
    return str(route.get("route_key") or "inspect_local_port")


def route_action(repo: dict[str, Any]) -> str:
    route = repo.get("route_recommendation")
    if not isinstance(route, dict):
        return "Inspect the repo-local eval port before designing or promoting any central surface."
    return str(route.get("action") or "Inspect the repo-local eval port.")


def recommended_next_route(repo: dict[str, Any], exact: list[dict[str, Any]], adjacent: list[dict[str, Any]]) -> str:
    execution = repo.get("suite_execution")
    suite_state = str(execution.get("state") or "absent") if isinstance(execution, dict) else "absent"
    if suite_state == "invalid":
        return "repair_invalid_local_suite_execution_contract_before_promotion_review"
    if suite_state == "stale":
        return "review_tracked_source_changes_and_refresh_suite_hashes_before_apply"
    if repo.get("inventory_status") == "invalid" or repo.get("validator_ok") is False:
        return "repair_local_eval_port_before_any_promotion_review"
    if exact:
        return "select_or_apply_existing_central_eval_before_new_central_draft"
    if adjacent:
        return "inspect_adjacent_central_evals_then_local_owner_review"
    key = route_key(repo)
    if suite_state == "ready" and ("suite" in key or "regression" in key):
        return "apply_local_suite_as_candidate_regression_check_before_central_draft"
    if "intake" in key or "design" in key:
        return "local_owner_review_then_design_or_central_draft_decision"
    if "reports_only" in key:
        return "local_owner_review_then_suite_extraction_or_reject"
    if "local_bundle" in key:
        return "central_adoption_review_after_overlap_check"
    return "local_owner_review_required"


def suite_execution_review_posture(repo: dict[str, Any]) -> dict[str, Any]:
    execution = repo.get("suite_execution")
    if not isinstance(execution, dict):
        execution = {"state": "absent", "suites": []}
    state = str(execution.get("state") or "absent")
    return {
        "state": state,
        "suite_count": int(execution.get("suite_count") or 0),
        "invalid_count": int(execution.get("invalid_count") or 0),
        "stale_count": int(execution.get("stale_count") or 0),
        "ready_count": int(execution.get("ready_count") or 0),
        "readiness_scope": str(execution.get("readiness_scope") or "source-contract-ready"),
        "runtime_reproducibility_proven": False,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "execution_allowed": False,
        "owner_apply_required": state == "ready",
        "promotion_review_executed_runner": False,
        "proof_authority": False,
        "promotion_allowed": False,
    }


def gate(
    gate_id: str,
    *,
    owner: str,
    status: str,
    evidence_refs: Iterable[str],
    required_next: str,
    finding: str = "",
) -> dict[str, Any]:
    payload = {
        "gate": gate_id,
        "owner": owner,
        "status": status,
        "evidence_refs": list(evidence_refs),
        "required_next": required_next,
    }
    if finding:
        payload["finding"] = finding
    return payload


def build_gates(
    repo: dict[str, Any],
    *,
    exact_matches: list[dict[str, Any]],
    adjacent_matches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    repo_id = str(repo.get("repo_id") or repo.get("repo") or "unknown")
    port_ref = f"{repo_id}/{repo.get('port_path', 'evals/PORT.yaml')}"
    local_status = "blocked" if repo.get("validator_ok") is False else "needs_owner_review"
    overlap_finding = "no central overlap found"
    if exact_matches:
        overlap_finding = f"exact_duplicate_count={len(exact_matches)}"
    elif adjacent_matches:
        overlap_finding = f"adjacent_count={len(adjacent_matches)}"
    draft_required_next = (
        "select existing central eval first"
        if exact_matches
        else "human owner must accept central draft pressure before any bundle files exist"
    )
    return [
        gate(
            "local_owner_review",
            owner=repo_id,
            status=local_status,
            evidence_refs=[port_ref],
            required_next="repo owner reviews local intake/suites/reports and confirms central-review pressure",
        ),
        gate(
            "central_overlap_check",
            owner="aoa-evals",
            status="satisfied",
            evidence_refs=["generated/eval_catalog.min.json", "scripts/build_local_eval_port_inventory.py"],
            required_next="inspect exact and adjacent central evals before any new central draft",
            finding=overlap_finding,
        ),
        gate(
            "source_bundle_draft",
            owner="aoa-evals",
            status="not_started" if not exact_matches else "blocked",
            evidence_refs=[],
            required_next=draft_required_next,
        ),
        gate(
            "fixture_runner_report_contract_review",
            owner="aoa-evals",
            status="not_started",
            evidence_refs=[],
            required_next="only after a central source bundle draft exists",
        ),
        gate(
            "human_acceptance",
            owner="human owner",
            status="needs_owner_review",
            evidence_refs=[],
            required_next="explicit owner acceptance is required before central adoption",
        ),
        gate(
            "catalog_report_regeneration",
            owner="aoa-evals",
            status="not_started",
            evidence_refs=[],
            required_next="run catalog/report builders only after accepted source changes",
        ),
        gate(
            "release_advisory_validation",
            owner="aoa-evals release route",
            status="not_started",
            evidence_refs=[],
            required_next="run release/advisory validation only after catalog/report regeneration",
        ),
    ]


def stage_boundaries(repo_id: str) -> list[dict[str, Any]]:
    return [
        {
            "stage": "local_report",
            "owner": repo_id,
            "allowed_meaning": "repo-local observation, suite result, report note, or intake pressure",
            "forbidden_meaning": "central verdict, score, baseline, or accepted proof",
        },
        {
            "stage": "central_draft",
            "owner": "aoa-evals",
            "allowed_meaning": "reviewable source proposal after local owner and central overlap review",
            "forbidden_meaning": "accepted proof or release artifact",
        },
        {
            "stage": "accepted_central_proof",
            "owner": "aoa-evals + human owner gate",
            "allowed_meaning": "only after source bundle review, human acceptance, and validation",
            "forbidden_meaning": "MCP, queue, local report, or dashboard-created acceptance",
        },
        {
            "stage": "release_artifact",
            "owner": "aoa-evals release route",
            "allowed_meaning": "only after catalog/report regeneration and release/advisory validation",
            "forbidden_meaning": "dry-run promotion review output",
        },
    ]


def build_promotion_review_payload(
    inventory_payload: dict[str, Any],
    catalog_payload: dict[str, Any],
    *,
    repo_id: str = "",
) -> dict[str, Any]:
    inventory_payload = (
        build_local_eval_port_inventory.normalize_inventory_for_suite_consumers(
            inventory_payload
        )
    )
    repo, selection_issues = select_repo_for_review(inventory_payload, repo_id=repo_id)
    records = catalog_records(catalog_payload)
    if repo is None:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "authority_boundary": AUTHORITY_BOUNDARY,
            "valid": False,
            "promotion_allowed": False,
            "mcp_promotion_allowed": False,
            "issues": selection_issues,
            "issue_count": len(selection_issues),
        }
        return payload

    exact = exact_catalog_matches(repo, records)
    adjacent = adjacent_catalog_matches(repo, records)
    selected_repo_id = str(repo.get("repo_id") or repo.get("repo") or "unknown")
    gates = build_gates(repo, exact_matches=exact, adjacent_matches=adjacent)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "review_kind": "dry_run",
        "selected_repo": {
            "repo_id": selected_repo_id,
            "repo_path": repo.get("repo_path"),
            "inventory_status": repo.get("inventory_status"),
            "validator_ok": repo.get("validator_ok"),
            "pressure_severity": severity_for_repo(repo),
            "pressure_counts": repo.get("pressure_counts", {}),
            "route_key": route_key(repo),
            "route_action": route_action(repo),
            "owner_boundary": repo.get("owner_boundary", {}),
            "suite_execution": suite_execution_review_posture(repo),
        },
        "central_overlap": {
            "catalog_ref": "generated/eval_catalog.min.json",
            "exact_name_matches": exact,
            "adjacent_matches": adjacent,
            "summary": {
                "exact_count": len(exact),
                "adjacent_count": len(adjacent),
                "catalog_records_checked": len(records),
            },
        },
        "promotion_gates": gates,
        "gate_summary": dict(Counter(str(item["status"]) for item in gates)),
        "stage_boundaries": stage_boundaries(selected_repo_id),
        "recommended_next_route": recommended_next_route(repo, exact, adjacent),
        "promotion_allowed": False,
        "mcp_promotion_allowed": False,
        "stop_lines": [
            "MCP cannot promote local pressure into a central bundle",
            "candidate queue states cannot accept proof",
            "local reports remain local until owner review and central overlap review",
            "central draft is not accepted proof",
            "release artifact meaning requires catalog/report regeneration and release/advisory validation",
            "promotion review inspects suite state but never executes runner.argv",
            "source-contract-ready does not prove runtime reproducibility; owner/apply JIT-revalidates and captures environment plus receipt",
        ],
    }
    issues = validate_promotion_review_payload(payload)
    payload["valid"] = not issues
    payload["issues"] = issues
    payload["issue_count"] = len(issues)
    return payload


def iter_field_paths(value: Any, prefix: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield path, item
            yield from iter_field_paths(item, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            path = f"{prefix}[{index}]"
            yield from iter_field_paths(item, path)


def validate_promotion_review_payload(payload: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append({"code": "schema_version", "message": f"schema_version must be {SCHEMA_VERSION}"})
    if payload.get("promotion_allowed") is not False:
        issues.append({"code": "promotion_allowed", "message": "promotion review must keep promotion_allowed false"})
    if payload.get("mcp_promotion_allowed") is not False:
        issues.append({"code": "mcp_promotion_allowed", "message": "MCP promotion must stay forbidden"})

    gate_ids = [
        str(item.get("gate"))
        for item in payload.get("promotion_gates", [])
        if isinstance(item, dict)
    ]
    if gate_ids != PROMOTION_GATES:
        issues.append({"code": "promotion_gates", "message": "promotion gates must match the local-to-central review sequence"})

    for path, value in iter_field_paths(payload):
        key = path.rsplit(".", 1)[-1]
        key = re.sub(r"\[\d+\]$", "", key)
        if key in FORBIDDEN_TRUE_FIELDS and value is not False:
            issues.append({"code": "forbidden_truthy_field", "message": f"{path} must be false"})
        if key in FORBIDDEN_ANY_FIELDS:
            issues.append({"code": "forbidden_proof_field", "message": f"{path} must not appear in a dry-run promotion review"})
    return issues


def build_review_payload_from_workspace(*, workspace_root: Path, repo_id: str = "") -> dict[str, Any]:
    inventory_payload = build_local_eval_port_inventory.build_inventory_payload(workspace_root)
    return build_promotion_review_payload(
        inventory_payload,
        load_central_catalog(),
        repo_id=repo_id,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# OS Abyss Eval Promotion Dry-Run Review",
        "",
        str(payload.get("authority_boundary", AUTHORITY_BOUNDARY)),
        "",
    ]
    if not payload.get("valid"):
        lines.extend(["## Issues", ""])
        for issue in payload.get("issues", []):
            lines.append(f"- {issue.get('code')}: {issue.get('message')}")
        return "\n".join(lines) + "\n"

    selected = payload["selected_repo"]
    overlap = payload["central_overlap"]["summary"]
    lines.extend(
        [
            "## Selected Local Pressure",
            "",
            f"- Repo: `{selected['repo_id']}`",
            f"- Status: `{selected['inventory_status']}` / `{selected['pressure_severity']}`",
            f"- Route: `{selected['route_key']}`",
            f"- Next: `{payload['recommended_next_route']}`",
            "",
            "## Central Overlap",
            "",
            f"- Exact matches: {overlap['exact_count']}",
            f"- Adjacent matches: {overlap['adjacent_count']}",
            f"- Catalog records checked: {overlap['catalog_records_checked']}",
            "",
            "## Gates",
            "",
        ]
    )
    for item in payload["promotion_gates"]:
        lines.append(
            f"- `{item['gate']}`: {item['status']} ({item['owner']}); next {item['required_next']}"
        )
    lines.extend(["", "## Stop Lines", ""])
    for line in payload["stop_lines"]:
        lines.append(f"- {line}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.review_payload:
        payload = read_json_mapping(Path(args.review_payload))
        issues = validate_promotion_review_payload(payload)
        payload["valid"] = not issues
        payload["issues"] = issues
        payload["issue_count"] = len(issues)
    else:
        payload = build_review_payload_from_workspace(
            workspace_root=Path(args.workspace_root),
            repo_id=args.repo_id,
        )

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(render_markdown(payload), end="")
    return 0 if payload.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
