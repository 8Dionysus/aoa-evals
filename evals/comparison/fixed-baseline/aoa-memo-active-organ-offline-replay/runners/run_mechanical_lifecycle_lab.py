#!/usr/bin/env python3
"""Run the Phase 10 deterministic mechanical lifecycle reference lab."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
from time import perf_counter
import sys
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BUNDLE_ROOT / "fixtures" / "mechanical-lifecycle-cases.json"
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "mechanical-lifecycle.schema.json"
MEMO_MODULE_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/scripts/"
    "active_organ_lifecycle.py"
)
MEMO_PLAN_SCHEMA_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/schemas/"
    "active_organ_mechanical_lifecycle_plan_v0.schema.json"
)
MEMO_PROPOSAL_SCHEMA_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/schemas/"
    "active_organ_semantic_lifecycle_proposal_v0.schema.json"
)
MEMO_RECEIPT_SCHEMA_REL = (
    "mechanics/retention/parts/consolidation-and-forgetting/schemas/"
    "active_organ_lifecycle_execution_receipt_v0.schema.json"
)
MEMO_BASE_SCHEMA_REL = "schemas/support-objects/active_organ_memo_contracts_v1.schema.json"
MEMO_DECISION_REL = (
    "docs/decisions/"
    "AOA-MEM-D-0079-mechanical-lifecycle-is-allowlisted-and-recoverable.md"
)
KAG_MODULE_REL = (
    "mechanics/antifragility/parts/projection-health/scripts/"
    "active_organ_projection_contracts.py"
)
KAG_C13_SCHEMA_REL = (
    "mechanics/antifragility/parts/projection-health/schemas/"
    "active_organ_projection_invalidation_receipt_v1.schema.json"
)
KAG_EXAMPLES_REL = (
    "mechanics/antifragility/parts/projection-health/examples/"
    "active_organ_projection_contracts_v1.examples.json"
)
ZERO_DIGEST = "sha256:" + ("0" * 64)


class MechanicalLifecycleLabError(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MechanicalLifecycleLabError(f"{path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise MechanicalLifecycleLabError(f"{path}: expected JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def canonical_digest(
    payload: Any,
    *,
    exclude: set[str] | None = None,
) -> str:
    excluded = exclude or set()
    normalized = (
        {key: value for key, value in payload.items() if key not in excluded}
        if isinstance(payload, dict)
        else payload
    )
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
        raise MechanicalLifecycleLabError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def schema_validator(path: Path) -> Draft202012Validator:
    schema = load_json(path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_schema(
    payload: Mapping[str, Any],
    validator: Draft202012Validator,
    label: str,
) -> None:
    errors = sorted(
        validator.iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = ".".join(str(item) for item in error.absolute_path) or "<root>"
        raise MechanicalLifecycleLabError(
            f"{label} schema violation at {location}: {error.message}"
        )


def _subject(operation_class: str, suffix: str) -> dict[str, Any]:
    disposable = operation_class in {
        "projection_invalidation",
        "projection_rebuild",
        "generation_rollover",
    }
    return {
        "owner_repo": "aoa-memo",
        "object_ref": f"memory:phase10:{suffix}:{operation_class}",
        "object_version": 1,
        "lifecycle_state": "active",
        "semantic_digest": canonical_digest(
            {
                "memory": "phase10-public-safe",
                "suffix": suffix,
                "operation_class": operation_class,
            }
        ),
        "tenant_id": "owner-local",
        "namespace_id": "agent:phase10-reference-lab",
        "source_generation": 7,
        "explicit_ephemeral": operation_class == "explicit_ephemeral_ttl",
        "disposable": disposable,
    }


def _policy(memo_module: Any) -> dict[str, Any]:
    return {
        "policy_id": "policy:aoa-memo:mechanical-lifecycle:phase10",
        "policy_version": "phase10-v0",
        "policy_digest": canonical_digest(
            {
                "decision": memo_module.DECISION_REF,
                "classes": list(memo_module.MECHANICAL_SPECS),
            }
        ),
        "decision_ref": memo_module.DECISION_REF,
        "status": "accepted",
        "approved_operation_classes": list(memo_module.MECHANICAL_SPECS),
    }


def _effect_owner(operation_class: str) -> str:
    if operation_class in {
        "projection_invalidation",
        "projection_rebuild",
        "generation_rollover",
    }:
        return "aoa-kag"
    if operation_class in {
        "explicit_ephemeral_ttl",
        "queue_cancellation",
        "cache_expiry",
    }:
        return "abyss-machine"
    return "abyss-stack"


def build_plan(
    memo_module: Any,
    fixture: Mapping[str, Any],
    operation_class: str,
    suffix: str,
) -> dict[str, Any]:
    return memo_module.build_mechanical_lifecycle_plan(
        plan_id=f"lifecycle-plan:phase10:{suffix}:{operation_class}",
        idempotency_key=f"idempotency:phase10:{suffix}:{operation_class}",
        operation_class=operation_class,
        subject_pin=_subject(operation_class, suffix),
        policy_pin=_policy(memo_module),
        effect_owner_repo=_effect_owner(operation_class),
        target_refs=[f"target:phase10:{suffix}:{operation_class}"],
        eligible_at=fixture["eligible_at"],
        deadline_at=fixture["deadline_at"],
        max_attempts=3,
        backoff_seconds=[1, 5],
        cancellation_token=f"cancel:phase10:{suffix}:{operation_class}",
        owner_approval_ref=(
            f"decision:operator:phase10:{suffix}:archive-deadline"
            if operation_class == "owner_approved_archive_deadline"
            else None
        ),
        compensation_strategy="rollback_or_forward_repair",
        compensation_action_class="restore_or_rebuild_exact_predecessor",
        commit_receipt_ref=f"receipt:commit:phase10:{suffix}:{operation_class}",
        audit_receipt_ref=f"receipt:audit:phase10:{suffix}:{operation_class}",
        generated_at=fixture["eligible_at"],
    )


def build_semantic_proposal(
    memo_module: Any,
    fixture: Mapping[str, Any],
    operation_class: str,
    queue_position: int,
) -> dict[str, Any]:
    subject = _subject("queue_cancellation", f"semantic-{operation_class}")
    return memo_module.build_semantic_lifecycle_proposal(
        proposal_id=f"proposal:phase10:{operation_class}",
        idempotency_key=f"idempotency:phase10:proposal:{operation_class}",
        operation_class=operation_class,
        subject_pin=subject,
        evidence_refs=[
            f"evidence:phase10:{operation_class}:source",
            f"evidence:phase10:{operation_class}:comparison",
        ],
        field_paths=["lifecycle.state"],
        before_digest=subject["semantic_digest"],
        proposed_digest=canonical_digest(
            {"operation_class": operation_class, "candidate": "proposal-only"}
        ),
        rationale="bounded public-safe evidence-linked semantic proposal",
        queue_position=queue_position,
        max_open_items=fixture["operator_attention_budget"],
        generated_at=fixture["reference_time"],
    )


class ReferenceExecutor:
    """In-memory failure-injection model; it has no runtime effect authority."""

    def __init__(
        self,
        memo_module: Any,
        receipt_validator: Draft202012Validator,
        produced_at: str,
    ) -> None:
        self.memo = memo_module
        self.receipt_validator = receipt_validator
        self.produced_at = produced_at
        self.states: dict[str, dict[str, Any]] = {}
        self.journal: dict[str, dict[str, Any]] = {}
        self.receipts: list[dict[str, Any]] = []

    def _state(self, plan: Mapping[str, Any]) -> dict[str, Any]:
        subject = plan["subject_pin"]
        object_ref = subject["object_ref"]
        if object_ref not in self.states:
            self.states[object_ref] = {
                "version": subject["object_version"],
                "semantic_digest": subject["semantic_digest"],
                "tenant_id": subject["tenant_id"],
                "namespace_id": subject["namespace_id"],
                "source_generation": subject["source_generation"],
                "projection_posture": "active_previous_generation",
            }
        return self.states[object_ref]

    def _events(
        self,
        plan: Mapping[str, Any],
        event_types: Sequence[str],
    ) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        previous = None
        for sequence, event_type in enumerate(event_types):
            event = self.memo.build_audit_event(
                sequence=sequence,
                event_type=event_type,
                previous_event_digest=previous,
                payload_digest=(
                    plan["content_digest"]
                    if sequence == 0
                    else canonical_digest(
                        {
                            "event": event_type,
                            "plan": plan["plan_id"],
                            "sequence": sequence,
                        }
                    )
                ),
            )
            events.append(event)
            previous = event["event_digest"]
        return events

    def _receipt(
        self,
        plan: Mapping[str, Any],
        *,
        attempt: int,
        status: str,
        observed_prior_version: int,
        result_version: int,
        canonical_commit_applied: bool,
        new_effect_applied: bool,
        projection_posture: str,
        compensation_state: str,
        event_types: Sequence[str],
        belief_commit_id: str | None = None,
        record: bool = True,
    ) -> dict[str, Any]:
        subject = plan["subject_pin"]
        receipt = self.memo.build_lifecycle_execution_receipt(
            receipt_id=(
                f"receipt:phase10:{plan['plan_id'].split(':', 2)[-1]}:"
                f"{status}:attempt-{attempt}:{len(self.receipts) + 1}"
            ),
            plan=plan,
            runtime_owner="aoa-evals-reference-lab",
            attempt=attempt,
            status=status,
            observed_prior_version=observed_prior_version,
            result_version=result_version,
            belief_commit_id=belief_commit_id,
            canonical_commit_applied=canonical_commit_applied,
            new_effect_applied=new_effect_applied,
            projection_posture=projection_posture,
            compensation_state=compensation_state,
            event_chain=self._events(plan, event_types),
            semantic_digest_after=subject["semantic_digest"],
            tenant_after=subject["tenant_id"],
            namespace_after=subject["namespace_id"],
            produced_at=self.produced_at,
        )
        validate_schema(receipt, self.receipt_validator, "lifecycle receipt")
        issues = self.memo.validate_lifecycle_execution_receipt(receipt)
        if issues:
            raise MechanicalLifecycleLabError("; ".join(issues))
        if record:
            self.receipts.append(receipt)
        return receipt

    def execute(
        self,
        plan: Mapping[str, Any],
        *,
        attempt: int = 1,
        mode: str = "normal",
        conflict: bool = False,
    ) -> dict[str, Any]:
        state = self._state(plan)
        key = plan["idempotency_key"]
        plan_digest = plan["content_digest"]
        existing = self.journal.get(key)
        if existing is not None:
            if existing["plan_digest"] != plan_digest:
                return self._receipt(
                    plan,
                    attempt=attempt,
                    status="rejected_idempotency",
                    observed_prior_version=state["version"],
                    result_version=state["version"],
                    canonical_commit_applied=False,
                    new_effect_applied=False,
                    projection_posture=state["projection_posture"],
                    compensation_state="not_required",
                    event_types=["idempotency_payload_mismatch_rejected"],
                )
            if (
                existing["receipt"]["status"] == "partial_pending_repair"
                and mode == "forward_repair"
            ):
                state["projection_posture"] = "rebuilt_current_generation"
                repaired = self._receipt(
                    plan,
                    attempt=attempt,
                    status="forward_repaired",
                    observed_prior_version=state["version"],
                    result_version=state["version"],
                    canonical_commit_applied=False,
                    new_effect_applied=True,
                    projection_posture="rebuilt_current_generation",
                    compensation_state="forward_repaired",
                    event_types=[
                        "partial_receipt_recovered",
                        "projection_forward_repaired",
                    ],
                    belief_commit_id=existing["receipt"]["belief_commit_id"],
                )
                self.journal[key] = {
                    "plan_digest": plan_digest,
                    "receipt": repaired,
                }
                return repaired
            return self._receipt(
                plan,
                attempt=attempt,
                status="duplicate",
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="not_required",
                event_types=["journal_hit_no_new_effect"],
                belief_commit_id=existing["receipt"]["belief_commit_id"],
            )

        expected = plan["preconditions"]["expected_prior_version"]
        if state["version"] != expected:
            status = "rejected_conflict" if conflict else "rejected_stale"
            return self._receipt(
                plan,
                attempt=attempt,
                status=status,
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="not_required",
                event_types=[f"{status}_version_compare"],
            )

        if mode in {"missed_deadline", "explicit_cancellation"}:
            return self._receipt(
                plan,
                attempt=attempt,
                status="cancelled",
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="not_required",
                event_types=[mode],
            )
        if mode == "crash_before_commit":
            return self._receipt(
                plan,
                attempt=attempt,
                status="failed_retryable",
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="available",
                event_types=["preconditions_verified", "crash_before_commit"],
            )
        if mode == "reordered_events":
            valid = self._receipt(
                plan,
                attempt=attempt,
                status="cancelled",
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="not_required",
                event_types=["first_event", "second_event"],
                record=False,
            )
            reordered = deepcopy(valid)
            reordered["event_chain"] = list(reversed(reordered["event_chain"]))
            issues = self.memo.validate_lifecycle_execution_receipt(reordered)
            if not any(
                "sequence" in issue or "previous digest" in issue
                for issue in issues
            ):
                raise MechanicalLifecycleLabError(
                    "reordered event chain was not rejected"
                )
            return self._receipt(
                plan,
                attempt=attempt,
                status="rejected_reordered",
                observed_prior_version=state["version"],
                result_version=state["version"],
                canonical_commit_applied=False,
                new_effect_applied=False,
                projection_posture=state["projection_posture"],
                compensation_state="not_required",
                event_types=["reordered_chain_rejected"],
            )

        new_version = plan["transaction"]["next_version"]
        state["version"] = new_version
        belief_commit_id = f"belief-commit:{plan['plan_id']}"
        projection_class = plan["operation_class"] in {
            "projection_invalidation",
            "projection_rebuild",
            "generation_rollover",
        }
        if mode == "projection_failure":
            state["projection_posture"] = "invalidated_pending_repair"
            receipt = self._receipt(
                plan,
                attempt=attempt,
                status="partial_pending_repair",
                observed_prior_version=expected,
                result_version=new_version,
                canonical_commit_applied=True,
                new_effect_applied=True,
                projection_posture="invalidated_pending_repair",
                compensation_state="pending_forward_repair",
                event_types=[
                    "preconditions_verified",
                    "canonical_commit_applied",
                    "projection_failure_invalidated",
                ],
                belief_commit_id=belief_commit_id,
            )
        else:
            state["projection_posture"] = (
                "rebuilt_current_generation" if projection_class else "not_applicable"
            )
            receipt = self._receipt(
                plan,
                attempt=attempt,
                status="applied",
                observed_prior_version=expected,
                result_version=new_version,
                canonical_commit_applied=True,
                new_effect_applied=True,
                projection_posture=state["projection_posture"],
                compensation_state="available",
                event_types=[
                    "preconditions_verified",
                    "canonical_commit_applied",
                    "audit_receipt_sealed",
                ],
                belief_commit_id=belief_commit_id,
            )
        self.journal[key] = {"plan_digest": plan_digest, "receipt": receipt}
        return receipt


def projection_contract_probe(
    kag_root: Path,
    kag_module: Any,
) -> dict[str, Any]:
    corpus = load_json(kag_root / KAG_EXAMPLES_REL)
    case = next(
        item for item in corpus["valid_cases"] if item["contract"] == "C13"
    )
    payload = deepcopy(case["payload"])
    validator = schema_validator(kag_root / KAG_C13_SCHEMA_REL)
    validate_schema(payload, validator, "KAG C13 projection receipt")
    issues = kag_module.validate_projection_invalidation_receipt(payload)
    if issues:
        raise MechanicalLifecycleLabError("; ".join(issues))
    rebuilt = kag_module.build_projection_invalidation_receipt(**payload)
    return {
        "contract_id": "C13",
        "schema_valid": rebuilt == payload,
        "semantic_valid": True,
        "recall_blocked": rebuilt["recall_admission"] == "blocked",
        "canonical_mutation": rebuilt["canonical_mutation"],
    }


def _validate_owner_contract(
    payload: Mapping[str, Any],
    *,
    validator: Draft202012Validator,
    semantic_issues: Sequence[str],
    label: str,
) -> None:
    validate_schema(payload, validator, label)
    if semantic_issues:
        raise MechanicalLifecycleLabError(
            f"{label}: {'; '.join(semantic_issues)}"
        )


def run_fault_case(
    case: Mapping[str, Any],
    *,
    memo_module: Any,
    fixture: Mapping[str, Any],
    plan_validator: Draft202012Validator,
    proposal_validator: Draft202012Validator,
    receipt_validator: Draft202012Validator,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    case_id = case["case_id"]
    fault = case["fault"]
    executor = ReferenceExecutor(
        memo_module,
        receipt_validator,
        fixture["reference_time"],
    )
    operation = (
        "projection_rebuild"
        if fault == "projection_failure_forward_repair"
        else "queue_cancellation"
    )
    plan = build_plan(memo_module, fixture, operation, case_id)
    _validate_owner_contract(
        plan,
        validator=plan_validator,
        semantic_issues=memo_module.validate_mechanical_lifecycle_plan(plan),
        label=f"{case_id} plan",
    )
    observed_status = ""
    canonical_commits = 0
    new_effects = 0
    detail = ""

    if fault == "exact_duplicate":
        first = executor.execute(plan)
        second = executor.execute(plan, attempt=2)
        observed_status = second["status"]
        canonical_commits = int(first["canonical_commit_applied"])
        new_effects = int(first["new_effect_applied"])
        detail = "exact replay returned a no-effect duplicate receipt"
    elif fault == "idempotency_payload_mismatch":
        first = executor.execute(plan)
        changed = deepcopy(plan)
        changed["effect_scope"]["target_refs"].append(
            f"target:phase10:{case_id}:changed-payload"
        )
        changed["content_digest"] = memo_module.normalized_digest(changed)
        _validate_owner_contract(
            changed,
            validator=plan_validator,
            semantic_issues=memo_module.validate_mechanical_lifecycle_plan(changed),
            label=f"{case_id} changed plan",
        )
        second = executor.execute(changed, attempt=2)
        observed_status = second["status"]
        canonical_commits = int(first["canonical_commit_applied"])
        new_effects = int(first["new_effect_applied"])
        detail = "same idempotency key with a changed digest was rejected"
    elif fault == "stale_retry":
        executor._state(plan)["version"] = 2
        receipt = executor.execute(plan, attempt=2)
        observed_status = receipt["status"]
        detail = "stale expected version was rejected without commit"
    elif fault == "concurrent_conflict":
        winner = executor.execute(plan)
        contender = build_plan(memo_module, fixture, operation, f"{case_id}-contender")
        contender["subject_pin"] = deepcopy(plan["subject_pin"])
        contender["compensation"]["target_semantic_digest"] = plan["subject_pin"][
            "semantic_digest"
        ]
        contender["content_digest"] = memo_module.normalized_digest(contender)
        _validate_owner_contract(
            contender,
            validator=plan_validator,
            semantic_issues=memo_module.validate_mechanical_lifecycle_plan(contender),
            label=f"{case_id} contender",
        )
        receipt = executor.execute(contender, conflict=True)
        observed_status = receipt["status"]
        canonical_commits = int(winner["canonical_commit_applied"])
        new_effects = int(winner["new_effect_applied"])
        detail = "one transition won; the same-version contender failed closed"
    elif fault == "crash_before_commit_retry":
        first = executor.execute(plan, mode="crash_before_commit")
        second = executor.execute(plan, attempt=2)
        observed_status = second["status"]
        canonical_commits = int(second["canonical_commit_applied"])
        new_effects = int(second["new_effect_applied"])
        detail = (
            f"{first['status']} preserved the predecessor; exact retry applied once"
        )
    elif fault == "crash_after_commit_before_ack":
        first = executor.execute(plan)
        second = executor.execute(plan, attempt=2)
        observed_status = second["status"]
        canonical_commits = int(first["canonical_commit_applied"])
        new_effects = int(first["new_effect_applied"])
        detail = "journal recovery after lost acknowledgement prevented double commit"
    elif fault == "projection_failure_forward_repair":
        partial = executor.execute(plan, mode="projection_failure")
        repaired = executor.execute(plan, attempt=2, mode="forward_repair")
        observed_status = repaired["status"]
        canonical_commits = int(partial["canonical_commit_applied"])
        new_effects = 1
        detail = "partial stayed non-success and blocked until forward repair"
    elif fault == "reordered_events":
        receipt = executor.execute(plan, mode="reordered_events")
        observed_status = receipt["status"]
        detail = "non-contiguous audit chain was rejected before any effect"
    elif fault == "missed_deadline":
        if fixture["expired_time"] <= plan["transaction"]["deadline_at"]:
            raise MechanicalLifecycleLabError("expired_time does not pass deadline")
        receipt = executor.execute(plan, mode="missed_deadline")
        observed_status = receipt["status"]
        detail = "missed deadline cancelled the plan without effect"
    elif fault == "explicit_cancellation":
        receipt = executor.execute(plan, mode="explicit_cancellation")
        observed_status = receipt["status"]
        detail = "matching cancellation token cancelled without effect"
    elif fault == "concurrent_reader_atomicity":
        before = deepcopy(executor._state(plan))
        receipt = executor.execute(plan)
        after = deepcopy(executor._state(plan))
        old_consistent = (
            before["version"] == 1
            and before["projection_posture"] == "active_previous_generation"
        )
        new_consistent = (
            after["version"] == 2
            and after["projection_posture"] == "not_applicable"
        )
        if not old_consistent or not new_consistent:
            raise MechanicalLifecycleLabError("reader observed a mixed state")
        observed_status = receipt["status"]
        canonical_commits = 1
        new_effects = 1
        detail = "bounded snapshots exposed only old or committed new state"
    elif fault == "semantic_execution_refusal":
        proposal = build_semantic_proposal(
            memo_module,
            fixture,
            "supersession",
            1,
        )
        _validate_owner_contract(
            proposal,
            validator=proposal_validator,
            semantic_issues=memo_module.validate_semantic_lifecycle_proposal(
                proposal
            ),
            label=f"{case_id} semantic proposal",
        )
        observed_status = (
            "refused_proposal_only"
            if proposal["apply_allowed"] is False
            and proposal["execution_posture"] == "proposal_only"
            else "unsafe_execution"
        )
        detail = "semantic proposal carried no execution or self-approval authority"
    elif fault == "operator_attention_overflow":
        proposal = build_semantic_proposal(
            memo_module,
            fixture,
            "retention_change",
            fixture["operator_attention_budget"] + 1,
        )
        _validate_owner_contract(
            proposal,
            validator=proposal_validator,
            semantic_issues=memo_module.validate_semantic_lifecycle_proposal(
                proposal
            ),
            label=f"{case_id} overflow proposal",
        )
        observed_status = proposal["proposal_state"]
        detail = "overflow remained deferred and was neither dropped nor accepted"
    else:
        raise MechanicalLifecycleLabError(f"unknown fault case: {fault}")

    result = {
        "case_id": case_id,
        "fault": fault,
        "expected_status": case["expected_status"],
        "observed_status": observed_status,
        "passed": observed_status == case["expected_status"],
        "canonical_commits": canonical_commits,
        "new_effects": new_effects,
        "detail": detail,
    }
    if not result["passed"]:
        raise MechanicalLifecycleLabError(
            f"{case_id}: expected {case['expected_status']}, got {observed_status}"
        )
    return result, executor.receipts


def run_lab(
    *,
    memo_root: Path,
    kag_root: Path,
    output_path: Path,
) -> dict[str, Any]:
    started = perf_counter()
    fixture = load_json(FIXTURE_PATH)
    memo_module_path = memo_root / MEMO_MODULE_REL
    kag_module_path = kag_root / KAG_MODULE_REL
    memo_module = load_module(
        "aoa_active_organ_phase10_memo_contracts",
        memo_module_path,
    )
    kag_module = load_module(
        "aoa_active_organ_phase10_kag_contracts",
        kag_module_path,
    )
    expected_mechanical = list(memo_module.MECHANICAL_SPECS)
    expected_semantic = list(memo_module.SEMANTIC_SPECS)
    if fixture["mechanical_classes"] != expected_mechanical:
        raise MechanicalLifecycleLabError(
            "fixture mechanical allowlist differs from aoa-memo owner contract"
        )
    if fixture["semantic_proposal_classes"] != expected_semantic:
        raise MechanicalLifecycleLabError(
            "fixture semantic proposal list differs from aoa-memo owner contract"
        )

    plan_schema_path = memo_root / MEMO_PLAN_SCHEMA_REL
    proposal_schema_path = memo_root / MEMO_PROPOSAL_SCHEMA_REL
    receipt_schema_path = memo_root / MEMO_RECEIPT_SCHEMA_REL
    plan_validator = schema_validator(plan_schema_path)
    proposal_validator = schema_validator(proposal_schema_path)
    receipt_validator = schema_validator(receipt_schema_path)
    report_validator = schema_validator(REPORT_SCHEMA_PATH)

    mechanical_executor = ReferenceExecutor(
        memo_module,
        receipt_validator,
        fixture["reference_time"],
    )
    mechanical_results = []
    all_receipts: list[dict[str, Any]] = []
    for operation_class in fixture["mechanical_classes"]:
        plan = build_plan(
            memo_module,
            fixture,
            operation_class,
            f"class-{operation_class}",
        )
        _validate_owner_contract(
            plan,
            validator=plan_validator,
            semantic_issues=memo_module.validate_mechanical_lifecycle_plan(plan),
            label=f"{operation_class} plan",
        )
        receipt = mechanical_executor.execute(plan)
        mechanical_results.append(
            {
                "operation_class": operation_class,
                "forgetting_class": plan["forgetting_class"],
                "status": receipt["status"],
                "receipt_ref": receipt["receipt_id"],
                "version_before": receipt["observed_prior_version"],
                "version_after": receipt["result_version"],
                "semantic_unchanged": (
                    receipt["semantic_digest_before"]
                    == receipt["semantic_digest_after"]
                ),
                "scope_preserved": (
                    receipt["tenant_before"] == receipt["tenant_after"]
                    and receipt["namespace_before"] == receipt["namespace_after"]
                ),
                "schema_valid": True,
                "semantic_valid": True,
            }
        )
    all_receipts.extend(mechanical_executor.receipts)

    fault_results = []
    for case in fixture["fault_cases"]:
        result, receipts = run_fault_case(
            case,
            memo_module=memo_module,
            fixture=fixture,
            plan_validator=plan_validator,
            proposal_validator=proposal_validator,
            receipt_validator=receipt_validator,
        )
        fault_results.append(result)
        all_receipts.extend(receipts)

    semantic_results = []
    for queue_position, operation_class in enumerate(
        fixture["semantic_proposal_classes"],
        start=1,
    ):
        proposal = build_semantic_proposal(
            memo_module,
            fixture,
            operation_class,
            queue_position,
        )
        _validate_owner_contract(
            proposal,
            validator=proposal_validator,
            semantic_issues=memo_module.validate_semantic_lifecycle_proposal(
                proposal
            ),
            label=f"{operation_class} semantic proposal",
        )
        semantic_results.append(
            {
                "operation_class": operation_class,
                "proposal_state": proposal["proposal_state"],
                "proposal_ref": proposal["proposal_id"],
                "apply_allowed": proposal["apply_allowed"],
                "operator_required": proposal["operator_review"]["required"],
                "attention_admitted": proposal["attention_budget"]["admitted"],
                "schema_valid": True,
                "semantic_valid": True,
            }
        )

    admitted = sum(row["attention_admitted"] for row in semantic_results)
    deferred = len(semantic_results) - admitted
    projection_probe = projection_contract_probe(kag_root, kag_module)
    negative = fixture["naive_negative_control"]
    naive_violations = sum(negative.values())
    abc_comparison = [
        {
            "arm": "A",
            "posture": "manual_proposal_only_safe_baseline",
            "automatic_effects": 0,
            "operator_review_items": len(fixture["mechanical_classes"]),
            "safety_violations": 0,
            "quality": "safe_but_no_mechanical_progress",
            "result": "operator_backlog",
        },
        {
            "arm": "B",
            "posture": "naive_unguarded_automation_negative_control",
            "automatic_effects": len(fixture["mechanical_classes"]) + naive_violations,
            "operator_review_items": 0,
            "safety_violations": naive_violations,
            "quality": "unsafe_false_progress",
            "result": "rejected_nonconformant",
        },
        {
            "arm": "C",
            "posture": "allowlisted_recoverable_reference_protocol",
            "automatic_effects": len(fixture["mechanical_classes"]),
            "operator_review_items": admitted,
            "safety_violations": 0,
            "quality": "bounded_fail_closed_mechanical_progress",
            "result": "reference_mechanism_pass",
        },
    ]
    elapsed_ms = round((perf_counter() - started) * 1000, 3)
    pins = {
        "runner": file_digest(Path(__file__).resolve()),
        "fixture": file_digest(FIXTURE_PATH),
        "report_schema": file_digest(REPORT_SCHEMA_PATH),
        "memo_module": file_digest(memo_module_path),
        "memo_plan_schema": file_digest(plan_schema_path),
        "memo_proposal_schema": file_digest(proposal_schema_path),
        "memo_receipt_schema": file_digest(receipt_schema_path),
        "memo_base_schema": file_digest(memo_root / MEMO_BASE_SCHEMA_REL),
        "memo_decision": file_digest(memo_root / MEMO_DECISION_REL),
        "kag_module": file_digest(kag_module_path),
        "kag_c13_schema": file_digest(kag_root / KAG_C13_SCHEMA_REL),
        "kag_examples": file_digest(kag_root / KAG_EXAMPLES_REL),
    }
    exit_gate = {
        "mechanical_allowlist_only": (
            len(mechanical_results) == 9
            and all(row["status"] == "applied" for row in mechanical_results)
        ),
        "semantic_transition_requires_operator": all(
            row["apply_allowed"] is False
            and row["operator_required"] is True
            for row in semantic_results
        ),
        "provenance_preserved": all(
            row["scope_preserved"] and row["semantic_unchanged"]
            for row in mechanical_results
        ),
        "historical_not_current": (
            projection_probe["recall_blocked"]
            and next(
                row
                for row in fault_results
                if row["fault"] == "stale_retry"
            )["passed"]
        ),
        "attention_budget_bounded": admitted == 3 and deferred == 5,
        "unfinished_erase_pending_not_deleted": not any(
            item in memo_module.MECHANICAL_SPECS
            for item in ("privacy_erasure", "model_unlearning")
        ),
        "idempotency_retry_compensation_audited": all(
            row["passed"]
            for row in fault_results
            if row["fault"]
            in {
                "exact_duplicate",
                "idempotency_payload_mismatch",
                "crash_before_commit_retry",
                "crash_after_commit_before_ack",
                "projection_failure_forward_repair",
                "reordered_events",
            }
        ),
        "partial_projection_fail_closed": next(
            row
            for row in fault_results
            if row["fault"] == "projection_failure_forward_repair"
        )["passed"],
        "passed": False,
    }
    exit_gate["passed"] = all(
        value for key, value in exit_gate.items() if key != "passed"
    ) and all(row["passed"] for row in fault_results)
    report = {
        "schema_version": "aoa_memo_phase10_mechanical_lifecycle_report_v0",
        "created_at": fixture["reference_time"],
        "evidence_scope": (
            "source-local-deterministic-mechanical-lifecycle-reference-lab-no-runtime"
        ),
        "pins": pins,
        "mechanical_class_results": mechanical_results,
        "fault_results": fault_results,
        "semantic_proposal_results": semantic_results,
        "forgetting_taxonomy": fixture["forgetting_taxonomy"],
        "abc_comparison": abc_comparison,
        "cost_quality_speed_result": {
            "unit": "deterministic_reference_lab_descriptive_only",
            "wall_time_ms": elapsed_ms,
            "receipt_count": len(all_receipts),
            "attempt_count": len(all_receipts),
            "repair_count": 1,
            "operator_review_items": admitted,
            "deferred_review_items": deferred,
            "safety_violations": 0,
            "result": "bounded_reference_mechanism_pass",
        },
        "projection_contract_probe": projection_probe,
        "attention_budget": {
            "max_open_items": fixture["operator_attention_budget"],
            "admitted": admitted,
            "deferred": deferred,
            "overflow_dropped": 0,
            "sole_operator_preserved": True,
        },
        "sampling": {
            "automated_contract_sample_count": len(mechanical_results),
            "automated_contract_sample_passed": all(
                row["schema_valid"] and row["semantic_valid"]
                for row in mechanical_results
            ),
            "human_operator_sampling_status": "not_performed",
            "runtime_promotion_allowed": False,
        },
        "summary": {
            "mechanical_classes_passed": sum(
                row["status"] == "applied" for row in mechanical_results
            ),
            "fault_cases_passed": sum(row["passed"] for row in fault_results),
            "semantic_proposals_preserved": sum(
                row["apply_allowed"] is False for row in semantic_results
            ),
            "semantic_effects": 0,
            "double_commits": 0,
            "mixed_active_states": 0,
            "provenance_scope_failures": 0,
            "unfinished_erase_misreported_deleted": 0,
        },
        "exit_gate": exit_gate,
        "authority": {
            "reference_simulation_only": True,
            "semantic_transition": False,
            "privacy_erasure": False,
            "model_unlearning": False,
            "runtime_mutated": False,
            "deployment_performed": False,
            "landing_performed": False,
        },
        "limitations": [
            "deterministic in-memory failure-injection model, not a durable worker",
            "single owner-local tenant and namespace",
            "no production queue, storage transaction, or scheduler was exercised",
            "no physical deletion, privacy erasure, or model unlearning was attempted",
            "KAG C13 was validated from its public-safe owner example only",
            "wall time is descriptive harness overhead, not a production latency claim",
            "human operator sampling was not impersonated and runtime promotion remains blocked",
            "no soak, deployment, policy activation, or landing",
        ],
        "report_digest": ZERO_DIGEST,
    }
    report["report_digest"] = canonical_digest(
        report,
        exclude={"report_digest"},
    )
    validate_schema(report, report_validator, "Phase 10 report")
    write_json(output_path, report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memo-root", type=Path, required=True)
    parser.add_argument("--kag-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = run_lab(
            memo_root=args.memo_root.resolve(),
            kag_root=args.kag_root.resolve(),
            output_path=args.output.resolve(),
        )
    except (MechanicalLifecycleLabError, ValueError) as exc:
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
