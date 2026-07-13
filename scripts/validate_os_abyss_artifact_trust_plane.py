#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SCHEMA = "aoa_evals_os_abyss_artifact_trust_plane_scenario_validation_v1"
SOURCE_REF_PROBE = "commit:aoa-evals-unpromoted-source-ref-probe"

REQUIRED_SCENARIO_CLASSES = {
    "bootstrap_install_bundle": "bootstrap install bundle",
    "runtime_or_container_artifact": "runtime/container artifact",
    "ai_model_or_runtime_bundle": "AI model/runtime bundle",
    "public_source_seed": "public source seed",
    "public_media_export": "public media export",
    "aoa_evals_generated_report_index_bundle": "eval report/result bundle",
    "browser_extension_package": "browser extension package",
    "host_local_evidence": "host-local evidence",
    "aoa_session_memory_portable_bundle": ".aoa generated/export/session-memory surface",
}

REQUIRED_OWNER_REPOS = {
    "abyss-machine",
    "abyss-stack",
    "Tree-of-Sophia",
    "Dionysus",
    "aoa-agents",
    "aoa-evals",
    "aoa-kag",
    "aoa-memo",
    "aoa-playbooks",
    "aoa-routing",
    "aoa-sdk",
    "aoa-session-memory",
    "aoa-skills",
    "aoa-stats",
    "aoa-techniques",
}

KNOWN_AFFECTED_VERDICTS = {
    "fresh",
    "stale",
    "needs_rebuild",
    "needs_reverify",
    "blocked_by_missing_sibling",
    "accepted_lag",
    "manual_review_required",
}

KNOWN_DRIFT_STATUSES = {
    "fresh",
    "missing_durable_evidence",
    "rebuild_required",
    "reverify_required",
    "blocked_missing_sibling",
    "accepted_lag",
    "manual_review_required",
}

CLAIM_LIMITS = [
    "This validator reads abyss-machine trust-plane read-models; it does not create signatures, attestations, SBOMs, C2PA manifests, registry records, or release artifacts.",
    "FULLY_COVERED is accepted only when abyss-machine reports durable latest selection, consumer trust-gate admission, and manual positive plus negative evidence for every declared artifact class.",
    "Declared real blockers are accepted only when the class-specific trust-plane evidence is otherwise durable, fresh, gate-admitted, and the blocker remains explicit.",
    "The durable-only pass must stay weaker than FULLY_COVERED: it proves persistent registry plus trust-gate coverage while intentionally ignoring tmp/manual evidence.",
    "Drift probes use synthetic source-ref and policy-change inputs to prove verdict behavior; they do not mutate sibling repositories.",
]

KNOWN_REAL_BLOCKERS = {
    "public_media_export": {
        "status": "DEFERRED_WITH_REAL_BLOCKER",
        "remaining_blocker_fragments": (
            "C2PA signing credential",
            "production trust-list trusted",
        ),
        "required_controls": ("c2pa",),
        "trust_gate_verdicts": ("warn",),
    },
}


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").is_file() and (parent / "docs" / "validation" / "VALIDATOR_TOPOLOGY.md").is_file():
            return parent
    return Path.cwd()


def _candidate_abyss_machine_roots(repo_root: Path) -> list[Path]:
    return [
        repo_root.parent / "abyss-machine",
        Path.home() / "src" / "abyss-machine",
        Path("/srv/AbyssOS/abyss-machine"),
    ]


def _source_module_root(candidate: Path) -> Path | None:
    module_root = candidate.expanduser() / "src"
    if (module_root / "abyss_machine" / "cli.py").is_file():
        return module_root
    return None


def _source_command_env(module_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    current = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(module_root) if not current else f"{module_root}{os.pathsep}{current}"
    return env


def _resolve_artifacts_command(args: list[str], *, repo_root: Path) -> tuple[list[str], dict[str, str]]:
    explicit_root = os.environ.get("ABYSS_MACHINE_REPO_ROOT")
    if explicit_root:
        module_root = _source_module_root(Path(explicit_root))
        if module_root is None:
            raise RuntimeError(
                "ABYSS_MACHINE_REPO_ROOT does not contain src/abyss_machine/cli.py: "
                + str(Path(explicit_root).expanduser())
            )
        return (
            [sys.executable, "-m", "abyss_machine.cli", "artifacts", *args, "--json"],
            _source_command_env(module_root),
        )

    installed_cli = shutil.which("abyss-machine")
    if installed_cli:
        return [installed_cli, "artifacts", *args, "--json"], os.environ.copy()

    for candidate in _candidate_abyss_machine_roots(repo_root):
        module_root = _source_module_root(candidate)
        if module_root is not None:
            return (
                [sys.executable, "-m", "abyss_machine.cli", "artifacts", *args, "--json"],
                _source_command_env(module_root),
            )

    raise RuntimeError(
        "No abyss-machine CLI found. Install abyss-machine or set ABYSS_MACHINE_REPO_ROOT "
        "to a checkout containing src/abyss_machine/cli.py."
    )


def _run_artifacts_command(args: list[str], *, repo_root: Path | None = None) -> dict[str, Any]:
    root = repo_root or _repo_root()
    command, env = _resolve_artifacts_command(args, repo_root=root)
    completed = subprocess.run(
        command,
        cwd=root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "abyss-machine artifacts command failed: "
            + " ".join(command)
            + "\n"
            + completed.stderr.strip()
        )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"abyss-machine artifacts command did not emit JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("abyss-machine artifacts command emitted non-object JSON")
    return payload


def collect_live_payloads(*, repo_root: Path | None = None) -> dict[str, dict[str, Any]]:
    return {
        "requirements": _run_artifacts_command(["requirements"], repo_root=repo_root),
        "producer_profiles": _run_artifacts_command(["producer-profiles"], repo_root=repo_root),
        "trust_coverage": _run_artifacts_command(["trust-coverage"], repo_root=repo_root),
        "durable_trust_coverage": _run_artifacts_command(["trust-coverage", "--durable-only"], repo_root=repo_root),
        "policy_drift": _run_artifacts_command(
            ["affected", "--changed-path", "manifests/artifact_signature_policy.manifest.json"],
            repo_root=repo_root,
        ),
        "sibling_blocked": _run_artifacts_command(
            [
                "affected",
                "--source-repo",
                "aoa-sdk",
                "--source-ref",
                SOURCE_REF_PROBE,
            ],
            repo_root=repo_root,
        ),
        "sibling_accepted_lag": _run_artifacts_command(
            [
                "affected",
                "--source-repo",
                "aoa-sdk",
                "--source-ref",
                SOURCE_REF_PROBE,
                "--accept-sibling-lag",
            ],
            repo_root=repo_root,
        ),
    }


def _rows_by_class(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        return {}
    return {
        str(row.get("artifact_class")): row
        for row in rows
        if isinstance(row, dict) and row.get("artifact_class")
    }


def _add_issue(issues: list[dict[str, str]], check: str, message: str) -> None:
    issues.append({"check": check, "message": message})


def _known_real_blocker_failures(row: dict[str, Any], *, durable_only: bool) -> list[str]:
    artifact_class = str(row.get("artifact_class") or "")
    blocker_spec = KNOWN_REAL_BLOCKERS.get(artifact_class)
    if blocker_spec is None:
        return [f"{artifact_class or '<unknown>'} is not a declared real-blocker class"]
    failures: list[str] = []
    if row.get("status") != blocker_spec["status"]:
        failures.append(f"status is not {blocker_spec['status']}")

    remaining_blocker = str(row.get("remaining_blocker") or "")
    for fragment in blocker_spec["remaining_blocker_fragments"]:
        if fragment not in remaining_blocker:
            failures.append(f"remaining_blocker does not mention {fragment}")

    required_controls = {str(item) for item in row.get("required_controls", [])}
    for control in blocker_spec["required_controls"]:
        if control not in required_controls:
            failures.append(f"required_controls does not include {control}")

    installed = row.get("installed_verification", {})
    if not isinstance(installed, dict):
        return failures + ["installed_verification is missing"]
    if installed.get("latest_record_verification_ok") is not True:
        failures.append("latest record verification is not ok")
    verified_controls = {str(item) for item in installed.get("verified_controls", [])}
    for control in blocker_spec["required_controls"]:
        if control not in verified_controls:
            failures.append(f"installed verification does not verify {control}")
    if installed.get("trust_gate_ok") is not True:
        failures.append("trust gate is not ok")
    if installed.get("trust_gate_verdict") not in blocker_spec["trust_gate_verdicts"]:
        failures.append("trust gate verdict is not an accepted blocker verdict")
    if not durable_only:
        if int(installed.get("manual_positive_evidence_count") or 0) <= 0:
            failures.append("manual positive evidence count is missing")
        if int(installed.get("manual_negative_evidence_count") or 0) <= 0:
            failures.append("manual negative evidence count is missing")
        if not row.get("manual_positive_evidence"):
            failures.append("manual positive evidence refs are missing")
        if not row.get("manual_negative_evidence"):
            failures.append("manual negative evidence refs are missing")

    freshness = row.get("source_freshness", {})
    if not isinstance(freshness, dict) or freshness.get("freshness") != "fresh":
        failures.append("source freshness is not fresh")

    registry = row.get("persistent_registry_status", {})
    if not isinstance(registry, dict):
        return failures + ["persistent registry status is missing"]
    if registry.get("has_latest") is not True:
        failures.append("persistent registry has no latest record")
    if registry.get("latest_eligible") is not True:
        failures.append("persistent registry latest is not eligible")
    if registry.get("verification_missing"):
        failures.append("persistent registry reports missing verification")
    if registry.get("verification_errors"):
        failures.append("persistent registry reports verification errors")
    if registry.get("trust_gate_verdict") not in blocker_spec["trust_gate_verdicts"]:
        failures.append("persistent registry trust gate verdict is not accepted")
    return failures


def _validate_requirements(payload: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, Any]:
    rows_by_class = _rows_by_class(payload)
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    owner_repos = {
        str(row.get("owner_repo"))
        for row in rows_by_class.values()
        if row.get("owner_repo")
    }

    if payload.get("ok") is not True:
        _add_issue(issues, "requirements.ok", "requirements read-model is not ok")
    if summary.get("missing_artifact_classes") not in ([], None):
        _add_issue(issues, "requirements.missing_artifact_classes", "requirements reports missing artifact classes")

    for artifact_class, scenario in REQUIRED_SCENARIO_CLASSES.items():
        if artifact_class not in rows_by_class:
            _add_issue(issues, "requirements.scenario_class", f"missing {scenario}: {artifact_class}")

    missing_owners = sorted(REQUIRED_OWNER_REPOS - owner_repos)
    if missing_owners:
        _add_issue(issues, "requirements.owner_repos", "missing producer owner profiles: " + ", ".join(missing_owners))

    for artifact_class, row in rows_by_class.items():
        controls = row.get("controls", {})
        required = controls.get("required") if isinstance(controls, dict) else None
        if not isinstance(required, list) or not required:
            _add_issue(issues, "requirements.controls", f"{artifact_class} has no required controls")
        if not isinstance(row.get("producer_profile"), dict) or not row["producer_profile"]:
            _add_issue(issues, "requirements.producer_profile", f"{artifact_class} has no producer profile")
        trust_gate_status = row.get("trust_gate_status", {})
        if not isinstance(trust_gate_status, dict) or trust_gate_status.get("verdict") not in {"allow", "warn"}:
            _add_issue(issues, "requirements.trust_gate_status", f"{artifact_class} has no allow/warn trust-gate status")
        consumer = row.get("consumer", {})
        if not isinstance(consumer, dict) or "trust-gate" not in str(consumer.get("trust_gate") or ""):
            _add_issue(issues, "requirements.consumer_path", f"{artifact_class} has no consumer trust-gate path")
        agent_loop = row.get("agent_loop", {})
        for key in ("requirements", "producer_profiles", "affected", "build_sidecars", "evidence_promote", "trust_gate"):
            if not isinstance(agent_loop, dict) or not agent_loop.get(key):
                _add_issue(issues, "requirements.agent_loop", f"{artifact_class} missing agent loop command {key}")

    return {"artifact_classes": sorted(rows_by_class), "owner_repos": sorted(owner_repos)}


def _validate_producer_profiles(payload: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, Any]:
    rows = payload.get("rows", [])
    if not isinstance(rows, list):
        rows = []
    profile_rows = [row for row in rows if isinstance(row, dict)]
    owner_repos = {str(row.get("owner_repo")) for row in profile_rows if row.get("owner_repo")}
    artifact_classes: set[str] = set()
    for row in profile_rows:
        classes = row.get("artifact_classes", [])
        if isinstance(classes, list):
            artifact_classes.update(str(item) for item in classes if item)

    if payload.get("ok") is not True:
        _add_issue(issues, "producer_profiles.ok", "producer-profiles read-model is not ok")

    missing_owners = sorted(REQUIRED_OWNER_REPOS - owner_repos)
    if missing_owners:
        _add_issue(issues, "producer_profiles.owner_repos", "missing producer profile owners: " + ", ".join(missing_owners))

    for artifact_class, scenario in REQUIRED_SCENARIO_CLASSES.items():
        if artifact_class not in artifact_classes:
            _add_issue(issues, "producer_profiles.scenario_class", f"missing producer profile for {scenario}: {artifact_class}")

    for row in profile_rows:
        profile_id = row.get("profile_id") or row.get("owner_repo") or "<unknown>"
        owner_repo = row.get("owner_repo")
        if not isinstance(owner_repo, str) or not owner_repo:
            _add_issue(issues, "producer_profiles.profile_shape", f"{profile_id} missing owner_repo")
        for key in (
            "owner_route_refs",
            "artifact_classes",
            "validator_commands",
            "produced_sidecars",
            "consumer_expectations",
            "owner_boundaries",
            "trust_root_modes",
        ):
            value = row.get(key)
            if not isinstance(value, list) or not value:
                _add_issue(issues, "producer_profiles.profile_shape", f"{profile_id} missing {key}")

    agent_loop = payload.get("agent_loop", {})
    if not isinstance(agent_loop, dict) or not agent_loop.get("producer_profiles"):
        _add_issue(issues, "producer_profiles.agent_loop", "producer-profiles report has no producer_profiles agent-loop command")
    if not isinstance(agent_loop, dict) or not agent_loop.get("trust_gate"):
        _add_issue(issues, "producer_profiles.agent_loop", "producer-profiles report has no trust_gate agent-loop command")

    claim_limits = payload.get("claim_limits", [])
    if not isinstance(claim_limits, list) or not any("read-model" in str(item) for item in claim_limits):
        _add_issue(issues, "producer_profiles.claim_limits", "producer-profiles report does not state read-model claim limit")

    return {
        "profiles": len(profile_rows),
        "owner_repos": sorted(owner_repos),
        "artifact_classes": sorted(artifact_classes),
    }


def _validate_full_coverage(payload: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, Any]:
    rows_by_class = _rows_by_class(payload)
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    artifact_count = int(summary.get("artifact_classes") or 0)
    fully_covered = int(summary.get("fully_covered") or 0)
    accepted_real_blockers: list[str] = []

    if payload.get("ok") is not True:
        _add_issue(issues, "trust_coverage.ok", "trust-coverage read-model is not ok")
    if summary.get("trust_tools_status") != "ready":
        _add_issue(issues, "trust_coverage.tools", "trust tools are not ready")

    for artifact_class, row in rows_by_class.items():
        if row.get("status") == "DEFERRED_WITH_REAL_BLOCKER":
            blocker_failures = _known_real_blocker_failures(row, durable_only=False)
            if blocker_failures:
                _add_issue(
                    issues,
                    "trust_coverage.accepted_real_blocker",
                    f"{artifact_class} real blocker is not accepted: " + "; ".join(blocker_failures),
                )
            else:
                accepted_real_blockers.append(artifact_class)
            continue
        if row.get("status") != "FULLY_COVERED":
            _add_issue(issues, "trust_coverage.row_status", f"{artifact_class} is not FULLY_COVERED")
            continue
        if not row.get("manual_positive_evidence"):
            _add_issue(issues, "trust_coverage.manual_positive", f"{artifact_class} has no manual positive evidence")
        if not row.get("manual_negative_evidence"):
            _add_issue(issues, "trust_coverage.manual_negative", f"{artifact_class} has no manual negative evidence")
        installed = row.get("installed_verification", {})
        if not isinstance(installed, dict) or installed.get("trust_gate_verdict") not in {"allow", "warn"}:
            _add_issue(issues, "trust_coverage.trust_gate", f"{artifact_class} has no allow/warn consumer gate")

    if artifact_count == 0 or fully_covered + len(accepted_real_blockers) != artifact_count:
        _add_issue(
            issues,
            "trust_coverage.fully_covered",
            "not every artifact class is FULLY_COVERED or an accepted declared real blocker",
        )

    return {
        "artifact_classes": sorted(rows_by_class),
        "summary": summary,
        "accepted_real_blockers": sorted(accepted_real_blockers),
    }


def _validate_durable_coverage(payload: dict[str, Any], issues: list[dict[str, str]]) -> dict[str, Any]:
    rows_by_class = _rows_by_class(payload)
    summary = payload.get("summary", {}) if isinstance(payload.get("summary"), dict) else {}
    artifact_count = int(summary.get("artifact_classes") or 0)
    durable_gate_covered = int(summary.get("durable_gate_covered") or 0)
    accepted_real_blockers: list[str] = []

    if payload.get("ok") is not True:
        _add_issue(issues, "durable_trust_coverage.ok", "durable-only trust-coverage read-model is not ok")
    if int(summary.get("fully_covered") or 0) != 0:
        _add_issue(issues, "durable_trust_coverage.claim_level", "durable-only coverage must not claim FULLY_COVERED")
    if payload.get("manual_evidence_roots") != []:
        _add_issue(issues, "durable_trust_coverage.manual_roots", "durable-only coverage should ignore manual evidence roots")

    for artifact_class, row in rows_by_class.items():
        if row.get("status") == "DEFERRED_WITH_REAL_BLOCKER":
            blocker_failures = _known_real_blocker_failures(row, durable_only=True)
            if blocker_failures:
                _add_issue(
                    issues,
                    "durable_trust_coverage.accepted_real_blocker",
                    f"{artifact_class} durable real blocker is not accepted: " + "; ".join(blocker_failures),
                )
            else:
                accepted_real_blockers.append(artifact_class)
        elif row.get("status") != "DURABLE_GATE_COVERED":
            _add_issue(issues, "durable_trust_coverage.row_status", f"{artifact_class} is not DURABLE_GATE_COVERED")
        if row.get("manual_positive_evidence") or row.get("manual_negative_evidence"):
            _add_issue(issues, "durable_trust_coverage.manual_evidence", f"{artifact_class} durable-only row contains manual evidence")

    if artifact_count == 0 or durable_gate_covered + len(accepted_real_blockers) != artifact_count:
        _add_issue(
            issues,
            "durable_trust_coverage.covered",
            "not every artifact class is DURABLE_GATE_COVERED or an accepted declared real blocker",
        )

    return {
        "artifact_classes": sorted(rows_by_class),
        "summary": summary,
        "accepted_real_blockers": sorted(accepted_real_blockers),
    }


def _validate_coverage_class_set(
    label: str,
    required_classes: set[str],
    observed_classes: set[str],
    issues: list[dict[str, str]],
) -> None:
    missing = sorted(required_classes - observed_classes)
    extra = sorted(observed_classes - required_classes)
    if missing:
        _add_issue(issues, f"{label}.artifact_classes", "missing required artifact classes: " + ", ".join(missing))
    if extra:
        _add_issue(issues, f"{label}.artifact_classes", "unexpected artifact classes: " + ", ".join(extra))


def _single_row(payload: dict[str, Any], artifact_class: str) -> dict[str, Any] | None:
    return _rows_by_class(payload).get(artifact_class)


def _row_drift(row: dict[str, Any] | None) -> dict[str, Any]:
    drift = row.get("drift") if row else None
    return drift if isinstance(drift, dict) else {}


def _row_source_ref(row: dict[str, Any] | None) -> dict[str, Any]:
    source_ref = row.get("source_ref_status") if row else None
    return source_ref if isinstance(source_ref, dict) else {}


def _validate_drift(payloads: dict[str, dict[str, Any]], issues: list[dict[str, str]]) -> dict[str, Any]:
    policy = payloads["policy_drift"]
    sibling_blocked = payloads["sibling_blocked"]
    sibling_accepted_lag = payloads["sibling_accepted_lag"]

    policy_summary = policy.get("summary", {}) if isinstance(policy.get("summary"), dict) else {}
    if policy_summary.get("status_counts", {}).get("needs_reverify") != policy_summary.get("artifact_classes"):
        _add_issue(issues, "affected.policy_manifest", "policy manifest drift does not force needs_reverify for every class")
    if set(policy.get("known_verdicts", [])) != KNOWN_AFFECTED_VERDICTS:
        _add_issue(issues, "affected.known_verdicts", "affected verdict vocabulary is incomplete")
    if set(policy.get("known_drift_statuses", [])) != KNOWN_DRIFT_STATUSES:
        _add_issue(issues, "affected.known_drift_statuses", "affected drift-status vocabulary is incomplete")

    policy_rows = _rows_by_class(policy)
    if len(policy_rows) != int(policy_summary.get("artifact_classes") or 0):
        _add_issue(issues, "affected.policy_manifest_rows", "policy manifest drift lacks row-level drift evidence for every class")
    for artifact_class, row in policy_rows.items():
        drift = _row_drift(row)
        if row.get("verdict") != "needs_reverify" or drift.get("status") != "reverify_required":
            _add_issue(issues, "affected.policy_drift_status", f"{artifact_class} policy drift is not marked reverify_required")
        if drift.get("operationally_blocking") is not True or drift.get("needs_reverify") is not True:
            _add_issue(issues, "affected.policy_drift_blocking", f"{artifact_class} policy drift is not operationally blocking")

    blocked_row = _single_row(sibling_blocked, "aoa_sdk_python_distribution")
    accepted_row = _single_row(sibling_accepted_lag, "aoa_sdk_python_distribution")
    blocked_drift = _row_drift(blocked_row)
    accepted_drift = _row_drift(accepted_row)
    if not blocked_row or blocked_row.get("verdict") != "blocked_by_missing_sibling":
        _add_issue(issues, "affected.blocked_sibling", "unpromoted sibling ref did not block without accepted lag")
    elif _row_source_ref(blocked_row).get("matched") is not False:
        _add_issue(issues, "affected.blocked_sibling_source_ref", "blocked sibling ref did not expose unmatched source_ref_status")
    elif blocked_drift.get("status") != "blocked_missing_sibling":
        _add_issue(issues, "affected.blocked_sibling_drift_status", "blocked sibling ref did not expose blocked_missing_sibling drift")
    elif blocked_drift.get("operationally_blocking") is not True or blocked_drift.get("needs_rebuild") is not True:
        _add_issue(issues, "affected.blocked_sibling_drift_blocking", "blocked sibling ref is not operationally blocking rebuild drift")
    elif blocked_drift.get("source_ref_state") != "missing_current_proof":
        _add_issue(issues, "affected.blocked_sibling_source_ref_state", "blocked sibling ref did not expose missing_current_proof")
    if not accepted_row or accepted_row.get("verdict") != "accepted_lag":
        _add_issue(issues, "affected.accepted_lag", "unpromoted sibling ref did not become accepted_lag with explicit flag")
    elif _row_source_ref(accepted_row).get("matched") is not False:
        _add_issue(issues, "affected.accepted_lag_source_ref", "accepted lag did not keep unmatched source_ref_status visible")
    elif accepted_drift.get("status") != "accepted_lag":
        _add_issue(issues, "affected.accepted_lag_drift_status", "accepted lag did not expose accepted_lag drift")
    elif accepted_drift.get("accepted_lag") is not True or accepted_drift.get("operationally_blocking") is not False:
        _add_issue(issues, "affected.accepted_lag_blocking", "accepted lag did not become explicit nonblocking lag")
    elif accepted_drift.get("source_ref_state") != "missing_current_proof":
        _add_issue(issues, "affected.accepted_lag_source_ref_state", "accepted lag stopped exposing missing_current_proof")

    return {
        "policy_status_counts": policy_summary.get("status_counts", {}),
        "policy_drift_statuses": sorted(
            {
                str(_row_drift(row).get("status"))
                for row in policy_rows.values()
                if _row_drift(row).get("status")
            }
        ),
        "sibling_blocked_verdict": blocked_row.get("verdict") if blocked_row else None,
        "sibling_blocked_drift_status": blocked_drift.get("status") if blocked_drift else None,
        "sibling_blocked_operationally_blocking": blocked_drift.get("operationally_blocking") if blocked_drift else None,
        "sibling_accepted_lag_verdict": accepted_row.get("verdict") if accepted_row else None,
        "sibling_accepted_lag_drift_status": accepted_drift.get("status") if accepted_drift else None,
        "sibling_accepted_lag_operationally_blocking": accepted_drift.get("operationally_blocking") if accepted_drift else None,
    }


def validate_payloads(payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    requirements = _validate_requirements(payloads["requirements"], issues)
    producer_profiles = _validate_producer_profiles(payloads["producer_profiles"], issues)
    trust_coverage = _validate_full_coverage(payloads["trust_coverage"], issues)
    durable_trust_coverage = _validate_durable_coverage(payloads["durable_trust_coverage"], issues)
    required_classes = set(requirements["artifact_classes"])
    _validate_coverage_class_set(
        "trust_coverage",
        required_classes,
        set(trust_coverage["artifact_classes"]),
        issues,
    )
    _validate_coverage_class_set(
        "durable_trust_coverage",
        required_classes,
        set(durable_trust_coverage["artifact_classes"]),
        issues,
    )
    checked = {
        "requirements": requirements,
        "producer_profiles": producer_profiles,
        "trust_coverage": trust_coverage,
        "durable_trust_coverage": durable_trust_coverage,
        "drift": _validate_drift(payloads, issues),
    }
    return {
        "schema": SCHEMA,
        "ok": not issues,
        "issues": issues,
        "checked": checked,
        "required_scenario_classes": REQUIRED_SCENARIO_CLASSES,
        "required_owner_repos": sorted(REQUIRED_OWNER_REPOS),
        "claim_limits": CLAIM_LIMITS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OS Abyss artifact trust-plane scenario coverage from abyss-machine read-models.")
    parser.add_argument("--json", action="store_true", help="print the full validation payload")
    args = parser.parse_args()

    payload = validate_payloads(collect_live_payloads())
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    elif payload["ok"]:
        full = payload["checked"]["trust_coverage"]["summary"]
        durable = payload["checked"]["durable_trust_coverage"]["summary"]
        full_blockers = payload["checked"]["trust_coverage"]["accepted_real_blockers"]
        durable_blockers = payload["checked"]["durable_trust_coverage"]["accepted_real_blockers"]
        print(
            "[ok] OS Abyss artifact trust-plane scenarios verified: "
            f"full={full.get('fully_covered')}/{full.get('artifact_classes')} "
            f"+ blockers={len(full_blockers)}; "
            f"durable={durable.get('durable_gate_covered')}/{durable.get('artifact_classes')} "
            f"+ blockers={len(durable_blockers)}"
        )
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
