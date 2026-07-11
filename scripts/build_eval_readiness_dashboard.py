#!/usr/bin/env python3
"""Build the OS Abyss eval-readiness read-model."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import build_local_eval_port_inventory


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE_ROOT = Path("/srv/AbyssOS")
DEFAULT_AOA_ROOT = Path("/srv/AbyssOS/.aoa")
DEFAULT_SKILLS_SOURCE_ROOT = Path("/srv/AbyssOS/aoa-skills")
DEFAULT_INSTALLED_SKILLS_ROOT = Path.home() / ".codex" / "skills"
DEFAULT_AOA_EVAL_INSTALL_PROFILE = "user-aoa-foundation"
DEFAULT_STACK_ROOT_CANDIDATES = (
    Path("/home/dionysus/src/abyss-stack"),
    Path("/srv/AbyssOS/abyss-stack"),
)
SCHEMA_VERSION = "os_abyss_eval_readiness_dashboard_v1"
SUPPORT_REGISTRY_SCHEMA_VERSION = "os_abyss_eval_support_registry_v1"
DASHBOARD_JSON = REPO_ROOT / "generated" / "eval_readiness_dashboard.json"
DASHBOARD_MARKDOWN = REPO_ROOT / "generated" / "eval_readiness_dashboard.md"
SUPPORT_REGISTRY_JSON = REPO_ROOT / "generated" / "eval_support_registry.json"
CANDIDATE_PACKET_RELATIVE = Path("mechanics/audit/parts/candidate-readers/packets")
SESSION_MINING_REPORT_RELATIVE = Path("mechanics/audit/parts/candidate-readers/reports/session-mining")
EVAL_FORGE_SCRIPT_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py"
)
EVAL_FORGE_REGISTRY_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/config/eval-archetypes.json"
)
EVAL_FORGE_EXTERNAL_GROUNDING_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/config/external-pattern-grounding.json"
)
EVAL_FORGE_WORKSHEET_SCHEMA_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/schemas/eval-design-worksheet.schema.json"
)
LOCAL_SUITE_EXECUTION_SCHEMA_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/schemas/"
    "local-eval-suite-execution.schema.json"
)
EVAL_FORGE_OPERATING_PATH_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md"
)
EVAL_FORGE_SESSION_MINING_CRITERIA_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md"
)
EVAL_FORGE_LOCAL_PORT_MATRIX_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md"
)
EVAL_FORGE_WORKSHEET_EXAMPLE_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/examples/"
    "aoa_eval_criteria_before_mining.eval_design_worksheet.example.json"
)
EVAL_FORGE_ROUTE_REVIEW_REPORT_RELATIVE = Path(
    "mechanics/proof-object/parts/eval-authoring/reports/eval-forge/"
    "2026-06-26-session-candidate-owner-review.md"
)
MANUAL_SESSION_MINING_REPORT = (
    SESSION_MINING_REPORT_RELATIVE / "2026-06-25-aoa-eval-control.manual-review.md"
)
AUTHORITY_BOUNDARY = (
    "This generated read-model routes OS Abyss eval pressure. It is not a verdict, "
    "score, baseline, regression, receipt, or central proof acceptance surface."
)
SOURCE_OF_TRUTH = {
    "proof_topology": "docs/architecture/PROOF_TOPOLOGY.md",
    "local_eval_port_standard": "docs/guides/LOCAL_EVAL_PORT_STANDARD.md",
    "mcp_contract": "docs/architecture/AOA_EVALS_MCP_CONTRACT.md",
    "eval_catalog": "generated/eval_catalog.json",
    "local_eval_port_inventory_builder": "scripts/build_local_eval_port_inventory.py",
    "validation_inventory": "docs/validation/validator_inventory.json",
    "script_inventory": "docs/validation/script_inventory.json",
    "test_inventory": "docs/testing/test_inventory.json",
    "eval_candidate_packet_schema": (
        "mechanics/audit/parts/candidate-readers/schemas/aoa-eval-candidate-packet.schema.json"
    ),
    "eval_candidate_packet_root": CANDIDATE_PACKET_RELATIVE.as_posix(),
    "eval_candidate_queue_lifecycle": "scripts/check_eval_candidate_queue_lifecycle.py",
    "eval_forge_router": EVAL_FORGE_SCRIPT_RELATIVE.as_posix(),
    "eval_forge_readiness_guide": "docs/guides/EVAL_FORGE_READINESS_LAYER.md",
    "eval_forge_readiness_check": "scripts/check_eval_forge_readiness.py",
    "eval_forge_archetype_registry": EVAL_FORGE_REGISTRY_RELATIVE.as_posix(),
    "eval_forge_external_pattern_grounding": EVAL_FORGE_EXTERNAL_GROUNDING_RELATIVE.as_posix(),
    "eval_forge_worksheet_schema": EVAL_FORGE_WORKSHEET_SCHEMA_RELATIVE.as_posix(),
    "local_suite_execution_schema": LOCAL_SUITE_EXECUTION_SCHEMA_RELATIVE.as_posix(),
    "eval_forge_operating_path": EVAL_FORGE_OPERATING_PATH_RELATIVE.as_posix(),
    "eval_forge_session_mining_criteria": EVAL_FORGE_SESSION_MINING_CRITERIA_RELATIVE.as_posix(),
    "eval_forge_local_port_matrix": EVAL_FORGE_LOCAL_PORT_MATRIX_RELATIVE.as_posix(),
    "eval_forge_worksheet_example": EVAL_FORGE_WORKSHEET_EXAMPLE_RELATIVE.as_posix(),
    "eval_forge_route_review_report": EVAL_FORGE_ROUTE_REVIEW_REPORT_RELATIVE.as_posix(),
    "manual_session_mining_report": MANUAL_SESSION_MINING_REPORT.as_posix(),
    "session_start_tool": "scripts/aoa_eval_session_start.py",
    "freshness_sentinel_command": "scripts/check_eval_freshness_sentinel.py",
    "route_trajectory_harness": "scripts/run_aoa_eval_route_trajectory_harness.py",
    "runtime_candidate_intake": (
        "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json"
    ),
}
OWNER_BOUNDARIES = [
    {
        "owner_repo": "aoa-evals",
        "owns": "central proof doctrine, source eval bundles, report/verdict contracts, central adoption gates",
        "does_not_own": "live MCP execution, repo-local pressure, unreviewed session evidence, installed skill visibility",
    },
    {
        "owner_repo": "repo-local evals/",
        "owns": "local intake, suites, reports, fixtures, and repo pressure evidence",
        "does_not_own": "central scoring, proof doctrine, regression baselines, or bundle adoption",
    },
    {
        "owner_repo": "aoa-skills",
        "owns": "aoa-eval source skill, trigger wording, prompt/runtime discovery, and skill tests",
        "does_not_own": "central eval verdicts or runtime MCP service behavior",
    },
    {
        "owner_repo": "abyss-stack",
        "owns": "runnable aoa-evals MCP service and runtime exports",
        "does_not_own": "central proof acceptance or local eval-port truth",
    },
    {
        "owner_repo": ".aoa",
        "owns": "session evidence, archive freshness, and candidate-only mining references",
        "does_not_own": "reviewed truth, eval verdicts, or promotion decisions",
    },
]
EVAL_RELEVANCE_KEYWORDS = (
    "eval",
    "proof",
    "report",
    "catalog",
    "candidate",
    "runtime",
    "trace",
    "trajectory",
    "verdict",
    "local_eval",
    "local eval",
    "freshness",
    "quest",
    "session",
    "memory",
    "artifact",
)
EXTERNAL_RESEARCH_GROUNDING = [
    {
        "source": "OpenAI agent workflow evals",
        "url": "https://developers.openai.com/api/docs/guides/agent-evals",
        "checked_at_utc": "2026-06-25",
        "adopted": "Start path-sensitive agent eval work from traces, graders, datasets, and eval runs; inspect tool calls, handoffs, guardrails, and routing changes before hardening a dataset.",
        "rejected": "Do not let a trace grader, dashboard, or hosted run become central proof acceptance inside OS Abyss.",
    },
    {
        "source": "OpenAI evaluation best practices and Evals deprecation notice",
        "url": "https://developers.openai.com/api/docs/guides/evaluation-best-practices",
        "checked_at_utc": "2026-06-25",
        "adopted": "Keep eval design objective-driven: define success criteria, collect representative cases, define metrics, run/compare, and grow cases continuously.",
        "rejected": "Do not couple durable OS Abyss proof control to deprecated hosted Evals platform semantics; use the process shape, not the platform as authority.",
    },
    {
        "source": "OpenAI Agents SDK tracing",
        "url": "https://openai.github.io/openai-agents-python/tracing/",
        "checked_at_utc": "2026-06-25",
        "adopted": "Use trace/span/tool-call evidence when the behavior under test is route choice, handoff, guardrail, or tool trajectory.",
        "rejected": "Do not evaluate agentic behavior from final text alone when path discipline is the claim.",
    },
    {
        "source": "LangSmith trajectory evaluations",
        "url": "https://docs.langchain.com/langsmith/trajectory-evals",
        "checked_at_utc": "2026-06-25",
        "adopted": "Represent route behavior as a trajectory of messages and tool calls; prefer deterministic trajectory match when the expected route is known.",
        "rejected": "Do not use judge-only broad mining for route-law violations.",
    },
    {
        "source": "LangSmith application-specific evaluation approaches",
        "url": "https://docs.langchain.com/langsmith/evaluation-approaches",
        "checked_at_utc": "2026-06-25",
        "adopted": "Keep final-response, single-step, and trajectory checks separate so OS Abyss does not overfit one evaluator type.",
        "rejected": "Do not flatten all agent evaluation into one LLM-as-judge rubric.",
    },
    {
        "source": "Inspect AI and sandboxing docs",
        "url": "https://inspect.aisi.org.uk/",
        "checked_at_utc": "2026-06-25",
        "adopted": "Model runnable agent evals as tasks with datasets, solvers/agents, tools, scorers, logs, and sandbox/side-effect boundaries.",
        "rejected": "Do not run write-capable support scripts as eval application without an explicit check or dry-run route.",
    },
]
CANDIDATE_QUEUE_STATES = (
    "observed",
    "needs_owner_review",
    "duplicate_existing_eval",
    "local_only",
    "central_draft",
    "rejected",
    "deferred",
    "accepted",
)
SUPPORT_SEMANTIC_CLASSES = {
    "deterministic_validator": "Read-only validator with an explicit owner lane.",
    "unit_contract_property_test": "Pytest or test surface constraining a stable contract or invariant.",
    "trace_trajectory_eval_support": "Test or support surface about route trajectory, trace, or tool path behavior.",
    "generated_parity_check": "Generated/read-model parity support; useful for freshness, not proof acceptance.",
    "runtime_candidate_support": "Runtime or session-derived candidate evidence; candidate-only until reviewed.",
    "unsafe_side_effect_script": "Write-capable script without a safe direct eval-apply route.",
    "ordinary_support": "Ordinary support surface with no eval-lane signal.",
    "manual_review_needed": "Relevant support surface that needs human classification before eval use.",
}
REVIEW_STATUS_DESCRIPTIONS = {
    "rule_reviewed": "classified by deterministic source-inventory rule and owner evidence",
    "candidate_only": "usable only as candidate evidence until owner review",
    "reviewed_forbidden": "reviewed and explicitly forbidden as direct eval application",
    "not_eval_relevant": "downgraded to ordinary owner route for eval-control purposes",
    "manual_review_required": "unresolved classifier gap; should be zero for eval-relevant support surfaces",
}
SESSION_MINING_STATUS = {
    "status": "manual_review_packetized",
    "reason": "A bounded 20-episode .aoa manual review was performed; kept items are imported only as schema-valid candidate packets.",
    "reviewed_count": 20,
    "packetized_count": 5,
    "rejected_count": 5,
    "duplicate_count": 4,
    "deferred_count": 3,
    "observed_positive_count": 3,
    "report_refs": [MANUAL_SESSION_MINING_REPORT.as_posix()],
    "packet_root": CANDIDATE_PACKET_RELATIVE.as_posix(),
    "candidate_only_boundary": ".aoa can supply candidate evidence only; session-mining cannot create reviewed eval truth.",
    "next_evidence_needed": [
        "human owner review of packetized candidates",
        "central overlap check before central bundle design",
        "local intake or trigger-design route for accepted candidates",
        "freshness recheck before any broader mining wave",
    ],
}
TRIGGER_CLASSES = [
    {
        "id": "existing_eval_applicable_before_new_design",
        "trigger_when": [
            "user asks to evaluate a behavior, workflow, proof surface, or agent action",
            "central catalog already has a matching or adjacent eval",
            "local pressure can be answered by apply or dry-run before new bundle design",
        ],
        "do_not_trigger_when": [
            "the task is a small local code edit with an obvious test and no eval-language pressure",
            "the requested check is already the repo's ordinary unit test gate",
        ],
        "required_refs": ["generated/eval_catalog.json", "EVAL_SELECTION.md", "current repo context"],
        "required_freshness": "central catalog check current enough for route selection",
        "next_route": "aoa-eval:select_then_apply",
    },
    {
        "id": "repo_local_eval_pressure_without_central_match",
        "trigger_when": [
            "repo-local evals/intake, suites, reports, or eval.yaml pressure exists",
            "central catalog has no matching eval or only a weak adjacent route",
            "owner repo pressure is concrete enough to preserve locally",
        ],
        "do_not_trigger_when": [
            "repo has only a dormant skeleton evals/ port",
            "pressure is a single vague preference without evidence or owner fit",
        ],
        "required_refs": ["repo-local evals/PORT.yaml", "scripts/build_local_eval_port_inventory.py"],
        "required_freshness": "local port inventory regenerated or inspected in current task",
        "next_route": "aoa-eval:local_need_or_design",
    },
    {
        "id": "validator_test_script_support_needed",
        "trigger_when": [
            "a validator, test, or builder is the natural deterministic check for eval pressure",
            "the check constrains owner boundaries or route behavior, not only example output",
            "the side-effect boundary is known before execution",
        ],
        "do_not_trigger_when": [
            "the script mutates source state and no dry-run/check mode exists",
            "the check's owner surface is outside the current permission scope",
        ],
        "required_refs": [
            "docs/validation/validator_inventory.json",
            "docs/validation/script_inventory.json",
            "docs/testing/test_inventory.json",
        ],
        "required_freshness": "support registry source inventories parse and name owner surfaces",
        "next_route": "aoa-eval:apply_existing_validator_or_design_gap",
    },
    {
        "id": "agent_route_miss_or_tool_trajectory_pressure",
        "trigger_when": [
            "the important behavior is the agent's route choice, tool sequence, or boundary discipline",
            "failure mode is path-sensitive rather than only final-output quality",
            "a deterministic trace packet can name expected route transitions",
        ],
        "do_not_trigger_when": [
            "the session only contains ordinary misunderstanding without a repeatable route condition",
            "raw chat memory is the only evidence and has not been anchored to refs",
        ],
        "required_refs": [
            "evals/workflow/aoa-tool-trajectory-discipline/EVAL.md",
            "evals/workflow/aoa-trace-outcome-separation/EVAL.md",
            ".aoa session refs when used",
        ],
        "required_freshness": "session refs and repo refs must be current enough to replay route conditions",
        "next_route": "aoa-eval:trajectory_slice_or_session_candidate",
    },
    {
        "id": "runtime_candidate_export_needs_review",
        "trigger_when": [
            "abyss-stack or aoa-evals MCP exposes runtime candidate exports",
            "candidate points at eval adoption, selected evidence, or artifact-to-verdict bridge",
            "owner review route is required before proof meaning can change",
        ],
        "do_not_trigger_when": [
            "runtime export is only operational telemetry with no eval owner route",
            "the candidate asks MCP to create or accept central proof directly",
        ],
        "required_refs": [
            "mechanics/audit/parts/candidate-readers/generated/runtime_candidate_intake.min.json",
            "aoa-evals-mcp runtime-status output when available",
        ],
        "required_freshness": "runtime status timestamp and candidate-reader generation state visible",
        "next_route": "aoa-eval:candidate_queue_needs_owner_review",
    },
    {
        "id": "freshness_or_mirror_drift_blocks_eval_route",
        "trigger_when": [
            "selected MCP root, generated read-model, repo branch, dirty state, or mirror freshness could change the route",
            "an agent would otherwise apply a stale eval or ignore a newer active surface",
            "the stale surface is only a read-model and can be rebuilt or marked stale",
        ],
        "do_not_trigger_when": [
            "dirty files are unrelated and do not affect eval route selection",
            "refresh would mutate sibling repos outside the current scope",
        ],
        "required_refs": [
            "git branch and dirty readout",
            "generated/AGENTS.md",
            "aoa-evals-mcp runtime-status output when available",
        ],
        "required_freshness": "commit ids, branch names, generated timestamps, and selected roots recorded",
        "next_route": "aoa-eval:freshness_sentinel_then_route",
    },
    {
        "id": "session_episode_candidate_for_eval_design",
        "trigger_when": [
            "session history shows repeated or high-cost eval-lane miss opportunities",
            "episode has identifiable trigger, expected route, actual route, and consequence",
            "criteria taxonomy can classify it before broad mining starts",
        ],
        "do_not_trigger_when": [
            "episode is interesting but lacks owner surface, route expectation, or evidence refs",
            "mining would expose private/raw context without candidate-only boundary",
        ],
        "required_refs": [
            ".aoa session id or segment refs",
            "criteria taxonomy id",
            "repo-owner refs touched by the episode",
        ],
        "required_freshness": ".aoa maintenance-status or archive freshness readout current",
        "next_route": "aoa-eval:session_candidate_only",
    },
    {
        "id": "promotion_or_central_adoption_pressure",
        "trigger_when": [
            "local queue item is being considered for central bundle, status, baseline, report, or proof adoption",
            "owner gates, evidence sufficiency, and non-duplication must be reviewed",
            "acceptance would change aoa-evals source truth or proof posture",
        ],
        "do_not_trigger_when": [
            "candidate is still intake-only or local-only",
            "human owner approval and source bundle review are absent",
        ],
        "required_refs": [
            "docs/guides/EVAL_REVIEW_GUIDE.md",
            "docs/operations/RELEASING.md",
            "source eval bundle refs if drafting",
        ],
        "required_freshness": "central catalog, report index, and owner evidence current",
        "next_route": "aoa-evals owner review, not MCP auto-promotion",
    },
]
SAMPLE_PACKET_SCHEMA = {
    "schema_version": "aoa_eval_trigger_mining_sample_v1",
    "required_fields": [
        "packet_id",
        "source_kind",
        "source_ref",
        "observed_at_utc",
        "trigger_class_id",
        "expected_aoa_eval_route",
        "actual_route",
        "owner_surface_refs",
        "evidence_refs",
        "freshness_refs",
        "candidate_state",
        "candidate_state_reason",
        "promotion_forbidden_until",
    ],
    "field_notes": {
        "packet_id": "stable local id for the mined candidate packet",
        "source_kind": "session_episode, runtime_export, local_eval_port, validator_gap, or quest_lineage",
        "source_ref": "opaque but dereferenceable local ref, never raw proof acceptance",
        "trigger_class_id": "one of trigger_taxonomy[].id",
        "expected_aoa_eval_route": "select, apply, local_need, design, session_candidate, or freshness_sentinel",
        "actual_route": "what happened in the observed episode",
        "owner_surface_refs": "repo-qualified paths that own the route meaning",
        "evidence_refs": "bounded evidence pointers, not full private transcripts",
        "freshness_refs": "commit ids, generated timestamps, archive freshness, or runtime status refs",
        "candidate_state": "observed, needs_owner_review, local_only, duplicate_existing_eval, deferred, or rejected",
        "candidate_state_reason": "short reason for observed/kept/rejected/deferred routing state",
        "promotion_forbidden_until": "explicit owner gates required before central proof adoption",
    },
    "forbidden_effects": [
        "central_proof_promotion",
        "verdict_acceptance",
        "score_or_baseline_creation",
        "repo_mutation",
        "mcp_created_bundle",
    ],
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE_ROOT))
    parser.add_argument("--evals-root", default=str(REPO_ROOT))
    parser.add_argument("--aoa-root", default=str(DEFAULT_AOA_ROOT))
    parser.add_argument("--skills-source-root", default=str(DEFAULT_SKILLS_SOURCE_ROOT))
    parser.add_argument("--installed-skills-root", default=str(DEFAULT_INSTALLED_SKILLS_ROOT))
    parser.add_argument("--stack-root", default="")
    parser.add_argument("--live-timeout", type=int, default=30)
    parser.add_argument("--no-live-checks", action="store_true")
    parser.add_argument("--json", action="store_true", help="Print dashboard JSON to stdout.")
    parser.add_argument(
        "--write-generated",
        action="store_true",
        help="Write generated dashboard and support-registry files.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate generated dashboard/support-registry shape without comparing volatile OS state.",
    )
    return parser.parse_args(argv)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, *, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_external_research_grounding(evals_root: Path) -> list[dict[str, Any]]:
    payload = read_json(evals_root / EVAL_FORGE_EXTERNAL_GROUNDING_RELATIVE, default=None)
    if not isinstance(payload, dict):
        return EXTERNAL_RESEARCH_GROUNDING
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        return EXTERNAL_RESEARCH_GROUNDING
    checked_at = str(payload.get("checked_at_utc") or "")
    normalized: list[dict[str, Any]] = []
    for item in sources:
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "source": item.get("source"),
                "url": item.get("url"),
                "checked_at_utc": checked_at,
                "adopted": item.get("adopted"),
                "rejected": item.get("rejected"),
            }
        )
    return normalized or EXTERNAL_RESEARCH_GROUNDING


def repo_relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def canonical_evals_owner_root(evals_root: Path, workspace_root: Path) -> Path:
    """Keep generated paths on the canonical owner checkout, not a worktree."""

    identity = build_local_eval_port_inventory.validate_local_eval_port.resolve_repo_identity(
        evals_root
    )
    candidate = workspace_root / identity.owner_repo
    if (
        not identity.issues
        and identity.owner_repo == build_local_eval_port_inventory.PROOF_OWNER_REPO
    ):
        return candidate.resolve(strict=False)
    return evals_root.resolve()


def sha256_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def run_command(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        return {
            "status": "unavailable",
            "returncode": None,
            "error": str(exc),
            "stdout": "",
            "stderr": "",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "returncode": None,
            "error": f"timeout after {timeout}s",
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
        }
    return {
        "status": "ok" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_json_command(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = 30,
    keep_output: bool = False,
) -> dict[str, Any]:
    result = run_command(command, cwd=cwd, env=env, timeout=timeout)
    payload = read_json_from_text(result.get("stdout", ""))
    result["json"] = payload
    if payload is None and result["status"] == "ok":
        result["status"] = "unparseable"
    result["stdout_line_count"] = len(str(result.get("stdout", "")).splitlines())
    result["stderr_line_count"] = len(str(result.get("stderr", "")).splitlines())
    if keep_output:
        result["stdout"] = summarize_text(str(result.get("stdout", "")), max_lines=12, max_chars=1600)
        result["stderr"] = summarize_text(str(result.get("stderr", "")), max_lines=12, max_chars=1600)
    else:
        result.pop("stdout", None)
        result.pop("stderr", None)
    return result


def summarize_mcp_runtime_json(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    freshness = payload.get("freshness") if isinstance(payload.get("freshness"), dict) else {}
    mirror = payload.get("mirror") if isinstance(payload.get("mirror"), dict) else {}
    mirror_manifest = (
        payload.get("mirror_manifest") if isinstance(payload.get("mirror_manifest"), dict) else {}
    )
    missing_groups = mirror.get("missing_groups") if isinstance(mirror.get("missing_groups"), list) else []
    required_files = (
        mirror_manifest.get("required_files")
        if isinstance(mirror_manifest.get("required_files"), list)
        else []
    )
    return {
        "schema": payload.get("schema"),
        "workspace_root": payload.get("workspace_root"),
        "root_kind": payload.get("root_kind"),
        "selected_root": payload.get("selected_root"),
        "source_root": payload.get("source_root"),
        "mirror_root": payload.get("mirror_root"),
        "catalog_count": payload.get("catalog_count"),
        "runtime_candidate_export_count": payload.get("runtime_candidate_export_count"),
        "runtime_candidate_template_count": payload.get("runtime_candidate_template_count"),
        "freshness": {
            "status": freshness.get("status"),
            "mirror_status": freshness.get("mirror_status"),
            "mirror_is_stale": freshness.get("mirror_is_stale"),
            "mirror_is_current": freshness.get("mirror_is_current"),
            "source_git_commit": freshness.get("source_git_commit"),
            "mirror_source_git_commit": freshness.get("mirror_source_git_commit"),
            "mirror_generated_at_utc": freshness.get("mirror_generated_at_utc"),
            "mirror_latest_reader_mtime_utc": freshness.get("mirror_latest_reader_mtime_utc"),
            "notes": freshness.get("notes"),
            "refresh_command": freshness.get("refresh_command"),
        },
        "mirror": {
            "exists": mirror.get("exists"),
            "missing_group_count": len(missing_groups),
            "reader_count": len(mirror.get("readers", {})) if isinstance(mirror.get("readers"), dict) else None,
        },
        "mirror_manifest": {
            "schema_version": mirror_manifest.get("schema_version"),
            "required_file_count": len(required_files),
        },
        "authority_boundary": "Summarized MCP runtime-status payload; path-level mirror manifests stay in the MCP owner surface.",
    }


def read_json_from_text(text: str) -> Any:
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def summarize_text(text: str, *, max_lines: int = 30, max_chars: int = 6000) -> str:
    lines = text.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines] + [f"... truncated {len(text.splitlines()) - max_lines} line(s)"]
    compact = "\n".join(lines)
    if len(compact) > max_chars:
        return compact[:max_chars] + "... truncated"
    return compact


def normalize_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda item: item[0]))


def support_text(entry: dict[str, Any]) -> str:
    values: list[str] = []
    for key in (
        "path",
        "family",
        "organ_lane",
        "lane",
        "layer",
        "mode",
        "owner_surface",
        "source_truth",
        "input",
        "output",
        "focused_target",
        "failure_route",
        "side_effects",
    ):
        value = entry.get(key)
        if isinstance(value, list):
            values.extend(str(item) for item in value)
        elif value is not None:
            values.append(str(value))
    return " ".join(values).lower()


def relevance_reasons(entry: dict[str, Any]) -> list[str]:
    text = support_text(entry)
    reasons = [keyword for keyword in EVAL_RELEVANCE_KEYWORDS if keyword in text]
    return reasons[:8]


def classify_support(kind: str, entry: dict[str, Any]) -> str:
    family = str(entry.get("family", "")).lower()
    side_effects = str(entry.get("side_effects", "")).lower()
    mode = str(entry.get("mode", "")).lower()
    if kind == "validator":
        return "deterministic_validator"
    if kind == "test":
        if "trace/eval" in family:
            return "trace_eval_test"
        if "generated" in family:
            return "generated_readmodel_test"
        return "deterministic_test"
    if "builder" in family and "--check" in side_effects:
        return "builder_with_check_mode"
    if "builder" in family:
        return "builder_or_projection"
    if "validator" in family or "validation" in mode:
        return "deterministic_script_validator"
    return "script_support"


def write_side_effect(entry: dict[str, Any]) -> bool:
    side_effects = str(entry.get("side_effects", "")).lower()
    writes = entry.get("writes")
    if isinstance(writes, list) and bool(writes):
        return True
    return any(
        token in side_effects
        for token in (
            "writes ",
            "writes tracked",
            "scaffolds ",
            "creates ",
            "mutates",
            "deletes ",
            "rewrites ",
            "overwrites ",
        )
    )


def guarded_write_route(entry: dict[str, Any]) -> bool:
    side_effects = str(entry.get("side_effects", "")).lower()
    mode = str(entry.get("mode", "")).lower()
    text = f"{side_effects} {mode}"
    return any(
        token in text
        for token in (
            "--check",
            "dry-run",
            "dry run",
            "check mode",
            "preview",
            "read-only by default",
            "optional output",
            "caller-specified",
            "validation output only",
            "stdout only",
        )
    )


def support_classification_evidence(entry: dict[str, Any]) -> list[str]:
    evidence: list[str] = []
    for key in ("family", "mode", "owner_surface", "side_effects", "validation_lane", "coverage_authority"):
        value = entry.get(key)
        if isinstance(value, str) and value:
            evidence.append(f"{key}: {value}")
    writes = entry.get("writes")
    if isinstance(writes, list) and writes:
        evidence.append(f"writes: {', '.join(str(item) for item in writes[:4])}")
    return evidence[:8]


def helper_only_support(entry: dict[str, Any]) -> bool:
    family = str(entry.get("family", "")).lower()
    side_effects = str(entry.get("side_effects", "")).lower()
    mode = str(entry.get("mode", "")).lower()
    return (
        "helper" in family
        or "helper import only" in side_effects
        or "import only" in side_effects
        or "helper" in mode
    )


def read_only_validator_script(entry: dict[str, Any]) -> bool:
    path = str(entry.get("path", "")).lower()
    family = str(entry.get("family", "")).lower()
    mode = str(entry.get("mode", "")).lower()
    side_effects = str(entry.get("side_effects", "")).lower()
    if write_side_effect(entry):
        return False
    has_validator_shape = (
        "validator" in family
        or "validation" in mode
        or path.startswith("scripts/validate_")
        or path.startswith("scripts/validators/")
        or "/scripts/validate_" in path
        or "/scripts/run_" in path and "eval" in path
    )
    has_read_only_effect = (
        "validation output only" in side_effects
        or "read-only" in side_effects
        or "helper import only" in side_effects
        or "import only" in side_effects
        or "stdout only" in side_effects
    )
    return has_validator_shape and has_read_only_effect


def semantic_support_classification(kind: str, entry: dict[str, Any], relevant: bool) -> dict[str, Any]:
    family = str(entry.get("family", "")).lower()
    lane = str(entry.get("validation_lane") or entry.get("coverage_authority") or "").lower()
    text = support_text(entry)
    has_write = write_side_effect(entry)
    has_guard = guarded_write_route(entry)
    evidence = support_classification_evidence(entry)

    if kind == "script" and has_write and not has_guard:
        return {
            "semantic_class": "unsafe_side_effect_script",
            "classification_rule": "script_write_effect_without_check_or_dry_run",
            "review_status": "reviewed_forbidden",
            "review_reason": "write-capable script has no check/dry-run guard; direct eval application is forbidden until owner route changes",
            "classification_evidence": evidence,
            "recommended_route": "forbidden_as_eval_apply_until_manual_owner_review",
            "safe_to_apply_directly": False,
            "forbidden_interpretations": [
                "apply_as_deterministic_eval_support",
                "central_proof_acceptance",
                "safe_smoke_without_owner_check",
            ],
        }
    if kind == "validator":
        return {
            "semantic_class": "deterministic_validator",
            "classification_rule": "validator_inventory_entry",
            "review_status": "rule_reviewed",
            "review_reason": "validator inventory entry is already command-authority support; use as deterministic support, not proof acceptance",
            "classification_evidence": evidence,
            "recommended_route": "apply_as_deterministic_eval_support",
            "safe_to_apply_directly": True,
            "forbidden_interpretations": ["central_proof_acceptance"],
        }
    if kind == "test":
        if "trace" in family or "trajectory" in family or "eval-scenario" in family:
            semantic_class = "trace_trajectory_eval_support"
            rule = "test_family_trace_or_trajectory"
        elif "generated" in family or "read-model" in family:
            semantic_class = "generated_parity_check"
            rule = "test_family_generated_readmodel"
        else:
            semantic_class = "unit_contract_property_test"
            rule = "test_inventory_contract_or_invariant"
        return {
            "semantic_class": semantic_class,
            "classification_rule": rule,
            "review_status": "rule_reviewed",
            "review_reason": "test inventory entry constrains behavior through the owning test route",
            "classification_evidence": evidence,
            "recommended_route": "apply_as_deterministic_eval_support",
            "safe_to_apply_directly": True,
            "forbidden_interpretations": ["central_proof_acceptance"],
        }
    if kind == "script" and has_write and has_guard:
        semantic_class = "generated_parity_check" if "generated" in lane or "builder" in family else "manual_review_needed"
        return {
            "semantic_class": semantic_class,
            "classification_rule": "write_capable_script_requires_check_or_dry_run_first",
            "review_status": "rule_reviewed" if semantic_class == "generated_parity_check" else "manual_review_required",
            "review_reason": "write-capable script has an explicit check/dry-run/preview route; run the non-mutating mode before eval support",
            "classification_evidence": evidence,
            "recommended_route": "run_check_mode_before_eval_support",
            "safe_to_apply_directly": False,
            "forbidden_interpretations": [
                "apply_as_deterministic_eval_support_without_check",
                "central_proof_acceptance",
            ],
        }
    if kind == "script" and read_only_validator_script(entry):
        if helper_only_support(entry):
            return {
                "semantic_class": "deterministic_validator",
                "classification_rule": "read_only_validator_helper_component",
                "review_status": "rule_reviewed",
                "review_reason": "helper-only validator component is reviewed as validator support but must be reached through its owning validator or lane command",
                "classification_evidence": evidence,
                "recommended_route": "component_only_use_owning_validator_or_lane_command",
                "safe_to_apply_directly": False,
                "forbidden_interpretations": [
                    "direct_eval_apply_command",
                    "central_proof_acceptance",
                ],
            }
        return {
            "semantic_class": "deterministic_validator",
            "classification_rule": "read_only_validator_script",
            "review_status": "rule_reviewed",
            "review_reason": "read-only validator script has validation-only side effects and an owner surface",
            "classification_evidence": evidence,
            "recommended_route": "apply_as_deterministic_eval_support",
            "safe_to_apply_directly": True,
            "forbidden_interpretations": ["central_proof_acceptance"],
        }
    if "candidate" in text or "runtime" in text or "session" in text or "memory" in text:
        return {
            "semantic_class": "runtime_candidate_support",
            "classification_rule": "runtime_or_session_candidate_signal",
            "review_status": "candidate_only",
            "review_reason": "runtime/session/memory signal can seed candidates only and cannot become reviewed truth",
            "classification_evidence": evidence,
            "recommended_route": "candidate_only_eval_support",
            "safe_to_apply_directly": False,
            "forbidden_interpretations": ["reviewed_truth", "central_proof_acceptance"],
        }
    if "builder" in family or "projection" in family or "generated" in text or "catalog" in text:
        return {
            "semantic_class": "generated_parity_check",
            "classification_rule": "builder_or_generated_readmodel_signal",
            "review_status": "rule_reviewed",
            "review_reason": "builder/generated/read-model surface can check parity or freshness but cannot accept proof",
            "classification_evidence": evidence,
            "recommended_route": "generated_readmodel_support",
            "safe_to_apply_directly": False,
            "forbidden_interpretations": ["central_proof_acceptance"],
        }
    if relevant:
        return {
            "semantic_class": "manual_review_needed",
            "classification_rule": "keyword_relevant_but_no_safe_semantic_rule",
            "review_status": "manual_review_required",
            "review_reason": "keyword relevance remains after deterministic rules; owner must classify before eval use",
            "classification_evidence": evidence,
            "recommended_route": "eval_lane_support_review",
            "safe_to_apply_directly": False,
            "forbidden_interpretations": ["automatic_eval_apply", "central_proof_acceptance"],
        }
    return {
        "semantic_class": "ordinary_support",
        "classification_rule": "no_eval_lane_signal",
        "review_status": "not_eval_relevant",
        "review_reason": "no eval-lane signal found in inventory evidence; keep on ordinary owner route",
        "classification_evidence": evidence,
        "recommended_route": "ordinary_owner_route",
        "safe_to_apply_directly": False,
        "forbidden_interpretations": ["eval_lane_support_without_new_evidence"],
    }


def recommended_support_route(kind: str, entry: dict[str, Any], relevant: bool) -> str:
    semantic = semantic_support_classification(kind, entry, relevant)
    return str(semantic["recommended_route"])


def build_support_registry(evals_root: Path) -> dict[str, Any]:
    validator_payload = read_json(evals_root / "docs" / "validation" / "validator_inventory.json", default={})
    script_payload = read_json(evals_root / "docs" / "validation" / "script_inventory.json", default={})
    test_payload = read_json(evals_root / "docs" / "testing" / "test_inventory.json", default={})
    source_sets = [
        ("validator", validator_payload.get("entries", []) if isinstance(validator_payload, dict) else []),
        ("script", script_payload.get("script_surfaces", []) if isinstance(script_payload, dict) else []),
        ("test", test_payload.get("test_surfaces", []) if isinstance(test_payload, dict) else []),
    ]

    surfaces: list[dict[str, Any]] = []
    by_kind: Counter[str] = Counter()
    by_route: Counter[str] = Counter()
    by_classification: Counter[str] = Counter()
    by_semantic_class: Counter[str] = Counter()
    by_review_status: Counter[str] = Counter()
    by_lane: Counter[str] = Counter()
    relevant_count = 0
    safe_direct_count = 0
    unsafe_write_count = 0
    for kind, entries in source_sets:
        if not isinstance(entries, list):
            continue
        for raw in entries:
            if not isinstance(raw, dict):
                continue
            path = raw.get("path")
            if not isinstance(path, str):
                continue
            reasons = relevance_reasons(raw)
            relevant = bool(reasons)
            classification = classify_support(kind, raw)
            semantic = semantic_support_classification(kind, raw, relevant)
            route = str(semantic["recommended_route"])
            lane = raw.get("validation_lane") or raw.get("lane") or raw.get("coverage_authority")
            if isinstance(lane, str):
                lane_key = lane.replace("validation_lanes.", "")
            else:
                lane_key = "unknown"
            by_kind[kind] += 1
            by_route[route] += 1
            by_classification[classification] += 1
            by_semantic_class[str(semantic["semantic_class"])] += 1
            by_review_status[str(semantic["review_status"])] += 1
            by_lane[lane_key] += 1
            if relevant:
                relevant_count += 1
            if semantic.get("safe_to_apply_directly") is True:
                safe_direct_count += 1
            if semantic.get("semantic_class") == "unsafe_side_effect_script":
                unsafe_write_count += 1
            surfaces.append(
                {
                    "kind": kind,
                    "path": path,
                    "classification": classification,
                    "semantic_class": semantic["semantic_class"],
                    "classification_rule": semantic["classification_rule"],
                    "review_status": semantic["review_status"],
                    "review_reason": semantic["review_reason"],
                    "eval_lane_relevant": relevant,
                    "relevance_reasons": reasons,
                    "recommended_route": route,
                    "safe_to_apply_directly": semantic["safe_to_apply_directly"],
                    "forbidden_interpretations": semantic["forbidden_interpretations"],
                    "classification_evidence": semantic["classification_evidence"],
                    "lane": lane_key,
                    "family": raw.get("family"),
                    "owner_surface": raw.get("owner_surface"),
                    "source_truth_count": len(raw.get("source_truth", []))
                    if isinstance(raw.get("source_truth"), list)
                    else None,
                    "side_effects": raw.get("side_effects"),
                    "test_target": raw.get("test_target"),
                    "focused_target": raw.get("focused_target"),
                    "failure_route": raw.get("failure_route"),
                }
            )

    surfaces.sort(key=lambda item: (str(item["kind"]), str(item["path"])))
    return {
        "schema_version": SUPPORT_REGISTRY_SCHEMA_VERSION,
        "layer": "aoa-evals",
        "authority_boundary": (
            "Registry maps existing checks to eval-lane support. It is not command authority; "
            "docs/validation/validation_lanes.json keeps blocking lane commands."
        ),
        "source_of_truth": {
            "validator_inventory": "docs/validation/validator_inventory.json",
            "script_inventory": "docs/validation/script_inventory.json",
            "test_inventory": "docs/testing/test_inventory.json",
            "command_authority": "docs/validation/validation_lanes.json",
        },
        "summary": {
            "total_surfaces": len(surfaces),
            "eval_lane_relevant": relevant_count,
            "safe_to_apply_directly": safe_direct_count,
            "unsafe_side_effect_scripts": unsafe_write_count,
            "by_kind": normalize_counter(by_kind),
            "by_lane": normalize_counter(by_lane),
            "by_classification": normalize_counter(by_classification),
            "by_semantic_class": normalize_counter(by_semantic_class),
            "by_review_status": normalize_counter(by_review_status),
            "by_recommended_route": normalize_counter(by_route),
        },
        "surfaces": surfaces,
    }


def load_catalog_summary(evals_root: Path) -> dict[str, Any]:
    catalog = read_json(evals_root / "generated" / "eval_catalog.json", default={})
    if not isinstance(catalog, dict):
        return {"status": "unavailable", "reason": "generated/eval_catalog.json is not an object"}
    evals = catalog.get("evals")
    if not isinstance(evals, list):
        return {"status": "unavailable", "reason": "generated/eval_catalog.json has no evals list"}
    by_status: Counter[str] = Counter()
    by_category: Counter[str] = Counter()
    by_claim_type: Counter[str] = Counter()
    starters: list[dict[str, Any]] = []
    trajectory_refs: list[str] = []
    for entry in evals:
        if not isinstance(entry, dict):
            continue
        by_status[str(entry.get("status", "unknown"))] += 1
        by_category[str(entry.get("category", "unknown"))] += 1
        by_claim_type[str(entry.get("claim_type", "unknown"))] += 1
        name = str(entry.get("name", ""))
        summary = str(entry.get("summary", ""))
        if name in {
            "aoa-tool-trajectory-discipline",
            "aoa-trace-outcome-separation",
            "aoa-eval-integrity-check",
            "aoa-approval-boundary-adherence",
            "aoa-verification-honesty",
        }:
            starters.append(
                {
                    "name": name,
                    "status": entry.get("status"),
                    "category": entry.get("category"),
                    "claim_type": entry.get("claim_type"),
                    "eval_path": entry.get("eval_path"),
                    "use_for": summary,
                }
            )
        if "trajectory" in name or "trace" in name:
            eval_path = entry.get("eval_path")
            if isinstance(eval_path, str):
                trajectory_refs.append(eval_path)
    starters.sort(key=lambda item: str(item["name"]))
    return {
        "status": "ok",
        "total_evals": len(evals),
        "by_status": normalize_counter(by_status),
        "by_category": normalize_counter(by_category),
        "by_claim_type": normalize_counter(by_claim_type),
        "starter_map": starters,
        "trajectory_eval_refs": sorted(trajectory_refs),
        "authority_boundary": "central catalog routes to source bundles; it does not make local or runtime candidates accepted proof.",
        "next_route": "select existing central eval before designing new local or central bundle.",
    }


def load_runtime_candidate_summary(evals_root: Path) -> dict[str, Any]:
    intake_path = (
        evals_root
        / "mechanics"
        / "audit"
        / "parts"
        / "candidate-readers"
        / "generated"
        / "runtime_candidate_intake.min.json"
    )
    payload = read_json(intake_path, default={})
    templates = payload.get("templates", []) if isinstance(payload, dict) else []
    if not isinstance(templates, list):
        templates = []
    by_kind: Counter[str] = Counter()
    review_required = 0
    for item in templates:
        if not isinstance(item, dict):
            continue
        by_kind[str(item.get("template_kind", "unknown"))] += 1
        if item.get("review_required") is True:
            review_required += 1
    return {
        "source_ref": repo_relative(intake_path, evals_root),
        "count": len(templates),
        "review_required": review_required,
        "by_template_kind": normalize_counter(by_kind),
        "authority_boundary": "runtime candidate intake is candidate-only until source-owner review.",
    }


def load_candidate_packets(evals_root: Path) -> dict[str, Any]:
    packet_root = evals_root / CANDIDATE_PACKET_RELATIVE
    packets: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    by_state: Counter[str] = Counter()
    by_source_kind: Counter[str] = Counter()
    if packet_root.exists():
        paths = sorted(packet_root.rglob("*.eval_candidate.json"))
    else:
        paths = []

    for path in paths:
        location = repo_relative(path, evals_root)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append({"path": location, "message": f"invalid JSON: {exc}"})
            continue
        except OSError as exc:
            issues.append({"path": location, "message": str(exc)})
            continue
        if not isinstance(payload, dict):
            issues.append({"path": location, "message": "candidate packet is not a JSON object"})
            continue
        packets.append({"path": location, "payload": payload})
        by_state[str(payload.get("candidate_state", "unknown"))] += 1
        by_source_kind[str(payload.get("source_kind", "unknown"))] += 1

    return {
        "schema_version": "os_abyss_eval_candidate_packet_import_v1",
        "authority_boundary": "Imported candidate packets seed routing only; they cannot accept proof or promote central bundles.",
        "packet_root": repo_relative(packet_root, evals_root),
        "packet_count": len(packets),
        "issue_count": len(issues),
        "summary": {
            "by_state": normalize_counter(by_state),
            "by_source_kind": normalize_counter(by_source_kind),
            "session_episode_packets": by_source_kind.get("session_episode", 0),
        },
        "issues": issues,
        "packets": packets,
    }


def git_state(repo_root: Path) -> dict[str, Any]:
    if not (repo_root / ".git").exists():
        return {"repo": repo_root.name, "status": "not_git"}
    branch = run_command(["git", "branch", "--show-current"], cwd=repo_root, timeout=10)
    head = run_command(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=10)
    status = run_command(["git", "status", "--porcelain=v1"], cwd=repo_root, timeout=10)
    upstream = run_command(["git", "status", "--short", "--branch"], cwd=repo_root, timeout=10)
    dirty_lines = [line for line in str(status.get("stdout", "")).splitlines() if line.strip()]
    branch_lines = [line for line in str(upstream.get("stdout", "")).splitlines() if line.strip()]
    return {
        "repo": repo_root.name,
        "repo_path": repo_root.as_posix(),
        "status": "ok" if head["status"] == "ok" else "unavailable",
        "branch": str(branch.get("stdout", "")).strip() or None,
        "head": str(head.get("stdout", "")).strip() or None,
        "dirty_count": len(dirty_lines),
        "branch_status": branch_lines[0] if branch_lines else None,
    }


def build_workspace_git_summary(workspace_root: Path, *, max_depth: int = 4) -> dict[str, Any]:
    if not workspace_root.exists():
        return {"status": "unavailable", "reason": f"{workspace_root} does not exist", "repos": []}
    repos = build_local_eval_port_inventory.discover_repo_roots(workspace_root, max_depth=max_depth)
    states = [git_state(path) for path in repos]
    states.sort(key=lambda item: str(item.get("repo_path", item.get("repo", ""))))
    return {
        "status": "ok",
        "workspace_root": workspace_root.as_posix(),
        "repos": states,
        "summary": {
            "repos": len(states),
            "dirty_repos": sum(1 for item in states if int(item.get("dirty_count") or 0) > 0),
            "unavailable_repos": sum(1 for item in states if item.get("status") != "ok"),
        },
        "authority_boundary": "dirty and branch drift are freshness signals only; unrelated dirty files are not mutated by this read-model.",
    }


def selected_stack_root(explicit_stack_root: Path | None = None) -> Path | None:
    if explicit_stack_root and explicit_stack_root.as_posix():
        return explicit_stack_root
    for candidate in DEFAULT_STACK_ROOT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def build_mcp_runtime_status(
    workspace_root: Path,
    evals_root: Path,
    stack_root: Path | None,
    *,
    include_live_checks: bool,
    timeout: int,
) -> dict[str, Any]:
    if not include_live_checks:
        return {"status": "skipped", "reason": "live checks disabled"}
    if not stack_root or not stack_root.exists():
        return {"status": "unavailable", "reason": "abyss-stack checkout not found"}
    source_path = stack_root / "mcp" / "services" / "aoa-evals-mcp" / "src"
    if not source_path.exists():
        return {
            "status": "unavailable",
            "selected_stack_root": stack_root.as_posix(),
            "reason": "aoa-evals-mcp source path not found",
        }
    env = os.environ.copy()
    env["PYTHONPATH"] = str(source_path)
    result = run_json_command(
        [
            sys.executable,
            "-m",
            "aoa_evals_mcp.cli",
            "--workspace-root",
            workspace_root.as_posix(),
            "--evals-root",
            evals_root.as_posix(),
            "runtime-status",
        ],
        cwd=stack_root,
        env=env,
        timeout=timeout,
    )
    result["json"] = summarize_mcp_runtime_json(result.get("json"))
    result["selected_stack_root"] = stack_root.as_posix()
    result["source_path"] = source_path.as_posix()
    result["authority_boundary"] = "MCP runtime status is access-plane freshness, not proof acceptance."
    return result


def build_aoa_freshness(aoa_root: Path, *, include_live_checks: bool, timeout: int) -> dict[str, Any]:
    if not include_live_checks:
        return {"status": "skipped", "reason": "live checks disabled"}
    script = aoa_root / "scripts" / "aoa_session_memory.py"
    if not script.exists():
        return {"status": "unavailable", "reason": f"{script} not found"}
    result = run_command(
        [sys.executable, "scripts/aoa_session_memory.py", "maintenance-status", "--full"],
        cwd=aoa_root,
        timeout=timeout,
    )
    stdout = str(result.get("stdout", ""))
    payload = read_json_from_text(stdout)
    if isinstance(payload, dict):
        agent_route = payload.get("agent_route") if isinstance(payload.get("agent_route"), dict) else {}
        live_tail = payload.get("live_tail") if isinstance(payload.get("live_tail"), dict) else {}
        next_actions = payload.get("next_actions") if isinstance(payload.get("next_actions"), list) else []
        first_next_action = next_actions[0] if next_actions and isinstance(next_actions[0], dict) else {}
        result["json_summary"] = {
            "ok": payload.get("ok"),
            "recommendation": payload.get("recommendation"),
            "route_status": (payload.get("route") or {}).get("status")
            if isinstance(payload.get("route"), dict)
            else None,
            "agent_action": agent_route.get("action"),
            "can_use_graph_search": agent_route.get("can_use_graph_search"),
            "maintenance_required": agent_route.get("maintenance_required"),
            "live_catchup_pending": agent_route.get("live_catchup_pending"),
            "live_tail_status": live_tail.get("status") or agent_route.get("live_tail_status"),
            "live_tail_ready_count": live_tail.get("ready_count")
            or agent_route.get("live_tail_ready_count"),
            "live_tail_waiting_count": live_tail.get("waiting_count")
            or agent_route.get("live_tail_waiting_count"),
            "live_tail_next_ready_at": live_tail.get("next_ready_at")
            or agent_route.get("live_tail_next_ready_at"),
            "next_action_id": first_next_action.get("id"),
            "next_action_reason": first_next_action.get("reason"),
            "exact_next_command": payload.get("exact_next_command"),
            "diagnostics": payload.get("diagnostics", []),
        }
        result["next_route"] = payload.get("exact_next_command")
    result["stdout_line_count"] = len(stdout.splitlines())
    result["stderr_line_count"] = len(str(result.get("stderr", "")).splitlines())
    result.pop("stdout", None)
    result.pop("stderr", None)
    lower = stdout.lower()
    result["freshness_hints"] = {
        "mentions_stale": "stale" in lower,
        "mentions_indexed_archive_freshness": "indexed_archive_freshness" in lower,
        "line_count": len(stdout.splitlines()),
    }
    result["aoa_root"] = aoa_root.as_posix()
    result["authority_boundary"] = ".aoa provides session evidence and candidate-only refs, not reviewed eval truth."
    return result


def build_aoa_eval_runtime_adoption(
    skills_source_root: Path,
    installed_skills_root: Path,
    *,
    timeout: int = 30,
) -> dict[str, Any]:
    source_skill = skills_source_root / ".agents" / "skills" / "aoa-eval" / "SKILL.md"
    installed_skill = installed_skills_root / "aoa-eval" / "SKILL.md"
    runtime_index = skills_source_root / "generated" / "runtime_discovery_index.json"
    trigger_suite = skills_source_root / "evals" / "suites" / "aoa-eval-trigger-corpus.suite.md"
    trigger_report = (
        skills_source_root
        / "evals"
        / "reports"
        / "aoa-eval-prompt-trigger-harness-20260625.report.md"
    )
    source_hash = sha256_file(source_skill)
    installed_hash = sha256_file(installed_skill)
    runtime_payload = read_json(runtime_index, default={})
    runtime_mentions = False
    if isinstance(runtime_payload, dict):
        runtime_mentions = "aoa-eval" in json.dumps(runtime_payload, sort_keys=True)
    profile_verification = build_skill_pack_profile_verification(
        skills_source_root,
        installed_skills_root,
        timeout=timeout,
    )
    return {
        "source_skill_ref": source_skill.as_posix(),
        "installed_skill_ref": installed_skill.as_posix(),
        "source_exists": source_skill.exists(),
        "installed_exists": installed_skill.exists(),
        "source_sha256": source_hash,
        "installed_sha256": installed_hash,
        "installed_matches_source": source_hash is not None and source_hash == installed_hash,
        "runtime_discovery_index_ref": runtime_index.as_posix(),
        "runtime_discovery_mentions_aoa_eval": runtime_mentions,
        "installed_profile": DEFAULT_AOA_EVAL_INSTALL_PROFILE,
        "installed_profile_verified": profile_verification.get("verified") is True,
        "installed_profile_verification": profile_verification,
        "trigger_suite_ref": trigger_suite.as_posix(),
        "trigger_suite_exists": trigger_suite.exists(),
        "trigger_report_ref": trigger_report.as_posix(),
        "trigger_report_exists": trigger_report.exists(),
        "prompt_visible_live_check": "external_live_check_required",
        "front_door_invoke_capable": "covered_by_aoa_skills_prompt_trigger_harness_when_command_passes",
        "subskills_posture": "manual_or_skill-local; root aoa-eval route remains the trigger surface",
        "verification_command": "python -m pytest -q tests/test_aoa_eval_prompt_trigger_harness.py",
        "authority_boundary": "aoa-skills owns trigger/runtime adoption; aoa-evals records read-only evidence only.",
    }


def build_skill_pack_profile_verification(
    skills_source_root: Path,
    installed_skills_root: Path,
    *,
    timeout: int = 30,
) -> dict[str, Any]:
    verifier = skills_source_root / "scripts" / "verify_skill_pack.py"
    command = [
        sys.executable,
        "scripts/verify_skill_pack.py",
        "--repo-root",
        ".",
        "--profile",
        DEFAULT_AOA_EVAL_INSTALL_PROFILE,
        "--install-root",
        installed_skills_root.as_posix(),
        "--format",
        "json",
    ]
    result: dict[str, Any] = {
        "profile": DEFAULT_AOA_EVAL_INSTALL_PROFILE,
        "verifier_ref": verifier.as_posix(),
        "install_root": installed_skills_root.as_posix(),
        "command": "python scripts/verify_skill_pack.py --repo-root . --profile "
        f"{DEFAULT_AOA_EVAL_INSTALL_PROFILE} --install-root {installed_skills_root.as_posix()} --format json",
        "authority_boundary": "aoa-skills owns profile verification; aoa-evals stores the read-only routing signal.",
    }
    if not verifier.exists():
        result.update(
            {
                "status": "unavailable",
                "verified": False,
                "reason": "aoa-skills verify_skill_pack.py is unavailable",
            }
        )
        return result

    completed = run_json_command(command, cwd=skills_source_root, timeout=timeout)
    payload = completed.get("json")
    result.update(
        {
            "status": completed.get("status"),
            "returncode": completed.get("returncode"),
            "stdout_line_count": completed.get("stdout_line_count"),
            "stderr_line_count": completed.get("stderr_line_count"),
        }
    )
    if not isinstance(payload, dict):
        result["verified"] = False
        result["reason"] = "verifier output was not parseable JSON"
        return result

    skills = payload.get("skills") if isinstance(payload.get("skills"), list) else []
    aoa_eval_entry = next(
        (
            skill
            for skill in skills
            if isinstance(skill, dict) and skill.get("name") == "aoa-eval"
        ),
        {},
    )
    missing = payload.get("missing_skills") if isinstance(payload.get("missing_skills"), list) else []
    mismatched = (
        payload.get("mismatched_skills")
        if isinstance(payload.get("mismatched_skills"), list)
        else []
    )
    extra = payload.get("extra_skill_dirs") if isinstance(payload.get("extra_skill_dirs"), list) else []
    result.update(
        {
            "verified": payload.get("verified") is True,
            "profile_revision": payload.get("profile_revision"),
            "expected_skill_count": payload.get("expected_skill_count"),
            "verified_skill_count": payload.get("verified_skill_count"),
            "missing_skill_count": len(missing),
            "mismatched_skill_count": len(mismatched),
            "missing_skills": missing,
            "mismatched_skills": mismatched,
            "extra_skill_dirs": extra,
            "aoa_eval_install_state": aoa_eval_entry.get("install_state"),
            "aoa_eval_is_symlink": aoa_eval_entry.get("is_symlink"),
            "aoa_eval_source_digest": aoa_eval_entry.get("source_digest"),
            "aoa_eval_target_digest": aoa_eval_entry.get("target_digest"),
            "release_identity": payload.get("release_identity"),
        }
    )
    return result


def candidate_entry(
    *,
    candidate_id: str,
    source_kind: str,
    source_ref: str,
    state: str,
    owner_repo: str,
    route: str,
    evidence_count: int,
    boundary: str,
    review_gate: str = "owner_review_required",
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if state not in CANDIDATE_QUEUE_STATES:
        raise ValueError(f"unsupported candidate state: {state}")
    entry = {
        "candidate_id": candidate_id,
        "source_kind": source_kind,
        "source_ref": source_ref,
        "state": state,
        "owner_repo": owner_repo,
        "next_route": route,
        "evidence_count": evidence_count,
        "review_gate": review_gate,
        "authority_boundary": boundary,
        "proof_authority": False,
        "promotion_allowed": False,
    }
    if extra:
        entry.update(extra)
    return entry


def owner_repo_from_refs(refs: Any) -> str:
    if not isinstance(refs, list):
        return "aoa-evals"
    text = " ".join(str(item) for item in refs)
    owners: list[str] = []
    if "docs/" in text or "scripts/" in text or "mechanics/" in text or "AGENTS.md" in text:
        owners.append("aoa-evals")
    if ".aoa" in text:
        owners.append(".aoa")
    if "aoa-skills" in text:
        owners.append("aoa-skills")
    if "abyss-stack" in text:
        owners.append("abyss-stack")
    if not owners:
        owners.append("aoa-evals")
    return " + ".join(dict.fromkeys(owners))


def short_join(values: Any, *, limit: int = 3) -> str:
    if isinstance(values, list):
        rendered = [str(item) for item in values[:limit]]
        if len(values) > limit:
            rendered.append(f"+{len(values) - limit} more")
        return "; ".join(rendered)
    if values is None:
        return ""
    return str(values)


def candidate_entry_from_packet(record: dict[str, Any]) -> dict[str, Any]:
    payload = record.get("payload") if isinstance(record, dict) else {}
    if not isinstance(payload, dict):
        raise ValueError("candidate packet record payload must be an object")
    state = str(payload.get("candidate_state") or "deferred")
    if state not in CANDIDATE_QUEUE_STATES:
        state = "deferred"
    evidence_refs = payload.get("evidence_refs")
    freshness_refs = payload.get("freshness_refs")
    owner_refs = payload.get("owner_surface_refs")
    promotion_gates = payload.get("promotion_forbidden_until")
    packet_ref = str(record.get("path") or "")
    return candidate_entry(
        candidate_id=f"packet:{payload.get('packet_id', packet_ref)}",
        source_kind=str(payload.get("source_kind") or "candidate_packet"),
        source_ref=str(payload.get("source_ref") or packet_ref),
        state=state,
        owner_repo=owner_repo_from_refs(owner_refs),
        route=str(payload.get("next_step") or payload.get("expected_aoa_eval_route") or "owner_review_required"),
        evidence_count=len(evidence_refs) if isinstance(evidence_refs, list) else 0,
        boundary="schema-valid candidate packet only; proof adoption remains forbidden until owner review",
        review_gate=short_join(promotion_gates) or "owner_review_required",
        extra={
            "packet_ref": packet_ref,
            "trigger_class_id": payload.get("trigger_class_id"),
            "expected_aoa_eval_route": payload.get("expected_aoa_eval_route"),
            "candidate_state_reason": payload.get("candidate_state_reason"),
            "owner_surface_refs": owner_refs if isinstance(owner_refs, list) else [],
            "freshness_refs": freshness_refs if isinstance(freshness_refs, list) else [],
            "evaluator_fit": payload.get("evaluator_fit"),
            "dedupe_key": f"{payload.get('trigger_class_id')}::{payload.get('source_ref')}",
        },
    )


def build_candidate_queue(
    local_inventory: dict[str, Any],
    runtime_candidates: dict[str, Any],
    catalog_summary: dict[str, Any],
    candidate_packets: dict[str, Any] | None = None,
) -> dict[str, Any]:
    local_inventory = (
        build_local_eval_port_inventory.normalize_inventory_for_suite_consumers(
            local_inventory
        )
    )
    entries: list[dict[str, Any]] = []
    packet_records = (
        candidate_packets.get("packets", [])
        if isinstance(candidate_packets, dict)
        else []
    )
    if isinstance(packet_records, list):
        for record in packet_records:
            if isinstance(record, dict):
                entries.append(candidate_entry_from_packet(record))
    repos = local_inventory.get("repos", []) if isinstance(local_inventory, dict) else []
    if isinstance(repos, list):
        for repo in repos:
            if not isinstance(repo, dict):
                continue
            counts = repo.get("pressure_counts")
            if not isinstance(counts, dict):
                continue
            active_total = int(counts.get("active_total") or 0)
            if active_total <= 0:
                continue
            repo_id = str(repo.get("repo_id", repo.get("repo", "unknown")))
            route = repo.get("route_recommendation") if isinstance(repo.get("route_recommendation"), dict) else {}
            central_matches = repo.get("central_eval_name_matches")
            has_central_overlap = isinstance(central_matches, list) and bool(central_matches)
            state = "duplicate_existing_eval" if has_central_overlap else "needs_owner_review"
            entries.append(
                candidate_entry(
                    candidate_id=f"local-port:{repo_id}",
                    source_kind="local_eval_port",
                    source_ref=str(repo.get("evals_path") or repo.get("repo_path") or repo_id),
                    state=state,
                    owner_repo=repo_id,
                    route=str(route.get("route_key", "inspect_local_port")),
                    evidence_count=active_total,
                    boundary="local pressure only; no central proof adoption without aoa-evals owner review",
                    review_gate="repo_local_owner_review_then_aoa_evals_overlap_check",
                )
            )
    runtime_count = int(runtime_candidates.get("count") or 0)
    if runtime_count:
        entries.append(
            candidate_entry(
                candidate_id="runtime-candidates:aoa-evals",
                source_kind="runtime_candidate_export",
                source_ref=str(runtime_candidates.get("source_ref")),
                state="observed",
                owner_repo="abyss-stack + aoa-evals",
                route="needs_owner_review_before_any_proof_meaning",
                evidence_count=runtime_count,
                boundary="runtime exports remain candidate-only and cannot create central bundles",
                review_gate="runtime_owner_review_then_aoa_evals_owner_review",
            )
        )
    session_packet_count = 0
    if isinstance(packet_records, list):
        session_packet_count = sum(
            1
            for record in packet_records
            if isinstance(record, dict)
            and isinstance(record.get("payload"), dict)
            and record["payload"].get("source_kind") == "session_episode"
        )
    if session_packet_count == 0:
        entries.append(
            candidate_entry(
                candidate_id="session-mining:criteria-gated",
                source_kind="session_memory_candidate",
                source_ref=".aoa session archive refs after manual criteria sampling",
                state="deferred",
                owner_repo=".aoa + aoa-evals",
                route="manual_review_20_to_50_episodes_reject_garbage_before_queue_import",
                evidence_count=0,
                boundary="session memory can propose candidates only; reviewed truth stays with source owners",
                review_gate="manual_episode_review_with_reject_accounting",
            )
        )
    entries.sort(key=lambda item: str(item["candidate_id"]))
    by_state: Counter[str] = Counter(str(entry["state"]) for entry in entries)
    by_source_kind: Counter[str] = Counter(str(entry["source_kind"]) for entry in entries)
    packet_count = (
        int(candidate_packets.get("packet_count") or 0)
        if isinstance(candidate_packets, dict)
        else 0
    )
    return {
        "schema_version": "os_abyss_eval_candidate_queue_v1",
        "authority_boundary": (
            "Central queue is a read-only candidate index over local ports, runtime exports, "
            "session candidates, and quest lineage. It cannot promote proof."
        ),
        "allowed_states": list(CANDIDATE_QUEUE_STATES),
        "lifecycle": [
            {
                "state": "observed",
                "entry_gate": "candidate evidence ref exists",
                "exit_gate": "owner and duplicate route inspected",
            },
            {
                "state": "needs_owner_review",
                "entry_gate": "owner surface refs are known",
                "exit_gate": "local-only, duplicate, central-draft, rejected, or deferred decision recorded",
            },
            {
                "state": "duplicate_existing_eval",
                "entry_gate": "central catalog overlap found",
                "exit_gate": "select/apply existing eval before new design",
            },
            {
                "state": "local_only",
                "entry_gate": "repo-local pressure should stay local",
                "exit_gate": "local suite/report/intake reviewed by repo owner",
            },
            {
                "state": "central_draft",
                "entry_gate": "human owner accepts central draft design pressure",
                "exit_gate": "source bundle review and catalog regeneration",
            },
            {
                "state": "rejected",
                "entry_gate": "manual or owner review found garbage, duplicate, stale, or out-of-scope evidence",
                "exit_gate": "closed as candidate; no proof meaning",
            },
            {
                "state": "deferred",
                "entry_gate": "freshness, owner, privacy, or evidence gap blocks current review",
                "exit_gate": "gap is resolved and candidate is re-reviewed",
            },
            {
                "state": "accepted",
                "entry_gate": "central owner acceptance after source review",
                "exit_gate": "catalog/report/release validation; not created by this read-model",
            },
        ],
        "evidence_minimums": [
            "source_kind",
            "source_ref",
            "owner_repo",
            "owner_surface_refs when known",
            "freshness_ref when route depends on generated/runtime/session evidence",
            "packet_ref when imported from a candidate packet",
            "next_route",
            "review_gate",
        ],
        "anti_promotion_checks": [
            "candidate.promotion_allowed must stay false in this read-model",
            "session-mining candidates require manual reviewed_keep before import",
            "runtime exports require runtime owner and aoa-evals owner review before proof meaning",
            "local ports require central overlap check before central draft",
            "packet imports remain candidate-only even when schema-valid",
        ],
        "candidate_packet_import": {
            "packet_root": candidate_packets.get("packet_root") if isinstance(candidate_packets, dict) else CANDIDATE_PACKET_RELATIVE.as_posix(),
            "packet_count": packet_count,
            "issue_count": candidate_packets.get("issue_count") if isinstance(candidate_packets, dict) else 0,
            "summary": candidate_packets.get("summary", {}) if isinstance(candidate_packets, dict) else {},
            "authority_boundary": "packet import is routing evidence only and cannot create proof meaning",
        },
        "summary": {
            "entries": len(entries),
            "by_state": normalize_counter(by_state),
            "by_source_kind": normalize_counter(by_source_kind),
            "packet_count": packet_count,
            "session_packet_count": session_packet_count,
            "session_mining_reviewed_count": SESSION_MINING_STATUS.get("reviewed_count"),
            "session_mining_report_refs": SESSION_MINING_STATUS.get("report_refs", []),
            "central_catalog_total_evals": catalog_summary.get("total_evals"),
        },
        "entries": entries,
    }


def load_eval_forge_module(evals_root: Path) -> tuple[Any | None, str | None]:
    script_path = evals_root / EVAL_FORGE_SCRIPT_RELATIVE
    if not script_path.is_file():
        return None, f"{EVAL_FORGE_SCRIPT_RELATIVE.as_posix()} is missing"
    script_dir = script_path.parent.as_posix()
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("aoa_eval_forge_route_readiness", script_path)
    if spec is None or spec.loader is None:
        return None, f"cannot load {EVAL_FORGE_SCRIPT_RELATIVE.as_posix()}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - defensive readiness reporting
        return None, f"cannot import eval forge router: {exc}"
    return module, None


def build_eval_forge_readiness(
    evals_root: Path,
    candidate_packets: dict[str, Any],
) -> dict[str, Any]:
    module, import_error = load_eval_forge_module(evals_root)
    registry = read_json(evals_root / EVAL_FORGE_REGISTRY_RELATIVE, default={})
    archetypes = registry.get("archetypes", []) if isinstance(registry, dict) else []
    if not isinstance(archetypes, list):
        archetypes = []
    route_kind_counts = Counter(
        str(item.get("route_kind", "unknown"))
        for item in archetypes
        if isinstance(item, dict)
    )
    registry_errors: list[str] = []
    if module is not None:
        try:
            loaded_registry, registry_errors = module.load_registry(evals_root)
            archetypes = loaded_registry.get("archetypes", [])
            if not isinstance(archetypes, list):
                archetypes = []
            route_kind_counts = Counter(
                str(item.get("route_kind", "unknown"))
                for item in archetypes
                if isinstance(item, dict)
            )
        except Exception as exc:  # pragma: no cover - defensive readiness reporting
            registry_errors = [str(exc)]
    elif import_error:
        registry_errors = [import_error]

    packet_records = (
        candidate_packets.get("packets", [])
        if isinstance(candidate_packets, dict)
        else []
    )
    candidate_hints: list[dict[str, Any]] = []
    if module is not None and isinstance(packet_records, list):
        for record in packet_records[:8]:
            if not isinstance(record, dict) or not isinstance(record.get("payload"), dict):
                continue
            packet_ref = str(record.get("path") or "")
            packet = record["payload"]
            candidate_id = f"packet:{packet.get('packet_id', packet_ref)}"
            try:
                case = module.candidate_packet_case(packet, packet_path=packet_ref)
                route = module.build_forge_route(case=case, repo_root=evals_root)
                worksheet = route.get("worksheet", {}) if isinstance(route, dict) else {}
                owner_route = route.get("owner_route", {}) if isinstance(route, dict) else {}
                admissibility = route.get("candidate_admissibility", {}) if isinstance(route, dict) else {}
                candidate_hints.append(
                    {
                        "candidate_id": candidate_id,
                        "packet_ref": packet_ref,
                        "decision": admissibility.get("decision"),
                        "reason": admissibility.get("reason"),
                        "selected_archetype_id": route.get("selected_archetype_id"),
                        "owner_repo": owner_route.get("owner_repo"),
                        "route_key": owner_route.get("route_key"),
                        "missing_evidence": admissibility.get("missing_evidence", []),
                        "exact_next_command": owner_route.get("recommended_next_command"),
                        "proof_authority": worksheet.get("proof_authority"),
                        "promotion_allowed": worksheet.get("promotion_allowed"),
                    }
                )
            except Exception as exc:  # pragma: no cover - defensive readiness reporting
                candidate_hints.append(
                    {
                        "candidate_id": candidate_id,
                        "packet_ref": packet_ref,
                        "decision": "defer",
                        "reason": f"forge route failed: {exc}",
                        "selected_archetype_id": None,
                        "missing_evidence": ["forge_route_failed"],
                        "proof_authority": False,
                        "promotion_allowed": False,
                    }
                )

    external_grounding = load_external_research_grounding(evals_root)
    front_door_refs = {
        "operating_path_ref": EVAL_FORGE_OPERATING_PATH_RELATIVE.as_posix(),
        "session_mining_criteria_ref": EVAL_FORGE_SESSION_MINING_CRITERIA_RELATIVE.as_posix(),
        "local_port_decision_matrix_ref": EVAL_FORGE_LOCAL_PORT_MATRIX_RELATIVE.as_posix(),
        "latest_route_review_report_ref": EVAL_FORGE_ROUTE_REVIEW_REPORT_RELATIVE.as_posix(),
        "worksheet_example_ref": EVAL_FORGE_WORKSHEET_EXAMPLE_RELATIVE.as_posix(),
        "candidate_packet_schema_ref": (
            "mechanics/audit/parts/candidate-readers/schemas/"
            "aoa-eval-candidate-packet.schema.json"
        ),
        "local_suite_execution_schema_ref": LOCAL_SUITE_EXECUTION_SCHEMA_RELATIVE.as_posix(),
    }
    missing_front_door_refs = [
        ref for ref in front_door_refs.values() if not (evals_root / ref).is_file()
    ]
    front_door_commands = [
        {
            "purpose": "raise the per-session Eval Forge front door",
            "command": "python scripts/aoa_eval_session_start.py --json",
        },
        {
            "purpose": "check front-door readiness gates and blockers",
            "command": "python scripts/check_eval_forge_readiness.py --json",
        },
        {
            "purpose": "inspect active/skeleton/missing/invalid local eval ports",
            "command": "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
        },
        {
            "purpose": "validate imported candidate packets before review",
            "command": "python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
        },
        {
            "purpose": "route a session candidate packet through Eval Forge",
            "command": (
                "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
                "--candidate-packet <path> --json"
            ),
        },
        {
            "purpose": "route one active local eval port through Eval Forge",
            "command": (
                "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
                "--local-port-repo <repo_id> "
                "--local-port-inventory /tmp/aoa_local_eval_ports.current.json "
                "--workspace-root /srv/AbyssOS --json"
            ),
        },
        {
            "purpose": "write a non-proof owner-review worksheet only after admission gates",
            "command": (
                "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
                "--candidate-packet <path> --write-worksheet <worksheet-path> --json"
            ),
        },
    ]
    return {
        "schema_version": "os_abyss_eval_forge_readiness_v1",
        "authority_boundary": (
            "Eval Forge is a design router and worksheet layer. It cannot accept proof, "
            "score evidence, create baselines, promote candidates, mutate local ports, "
            "or execute local suite runner argv."
        ),
        "local_suite_execution_boundary": {
            "state_vocabulary": ["absent", "invalid", "stale", "ready"],
            "aggregate_priority": ["invalid", "stale", "ready", "absent"],
            "readiness_scope": "source-contract-ready",
            "runtime_reproducibility_proven": False,
            "jit_revalidation_required": True,
            "execution_receipt_required": True,
            "environment_capture_required": True,
            "execution_allowed": False,
            "owner_apply_required": True,
            "proof_authority": False,
            "promotion_allowed": False,
        },
        "registry_ref": EVAL_FORGE_REGISTRY_RELATIVE.as_posix(),
        "worksheet_schema_ref": EVAL_FORGE_WORKSHEET_SCHEMA_RELATIVE.as_posix(),
        "external_pattern_grounding_ref": EVAL_FORGE_EXTERNAL_GROUNDING_RELATIVE.as_posix(),
        "front_door_refs": front_door_refs,
        "front_door_commands": front_door_commands,
        "front_door_surface_status": {
            "valid": not missing_front_door_refs,
            "missing_refs": missing_front_door_refs,
            "proof_authority": False,
            "promotion_allowed": False,
        },
        "router_command": (
            "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
            "--candidate-packet <path> --json"
        ),
        "local_port_pressure_hint_command": (
            "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
            "--local-port-repo <repo_id> "
            "--local-port-inventory /tmp/aoa_local_eval_ports.current.json "
            "--workspace-root /srv/AbyssOS --json"
        ),
        "worksheet_write_command": (
            "python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py "
            "--candidate-packet <path> --write-worksheet <worksheet-path> --json"
        ),
        "registry_validation": {
            "valid": not registry_errors,
            "errors": registry_errors,
            "archetype_count": len(archetypes),
        },
        "archetype_count": len(archetypes),
        "archetype_ids": [
            str(item.get("id"))
            for item in archetypes
            if isinstance(item, dict) and item.get("id")
        ],
        "by_route_kind": normalize_counter(route_kind_counts),
        "external_patterns_count": len(external_grounding),
        "candidate_archetype_hints": candidate_hints,
        "stop_lines": [
            "check existing central/local eval surfaces before new source authoring",
            "keep candidate packets, local ports, MCP exports, and dashboards non-proof",
            "treat .suite.md as a note; only a ready sidecar can route to owner/apply",
            "inventory, Eval Forge, readiness, dashboard, session-start, promotion review, and MCP never execute runner.argv",
            "write worksheets only after admission gates; write source bundles only after human owner acceptance",
            "refresh external grounding when eval tooling patterns materially change",
        ],
    }


def pressure_total(repo: dict[str, Any]) -> int:
    counts = repo.get("pressure_counts")
    if not isinstance(counts, dict):
        return 0
    return int(counts.get("active_total") or 0)


def pressure_severity(active_total: int, inventory_status: str) -> str:
    if inventory_status == "invalid":
        return "blocked"
    if active_total >= 5:
        return "high"
    if active_total >= 2:
        return "medium"
    if active_total == 1:
        return "low"
    return "none"


def git_state_for_repo(repo: dict[str, Any], git_summary: dict[str, Any]) -> dict[str, Any] | None:
    repo_path = str(repo.get("root") or "")
    repo_id = str(repo.get("repo_id") or repo.get("repo") or "")
    repos = git_summary.get("repos") if isinstance(git_summary, dict) else None
    if not isinstance(repos, list):
        return None
    for item in repos:
        if not isinstance(item, dict):
            continue
        if item.get("repo_path") == repo_path or item.get("repo") == repo_id:
            return item
    return None


def freshness_gate_for_repo(
    repo: dict[str, Any],
    git_summary: dict[str, Any],
    mcp_runtime_status: dict[str, Any],
    aoa_freshness: dict[str, Any],
) -> dict[str, Any]:
    warnings: list[str] = []
    blocks: list[str] = []
    git_state = git_state_for_repo(repo, git_summary)
    if git_state is None:
        warnings.append("repo_git_state_missing_from_workspace_summary")
    elif git_state.get("status") != "ok":
        warnings.append("repo_git_state_unavailable")
    elif int(git_state.get("dirty_count") or 0) > 0:
        warnings.append("repo_has_dirty_worktree")

    mcp_json = mcp_runtime_status.get("json") if isinstance(mcp_runtime_status, dict) else None
    freshness = mcp_json.get("freshness") if isinstance(mcp_json, dict) else None
    if isinstance(freshness, dict) and freshness.get("mirror_is_stale") is True:
        warnings.append("aoa_evals_mcp_mirror_stale")
    if mcp_runtime_status.get("status") in {"failed", "timeout", "unparseable"}:
        warnings.append("mcp_runtime_status_unhealthy")

    if aoa_freshness.get("status") in {"failed", "timeout", "unparseable", "unavailable"}:
        warnings.append("aoa_session_memory_freshness_unhealthy")

    if repo.get("inventory_status") == "invalid" or repo.get("validator_ok") is False:
        blocks.append("invalid_local_eval_port")
    suite_execution = repo.get("suite_execution")
    suite_state = (
        str(suite_execution.get("state") or "absent")
        if isinstance(suite_execution, dict)
        else "absent"
    )
    if suite_state == "invalid":
        blocks.append("invalid_local_suite_execution_contract")
    elif suite_state == "stale":
        blocks.append("stale_local_suite_execution_contract")

    return {
        "status": "blocked" if blocks else ("warning" if warnings else "ok"),
        "blocks_eval_route": bool(blocks),
        "warnings": warnings,
        "blocks": blocks,
        "refs": {
            "git_head": git_state.get("head") if isinstance(git_state, dict) else None,
            "git_branch": git_state.get("branch") if isinstance(git_state, dict) else None,
            "mcp_status": mcp_runtime_status.get("status"),
            "aoa_freshness_status": aoa_freshness.get("status"),
        },
    }


def repo_readiness_state(repo: dict[str, Any], freshness_gate: dict[str, Any]) -> str:
    suite_execution = repo.get("suite_execution")
    suite_state = (
        str(suite_execution.get("state") or "absent")
        if isinstance(suite_execution, dict)
        else "absent"
    )
    if suite_state == "invalid":
        return "repair_invalid_local_suite_execution_contract"
    if suite_state == "stale":
        return "refresh_stale_local_suite_execution_contract"
    if freshness_gate.get("blocks_eval_route"):
        return "blocked_by_freshness_or_invalid_port"
    active_total = pressure_total(repo)
    central_matches = repo.get("central_eval_name_matches")
    has_central_overlap = isinstance(central_matches, list) and bool(central_matches)
    route = repo.get("route_recommendation") if isinstance(repo.get("route_recommendation"), dict) else {}
    route_key = str(route.get("route_key", ""))
    if active_total <= 0:
        return "dormant_no_current_eval_pressure"
    if has_central_overlap:
        return "apply_existing_eval_or_duplicate_review"
    if suite_state == "ready" and ("suite" in route_key or "regression" in route_key):
        return "apply_local_suite_or_regression_check"
    if "intake" in route_key or "design" in route_key:
        return "needs_local_design_or_owner_review"
    return "needs_human_review"


def repo_route_confidence(repo: dict[str, Any], route_state: str, freshness_gate: dict[str, Any]) -> str:
    if freshness_gate.get("blocks_eval_route"):
        return "blocked"
    if route_state == "dormant_no_current_eval_pressure":
        return "high"
    if freshness_gate.get("status") == "warning":
        return "medium"
    if repo.get("validator_ok") is True and pressure_total(repo) > 0:
        return "high"
    return "medium"


def exact_next_command_for_repo(repo: dict[str, Any], workspace_root: Path) -> str:
    repo_id = str(repo.get("repo_id") or repo.get("repo") or "")
    escaped = repo_id.replace('"', '\\"')
    return (
        "python scripts/build_local_eval_port_inventory.py "
        f"--workspace-root {workspace_root.as_posix()} --json "
        f"| jq '.repos[] | select(.repo_id == \"{escaped}\")'"
    )


def suite_execution_readiness(repo: dict[str, Any]) -> dict[str, Any]:
    execution = repo.get("suite_execution")
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
        "invalid_count": int(execution.get("invalid_count") or 0),
        "stale_count": int(execution.get("stale_count") or 0),
        "ready_count": int(execution.get("ready_count") or len(ready_suites)),
        "ready_suites": ready_suites,
        "readiness_scope": str(execution.get("readiness_scope") or "source-contract-ready"),
        "runtime_reproducibility_proven": False,
        "jit_revalidation_required": True,
        "execution_receipt_required": True,
        "environment_capture_required": True,
        "execution_allowed": False,
        "owner_apply_required": state == "ready",
        "readiness_executed_runner": False,
        "proof_authority": False,
        "promotion_allowed": False,
    }


def build_repo_readiness(
    local_inventory: dict[str, Any],
    *,
    workspace_root: Path,
    git_summary: dict[str, Any],
    mcp_runtime_status: dict[str, Any],
    aoa_freshness: dict[str, Any],
) -> dict[str, Any]:
    local_inventory = (
        build_local_eval_port_inventory.normalize_inventory_for_suite_consumers(
            local_inventory
        )
    )
    repos = local_inventory.get("repos", []) if isinstance(local_inventory, dict) else []
    readiness: list[dict[str, Any]] = []
    by_state: Counter[str] = Counter()
    by_severity: Counter[str] = Counter()
    by_confidence: Counter[str] = Counter()
    by_suite_execution_state: Counter[str] = Counter()
    if isinstance(repos, list):
        for repo in repos:
            if not isinstance(repo, dict):
                continue
            active_total = pressure_total(repo)
            inventory_status = str(repo.get("inventory_status") or repo.get("declared_status") or "unknown")
            freshness_gate = freshness_gate_for_repo(repo, git_summary, mcp_runtime_status, aoa_freshness)
            route_state = repo_readiness_state(repo, freshness_gate)
            severity = pressure_severity(active_total, inventory_status)
            confidence = repo_route_confidence(repo, route_state, freshness_gate)
            by_state[route_state] += 1
            by_severity[severity] += 1
            by_confidence[confidence] += 1
            route = repo.get("route_recommendation") if isinstance(repo.get("route_recommendation"), dict) else {}
            suite_execution = suite_execution_readiness(repo)
            by_suite_execution_state[str(suite_execution["state"])] += 1
            readiness.append(
                {
                    "repo_id": repo.get("repo_id") or repo.get("repo"),
                    "repo_path": repo.get("repo_path"),
                    "inventory_status": inventory_status,
                    "pressure_severity": severity,
                    "active_pressure_count": active_total,
                    "route_state": route_state,
                    "route_confidence": confidence,
                    "route_key": route.get("route_key"),
                    "route_action": route.get("action"),
                    "freshness_gate": freshness_gate,
                    "central_eval_name_matches": repo.get("central_eval_name_matches", []),
                    "suite_execution": suite_execution,
                    "exact_next_command": exact_next_command_for_repo(repo, workspace_root),
                    "safe_actions": [
                        "inspect_local_port_inventory",
                        "select_existing_central_eval_before_new_design",
                        "keep_candidate_only_until_owner_review",
                        "route_ready_suite_to_repo_owner_or_aoa_eval_apply",
                    ],
                    "forbidden_actions": [
                        "central_proof_acceptance_from_local_port",
                        "mcp_auto_promotion",
                        "session_memory_as_reviewed_truth",
                        "readiness_or_dashboard_executes_runner_argv",
                    ],
                }
            )
    readiness.sort(
        key=lambda item: (
            {"blocked": 0, "high": 1, "medium": 2, "low": 3, "none": 4}.get(
                str(item["pressure_severity"]), 9
            ),
            str(item.get("repo_id")),
        )
    )
    actionable = [
        item
        for item in readiness
        if item["route_state"]
        in {
            "blocked_by_freshness_or_invalid_port",
            "apply_existing_eval_or_duplicate_review",
            "apply_local_suite_or_regression_check",
            "repair_invalid_local_suite_execution_contract",
            "refresh_stale_local_suite_execution_contract",
            "needs_local_design_or_owner_review",
            "needs_human_review",
        }
    ]
    return {
        "schema_version": "os_abyss_eval_repo_readiness_v1",
        "authority_boundary": "Per-repo readiness routes local eval pressure; it does not mutate repos, execute local suites, or accept proof.",
        "summary": {
            "repos": len(readiness),
            "actionable_repos": len(actionable),
            "by_route_state": normalize_counter(by_state),
            "by_pressure_severity": normalize_counter(by_severity),
            "by_route_confidence": normalize_counter(by_confidence),
            "by_suite_execution_state": normalize_counter(by_suite_execution_state),
        },
        "repos": readiness,
    }


def build_promotion_path() -> dict[str, Any]:
    return {
        "schema_version": "local_to_central_eval_promotion_path_v1",
        "authority_boundary": "MCP and local queue may route review but cannot create accepted central proof.",
        "states": [
            "local_observed",
            "local_owner_review",
            "central_overlap_check",
            "central_draft_proposed",
            "source_bundle_review",
            "report_or_fixture_contract_review",
            "human_owner_acceptance",
            "central_catalog_regeneration",
            "release_or_advisory_validation",
        ],
        "owner_gates": [
            {
                "gate": "local_owner_review",
                "owner": "repo-local evals/",
                "requires": ["PORT.yaml validity", "intake/suite/report refs", "non-proof boundary wording"],
            },
            {
                "gate": "central_overlap_check",
                "owner": "aoa-evals",
                "requires": ["generated/eval_catalog.json", "EVAL_SELECTION.md", "duplicate/adjacent eval review"],
            },
            {
                "gate": "source_bundle_review",
                "owner": "aoa-evals",
                "requires": ["EVAL.md", "eval.yaml", "bundle-local support contracts as relevant"],
            },
            {
                "gate": "runtime_or_session_evidence_review",
                "owner": "abyss-stack or .aoa plus aoa-evals",
                "requires": ["candidate-only evidence refs", "freshness refs", "human review before proof meaning"],
            },
        ],
        "forbidden_shortcuts": [
            "MCP creates central bundle",
            "local report becomes central verdict",
            "session memory becomes reviewed truth",
            "runtime candidate export becomes accepted proof",
            "dirty sibling checkout silently changes release identity",
        ],
    }


def build_trajectory_eval_slice() -> dict[str, Any]:
    return {
        "slice_id": "aoa_eval_route_selection_v1",
        "purpose": "Check whether an agent routes eval-lane pressure through existing central evals, local ports, freshness checks, and candidate-only boundaries before designing new proof.",
        "source_eval_refs": [
            "evals/workflow/aoa-tool-trajectory-discipline/EVAL.md",
            "evals/workflow/aoa-trace-outcome-separation/EVAL.md",
            "evals/capability/aoa-eval-integrity-check/EVAL.md",
        ],
        "external_harness": {
            "owner_repo": "aoa-skills",
            "command": "python -m pytest -q tests/test_aoa_eval_prompt_trigger_harness.py",
            "claim_limit": "trigger visibility and route prompt harness only; not central proof acceptance",
        },
        "deterministic_harness": {
            "owner_repo": "aoa-evals",
            "command": "python scripts/run_aoa_eval_route_trajectory_harness.py --json",
            "claim_limit": "route trajectory and stop-line coverage only; not central proof acceptance, scoring, or candidate promotion",
        },
        "deterministic_cases": [
            {
                "case_id": "local_pressure_before_design",
                "given": "repo-local evals/intake pressure exists",
                "expect": "agent inspects local port and central catalog before proposing new central bundle",
            },
            {
                "case_id": "central_overlap_first",
                "given": "local pressure overlaps an existing central eval",
                "expect": "agent applies/selects existing eval route before local duplicate design",
            },
            {
                "case_id": "stale_runtime_surface",
                "given": "MCP/root/read-model freshness is stale or unknown",
                "expect": "agent runs freshness sentinel or marks candidate deferred before proof claims",
            },
            {
                "case_id": "session_candidate_only",
                "given": ".aoa session episode suggests eval opportunity",
                "expect": "agent emits criteria-scored candidate packet, not proof adoption",
            },
        ],
        "next_route": "promote to a bounded source eval only after deterministic trace packet examples and owner review.",
    }


def build_freshness_sentinel(
    *,
    local_inventory: dict[str, Any],
    mcp_runtime_status: dict[str, Any],
    aoa_freshness: dict[str, Any],
    git_summary: dict[str, Any],
    support_registry: dict[str, Any],
) -> dict[str, Any]:
    dirty_repos = []
    summary = git_summary.get("summary") if isinstance(git_summary, dict) else {}
    if isinstance(git_summary.get("repos"), list):
        dirty_repos = [
            {
                "repo": item.get("repo"),
                "branch": item.get("branch"),
                "head": item.get("head"),
                "dirty_count": item.get("dirty_count"),
            }
            for item in git_summary["repos"]
            if isinstance(item, dict) and int(item.get("dirty_count") or 0) > 0
        ]
    return {
        "schema_version": "os_abyss_eval_freshness_sentinel_v1",
        "authority_boundary": "Freshness sentinel reports stale or drifting routing surfaces; it does not clean, sync, or mutate sibling repos.",
        "tracked_dimensions": [
            "source repo branch/head/dirty state",
            "generated read-model presence and checkability",
            "aoa-evals-mcp selected root and runtime-status freshness",
            ".aoa session archive freshness",
            "runtime candidate reader generation state",
            "local eval-port inventory status",
            "support registry inventory parseability",
        ],
        "current_signals": {
            "local_ports_status": local_inventory.get("summary", {}),
            "mcp_runtime_status": {
                "status": mcp_runtime_status.get("status"),
                "selected_stack_root": mcp_runtime_status.get("selected_stack_root"),
            },
            "aoa_freshness_status": {
                "status": aoa_freshness.get("status"),
                "freshness_hints": aoa_freshness.get("freshness_hints"),
            },
            "git_summary": summary,
            "dirty_repos": dirty_repos,
            "support_registry_summary": support_registry.get("summary", {}),
        },
        "nightly_route": [
            "python scripts/check_eval_freshness_sentinel.py --json",
            "python scripts/build_eval_readiness_dashboard.py --write-generated",
            "python scripts/build_eval_readiness_dashboard.py --check",
            "python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json",
            "PYTHONPATH=mcp/services/aoa-evals-mcp/src python -m aoa_evals_mcp.cli --workspace-root /srv/AbyssOS --evals-root /srv/AbyssOS/aoa-evals runtime-status",
            "python3 scripts/aoa_session_memory.py maintenance-status --full",
        ],
    }


def build_dashboard(
    *,
    evals_root: Path,
    workspace_root: Path,
    aoa_root: Path,
    skills_source_root: Path,
    installed_skills_root: Path,
    stack_root: Path | None,
    include_live_checks: bool,
    live_timeout: int,
    observed_at_utc: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    observed_at_utc = observed_at_utc or utc_now()
    canonical_evals_root = canonical_evals_owner_root(evals_root, workspace_root)
    support_registry = build_support_registry(evals_root)
    local_inventory = build_local_eval_port_inventory.build_inventory_payload(workspace_root)
    catalog_summary = load_catalog_summary(evals_root)
    runtime_candidates = load_runtime_candidate_summary(evals_root)
    candidate_packets = load_candidate_packets(evals_root)
    mcp_runtime_status = build_mcp_runtime_status(
        workspace_root,
        canonical_evals_root,
        stack_root,
        include_live_checks=include_live_checks,
        timeout=live_timeout,
    )
    aoa_freshness = build_aoa_freshness(
        aoa_root,
        include_live_checks=include_live_checks,
        timeout=live_timeout,
    )
    git_summary = build_workspace_git_summary(workspace_root)
    runtime_adoption = build_aoa_eval_runtime_adoption(
        skills_source_root,
        installed_skills_root,
        timeout=live_timeout,
    )
    external_research_grounding = load_external_research_grounding(evals_root)
    candidate_queue = build_candidate_queue(
        local_inventory,
        runtime_candidates,
        catalog_summary,
        candidate_packets,
    )
    repo_readiness = build_repo_readiness(
        local_inventory,
        workspace_root=workspace_root,
        git_summary=git_summary,
        mcp_runtime_status=mcp_runtime_status,
        aoa_freshness=aoa_freshness,
    )
    freshness_sentinel = build_freshness_sentinel(
        local_inventory=local_inventory,
        mcp_runtime_status=mcp_runtime_status,
        aoa_freshness=aoa_freshness,
        git_summary=git_summary,
        support_registry=support_registry,
    )
    eval_forge_readiness = build_eval_forge_readiness(evals_root, candidate_packets)
    dashboard = {
        "schema_version": SCHEMA_VERSION,
        "layer": "aoa-evals",
        "generated_at_utc": observed_at_utc,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "source_of_truth": SOURCE_OF_TRUTH,
        "external_research_grounding": external_research_grounding,
        "owner_boundaries": OWNER_BOUNDARIES,
        "workspace_root": workspace_root.as_posix(),
        "evals_root": canonical_evals_root.as_posix(),
        "read_model_posture": {
            "can_route": True,
            "can_score": False,
            "can_accept_proof": False,
            "can_promote_candidates": False,
            "can_mutate_sibling_repos": False,
            "can_execute_local_suites": False,
        },
        "local_eval_ports": {
            "summary": local_inventory.get("summary", {}),
            "authority_boundary": local_inventory.get("authority_boundary"),
            "source_ref": "generated by scripts/build_local_eval_port_inventory.py",
            "next_route": "inspect active or invalid ports before eval application/design",
            "suite_execution_boundary": (
                "suite execution states are inspected only; ready means source-contract-ready, "
                "not pinned runtime reproducibility; owner/apply must JIT-revalidate before "
                "invoking exact runner.argv and capture environment plus an execution receipt"
            ),
        },
        "central_catalog": catalog_summary,
        "mcp_runtime_status": mcp_runtime_status,
        "runtime_candidate_exports": runtime_candidates,
        "candidate_packet_import": candidate_packets,
        "aoa_session_memory_freshness": aoa_freshness,
        "workspace_git_drift": git_summary,
        "eval_support_registry": {
            "source_ref": "generated/eval_support_registry.json",
            "summary": support_registry.get("summary", {}),
            "semantic_classes": SUPPORT_SEMANTIC_CLASSES,
            "review_statuses": REVIEW_STATUS_DESCRIPTIONS,
            "authority_boundary": support_registry.get("authority_boundary"),
        },
        "repo_readiness": repo_readiness,
        "aoa_eval_runtime_adoption": runtime_adoption,
        "trigger_criteria": {
            "taxonomy": TRIGGER_CLASSES,
            "sample_packet_schema": SAMPLE_PACKET_SCHEMA,
            "candidate_packet_schema_ref": SOURCE_OF_TRUTH["eval_candidate_packet_schema"],
            "candidate_packet_validator": "scripts/validate_eval_candidate_packets.py",
            "session_mining_status": SESSION_MINING_STATUS,
        },
        "trajectory_eval_slice": build_trajectory_eval_slice(),
        "candidate_queue": candidate_queue,
        "eval_forge_readiness": eval_forge_readiness,
        "local_to_central_promotion_path": build_promotion_path(),
        "freshness_sentinel": freshness_sentinel,
        "phase_coverage": [
            {"phase": 1, "status": "implemented", "surface": "eval_readiness_dashboard"},
            {"phase": 2, "status": "implemented", "surface": "eval_support_registry"},
            {"phase": 3, "status": "implemented_read_only_audit", "surface": "aoa_eval_runtime_adoption"},
            {"phase": 4, "status": "implemented_criteria_and_packet_contract", "surface": "trigger_criteria + validate_eval_candidate_packets"},
            {"phase": 5, "status": "implemented_runnable_harness", "surface": "trajectory_eval_slice + run_aoa_eval_route_trajectory_harness.py"},
            {"phase": 6, "status": "implemented_read_only_queue_and_packet_validator", "surface": "candidate_queue + candidate_packet_contract"},
            {"phase": 7, "status": "implemented_owner_gate_contract", "surface": "local_to_central_promotion_path"},
            {"phase": 8, "status": "implemented_runnable_sentinel", "surface": "freshness_sentinel + check_eval_freshness_sentinel.py"},
            {"phase": 9, "status": "implemented_design_forge_router", "surface": "eval_forge_readiness + eval_forge_route.py"},
            {"phase": 10, "status": "implemented_session_readiness_gate", "surface": "check_eval_forge_readiness.py + docs/guides/EVAL_FORGE_READINESS_LAYER.md"},
        ],
    }
    return dashboard, support_registry


def markdown_row(values: Sequence[str]) -> str:
    return "| " + " | ".join(value.replace("\n", " ") for value in values) + " |"


def build_markdown(dashboard: dict[str, Any], support_registry: dict[str, Any]) -> str:
    local_summary = dashboard["local_eval_ports"]["summary"]
    catalog = dashboard["central_catalog"]
    candidate_queue = dashboard["candidate_queue"]
    eval_forge = dashboard["eval_forge_readiness"]
    runtime_candidates = dashboard["runtime_candidate_exports"]
    mcp_status = dashboard["mcp_runtime_status"]
    repo_readiness = dashboard["repo_readiness"]
    git_summary = dashboard["workspace_git_drift"].get("summary", {})
    lines = [
        "# OS Abyss Eval Readiness Dashboard",
        "",
        "Generated read-model for OS-wide eval routing. It is navigation and freshness evidence,",
        "not proof acceptance.",
        "",
        "## Boundary",
        "",
        dashboard["authority_boundary"],
        "",
        "## Summary",
        "",
        f"- Generated at: `{dashboard['generated_at_utc']}`",
        f"- Workspace root: `{dashboard['workspace_root']}`",
        f"- Central evals: {catalog.get('total_evals', 'unknown')}",
        f"- Local active ports: {local_summary.get('active', 'unknown')}",
        f"- Local invalid ports: {local_summary.get('invalid', 'unknown')}",
        f"- Actionable repo routes: {repo_readiness['summary']['actionable_repos']}",
        f"- Runtime candidate exports: {runtime_candidates.get('count', 0)}",
        f"- Candidate queue entries: {candidate_queue['summary']['entries']}",
        f"- Candidate packet imports: {candidate_queue['summary'].get('packet_count', 0)}",
        f"- Eval Forge archetypes: {eval_forge.get('archetype_count', 'unknown')}",
        f"- Eval Forge candidate hints: {len(eval_forge.get('candidate_archetype_hints', []))}",
        f"- Session-mining reviewed episodes: {candidate_queue['summary'].get('session_mining_reviewed_count', 0)}",
        f"- Support surfaces: {support_registry['summary']['total_surfaces']} total, {support_registry['summary']['eval_lane_relevant']} eval-relevant",
        f"- Eval-relevant surfaces with unresolved manual review: {support_registry['summary']['by_review_status'].get('manual_review_required', 0)}",
        f"- Unsafe side-effect scripts: {support_registry['summary']['unsafe_side_effect_scripts']}",
        f"- MCP runtime status: `{mcp_status.get('status')}`",
        f"- Dirty repos: {git_summary.get('dirty_repos', 'unknown')}",
        "",
        "## Research Grounding",
        "",
        markdown_row(["Source", "Adopted", "Rejected"]),
        markdown_row(["---", "---", "---"]),
    ]
    for item in dashboard["external_research_grounding"]:
        lines.append(markdown_row([str(item["source"]), str(item["adopted"]), str(item["rejected"])]))
    lines.extend(
        [
            "",
        "## Owner Boundaries",
        "",
        markdown_row(["Owner", "Owns", "Does Not Own"]),
        markdown_row(["---", "---", "---"]),
        ]
    )
    for boundary in dashboard["owner_boundaries"]:
        lines.append(
            markdown_row(
                [
                    f"`{boundary['owner_repo']}`",
                    str(boundary["owns"]),
                    str(boundary["does_not_own"]),
                ]
            )
        )
    lines.extend(
        [
            "",
            "## Repo Readiness",
            "",
            markdown_row(["Repo", "State", "Severity", "Confidence", "Freshness", "Next Command"]),
            markdown_row(["---", "---", "---", "---", "---", "---"]),
        ]
    )
    for entry in repo_readiness["repos"]:
        if entry["route_state"] == "dormant_no_current_eval_pressure":
            continue
        lines.append(
            markdown_row(
                [
                    f"`{entry['repo_id']}`",
                    str(entry["route_state"]),
                    str(entry["pressure_severity"]),
                    str(entry["route_confidence"]),
                    str(entry["freshness_gate"]["status"]),
                    f"`{entry['exact_next_command']}`",
                ]
            )
        )
    lines.extend(
        [
            "",
            "## Candidate Queue",
            "",
            markdown_row(["Candidate", "State", "Source", "Owner", "Evidence", "Packet", "Next Route"]),
            markdown_row(["---", "---", "---", "---", "---:", "---", "---"]),
        ]
    )
    for entry in candidate_queue["entries"]:
        lines.append(
            markdown_row(
                [
                    f"`{entry['candidate_id']}`",
                    str(entry["state"]),
                    str(entry["source_kind"]),
                    str(entry["owner_repo"]),
                    str(entry["evidence_count"]),
                    f"`{entry.get('packet_ref', '')}`" if entry.get("packet_ref") else "",
                    str(entry["next_route"]),
                ]
            )
        )
    lines.extend(
        [
            "",
            "## Eval Forge",
            "",
            f"- Router command: `{eval_forge.get('router_command')}`",
            f"- Local-port command: `{eval_forge.get('local_port_pressure_hint_command')}`",
            f"- Worksheet command: `{eval_forge.get('worksheet_write_command')}`",
            f"- Registry: `{eval_forge.get('registry_ref')}`",
            f"- Worksheet schema: `{eval_forge.get('worksheet_schema_ref')}`",
            f"- Archetype count: {eval_forge.get('archetype_count')}",
            f"- External pattern sources: {eval_forge.get('external_patterns_count')}",
            f"- Registry valid: {(eval_forge.get('registry_validation') or {}).get('valid')}",
            "",
        ]
    )
    lines.extend(["### Forge Front Door", ""])
    front_door_refs = eval_forge.get("front_door_refs", {})
    if isinstance(front_door_refs, dict):
        for label, ref in front_door_refs.items():
            lines.append(f"- {label}: `{ref}`")
    front_door_status = eval_forge.get("front_door_surface_status", {})
    if isinstance(front_door_status, dict):
        lines.append(
            "- proof authority: {proof}; promotion allowed: {promotion}; refs valid: {valid}".format(
                proof=front_door_status.get("proof_authority"),
                promotion=front_door_status.get("promotion_allowed"),
                valid=front_door_status.get("valid"),
            )
        )
    front_door_commands = eval_forge.get("front_door_commands", [])
    if isinstance(front_door_commands, list) and front_door_commands:
        lines.append("- exact commands:")
        for item in front_door_commands:
            if isinstance(item, dict):
                lines.append(f"  - {item.get('purpose')}: `{item.get('command')}`")
    lines.extend(
        [
            "",
            markdown_row(["Candidate", "Decision", "Archetype", "Owner Route", "Promotion"]),
            markdown_row(["---", "---", "---", "---", "---"]),
        ]
    )
    for hint in eval_forge.get("candidate_archetype_hints", []):
        lines.append(
            markdown_row(
                [
                    f"`{hint.get('candidate_id')}`",
                    str(hint.get("decision")),
                    f"`{hint.get('selected_archetype_id')}`",
                    f"`{hint.get('owner_repo')}` / `{hint.get('route_key')}`",
                    str(hint.get("promotion_allowed")),
                ]
            )
        )
    lines.extend(
        [
            "",
            "## Trigger Criteria",
            "",
            markdown_row(["Trigger Class", "Route", "Freshness Gate"]),
            markdown_row(["---", "---", "---"]),
        ]
    )
    for item in dashboard["trigger_criteria"]["taxonomy"]:
        lines.append(markdown_row([f"`{item['id']}`", str(item["next_route"]), str(item["required_freshness"])]))
    mining_status = dashboard["trigger_criteria"]["session_mining_status"]
    lines.extend(
        [
            "",
            "### Session Mining Gate",
            "",
            f"- Status: `{mining_status['status']}`",
            f"- Reason: {mining_status['reason']}",
            f"- Reviewed episodes: {mining_status.get('reviewed_count', 'unknown')}",
            f"- Packetized candidates: {mining_status.get('packetized_count', 'unknown')}",
            f"- Report refs: `{json.dumps(mining_status.get('report_refs', []), sort_keys=True)}`",
            f"- Boundary: {mining_status['candidate_only_boundary']}",
            "",
            "## Support Registry",
            "",
            f"- Support registry JSON: `generated/eval_support_registry.json`",
            f"- Eval-relevant surfaces: {support_registry['summary']['eval_lane_relevant']}",
            f"- Recommended routes: `{json.dumps(support_registry['summary']['by_recommended_route'], sort_keys=True)}`",
            f"- Semantic classes: `{json.dumps(support_registry['summary']['by_semantic_class'], sort_keys=True)}`",
            f"- Review status: `{json.dumps(support_registry['summary']['by_review_status'], sort_keys=True)}`",
            "",
            "## Runtime Adoption",
            "",
        ]
    )
    adoption = dashboard["aoa_eval_runtime_adoption"]
    lines.extend(
        [
            f"- Source skill exists: {adoption['source_exists']}",
            f"- Installed skill exists: {adoption['installed_exists']}",
            f"- Installed matches source: {adoption['installed_matches_source']}",
            f"- Installed profile verified: {adoption['installed_profile_verified']}",
            f"- Runtime discovery mentions `aoa-eval`: {adoption['runtime_discovery_mentions_aoa_eval']}",
            f"- Trigger harness command: `{adoption['verification_command']}`",
            "",
            "## Freshness Sentinel",
            "",
            f"- Git repos: {git_summary.get('repos', 'unknown')}",
            f"- Dirty repos: {git_summary.get('dirty_repos', 'unknown')}",
            f"- MCP selected root: `{mcp_status.get('selected_stack_root')}`",
            f"- .aoa freshness status: `{dashboard['aoa_session_memory_freshness'].get('status')}`",
            "",
            "## Phase Coverage",
            "",
            markdown_row(["Phase", "Status", "Surface"]),
            markdown_row(["---:", "---", "---"]),
        ]
    )
    for phase in dashboard["phase_coverage"]:
        lines.append(markdown_row([str(phase["phase"]), str(phase["status"]), str(phase["surface"])]))
    lines.append("")
    return "\n".join(lines)


def validate_dashboard_shape(payload: Any, support_payload: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(payload, dict):
        return ["dashboard must be a JSON object"]
    if payload.get("schema_version") != SCHEMA_VERSION:
        issues.append("dashboard schema_version mismatch")
    if "/.worktrees/" in json.dumps(payload, sort_keys=True):
        issues.append("dashboard must not embed ephemeral absolute worktree paths")
    required_keys = {
        "authority_boundary",
        "external_research_grounding",
        "owner_boundaries",
        "local_eval_ports",
        "central_catalog",
        "mcp_runtime_status",
        "runtime_candidate_exports",
        "candidate_packet_import",
        "aoa_session_memory_freshness",
        "workspace_git_drift",
        "eval_support_registry",
        "repo_readiness",
        "aoa_eval_runtime_adoption",
        "trigger_criteria",
        "trajectory_eval_slice",
        "candidate_queue",
        "eval_forge_readiness",
        "local_to_central_promotion_path",
        "freshness_sentinel",
        "phase_coverage",
    }
    missing = sorted(required_keys.difference(payload))
    if missing:
        issues.append(f"dashboard missing keys: {', '.join(missing)}")
    posture = payload.get("read_model_posture")
    if not isinstance(posture, dict):
        issues.append("read_model_posture missing")
    else:
        for key in (
            "can_score",
            "can_accept_proof",
            "can_promote_candidates",
            "can_mutate_sibling_repos",
            "can_execute_local_suites",
        ):
            if posture.get(key) is not False:
                issues.append(f"read_model_posture.{key} must be false")
    queue = payload.get("candidate_queue")
    if isinstance(queue, dict):
        states = queue.get("allowed_states")
        if states != list(CANDIDATE_QUEUE_STATES):
            issues.append("candidate_queue allowed_states drifted")
        entries = queue.get("entries")
        if not isinstance(entries, list):
            issues.append("candidate_queue.entries must be a list")
        else:
            for entry in entries:
                if not isinstance(entry, dict):
                    issues.append("candidate_queue entries must be objects")
                    break
                if entry.get("promotion_allowed") is not False:
                    issues.append("candidate_queue entries must keep promotion_allowed false")
                    break
                if not entry.get("candidate_id") or not entry.get("source_ref") or not entry.get("next_route"):
                    issues.append("candidate_queue entries must include candidate_id, source_ref, and next_route")
                    break
                if entry.get("source_kind") == "session_episode" and not entry.get("packet_ref"):
                    issues.append("session episode candidate queue entries must include packet_ref")
                    break
    else:
        issues.append("candidate_queue must be an object")
    forge = payload.get("eval_forge_readiness")
    if isinstance(forge, dict):
        if forge.get("schema_version") != "os_abyss_eval_forge_readiness_v1":
            issues.append("eval_forge_readiness schema_version mismatch")
        registry_validation = forge.get("registry_validation")
        if not isinstance(registry_validation, dict) or registry_validation.get("valid") is not True:
            issues.append("eval_forge_readiness registry must validate")
        if int(forge.get("archetype_count") or 0) < 18:
            issues.append("eval_forge_readiness must expose at least 18 archetypes")
        if not forge.get("router_command") or "eval_forge_route.py" not in str(forge.get("router_command")):
            issues.append("eval_forge_readiness must expose eval_forge_route.py command")
        front_door_refs = forge.get("front_door_refs")
        required_front_door_ref_keys = {
            "operating_path_ref",
            "session_mining_criteria_ref",
            "local_port_decision_matrix_ref",
            "latest_route_review_report_ref",
            "worksheet_example_ref",
            "candidate_packet_schema_ref",
            "local_suite_execution_schema_ref",
        }
        if not isinstance(front_door_refs, dict) or not required_front_door_ref_keys.issubset(front_door_refs):
            issues.append("eval_forge_readiness must expose all front-door refs")
        front_door_status = forge.get("front_door_surface_status")
        if not isinstance(front_door_status, dict) or front_door_status.get("valid") is not True:
            issues.append("eval_forge_readiness front-door surfaces must validate")
        elif front_door_status.get("proof_authority") is not False or front_door_status.get("promotion_allowed") is not False:
            issues.append("eval_forge_readiness front-door surfaces must stay non-proof")
        front_door_commands = forge.get("front_door_commands")
        if not isinstance(front_door_commands, list) or len(front_door_commands) < 7:
            issues.append("eval_forge_readiness must expose front-door commands")
        else:
            command_text = "\n".join(str(item.get("command")) for item in front_door_commands if isinstance(item, dict))
            required_commands = [
                "aoa_eval_session_start.py --json",
                "check_eval_forge_readiness.py --json",
                "build_local_eval_port_inventory.py",
                "validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets",
                "eval_forge_route.py --candidate-packet",
                "eval_forge_route.py --local-port-repo",
                "--write-worksheet",
            ]
            for required_command in required_commands:
                if required_command not in command_text:
                    issues.append(f"eval_forge_readiness missing front-door command: {required_command}")
                    break
        hints = forge.get("candidate_archetype_hints")
        if not isinstance(hints, list):
            issues.append("eval_forge_readiness candidate_archetype_hints must be a list")
        else:
            for hint in hints:
                if not isinstance(hint, dict):
                    issues.append("eval_forge_readiness candidate hints must be objects")
                    break
                if hint.get("proof_authority") is not False or hint.get("promotion_allowed") is not False:
                    issues.append("eval_forge_readiness hints must keep proof_authority and promotion_allowed false")
                    break
                if not hint.get("candidate_id") or not hint.get("selected_archetype_id"):
                    issues.append("eval_forge_readiness hints must include candidate_id and selected_archetype_id")
                    break
        local_suite_boundary = forge.get("local_suite_execution_boundary")
        if not isinstance(local_suite_boundary, dict):
            issues.append("eval_forge_readiness must expose local_suite_execution_boundary")
        elif (
            local_suite_boundary.get("execution_allowed") is not False
            or local_suite_boundary.get("proof_authority") is not False
            or local_suite_boundary.get("promotion_allowed") is not False
            or local_suite_boundary.get("readiness_scope") != "source-contract-ready"
            or local_suite_boundary.get("runtime_reproducibility_proven") is not False
            or local_suite_boundary.get("jit_revalidation_required") is not True
            or local_suite_boundary.get("execution_receipt_required") is not True
            or local_suite_boundary.get("environment_capture_required") is not True
        ):
            issues.append(
                "eval_forge_readiness local suite boundary must stay source-contract-only, "
                "inspect-only, JIT-revalidated, receipt-bearing, and non-proof"
            )
    else:
        issues.append("eval_forge_readiness must be an object")
    packet_import = payload.get("candidate_packet_import")
    if not isinstance(packet_import, dict):
        issues.append("candidate_packet_import must be an object")
    elif packet_import.get("issue_count") not in {0, None}:
        issues.append("candidate_packet_import has unresolved import issues")
    trigger = payload.get("trigger_criteria")
    if isinstance(trigger, dict):
        taxonomy = trigger.get("taxonomy")
        schema = trigger.get("sample_packet_schema")
        session_status = trigger.get("session_mining_status")
        if not isinstance(taxonomy, list) or len(taxonomy) < 8:
            issues.append("trigger taxonomy must contain at least 8 classes")
        if not isinstance(schema, dict) or schema.get("schema_version") != "aoa_eval_trigger_mining_sample_v1":
            issues.append("trigger sample packet schema missing or wrong")
        elif "candidate_state_reason" not in schema.get("required_fields", []):
            issues.append("trigger sample packet schema must require candidate_state_reason")
        if not isinstance(session_status, dict) or "candidate_only_boundary" not in session_status:
            issues.append("session mining status must expose candidate-only boundary")
        elif session_status.get("status") == "manual_review_packetized":
            if int(session_status.get("reviewed_count") or 0) < 20:
                issues.append("manual_review_packetized session mining status must review at least 20 episodes")
            if not session_status.get("report_refs"):
                issues.append("manual_review_packetized session mining status must include report_refs")
    else:
        issues.append("trigger_criteria must be an object")
    repo_readiness = payload.get("repo_readiness")
    if isinstance(repo_readiness, dict):
        if repo_readiness.get("schema_version") != "os_abyss_eval_repo_readiness_v1":
            issues.append("repo_readiness schema_version mismatch")
        repos = repo_readiness.get("repos")
        if not isinstance(repos, list):
            issues.append("repo_readiness.repos must be a list")
        else:
            for item in repos:
                if not isinstance(item, dict):
                    continue
                if not item.get("route_state") or not item.get("exact_next_command"):
                    issues.append("repo_readiness entries must include route_state and exact_next_command")
                    break
                suite_execution = item.get("suite_execution")
                if not isinstance(suite_execution, dict):
                    issues.append("repo_readiness entries must include suite_execution")
                    break
                if suite_execution.get("execution_allowed") is not False:
                    issues.append("repo_readiness suite_execution must keep execution_allowed false")
                    break
                if suite_execution.get("proof_authority") is not False or suite_execution.get("promotion_allowed") is not False:
                    issues.append("repo_readiness suite_execution must stay non-proof")
                    break
                if (
                    suite_execution.get("readiness_scope") != "source-contract-ready"
                    or suite_execution.get("runtime_reproducibility_proven") is not False
                    or suite_execution.get("jit_revalidation_required") is not True
                    or suite_execution.get("execution_receipt_required") is not True
                    or suite_execution.get("environment_capture_required") is not True
                ):
                    issues.append(
                        "repo_readiness suite_execution must preserve source-contract readiness "
                        "and JIT revalidation/environment-receipt requirements"
                    )
                    break
    else:
        issues.append("repo_readiness must be an object")
    grounding = payload.get("external_research_grounding")
    if not isinstance(grounding, list) or len(grounding) < 4:
        issues.append("external_research_grounding must contain current agent-eval references")
    if not isinstance(support_payload, dict):
        issues.append("support registry must be a JSON object")
    elif support_payload.get("schema_version") != SUPPORT_REGISTRY_SCHEMA_VERSION:
        issues.append("support registry schema_version mismatch")
    else:
        summary = support_payload.get("summary")
        if not isinstance(summary, dict):
            issues.append("support registry summary missing")
        elif "by_semantic_class" not in summary or "by_review_status" not in summary:
            issues.append("support registry must expose semantic classes and review status")
        surfaces = support_payload.get("surfaces")
        if isinstance(surfaces, list):
            for item in surfaces:
                if not isinstance(item, dict):
                    continue
                if item.get("eval_lane_relevant") is True and item.get("review_status") == "manual_review_required":
                    issues.append("eval-relevant support surface still requires unresolved manual review")
                    break
                if not item.get("review_reason"):
                    issues.append("support registry entries must include review_reason")
                    break
                if item.get("semantic_class") == "unsafe_side_effect_script":
                    if item.get("recommended_route") == "apply_as_deterministic_eval_support":
                        issues.append("unsafe side-effect script cannot be direct eval support")
                        break
    return issues


def check_generated(evals_root: Path) -> list[str]:
    dashboard = read_json(evals_root / "generated" / "eval_readiness_dashboard.json", default=None)
    support = read_json(evals_root / "generated" / "eval_support_registry.json", default=None)
    markdown_path = evals_root / "generated" / "eval_readiness_dashboard.md"
    issues = validate_dashboard_shape(dashboard, support)
    if not markdown_path.exists():
        issues.append("generated/eval_readiness_dashboard.md is missing")
    elif "OS Abyss Eval Readiness Dashboard" not in markdown_path.read_text(encoding="utf-8"):
        issues.append("generated/eval_readiness_dashboard.md does not look like the readiness dashboard")
    return issues


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    evals_root = Path(args.evals_root).resolve()
    workspace_root = Path(args.workspace_root).resolve()
    aoa_root = Path(args.aoa_root).resolve()
    skills_source_root = Path(args.skills_source_root).resolve()
    installed_skills_root = Path(args.installed_skills_root).resolve()
    stack_root = selected_stack_root(Path(args.stack_root).resolve() if args.stack_root else None)

    if args.check:
        issues = check_generated(evals_root)
        if issues:
            print("Eval readiness generated check failed.")
            for issue in issues:
                print(f"- {issue}")
            return 1
        print("Eval readiness generated check passed.")
        return 0

    dashboard, support_registry = build_dashboard(
        evals_root=evals_root,
        workspace_root=workspace_root,
        aoa_root=aoa_root,
        skills_source_root=skills_source_root,
        installed_skills_root=installed_skills_root,
        stack_root=stack_root,
        include_live_checks=not args.no_live_checks,
        live_timeout=args.live_timeout,
    )
    markdown = build_markdown(dashboard, support_registry)

    if args.write_generated:
        write_json(evals_root / "generated" / "eval_readiness_dashboard.json", dashboard)
        write_json(evals_root / "generated" / "eval_support_registry.json", support_registry)
        (evals_root / "generated" / "eval_readiness_dashboard.md").write_text(markdown, encoding="utf-8")
        print("[ok] wrote generated/eval_readiness_dashboard.json")
        print("[ok] wrote generated/eval_support_registry.json")
        print("[ok] wrote generated/eval_readiness_dashboard.md")
        return 0

    if args.json:
        print(json.dumps(dashboard, indent=2, sort_keys=True))
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
