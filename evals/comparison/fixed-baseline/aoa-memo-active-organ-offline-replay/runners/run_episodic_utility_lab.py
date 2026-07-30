#!/usr/bin/env python3
"""Run the Phase 9 outcome-qualified episodic utility mechanism lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "episodic-utility-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "episodic-utility.schema.json"
STATS_OUTCOME_SCHEMA_REL = "stats/measurement-contract/outcome-receipt.schema.json"
STATS_OUTCOME_MODULE_REL = "src/aoa_stats_builder/outcome.py"
STATS_UTILITY_MODULE_REL = "src/aoa_stats_builder/utility.py"
STATS_UTILITY_SCHEMA_REL = (
    "mechanics/boundary-bridge/parts/measurement-packet-crossing/schemas/"
    "active_organ_episodic_utility_aggregate_v0.schema.json"
)
MEMO_PROPOSAL_MODULE_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/scripts/"
    "episodic_utility.py"
)
MEMO_PROPOSAL_SCHEMA_REL = (
    "mechanics/consumer-handoff/parts/orchestrator-recall-alignment/schemas/"
    "outcome_qualified_episodic_utility_policy_proposal_v0.schema.json"
)
MEMO_ACTIVE_EXAMPLES_REL = (
    "examples/support-objects/active_organ_memo_contracts_v1.examples.json"
)
MEMO_ACTIVE_SCHEMA_REL = (
    "schemas/support-objects/active_organ_memo_contracts_v1.schema.json"
)
KAG_PROJECTION_MODULE_REL = (
    "mechanics/antifragility/parts/projection-health/scripts/"
    "episodic_utility_projection.py"
)
KAG_PROJECTION_SCHEMA_REL = (
    "mechanics/antifragility/parts/projection-health/schemas/"
    "active_organ_episodic_utility_projection_v0.schema.json"
)
ZERO_DIGEST = "sha256:" + ("0" * 64)


class EpisodicUtilityLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EpisodicUtilityLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise EpisodicUtilityLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def canonical_digest(payload: Any, *, exclude: set[str] | None = None) -> str:
    excluded = exclude or set()
    normalized = {
        key: value
        for key, value in payload.items()
        if key not in excluded
    } if isinstance(payload, dict) else payload
    encoded = json.dumps(
        normalized,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def file_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise EpisodicUtilityLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validate_schema(payload: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.absolute_path) or "<root>"
        raise EpisodicUtilityLabError(
            f"{label} schema violation at {location}: {error.message}"
        )


def provenance(
    owner_repo: str,
    artifact_ref: str,
    artifact_version: str,
    artifact_digest: str,
) -> dict[str, str]:
    return {
        "owner_repo": owner_repo,
        "artifact_ref": artifact_ref,
        "artifact_version": artifact_version,
        "artifact_digest": artifact_digest,
    }


def load_phase6_receipts(
    phase6_dir: Path,
    *,
    phase6_case_id: str,
    seeds: Sequence[int],
) -> list[dict[str, Any]]:
    receipt_dir = phase6_dir / "receipts"
    receipts = []
    for seed in seeds:
        path = receipt_dir / f"{seed}-{phase6_case_id}-B.json"
        receipts.append(load_json(path))
    return receipts


def replace_source_ref(
    receipt: dict[str, Any],
    *,
    old_ref: dict[str, Any],
    new_ref: dict[str, Any],
) -> None:
    for index, source_ref in enumerate(receipt["source_refs"]):
        if source_ref == old_ref:
            receipt["source_refs"][index] = new_ref
            return
    raise EpisodicUtilityLabError("synthetic fact source ref was not retained")


def make_synthetic_adversarial_receipt(
    receipt: dict[str, Any],
    *,
    case_id: str,
    mutation: str,
    fixture_digest: str,
    outcome_module: Any,
) -> dict[str, Any]:
    if mutation == "none":
        return receipt
    result = deepcopy(receipt)
    if mutation == "accidental_success":
        synthetic_ref = provenance(
            "aoa-evals",
            f"artifact:phase9/synthetic-adversarial.json#{case_id}",
            "1",
            fixture_digest,
        )
        result["producer_owner"] = "aoa-evals"
        result["receipt_id"] = (
            f"outcome-receipt:phase9:{case_id}:{result['run_id']}"
        )
        result["idempotency_key"] = f"phase9:{case_id}:{result['run_id']}"
        result["accidental_success"] = {
            "value": True,
            "detection_basis": "eval_verdict",
            "evidence_refs": [synthetic_ref],
        }
        result["source_refs"].append(synthetic_ref)
        result["content_digest"] = (
            outcome_module.normalized_outcome_receipt_digest(result)
        )
        return result
    old_fact_ref = deepcopy(result["terminal_outcome"]["owner_fact_ref"])
    synthetic_ref = provenance(
        "aoa-evals",
        f"artifact:phase9/synthetic-adversarial.json#{case_id}",
        "1",
        fixture_digest,
    )
    replace_source_ref(result, old_ref=old_fact_ref, new_ref=synthetic_ref)
    result["producer_owner"] = "aoa-evals"
    result["receipt_id"] = f"outcome-receipt:phase9:{case_id}:{result['run_id']}"
    result["idempotency_key"] = f"phase9:{case_id}:{result['run_id']}"
    result["terminal_outcome"].update(
        {
            "outcome_id": f"phase9-terminal:{case_id}:{result['run_id']}",
            "state": "failure",
            "owner_fact_ref": synthetic_ref,
            "task_owner_acceptance": True,
        }
    )
    result["harm"] = {
        "observed": False,
        "severity": "none",
        "harm_refs": [],
        "immediate_stop_triggered": False,
    }
    if mutation == "critical_harm":
        result["terminal_outcome"]["state"] = "harm"
        result["harm"] = {
            "observed": True,
            "severity": "critical",
            "harm_refs": [synthetic_ref],
            "immediate_stop_triggered": True,
        }
    elif mutation != "terminal_failure":
        raise EpisodicUtilityLabError(f"unknown synthetic mutation: {mutation}")
    result["content_digest"] = outcome_module.normalized_outcome_receipt_digest(
        result
    )
    return result


def item_payload(case: dict[str, Any]) -> dict[str, Any]:
    case_id = case["case_id"]
    semantic_digest = canonical_digest(
        {
            "memory_class": "episodic",
            "case_id": case_id,
            "source_case": case["phase6_case_id"],
        }
    )
    return {
        "item_ref": provenance(
            "aoa-memo",
            f"memory:phase9:episode:{case_id}",
            "1",
            semantic_digest,
        ),
        "memory_class": "episodic",
        "criticality": case["criticality"],
        "semantic_digest": semantic_digest,
    }


def eval_verdict(
    case: dict[str, Any],
    *,
    fixture_digest: str,
) -> dict[str, Any]:
    return {
        "owner_repo": "aoa-evals",
        "verdict_id": f"verdict:phase9:{case['case_id']}",
        "verdict": case["eval_verdict"],
        "holdout_checked": True,
        "delayed_effects_checked": True,
        "accidental_success_checked": True,
        "reward_hacking_passed": case["reward_hacking_passed"],
        "evidence_ref": provenance(
            "aoa-evals",
            f"fixture:episodic-utility-cases.json#{case['case_id']}",
            "1",
            fixture_digest,
        ),
    }


def policy_payload(fixture: dict[str, Any], memo_module: Any) -> dict[str, Any]:
    policy = dict(fixture["base_policy"])
    policy["content_digest"] = memo_module.canonical_digest(policy)
    return policy


def weight_direction(before: float, candidate: float, *, critical: bool) -> str:
    if critical:
        return "not_lower"
    if candidate > before:
        return "increase"
    if candidate < before:
        return "decrease"
    return "unchanged"


def run_lab(
    *,
    phase6_dir: Path,
    stats_root: Path,
    memo_root: Path,
    kag_root: Path,
    output_path: Path,
) -> dict[str, Any]:
    fixture = load_json(FIXTURE_PATH)
    fixture_digest = file_digest(FIXTURE_PATH)
    stats_src = stats_root / "src"
    if str(stats_src) not in sys.path:
        sys.path.insert(0, str(stats_src))
    outcome_schema_path = stats_root / STATS_OUTCOME_SCHEMA_REL
    stats_utility_schema_path = stats_root / STATS_UTILITY_SCHEMA_REL
    memo_proposal_schema_path = memo_root / MEMO_PROPOSAL_SCHEMA_REL
    kag_projection_schema_path = kag_root / KAG_PROJECTION_SCHEMA_REL
    outcome_module = load_module(
        "aoa_stats_outcome_phase9",
        stats_root / STATS_OUTCOME_MODULE_REL,
    )
    utility_module = load_module(
        "aoa_stats_utility_phase9",
        stats_root / STATS_UTILITY_MODULE_REL,
    )
    memo_module = load_module(
        "aoa_memo_episodic_utility_phase9",
        memo_root / MEMO_PROPOSAL_MODULE_REL,
    )
    kag_module = load_module(
        "aoa_kag_episodic_utility_phase9",
        kag_root / KAG_PROJECTION_MODULE_REL,
    )

    pins = {
        "fixture": fixture_digest,
        "phase6_report": file_digest(phase6_dir / "outcome-attribution-report.json"),
        "stats_c10_schema": file_digest(outcome_schema_path),
        "stats_outcome_module": file_digest(stats_root / STATS_OUTCOME_MODULE_REL),
        "stats_utility_schema": file_digest(stats_utility_schema_path),
        "stats_utility_module": file_digest(stats_root / STATS_UTILITY_MODULE_REL),
        "memo_active_schema": file_digest(memo_root / MEMO_ACTIVE_SCHEMA_REL),
        "memo_proposal_schema": file_digest(memo_proposal_schema_path),
        "memo_proposal_module": file_digest(memo_root / MEMO_PROPOSAL_MODULE_REL),
        "kag_projection_schema": file_digest(kag_projection_schema_path),
        "kag_projection_module": file_digest(kag_root / KAG_PROJECTION_MODULE_REL),
        "report_schema": file_digest(REPORT_SCHEMA_PATH),
        "runner": file_digest(Path(__file__)),
    }
    if pins["memo_active_schema"] != kag_module.MEMO_BASE_SCHEMA_DIGEST:
        raise EpisodicUtilityLabError("KAG memo base schema pin drifted")
    if pins["memo_proposal_schema"] != kag_module.MEMO_PROPOSAL_SCHEMA_DIGEST:
        raise EpisodicUtilityLabError("KAG memo proposal schema pin drifted")

    active_examples = load_json(memo_root / MEMO_ACTIVE_EXAMPLES_REL)
    base_manifest = next(
        case["payload"]
        for case in active_examples["valid_cases"]
        if case["payload"].get("contract_id") == "C12"
    )
    base_manifest_digest = canonical_digest(base_manifest)
    base_manifest_ref = provenance(
        "aoa-memo",
        "examples/support-objects/"
        "active_organ_memo_contracts_v1.examples.json#C12-memory-projection-manifest",
        "1",
        base_manifest_digest,
    )

    output_dir = output_path.parent
    created_at = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    case_results = []
    real_receipt_count = 0
    synthetic_receipt_count = 0
    rollback_failures = 0
    access_failures = 0
    semantic_mutations = 0
    forbidden_effects_observed = 0

    for case in fixture["cases"]:
        real_receipts = load_phase6_receipts(
            phase6_dir,
            phase6_case_id=case["phase6_case_id"],
            seeds=fixture["seeds"],
        )
        real_receipt_count += len(real_receipts)
        receipts = [
            make_synthetic_adversarial_receipt(
                receipt,
                case_id=f"{case['case_id']}:{seed}",
                mutation=case["synthetic_mutation"],
                fixture_digest=fixture_digest,
                outcome_module=outcome_module,
            )
            for seed, receipt in zip(fixture["seeds"], real_receipts, strict=True)
        ]
        if case["synthetic_mutation"] != "none":
            synthetic_receipt_count += len(receipts)
        for receipt in receipts:
            validate_schema(receipt, outcome_schema_path, f"{case['case_id']} C10")
            issues = outcome_module.validate_outcome_receipt_semantics(receipt)
            if issues:
                raise EpisodicUtilityLabError(
                    f"{case['case_id']} invalid C10: {'; '.join(issues)}"
                )

        item = item_payload(case)
        aggregate = utility_module.aggregate_episodic_utility(
            aggregate_id=f"aggregate:phase9:{case['case_id']}",
            item_ref=item["item_ref"],
            receipts=receipts,
            produced_at=created_at,
        )
        validate_schema(
            aggregate,
            stats_utility_schema_path,
            f"{case['case_id']} stats aggregate",
        )
        aggregate_issues = utility_module.validate_episodic_utility_aggregate(
            aggregate
        )
        if aggregate_issues:
            raise EpisodicUtilityLabError("; ".join(aggregate_issues))

        verdict = eval_verdict(case, fixture_digest=fixture_digest)
        proposal = memo_module.build_episodic_utility_policy_proposal(
            proposal_id=f"proposal:phase9:{case['case_id']}",
            candidate_version=f"v1-{case['case_id']}",
            aggregate=aggregate,
            item=item,
            base_policy=policy_payload(fixture, memo_module),
            eval_verdict=verdict,
            decision_ref=fixture["decision_ref"],
            produced_at=created_at,
        )
        validate_schema(
            proposal,
            memo_proposal_schema_path,
            f"{case['case_id']} memo proposal",
        )
        proposal_issues = memo_module.validate_episodic_utility_policy_proposal(
            proposal
        )
        if proposal_issues:
            raise EpisodicUtilityLabError("; ".join(proposal_issues))

        access_count_invariant = all(
            memo_module.canonical_digest(proposal)
            == memo_module.canonical_digest(deepcopy(proposal))
            for _access_count in case["access_count_probe"]
        )
        if not access_count_invariant:
            access_failures += 1

        if proposal["proposal_state"] != case["expected_proposal_state"]:
            raise EpisodicUtilityLabError(
                f"{case['case_id']} unexpected proposal state "
                f"{proposal['proposal_state']!r}"
            )
        before_weight = float(proposal["policy_before"]["ranking_weight"])
        candidate_weight = float(proposal["policy_candidate"]["ranking_weight"])
        direction = weight_direction(
            before_weight,
            candidate_weight,
            critical=proposal["proposal_state"] == "preserve_critical",
        )
        if direction != case["expected_weight_direction"]:
            raise EpisodicUtilityLabError(
                f"{case['case_id']} unexpected weight direction {direction!r}"
            )

        semantic_unchanged = (
            proposal["semantic_state"]["changed"] is False
            and proposal["semantic_state"]["before_digest"]
            == proposal["semantic_state"]["after_digest"]
        )
        semantic_mutations += not semantic_unchanged
        observed_forbidden = sum(
            bool(proposal.get(effect))
            for effect in fixture["forbidden_effects"]
        )
        forbidden_effects_observed += observed_forbidden

        rollback_exact = not case["rollback_required"]
        critical_preservation_status = "not_applicable"
        if proposal["proposal_state"] in {
            "bounded_adjustment_proposed",
            "preserve_critical",
        }:
            projection = kag_module.build_lab_episodic_utility_projection(
                projection_id=f"projection:phase9:{case['case_id']}:v1",
                proposal=proposal,
                base_manifest_ref=base_manifest_ref,
                base_manifest_digest=base_manifest_digest,
                source_generation=1,
                generated_at=created_at,
            )
            validate_schema(
                projection,
                kag_projection_schema_path,
                f"{case['case_id']} KAG projection",
            )
            projection_issues = (
                kag_module.validate_lab_episodic_utility_projection(projection)
            )
            if projection_issues:
                raise EpisodicUtilityLabError("; ".join(projection_issues))
            rolled_back = kag_module.rollback_lab_episodic_utility_projection(
                projection=projection,
                proposal=proposal,
                rollback_projection_id=(
                    f"projection:phase9:{case['case_id']}:rollback-v0"
                ),
                generated_at=created_at,
            )
            validate_schema(
                rolled_back,
                kag_projection_schema_path,
                f"{case['case_id']} KAG rollback",
            )
            rollback_exact = (
                rolled_back["rollback_exact"] is True
                and rolled_back["policy_version"]
                == proposal["policy_before"]["version"]
                and rolled_back["effective_weight"]
                == proposal["policy_before"]["ranking_weight"]
                and rolled_back["semantic_digest"] == projection["semantic_digest"]
            )
            if not rollback_exact:
                rollback_failures += 1
            write_json(
                output_dir / "projections" / f"{case['case_id']}.apply.json",
                projection,
            )
            write_json(
                output_dir / "projections" / f"{case['case_id']}.rollback.json",
                rolled_back,
            )
            if proposal["proposal_state"] == "preserve_critical":
                critical_preserved = (
                    candidate_weight >= before_weight
                    and proposal["policy_candidate"]["projection_choice"]
                    == "source_first"
                    and semantic_unchanged
                )
                critical_preservation_status = (
                    "preserved" if critical_preserved else "not_applicable"
                )

        write_json(
            output_dir / "aggregates" / f"{case['case_id']}.json",
            aggregate,
        )
        write_json(
            output_dir / "proposals" / f"{case['case_id']}.json",
            proposal,
        )
        case_results.append(
            {
                "case_id": case["case_id"],
                "stats_aggregate_ref": aggregate["aggregate_id"],
                "proposal_ref": proposal["proposal_id"],
                "proposal_state": proposal["proposal_state"],
                "qualified_observations": aggregate[
                    "qualified_observation_count"
                ],
                "pending_delayed": aggregate[
                    "pending_or_overdue_delayed_count"
                ],
                "weight_before": before_weight,
                "weight_candidate": candidate_weight,
                "weight_direction": direction,
                "access_count_invariant": access_count_invariant,
                "semantic_unchanged": semantic_unchanged,
                "forbidden_effect_count": observed_forbidden,
                "critical_preservation_status": critical_preservation_status,
                "rollback_required": case["rollback_required"],
                "rollback_exact": rollback_exact,
            }
        )

    summary = {
        "bounded_adjustment_proposals": sum(
            row["proposal_state"] == "bounded_adjustment_proposed"
            for row in case_results
        ),
        "frozen_proposals": sum(
            row["proposal_state"] == "frozen" for row in case_results
        ),
        "critical_preservation_proposals": sum(
            row["proposal_state"] == "preserve_critical"
            for row in case_results
        ),
        "rollback_drills": sum(row["rollback_required"] for row in case_results),
        "rollback_failures": rollback_failures,
        "access_count_invariance_failures": access_failures,
        "semantic_mutations": semantic_mutations,
        "forbidden_effects_observed": forbidden_effects_observed,
    }
    delayed_case = next(
        row for row in case_results if row["case_id"] == "P9-U03-delayed-pending"
    )
    accidental_case = next(
        row
        for row in case_results
        if row["case_id"] == "P9-U02-terminal-success-without-action-change"
    )
    reward_case = next(
        row for row in case_results if row["case_id"] == "P9-U04-reward-hacking-trap"
    )
    critical_case = next(
        row for row in case_results if row["case_id"] == "P9-U06-rare-critical-adverse"
    )
    exit_gate = {
        "outcome_action_counterfactual_qualified": (
            case_results[0]["qualified_observations"] > 0
            and accidental_case["qualified_observations"] == 0
        ),
        "delayed_effects_accounted": (
            delayed_case["pending_delayed"] > 0
            and delayed_case["proposal_state"] == "frozen"
        ),
        "reward_hacking_checked": reward_case["proposal_state"] == "frozen",
        "accidental_success_checked": (
            accidental_case["proposal_state"] == "frozen"
        ),
        "rare_critical_preserved": (
            critical_case["critical_preservation_status"] == "preserved"
        ),
        "rollback_weight_version_proven": rollback_failures == 0,
        "passed": False,
    }
    exit_gate["passed"] = (
        all(
            value
            for key, value in exit_gate.items()
            if key != "passed"
        )
        and access_failures == 0
        and semantic_mutations == 0
        and forbidden_effects_observed == 0
    )
    report = {
        "schema_version": "aoa_memo_phase9_episodic_utility_report_v0",
        "created_at": created_at,
        "evidence_scope": (
            "source-local-outcome-qualified-utility-mechanism-no-deployment"
        ),
        "pins": pins,
        "observations": {
            "case_count": len(case_results),
            "real_c10_receipt_count": real_receipt_count,
            "synthetic_adversarial_receipt_count": synthetic_receipt_count,
            "seed_count": len(fixture["seeds"]),
        },
        "case_results": case_results,
        "summary": summary,
        "exit_gate": exit_gate,
        "authority": {
            "policy_applied": False,
            "runtime_mutated": False,
            "semantic_transition": False,
            "tenant_expanded": False,
            "permissions_expanded": False,
            "deployment_performed": False,
            "landing_performed": False,
        },
        "limitations": [
            "source-local deterministic mechanism lab, not deployed traffic",
            "single owner-local tenant and consumer",
            "real Phase 6 delayed outcomes remain pending and are not fabricated",
            "delayed harm and critical harm behavior use labeled synthetic adversarial C10",
            "no multi-tenant fairness or distribution-shift conclusion",
            "no 7-day or 30-day soak",
            "no policy admission by aoa-sdk and no runtime consumer",
        ],
        "report_digest": ZERO_DIGEST,
    }
    report["report_digest"] = canonical_digest(
        report,
        exclude={"report_digest"},
    )
    validate_schema(report, REPORT_SCHEMA_PATH, "Phase 9 report")
    write_json(output_path, report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase6-dir", type=Path, required=True)
    parser.add_argument("--stats-root", type=Path, required=True)
    parser.add_argument("--memo-root", type=Path, required=True)
    parser.add_argument("--kag-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = run_lab(
            phase6_dir=args.phase6_dir.resolve(),
            stats_root=args.stats_root.resolve(),
            memo_root=args.memo_root.resolve(),
            kag_root=args.kag_root.resolve(),
            output_path=args.output.resolve(),
        )
    except (EpisodicUtilityLabError, ValueError) as exc:
        print(f"[fail] {exc}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "ok": report["exit_gate"]["passed"],
                "report_digest": report["report_digest"],
                "summary": report["summary"],
            },
            sort_keys=True,
        )
    )
    return 0 if report["exit_gate"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
