#!/usr/bin/env python3
"""Route a live eval case through the OS Abyss Eval Forge design layer."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import jsonschema

import scaffold_eval_bundle as scaffold


REPO_ROOT = Path(__file__).resolve().parents[5]
ROOT_SCRIPTS = REPO_ROOT / "scripts"
if str(ROOT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(ROOT_SCRIPTS))

import build_local_eval_port_inventory as local_port_inventory


PART_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/config/eval-archetypes.json"
)
REGISTRY_SCHEMA_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/schemas/eval-archetype-registry.schema.json"
)
WORKSHEET_SCHEMA_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/schemas/eval-design-worksheet.schema.json"
)
SCHEMA_VERSION = "eval_forge_route_v1"
WORKSHEET_SCHEMA_VERSION = "eval_design_worksheet_v1"
AUTHORITY_BOUNDARY = (
    "Eval Forge routes case design only. It does not create source bundles, "
    "accept proof, score evidence, mint baselines, promote candidates, or mutate "
    "repo-local eval ports, and it never executes local suite runner argv."
)
FORBIDDEN_ACTIONS = [
    "central_proof_promotion",
    "verdict_acceptance",
    "score_or_baseline_creation",
    "repo_mutation",
    "mcp_created_bundle",
    "candidate_auto_acceptance",
    "local_suite_runner_execution",
]
CRITICAL_GATES = {
    "expected_route_clarity",
    "observed_break_or_origin_pressure",
    "consequence",
    "owner_surface",
    "repeatability_path",
}
WEAK_POINTER_WORDS = {"eval", "evals", "test", "tests", "landing", "done"}
GENERIC_WORDS = WEAK_POINTER_WORDS | {
    "case",
    "candidate",
    "need",
    "route",
    "thing",
    "stuff",
    "work",
}
ARCHETYPE_HINTS = {
    "trace_trajectory_eval": "trace-trajectory-eval",
    "trajectory_eval": "trace-trajectory-eval",
    "skill_trigger_design": "aoa-skills-trigger-eval",
    "trigger_design": "aoa-skills-trigger-eval",
    "human_review_rubric": "human-review-rubric",
    "runtime_smoke": "abyss-stack-runtime-mcp-smoke",
    "local_intake": "local-intake-pressure-packet",
    "central_draft": "central-proof-bundle-draft",
    "design": "human-review-rubric",
    "session_candidate": "trace-trajectory-eval",
}


@dataclass(frozen=True)
class NormalizedCase:
    input_kind: str
    case_id: str
    objective: str
    object_under_evaluation: str
    task_pressure: str
    expected_route: str
    observed_break: str
    first_failure: str
    consequence: str
    owner_refs: list[str]
    evidence_refs: list[str]
    source_refs: list[str]
    freshness_refs: list[str]
    privacy_boundary: str
    repeatability_path: list[str]
    success_criteria: list[str]
    failure_criteria: list[str]
    positive_cases: list[str]
    negative_cases: list[str]
    fixtures: list[str]
    runner_solver_tool_needs: list[str]
    calibration_needs: list[str]
    archetype_hint: str | None
    raw: dict[str, Any]
    proposal_path: str | None = None
    candidate_packet_path: str | None = None


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help="aoa-evals repo root.")
    parser.add_argument("--proposal", help="eval_need_v1 proposal JSON to route.")
    parser.add_argument("--candidate-packet", help="aoa-eval candidate packet JSON to route.")
    parser.add_argument("--local-port-repo", help="Repo id from local eval-port inventory to route.")
    parser.add_argument("--local-port-inventory", help="Optional local eval-port inventory JSON.")
    parser.add_argument("--workspace-root", default="/srv/AbyssOS")
    parser.add_argument("--write-worksheet", help="Optional path to write eval_design_worksheet_v1 JSON.")
    parser.add_argument("--force", action="store_true", help="Overwrite --write-worksheet if it exists.")

    parser.add_argument("--case-id", default="manual:eval-forge-case")
    parser.add_argument("--objective")
    parser.add_argument("--object-under-evaluation")
    parser.add_argument("--task-pressure")
    parser.add_argument("--expected-route")
    parser.add_argument("--observed-break")
    parser.add_argument("--first-failure")
    parser.add_argument("--consequence")
    parser.add_argument("--owner-ref", action="append", default=[])
    parser.add_argument("--evidence-ref", action="append", default=[])
    parser.add_argument("--source-ref", action="append", default=[])
    parser.add_argument("--freshness-ref", action="append", default=[])
    parser.add_argument("--privacy-boundary")
    parser.add_argument("--repeatability-path", action="append", default=[])
    parser.add_argument("--success-criterion", action="append", default=[])
    parser.add_argument("--failure-criterion", action="append", default=[])
    parser.add_argument("--positive-case", action="append", default=[])
    parser.add_argument("--negative-case", action="append", default=[])
    parser.add_argument("--fixture", action="append", default=[])
    parser.add_argument("--runner-need", action="append", default=[])
    parser.add_argument("--calibration-need", action="append", default=[])
    parser.add_argument("--archetype-hint")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def resolve_path(path_value: str, *, base: Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else base / path


def repo_surface_path(repo_root: Path, relative: Path) -> Path:
    candidate = repo_root / relative
    return candidate if candidate.exists() else REPO_ROOT / relative


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise scaffold.ScaffoldError(f"{path}: invalid JSON: {exc}") from exc


def validate_json(payload: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    messages: list[str] = []
    for error in sorted(validator.iter_errors(payload), key=lambda item: list(item.absolute_path)):
        location = ".".join(str(part) for part in error.absolute_path)
        messages.append(f"{location}: {error.message}" if location else error.message)
    return messages


def load_registry(repo_root: Path) -> tuple[dict[str, Any], list[str]]:
    registry_path = repo_surface_path(repo_root, REGISTRY_RELATIVE)
    schema_path = repo_surface_path(repo_root, REGISTRY_SCHEMA_RELATIVE)
    registry = load_json(registry_path)
    errors = validate_json(registry, schema_path)
    if not isinstance(registry, dict):
        raise scaffold.ScaffoldError("eval forge archetype registry must be a JSON object")
    return registry, errors


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def first_text(*values: Any, fallback: str = "") -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def normalize_archetype_hint(value: str | None) -> str | None:
    if not value:
        return None
    normalized = value.strip()
    if normalized in ARCHETYPE_HINTS:
        return ARCHETYPE_HINTS[normalized]
    normalized = normalized.replace("_", "-")
    return normalized if normalized else None


def proposal_case(payload: dict[str, Any], *, proposal_path: str | None) -> NormalizedCase:
    source_refs = as_list(payload.get("source_refs"))
    evidence_refs = [
        *as_list(payload.get("candidate_evidence_refs")),
        *as_list(payload.get("quest_refs")),
        *source_refs,
    ]
    return NormalizedCase(
        input_kind="eval_need_v1",
        case_id=str(payload.get("name") or "proposal:unknown"),
        objective=str(payload.get("proof_question") or ""),
        object_under_evaluation=str(payload.get("object_under_evaluation") or ""),
        task_pressure=str(payload.get("origin_need") or ""),
        expected_route=str(payload.get("authoring_route") or ""),
        observed_break=str(payload.get("origin_need") or ""),
        first_failure=str(payload.get("origin_need") or ""),
        consequence=str(payload.get("summary") or ""),
        owner_refs=source_refs,
        evidence_refs=evidence_refs,
        source_refs=source_refs,
        freshness_refs=[],
        privacy_boundary="proposal contains source refs only; no raw private evidence is accepted as proof",
        repeatability_path=as_list(payload.get("expected_use_when")),
        success_criteria=[str(payload.get("proof_question") or "review the bounded proof question")],
        failure_criteria=as_list(payload.get("blind_spot_notes"))
        or ["the case widens past its named blind spots"],
        positive_cases=as_list(payload.get("expected_use_when"))
        or ["a bounded case matching the proposal trigger"],
        negative_cases=as_list(payload.get("blind_spot_notes"))
        or ["a broader case outside the proposal trigger"],
        fixtures=source_refs or ["source refs still need review"],
        runner_solver_tool_needs=["scaffold dry-run", "owner review"],
        calibration_needs=["human owner acceptance before source bundle write"],
        archetype_hint=infer_proposal_hint(payload),
        raw=payload,
        proposal_path=proposal_path,
    )


def infer_proposal_hint(payload: dict[str, Any]) -> str:
    baseline_mode = str(payload.get("baseline_mode") or "none")
    claim_type = str(payload.get("claim_type") or "")
    authoring_route = str(payload.get("authoring_route") or "")
    if baseline_mode == "longitudinal-window" or claim_type == "longitudinal":
        return "longitudinal-window-eval"
    if baseline_mode != "none" or claim_type in {"comparative", "regression"}:
        return "comparison-fixed-baseline-eval"
    if authoring_route == "candidate_evidence_packet":
        return "trace-trajectory-eval"
    if authoring_route == "new_draft_bundle":
        return "central-proof-bundle-draft"
    if authoring_route == "quest_record":
        return "human-review-rubric"
    return "central-proof-bundle-draft"


def candidate_packet_case(payload: dict[str, Any], *, packet_path: str | None) -> NormalizedCase:
    owner_refs = as_list(payload.get("owner_surface_refs"))
    evidence_refs = [str(payload.get("source_ref") or ""), *as_list(payload.get("evidence_refs"))]
    evidence_refs = [item for item in evidence_refs if item]
    evaluator_fit = first_text(payload.get("evaluator_fit"), payload.get("expected_aoa_eval_route"))
    return NormalizedCase(
        input_kind="candidate_packet",
        case_id=str(payload.get("packet_id") or "packet:unknown"),
        objective=first_text(
            payload.get("task_pressure"),
            payload.get("expected_aoa_eval_route"),
            fallback="route candidate evidence before eval design",
        ),
        object_under_evaluation=first_text(
            payload.get("trigger_class_id"),
            payload.get("packet_id"),
            fallback="session candidate route",
        ),
        task_pressure=str(payload.get("task_pressure") or ""),
        expected_route=first_text(payload.get("expected_route"), payload.get("expected_aoa_eval_route")),
        observed_break=first_text(payload.get("actual_trajectory"), payload.get("actual_route")),
        first_failure=str(payload.get("first_failure") or ""),
        consequence=str(payload.get("consequence") or ""),
        owner_refs=owner_refs,
        evidence_refs=evidence_refs,
        source_refs=evidence_refs,
        freshness_refs=as_list(payload.get("freshness_refs")),
        privacy_boundary=first_text(
            payload.get("privacy_boundary"),
            fallback="candidate packet stores refs only; raw evidence remains with the source owner",
        ),
        repeatability_path=[
            *as_list(payload.get("next_step")),
            *as_list(payload.get("promotion_forbidden_until")),
            evaluator_fit,
        ],
        success_criteria=as_list(payload.get("success_criteria")),
        failure_criteria=as_list(payload.get("failure_criteria")),
        positive_cases=as_list(payload.get("positive_cases")),
        negative_cases=as_list(payload.get("negative_cases")),
        fixtures=evidence_refs or ["bounded evidence refs still need owner review"],
        runner_solver_tool_needs=["candidate packet validator", "owner review"],
        calibration_needs=as_list(payload.get("promotion_forbidden_until")),
        archetype_hint=normalize_archetype_hint(evaluator_fit),
        raw=payload,
        candidate_packet_path=packet_path,
    )


def manual_case(args: argparse.Namespace) -> NormalizedCase:
    return NormalizedCase(
        input_kind="manual_fields",
        case_id=args.case_id,
        objective=args.objective or args.task_pressure or "",
        object_under_evaluation=args.object_under_evaluation or "",
        task_pressure=args.task_pressure or "",
        expected_route=args.expected_route or "",
        observed_break=args.observed_break or "",
        first_failure=args.first_failure or args.observed_break or "",
        consequence=args.consequence or "",
        owner_refs=list(args.owner_ref),
        evidence_refs=list(args.evidence_ref),
        source_refs=list(args.source_ref),
        freshness_refs=list(args.freshness_ref),
        privacy_boundary=args.privacy_boundary or "",
        repeatability_path=list(args.repeatability_path),
        success_criteria=list(args.success_criterion),
        failure_criteria=list(args.failure_criterion),
        positive_cases=list(args.positive_case),
        negative_cases=list(args.negative_case),
        fixtures=list(args.fixture),
        runner_solver_tool_needs=list(args.runner_need),
        calibration_needs=list(args.calibration_need),
        archetype_hint=normalize_archetype_hint(args.archetype_hint),
        raw={},
    )


def local_port_case(
    repo_id: str,
    *,
    repo_root: Path,
    workspace_root: Path,
    inventory_path: str | None,
) -> NormalizedCase:
    inventory = load_local_port_inventory(repo_root, workspace_root, inventory_path)
    repos = inventory.get("repos", []) if isinstance(inventory, dict) else []
    selected = None
    for item in repos:
        if isinstance(item, dict) and item.get("repo_id") == repo_id:
            selected = item
            break
    if selected is None:
        raise scaffold.ScaffoldError(f"local eval port repo not found in inventory: {repo_id}")
    counts = selected.get("pressure_counts") if isinstance(selected.get("pressure_counts"), dict) else {}
    suite_execution = (
        selected.get("suite_execution")
        if isinstance(selected.get("suite_execution"), dict)
        else {"state": "absent", "suites": []}
    )
    route = selected.get("route_recommendation") if isinstance(selected.get("route_recommendation"), dict) else {}
    owner = selected.get("owner_boundary") if isinstance(selected.get("owner_boundary"), dict) else {}
    pressure_summary = (
        f"local port status={selected.get('inventory_status')} active_total={counts.get('active_total')} "
        f"intake={counts.get('intake_packets')} suite_notes={counts.get('suite_notes')} "
        f"suite_execution={suite_execution.get('state')} reports={counts.get('report_notes')}"
    )
    root = str(selected.get("root") or "")
    port_path = str(selected.get("port_path") or "evals/PORT.yaml")
    hint = (
        "local-runnable-suite"
        if suite_execution.get("state") == "ready"
        else "local-intake-pressure-packet"
    )
    suite_refs = [
        str(item.get("path"))
        for item in suite_execution.get("suites", [])
        if isinstance(item, dict) and item.get("path")
    ]
    return NormalizedCase(
        input_kind="local_eval_port",
        case_id=f"local-port:{repo_id}",
        objective=f"Route repo-local eval pressure for {repo_id}",
        object_under_evaluation=f"{repo_id} local eval port",
        task_pressure=pressure_summary,
        expected_route=str(route.get("action") or route.get("route_key") or ""),
        observed_break=pressure_summary,
        first_failure="local eval pressure needs owner review before central adoption",
        consequence="local pressure can drift, duplicate central evals, or be over-promoted without route review",
        owner_refs=[f"{root}/{port_path}" if root else port_path, str(owner.get("owner_repo") or repo_id)],
        evidence_refs=[f"{root}/{port_path}" if root else port_path, *suite_refs],
        source_refs=[f"{root}/{port_path}" if root else port_path, *suite_refs],
        freshness_refs=[
            f"inventory_status:{selected.get('inventory_status')}",
            f"suite_execution_state:{suite_execution.get('state')}",
        ],
        privacy_boundary="repo-local port inventory contains route pressure only, not central proof",
        repeatability_path=[str(route.get("route_key") or ""), str(route.get("proof_boundary") or "")],
        success_criteria=["repo owner reviews local pressure before central overlap or suite application"],
        failure_criteria=["local pressure is treated as central proof, score, or verdict"],
        positive_cases=["active local port pressure with owner route and central boundary"],
        negative_cases=["dormant skeleton port with no active pressure"],
        fixtures=[port_path],
        runner_solver_tool_needs=[
            "local port inventory and validator inspect only; they never execute runner argv",
            "repo owner or aoa-eval-apply JIT-revalidates and invokes typed exact argv only when suite state is source-contract-ready",
            "owner/apply captures environment metadata and an execution receipt; ready is not runtime reproducibility",
        ],
        calibration_needs=["repo-local owner review"],
        archetype_hint=hint,
        raw=selected,
    )


def load_local_port_inventory(
    repo_root: Path,
    workspace_root: Path,
    inventory_path: str | None,
) -> dict[str, Any]:
    if inventory_path:
        payload = load_json(resolve_path(inventory_path, base=Path.cwd()))
        if isinstance(payload, dict):
            return local_port_inventory.normalize_inventory_for_suite_consumers(payload)
        raise scaffold.ScaffoldError(f"{inventory_path}: local port inventory must be an object")
    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_local_eval_port_inventory.py",
            "--workspace-root",
            workspace_root.as_posix(),
            "--json",
        ],
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise scaffold.ScaffoldError(
            "local port inventory command failed: " + (result.stderr.strip() or result.stdout.strip())
        )
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict):
        raise scaffold.ScaffoldError("local port inventory command returned non-object JSON")
    return local_port_inventory.normalize_inventory_for_suite_consumers(payload)


def text_for(case: NormalizedCase) -> str:
    values = [
        case.case_id,
        case.objective,
        case.object_under_evaluation,
        case.task_pressure,
        case.expected_route,
        case.observed_break,
        case.first_failure,
        case.consequence,
        case.archetype_hint or "",
        " ".join(case.owner_refs),
        " ".join(case.evidence_refs),
        " ".join(case.repeatability_path),
    ]
    return " ".join(values).lower()


def token_set(text: str) -> set[str]:
    return {
        token
        for token in "".join(ch if ch.isalnum() else " " for ch in text.lower()).split()
        if len(token) >= 3
    }


def gate_results(case: NormalizedCase, duplicate_reviewed: bool) -> list[dict[str, Any]]:
    gates = [
        (
            "evidence_boundedness",
            bool(case.evidence_refs or case.source_refs),
            "source/evidence refs point at a bounded span, file, command, or packet",
        ),
        (
            "expected_route_clarity",
            len(case.expected_route.strip()) >= 5,
            "expected route can be named without inventing doctrine",
        ),
        (
            "observed_break_or_origin_pressure",
            len(case.observed_break.strip()) >= 5 or len(case.task_pressure.strip()) >= 8,
            "observed break or origin pressure is explicit",
        ),
        (
            "first_failure_clarity",
            len(case.first_failure.strip()) >= 5,
            "first meaningful failure is named separately from downstream noise",
        ),
        (
            "consequence",
            len(case.consequence.strip()) >= 5,
            "consequence matters for correctness, proof, safety, freshness, cost, trust, or OS growth",
        ),
        (
            "owner_surface",
            bool(case.owner_refs),
            "owner source surface or runtime owner can judge the expected route",
        ),
        (
            "repeatability_path",
            bool([item for item in case.repeatability_path if item.strip()]),
            "future check route is plausible",
        ),
        (
            "duplicate_check",
            duplicate_reviewed,
            "central catalog duplicate check was performed or marked unavailable",
        ),
        (
            "privacy_freshness",
            bool(case.privacy_boundary or case.freshness_refs),
            "privacy and freshness posture is explicit enough for next route",
        ),
    ]
    return [
        {"gate": name, "passed": passed, "condition": condition}
        for name, passed, condition in gates
    ]


def is_keyword_only(case: NormalizedCase, gates: list[dict[str, Any]]) -> bool:
    critical_passes = {
        item["gate"]
        for item in gates
        if item["passed"] and item["gate"] in CRITICAL_GATES
    }
    if critical_passes:
        return False
    tokens = token_set(
        " ".join(
            [
                case.objective,
                case.object_under_evaluation,
                case.task_pressure,
                case.expected_route,
                case.observed_break,
                case.first_failure,
                case.consequence,
                case.archetype_hint or "",
            ]
        )
    )
    return bool(tokens & WEAK_POINTER_WORDS) and not bool(tokens - GENERIC_WORDS)


def load_catalog_matches(case: NormalizedCase, repo_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if case.input_kind != "eval_need_v1":
        return [], []
    proposal = case.raw
    entries, warnings = scaffold.load_catalog(repo_root)
    return scaffold.find_existing_matches(proposal, entries), warnings


def rank_archetypes(
    case: NormalizedCase,
    registry: dict[str, Any],
    existing_matches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    text = text_for(case)
    tokens = token_set(text)
    ranked: list[dict[str, Any]] = []
    hint = normalize_archetype_hint(case.archetype_hint)
    for archetype in registry["archetypes"]:
        score = 0
        reasons: list[str] = []
        if hint and hint == archetype["id"]:
            score += 50
            reasons.append("explicit archetype hint")
        for signal in archetype["signals"]:
            signal_text = str(signal).lower()
            signal_tokens = token_set(signal_text)
            if signal_text in text or signal_tokens & tokens:
                score += 7
                reasons.append(f"signal:{signal}")
        route_kind = archetype["route_kind"]
        if case.input_kind == "local_eval_port" and route_kind in {"local-intake", "local-suite"}:
            score += 35
            reasons.append("local eval port pressure")
        if case.input_kind == "candidate_packet" and route_kind in {"trajectory", "human-rubric", "skill-trigger"}:
            score += 14
            reasons.append("candidate packet evidence")
        if existing_matches and route_kind in {"central-proof", "boundary"}:
            score += 8
            reasons.append("central match review needed")
        if "mcp" in tokens and route_kind in {"freshness", "runtime-smoke", "boundary"}:
            score += 12
            reasons.append("MCP/runtime signal")
        if "proof" in tokens and route_kind in {"boundary", "central-proof"}:
            score += 10
            reasons.append("proof authority signal")
        if score == 0:
            continue
        ranked.append(
            {
                "archetype_id": archetype["id"],
                "label": archetype["label"],
                "route_kind": route_kind,
                "score": score,
                "reasons": reasons[:8],
                "local_vs_central_route": archetype["local_vs_central_route"],
                "grader_family": archetype["grader_family"],
                "validation_route": archetype["validation_route"],
            }
        )
    if not ranked:
        fallback = next(item for item in registry["archetypes"] if item["id"] == "human-review-rubric")
        ranked.append(
            {
                "archetype_id": fallback["id"],
                "label": fallback["label"],
                "route_kind": fallback["route_kind"],
                "score": 1,
                "reasons": ["fallback until stronger criteria exist"],
                "local_vs_central_route": fallback["local_vs_central_route"],
                "grader_family": fallback["grader_family"],
                "validation_route": fallback["validation_route"],
            }
        )
    return sorted(ranked, key=lambda item: (-int(item["score"]), str(item["archetype_id"])))


def decision_for(
    case: NormalizedCase,
    gates: list[dict[str, Any]],
    existing_matches: list[dict[str, Any]],
    registry_errors: list[str],
) -> dict[str, Any]:
    missing = [item["gate"] for item in gates if not item["passed"]]
    failed_critical = [gate for gate in missing if gate in CRITICAL_GATES]
    if registry_errors:
        return {
            "decision": "defer",
            "reason": "forge registry validation must pass before routing cases",
            "missing_evidence": registry_errors,
        }
    if is_keyword_only(case, gates):
        return {
            "decision": "reject",
            "reason": "keyword-only pointer has no route break, owner, consequence, or repeatability",
            "missing_evidence": failed_critical or missing,
        }
    exact_matches = [match for match in existing_matches if match.get("name") == case.case_id]
    if exact_matches:
        return {
            "decision": "duplicate",
            "reason": "same central eval name already exists; inspect existing source eval before authoring",
            "missing_evidence": [],
        }
    if existing_matches:
        return {
            "decision": "duplicate",
            "reason": "adjacent central eval route exists; inspect likely matches before parallel design",
            "missing_evidence": [],
        }
    if failed_critical:
        return {
            "decision": "defer",
            "reason": "case lacks critical admission gates for eval design",
            "missing_evidence": failed_critical,
        }
    if missing:
        return {
            "decision": "keep",
            "reason": "core gates pass, but worksheet must carry missing design evidence",
            "missing_evidence": missing,
        }
    return {
        "decision": "keep",
        "reason": "case passes forge admission gates and can move to owner review worksheet",
        "missing_evidence": [],
    }


def evaluator_mode_for(archetype: dict[str, Any]) -> str:
    route_kind = archetype["route_kind"]
    if route_kind in {"validator", "test", "property", "tool", "state", "freshness", "runtime-smoke"}:
        return "deterministic"
    if route_kind == "llm-judge":
        return "llm_judge"
    if route_kind == "human-rubric":
        return "human_review"
    return "mixed"


def next_command_for(
    case: NormalizedCase,
    decision: dict[str, Any],
    selected: dict[str, Any],
) -> str:
    if case.proposal_path:
        return (
            "python mechanics/proof-object/parts/eval-authoring/scripts/scaffold_eval_bundle.py "
            f"--proposal {case.proposal_path} --json"
        )
    if case.candidate_packet_path:
        return (
            "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
            f"--candidate-packet {case.candidate_packet_path} --json"
        )
    if case.input_kind == "local_eval_port":
        suite_execution = case.raw.get("suite_execution") if isinstance(case.raw, dict) else None
        if isinstance(suite_execution, dict) and suite_execution.get("state") == "ready":
            return (
                "route to repo owner or aoa-eval-apply; JIT-revalidate the "
                "source-contract-ready suite, invoke typed runner.argv exactly, "
                "and capture environment plus execution receipt"
            )
        return "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json"
    if decision["decision"] == "reject":
        return "record reject reason; do not create intake, worksheet, suite, or central bundle"
    return f"prepare eval design worksheet for `{selected['archetype_id']}` and request owner review"


def scaffold_posture_for(
    case: NormalizedCase,
    decision: dict[str, Any],
    selected: dict[str, Any],
) -> dict[str, Any]:
    if decision["decision"] == "reject":
        return {"status": "blocked", "reason": "rejected cases must not scaffold"}
    if decision["decision"] == "defer":
        return {"status": "premature", "reason": "critical admission evidence is missing"}
    if decision["decision"] == "duplicate":
        return {"status": "blocked", "reason": "existing route must be inspected first"}
    if selected["archetype_id"] == "central-proof-bundle-draft" and case.input_kind == "eval_need_v1":
        return {
            "status": "dry_run_only",
            "reason": "central scaffold may be dry-run after review; --write still requires human acceptance",
            "write_allowed": False,
        }
    return {
        "status": "not_applicable",
        "reason": "selected archetype routes to local, runtime, trigger, validator, or review surface before central scaffold",
        "write_allowed": False,
    }


def fill_required(values: list[str], fallback: str) -> list[str]:
    return values if values else [fallback]


def worksheet_for(
    case: NormalizedCase,
    selected_archetype: dict[str, Any],
    decision: dict[str, Any],
    next_command: str,
) -> dict[str, Any]:
    route = selected_archetype["local_vs_central_route"]
    return {
        "schema_version": WORKSHEET_SCHEMA_VERSION,
        "objective": first_text(case.objective, case.task_pressure, fallback="route eval pressure"),
        "object_under_evaluation": first_text(case.object_under_evaluation, fallback=case.case_id),
        "task_pressure": first_text(case.task_pressure, fallback=case.objective),
        "expected_route": first_text(case.expected_route, fallback="owner review before eval authoring"),
        "observed_break": first_text(case.observed_break, fallback=case.task_pressure),
        "first_failure": first_text(case.first_failure, fallback="first failure still needs owner review"),
        "consequence": first_text(case.consequence, fallback="missing consequence must be resolved before promotion"),
        "owner_refs": fill_required(case.owner_refs, "owner refs still need review"),
        "source_refs": case.source_refs or case.evidence_refs,
        "freshness_refs": case.freshness_refs,
        "privacy_boundary": first_text(
            case.privacy_boundary,
            fallback="raw/private evidence must stay with the owning source until review",
        ),
        "selected_archetype_id": selected_archetype["archetype_id"],
        "success_criteria": fill_required(
            case.success_criteria,
            f"owner can confirm the {selected_archetype['label']} route applies",
        ),
        "failure_criteria": fill_required(
            case.failure_criteria,
            "case lacks owner route, consequence, repeatability, or calibrated criteria",
        ),
        "positive_cases": fill_required(case.positive_cases, "one bounded passing case still needs review"),
        "negative_cases": fill_required(case.negative_cases, "one reject/defer case still needs review"),
        "fixtures": case.fixtures,
        "runner_solver_tool_needs": case.runner_solver_tool_needs,
        "grader_family": selected_archetype["grader_family"],
        "evaluator_mode": evaluator_mode_for(selected_archetype),
        "calibration_needs": case.calibration_needs,
        "repeat_count": 1,
        "nondeterminism_posture": "Start with one reviewed route case; add repeat runs only after the fixture and grader are stable.",
        "state_change_verification": "State changes must be verified only when the selected archetype mutates or inspects live state.",
        "anti_gaming_risks": [
            "selected archetype is overfit to this one case",
            "candidate evidence is promoted before owner review",
            "final text is graded while trajectory or state is the real claim",
        ],
        "maintenance_drift_risk": "Re-run forge route when source owner docs, local ports, runtime status, or external eval patterns drift.",
        "local_central_promotion_route": (
            f"{route['target']} via {route['owner_repo']} / {route['route_key']}; "
            "candidate-only until owner review"
        ),
        "exact_next_command": next_command,
        "proof_authority": False,
        "promotion_allowed": False,
    }


def write_worksheet(path: Path, worksheet: dict[str, Any], *, force: bool) -> dict[str, Any]:
    if path.exists() and not force:
        return {
            "status": "blocked",
            "path": path.as_posix(),
            "reason": "target exists; pass --force to overwrite",
        }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(worksheet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": "written", "path": path.as_posix()}


def build_forge_route(
    *,
    case: NormalizedCase,
    repo_root: Path,
    write_worksheet_path: str | None = None,
    force: bool = False,
) -> dict[str, Any]:
    registry, registry_errors = load_registry(repo_root)
    existing_matches, catalog_warnings = load_catalog_matches(case, repo_root)
    gates = gate_results(case, duplicate_reviewed=True)
    decision = decision_for(case, gates, existing_matches, registry_errors)
    ranked = rank_archetypes(case, registry, existing_matches)
    selected = ranked[0]
    next_command = next_command_for(case, decision, selected)
    worksheet = worksheet_for(case, selected, decision, next_command)
    worksheet_schema = repo_surface_path(repo_root, WORKSHEET_SCHEMA_RELATIVE)
    worksheet_errors = validate_json(worksheet, worksheet_schema)
    worksheet_write = {"status": "not_requested"}
    if write_worksheet_path:
        if decision["decision"] == "reject":
            worksheet_write = {
                "status": "blocked",
                "reason": "rejected cases do not get design worksheets",
            }
        elif worksheet_errors:
            worksheet_write = {
                "status": "blocked",
                "reason": "worksheet schema validation failed",
            }
        else:
            worksheet_write = write_worksheet(
                resolve_path(write_worksheet_path, base=repo_root),
                worksheet,
                force=force,
            )
    local_suite_execution = local_suite_execution_posture(case)
    return {
        "schema_version": SCHEMA_VERSION,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "input_kind": case.input_kind,
        "case_id": case.case_id,
        "candidate_admissibility": {
            **decision,
            "gates": gates,
        },
        "existing_surface_check": {
            "catalog_checked": True,
            "warnings": catalog_warnings,
            "matches": existing_matches,
        },
        "archetype_ranking": ranked[:8],
        "selected_archetype_id": selected["archetype_id"],
        "owner_route": {
            "owner_repo": selected["local_vs_central_route"]["owner_repo"],
            "local_or_central_target": selected["local_vs_central_route"]["target"],
            "route_key": selected["local_vs_central_route"]["route_key"],
            "recommended_next_command": next_command,
            "proof_boundary": "candidate/readmodel/local pressure remains non-proof until owner review",
        },
        "local_suite_execution": local_suite_execution,
        "scaffold_posture": scaffold_posture_for(case, decision, selected),
        "worksheet": worksheet,
        "worksheet_validation": {
            "valid": not worksheet_errors,
            "errors": worksheet_errors,
        },
        "worksheet_write": worksheet_write,
        "forbidden_actions": FORBIDDEN_ACTIONS,
        "registry_validation": {
            "valid": not registry_errors,
            "errors": registry_errors,
            "archetype_count": len(registry.get("archetypes", [])),
        },
        "stop_lines": [
            "do not scaffold central bundles before duplicate and owner review",
            "do not treat candidate packets, local ports, MCP packets, or generated dashboards as proof",
            "do not use LLM judge routes without human rubric calibration",
            "do not fossilize one temporary workflow accident as durable eval doctrine",
            "Eval Forge and inventory inspect local suite sidecars but never execute runner.argv",
        ],
    }


def local_suite_execution_posture(case: NormalizedCase) -> dict[str, Any]:
    if case.input_kind != "local_eval_port" or not isinstance(case.raw, dict):
        return {
            "state": "not_applicable",
            "readiness_scope": "source-contract-ready",
            "runtime_reproducibility_proven": False,
            "execution_allowed": False,
            "owner_apply_required": False,
            "proof_authority": False,
            "promotion_allowed": False,
        }
    execution = case.raw.get("suite_execution")
    if not isinstance(execution, dict):
        execution = {"state": "absent", "suites": []}
    suites = execution.get("suites") if isinstance(execution.get("suites"), list) else []
    ready_suites = [
        {
            "path": item.get("path"),
            "suite_id": item.get("suite_id"),
            "runner": item.get("runner"),
            "entrypoint_ref": item.get("entrypoint_ref"),
            "entrypoint_arg": item.get("entrypoint_arg"),
            "timeout_seconds": item.get("timeout_seconds"),
            "success_exit_codes": item.get("success_exit_codes"),
        }
        for item in suites
        if isinstance(item, dict) and item.get("state") == "ready"
    ]
    state = str(execution.get("state") or "absent")
    return {
        "state": state,
        "suite_count": int(execution.get("suite_count") or len(suites)),
        "ready_count": int(execution.get("ready_count") or len(ready_suites)),
        "ready_suites": ready_suites,
        "readiness_scope": str(execution.get("readiness_scope") or "source-contract-ready"),
        "runtime_reproducibility_proven": False,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "execution_allowed": False,
        "owner_apply_required": state == "ready",
        "inventory_executed_runner": False,
        "proof_authority": False,
        "promotion_allowed": False,
        "boundary": (
            "Eval Forge only routes validated suite metadata; the selected repo "
            "owner or aoa-eval-apply is the sole invocation route. Ready means "
            "source-contract-ready, not a pinned or reproducible runtime."
        ),
    }


def case_from_args(args: argparse.Namespace, repo_root: Path) -> NormalizedCase:
    selected_inputs = [bool(args.proposal), bool(args.candidate_packet), bool(args.local_port_repo)]
    if sum(selected_inputs) > 1:
        raise scaffold.ScaffoldError("choose only one of --proposal, --candidate-packet, or --local-port-repo")
    if args.proposal:
        path = resolve_path(args.proposal, base=Path.cwd())
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise scaffold.ScaffoldError(f"{path}: proposal must be a JSON object")
        return proposal_case(payload, proposal_path=path.as_posix())
    if args.candidate_packet:
        path = resolve_path(args.candidate_packet, base=Path.cwd())
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise scaffold.ScaffoldError(f"{path}: candidate packet must be a JSON object")
        return candidate_packet_case(payload, packet_path=path.as_posix())
    if args.local_port_repo:
        return local_port_case(
            args.local_port_repo,
            repo_root=repo_root,
            workspace_root=Path(args.workspace_root),
            inventory_path=args.local_port_inventory,
        )
    return manual_case(args)


def render_text(payload: dict[str, Any]) -> str:
    admissibility = payload["candidate_admissibility"]
    owner_route = payload["owner_route"]
    lines = [
        "# Eval Forge Route",
        "",
        payload["authority_boundary"],
        "",
        f"- case: `{payload['case_id']}`",
        f"- decision: `{admissibility['decision']}`",
        f"- reason: {admissibility['reason']}",
        f"- selected archetype: `{payload['selected_archetype_id']}`",
        f"- owner route: `{owner_route['owner_repo']}` / `{owner_route['route_key']}`",
        f"- target: `{owner_route['local_or_central_target']}`",
        f"- next command: `{owner_route['recommended_next_command']}`",
        f"- scaffold posture: `{payload['scaffold_posture']['status']}`",
        "",
        "## Missing Evidence",
    ]
    missing = admissibility.get("missing_evidence") or []
    if not missing:
        lines.append("- none")
    else:
        for item in missing:
            lines.append(f"- {item}")
    lines.extend(["", "## Top Archetypes"])
    for item in payload["archetype_ranking"][:5]:
        lines.append(
            f"- `{item['archetype_id']}` score={item['score']} route={item['local_vs_central_route']['route_key']}"
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    try:
        case = case_from_args(args, repo_root)
        payload = build_forge_route(
            case=case,
            repo_root=repo_root,
            write_worksheet_path=args.write_worksheet,
            force=args.force,
        )
    except (scaffold.ScaffoldError, jsonschema.ValidationError) as exc:
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
    if payload.get("errors"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
