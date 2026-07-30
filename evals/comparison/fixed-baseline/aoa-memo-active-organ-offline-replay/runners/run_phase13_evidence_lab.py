#!/usr/bin/env python3
"""Validate Phase 13 external evidence without claiming benchmark benefit."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = BUNDLE_ROOT / "fixtures" / "phase13-evidence-plan.json"
OS_REPLAY_PATH = BUNDLE_ROOT / "fixtures" / "phase13-os-replay-cases.json"
OS_REPLAY_ANCHOR_PATH = (
    BUNDLE_ROOT / "fixtures" / "phase13-os-mutable-episode-anchors.json"
)
REPORT_SCHEMA_PATH = BUNDLE_ROOT / "reports" / "phase13-evidence.schema.json"
MODEL_REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-model-lane.schema.json"
)
OPERATOR_REPLAY_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-operator-replay.schema.json"
)
SOAK_REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-accelerated-soak.schema.json"
)
WALL_CLOCK_REPORT_SCHEMA_PATH = (
    BUNDLE_ROOT / "reports" / "phase13-wall-clock-soak.schema.json"
)


class EvidenceError(RuntimeError):
    """Raised when a pinned artifact or selection contract is invalid."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(payload: Any) -> str:
    encoded = (
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def validate_session_index_anchor(
    case: dict[str, Any],
    index_path: Path,
    episode: dict[str, Any],
    *,
    label: str,
    mutable_anchor: dict[str, Any] | None,
) -> None:
    if mutable_anchor is None:
        if sha256_file(index_path) != case["session_index_sha256"]:
            raise EvidenceError(
                f"{label} session index digest drift: {case['case_id']}"
            )
        return
    expected_anchor = {
        "case_id": case["case_id"],
        "session_index_ref": case["session_index_ref"],
        "session_index_review_cutoff_sha256": case["session_index_sha256"],
        "session_index_generation_id": case["session_index_generation_id"],
        "episode_id": case["episode_id"],
        "stable_episode_id": case["stable_episode_id"],
    }
    if any(
        mutable_anchor.get(key) != value
        for key, value in expected_anchor.items()
    ):
        raise EvidenceError(
            f"{label} mutable anchor identity drift: {case['case_id']}"
        )
    expected_episode_digest = mutable_anchor.get("episode_projection_sha256")
    if (
        not isinstance(expected_episode_digest, str)
        or canonical_sha256(episode)
        != f"sha256:{expected_episode_digest}"
    ):
        raise EvidenceError(
            f"{label} episode projection digest drift: {case['case_id']}"
        )


def load_mutable_episode_anchors(
    fixture: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    document = json.loads(OS_REPLAY_ANCHOR_PATH.read_text(encoding="utf-8"))
    if (
        document.get("schema_version") != 1
        or document.get("posture")
        != "closed_episode_inside_mutable_session_projection"
    ):
        raise EvidenceError("OS replay mutable-anchor contract drift")
    cases = {
        case["case_id"]: case
        for lane in ("cases", "reviewed_outcomes")
        for case in fixture[lane]
    }
    anchors: dict[str, dict[str, Any]] = {}
    for anchor in document.get("anchors", []):
        case_id = anchor.get("case_id")
        if (
            not isinstance(case_id, str)
            or case_id not in cases
            or case_id in anchors
            or not isinstance(anchor.get("claim_limit"), str)
            or not anchor["claim_limit"].strip()
        ):
            raise EvidenceError("OS replay mutable-anchor entry invalid")
        anchors[case_id] = anchor
    return anchors


def load_validated_report(
    path: Path,
    schema_path: Path,
    *,
    label: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    if not path.is_file():
        raise EvidenceError(f"{label} report is missing: {path}")
    report = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(report),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        detail = "\n".join(
            f"{'/'.join(map(str, error.absolute_path))}: {error.message}"
            for error in errors
        )
        raise EvidenceError(f"{label} report schema validation failed:\n{detail}")
    return report, {
        "path": str(path),
        "sha256": f"sha256:{sha256_file(path)}",
    }


def iter_json_array(path: Path) -> Iterator[Any]:
    """Stream one top-level JSON array without retaining the full corpus."""

    decoder = json.JSONDecoder()
    buffer = ""
    started = False
    finished = False

    with path.open("r", encoding="utf-8") as handle:
        while not finished:
            chunk = handle.read(1024 * 1024)
            if chunk:
                buffer += chunk

            while True:
                buffer = buffer.lstrip()
                if not started:
                    if not buffer:
                        break
                    if buffer[0] != "[":
                        raise EvidenceError(f"{path}: expected a JSON array")
                    buffer = buffer[1:]
                    started = True
                    continue

                buffer = buffer.lstrip()
                if buffer.startswith("]"):
                    buffer = buffer[1:]
                    finished = True
                    break
                if buffer.startswith(","):
                    buffer = buffer[1:]
                    continue
                if not buffer:
                    break

                try:
                    value, end = decoder.raw_decode(buffer)
                except json.JSONDecodeError:
                    if chunk:
                        break
                    raise EvidenceError(f"{path}: truncated JSON array")
                yield value
                buffer = buffer[end:]

            if not chunk and not finished:
                raise EvidenceError(f"{path}: missing closing array delimiter")

    if buffer.strip():
        raise EvidenceError(f"{path}: trailing content after JSON array")


def deterministic_selection(
    ids_by_stratum: dict[str, list[str]], counts: dict[str, int]
) -> dict[str, list[str]]:
    selected: dict[str, list[str]] = {}
    for stratum, expected_count in counts.items():
        ranked = sorted(
            ids_by_stratum.get(stratum, []),
            key=lambda value: (hashlib.sha256(value.encode()).hexdigest(), value),
        )
        selected[stratum] = ranked[:expected_count]
    return selected


def artifact_checks(
    plan: dict[str, Any], benchmark_root: Path
) -> tuple[list[dict[str, Any]], dict[str, Path]]:
    checks: list[dict[str, Any]] = []
    resolved: dict[str, Path] = {}
    for benchmark in plan["public_benchmarks"]:
        for artifact in benchmark["artifacts"]:
            relative_path = artifact["relative_path"]
            path = benchmark_root / relative_path
            actual_bytes: int | None = None
            actual_sha256: str | None = None
            status = "missing"
            if path.is_file():
                actual_bytes = path.stat().st_size
                actual_sha256 = sha256_file(path)
                if actual_bytes != artifact["bytes"]:
                    status = "size_mismatch"
                elif actual_sha256 != artifact["sha256"]:
                    status = "digest_mismatch"
                else:
                    status = "verified"
                    resolved[f"{benchmark['benchmark_id']}:{relative_path}"] = path
            checks.append(
                {
                    "benchmark_id": benchmark["benchmark_id"],
                    "relative_path": relative_path,
                    "expected_bytes": artifact["bytes"],
                    "actual_bytes": actual_bytes,
                    "expected_sha256": artifact["sha256"],
                    "actual_sha256": actual_sha256,
                    "status": status,
                }
            )
    return checks, resolved


def require_verified(
    benchmark: dict[str, Any],
    checks: list[dict[str, Any]],
) -> None:
    relevant = [
        item
        for item in checks
        if item["benchmark_id"] == benchmark["benchmark_id"]
    ]
    failures = [item for item in relevant if item["status"] != "verified"]
    if failures:
        detail = ", ".join(
            f"{item['relative_path']}={item['status']}" for item in failures
        )
        raise EvidenceError(f"{benchmark['benchmark_id']}: {detail}")


def validate_lme_v1(
    benchmark: dict[str, Any],
    benchmark_root: Path,
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    require_verified(benchmark, checks)
    paths = {
        item["required_for"]: benchmark_root / item["relative_path"]
        for item in benchmark["artifacts"]
    }
    ids_by_type: dict[str, list[str]] = defaultdict(list)
    oracle_ids: set[str] = set()
    for row in iter_json_array(paths["reviewed_pull_upper_bound"]):
        question_id = row["question_id"]
        question_type = row["question_type"]
        oracle_ids.add(question_id)
        ids_by_type[question_type].append(question_id)

    noisy_ids: set[str] = set()
    noisy_type_by_id: dict[str, str] = {}
    for row in iter_json_array(paths["noisy_history_retrieval"]):
        question_id = row["question_id"]
        noisy_ids.add(question_id)
        noisy_type_by_id[question_id] = row["question_type"]

    if len(oracle_ids) != benchmark["expected_case_count"]:
        raise EvidenceError("LongMemEval V1 oracle case count drift")
    if oracle_ids != noisy_ids:
        raise EvidenceError("LongMemEval V1 oracle/noisy question ids differ")
    if any(
        noisy_type_by_id[question_id] != question_type
        for question_type, question_ids in ids_by_type.items()
        for question_id in question_ids
    ):
        raise EvidenceError("LongMemEval V1 question type drift")

    expected_selection = benchmark["selected_cases"]
    counts = {key: len(value) for key, value in expected_selection.items()}
    actual_selection = deterministic_selection(ids_by_type, counts)
    selection_verified = actual_selection == expected_selection
    if not selection_verified:
        raise EvidenceError("LongMemEval V1 frozen selection drift")

    return {
        "benchmark_id": benchmark["benchmark_id"],
        "status": "complete",
        "observed_case_count": len(oracle_ids),
        "selected_case_count": sum(counts.values()),
        "stratum_counts": dict(sorted(Counter(
            question_type
            for question_type, question_ids in ids_by_type.items()
            for _ in question_ids
        ).items())),
        "score_ready": True,
        "selection_verified": True,
        "reasons": [],
        "claim_limit": benchmark["claim_limit"],
    }


def validate_lme_v2(
    benchmark: dict[str, Any],
    benchmark_root: Path,
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    require_verified(benchmark, checks)
    paths = {
        item["required_for"]: benchmark_root / item["relative_path"]
        for item in benchmark["artifacts"]
    }
    ids_by_type: dict[str, list[str]] = defaultdict(list)
    with paths["question_contract"].open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise EvidenceError(
                    f"LongMemEval V2 questions line {line_number}: {error}"
                ) from error
            ids_by_type[row["question_type"]].append(row["id"])

    haystacks = json.loads(
        paths["small_haystack_membership"].read_text(encoding="utf-8")
    )
    question_ids = {
        question_id
        for question_ids_for_type in ids_by_type.values()
        for question_id in question_ids_for_type
    }
    if len(question_ids) != benchmark["expected_case_count"]:
        raise EvidenceError("LongMemEval V2 question count drift")
    if set(haystacks) != question_ids:
        raise EvidenceError("LongMemEval V2 question/haystack membership drift")
    if any(
        not isinstance(trajectory_ids, list) or len(trajectory_ids) != 100
        for trajectory_ids in haystacks.values()
    ):
        raise EvidenceError("LongMemEval V2 small haystack width drift")

    expected_selection = benchmark["selected_cases"]
    counts = {key: len(value) for key, value in expected_selection.items()}
    actual_selection = deterministic_selection(ids_by_type, counts)
    if actual_selection != expected_selection:
        raise EvidenceError("LongMemEval V2 frozen selection drift")

    reasons = [
        f"missing {item['relative_path']}: {item['reason']}"
        for item in benchmark["missing_scored_artifacts"]
    ]
    return {
        "benchmark_id": benchmark["benchmark_id"],
        "status": "partial",
        "observed_case_count": len(question_ids),
        "selected_case_count": sum(counts.values()),
        "stratum_counts": dict(
            sorted((key, len(value)) for key, value in ids_by_type.items())
        ),
        "score_ready": False,
        "selection_verified": True,
        "reasons": reasons,
        "claim_limit": benchmark["claim_limit"],
    }


def validate_locomo_plus(
    benchmark: dict[str, Any],
    benchmark_root: Path,
    checks: list[dict[str, Any]],
) -> dict[str, Any]:
    require_verified(benchmark, checks)
    path = benchmark_root / benchmark["artifacts"][0]["relative_path"]
    rows = json.loads(path.read_text(encoding="utf-8"))
    if len(rows) != benchmark["expected_case_count"]:
        raise EvidenceError("LoCoMo-Plus case count drift")

    ids_by_relation: dict[str, list[str]] = defaultdict(list)
    for index, row in enumerate(rows):
        ids_by_relation[row["relation_type"]].append(str(index))

    expected_selection = {
        key: [str(value) for value in values]
        for key, values in benchmark["selected_cases"].items()
    }
    counts = {key: len(value) for key, value in expected_selection.items()}
    actual_selection = deterministic_selection(ids_by_relation, counts)
    if actual_selection != expected_selection:
        raise EvidenceError("LoCoMo-Plus frozen selection drift")

    return {
        "benchmark_id": benchmark["benchmark_id"],
        "status": "partial",
        "observed_case_count": len(rows),
        "selected_case_count": sum(counts.values()),
        "stratum_counts": dict(
            sorted((key, len(value)) for key, value in ids_by_relation.items())
        ),
        "score_ready": False,
        "selection_verified": True,
        "reasons": [
            "source repository has no LICENSE file; diagnostic use only",
            "upstream stitching uses unseeded random selection; deterministic adapter required",
            "cognitive cases have no gold answer and require a separately pinned judge",
        ],
        "claim_limit": benchmark["claim_limit"],
    }


def validate_os_replay(aoa_root: Path) -> dict[str, Any]:
    fixture = json.loads(OS_REPLAY_PATH.read_text(encoding="utf-8"))
    mutable_anchors = load_mutable_episode_anchors(fixture)
    cases = fixture["cases"]
    reviewed_outcomes = fixture["reviewed_outcomes"]
    scoring = fixture["scoring_posture"]
    if fixture["privacy_posture"] != "refs_only_no_raw_transcript_bodies":
        raise EvidenceError("OS replay privacy posture drift")
    if scoring["prepared_case_count"] != len(cases):
        raise EvidenceError("OS replay prepared-case count drift")
    if scoring["reviewed_case_count"] != len(reviewed_outcomes):
        raise EvidenceError("OS replay reviewed-case count drift")

    for case in cases:
        index_path = aoa_root / case["session_index_ref"]
        if not index_path.is_file():
            raise EvidenceError(
                f"OS replay session index is missing: {index_path}"
            )
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if index.get("session_id") != case["session_id"]:
            raise EvidenceError(
                f"OS replay session identity drift: {case['case_id']}"
            )
        if index.get("generation_id") != case["session_index_generation_id"]:
            raise EvidenceError(
                f"OS replay index generation drift: {case['case_id']}"
            )
        episode = next(
            (
                item
                for item in index.get("task_episodes", [])
                if item.get("episode_id") == case["episode_id"]
            ),
            None,
        )
        if episode is None or episode.get("status") != "closed":
            raise EvidenceError(
                f"OS replay episode is not closed: {case['case_id']}"
            )
        validate_session_index_anchor(
            case,
            index_path,
            episode,
            label="OS replay",
            mutable_anchor=mutable_anchors.get(case["case_id"]),
        )
        if episode.get("stable_id") != case["stable_episode_id"]:
            raise EvidenceError(
                f"OS replay stable episode id drift: {case['case_id']}"
            )
        observed_counts = {
            "verification": len(episode.get("verification_refs", [])),
            "answer": len(episode.get("answer_refs", [])),
            "closeout": len(episode.get("closeout_refs", [])),
        }
        if observed_counts != case["ref_counts"]:
            raise EvidenceError(
                f"OS replay reference count drift: {case['case_id']}"
            )
        raw_refs = {
            ref.get("raw_ref")
            for key in (
                "verification_refs",
                "answer_refs",
                "closeout_refs",
            )
            for ref in episode.get(key, [])
        }
        raw_refs.add(episode.get("start_user_ref", {}).get("raw_ref"))
        declared_refs = {
            case["start_raw_ref"],
            *case.get("verification_ref_samples", []),
            *case.get("answer_ref_samples", []),
            *case.get("closeout_ref_samples", []),
        }
        if not declared_refs <= raw_refs:
            raise EvidenceError(
                f"OS replay raw-coordinate drift: {case['case_id']}"
            )
        if not case["expected_invariants"] or not case["current_owner_refs"]:
            raise EvidenceError(
                f"OS replay review contract is incomplete: {case['case_id']}"
            )

    observed_operator_corrections = 0
    for case in reviewed_outcomes:
        index_path = aoa_root / case["session_index_ref"]
        if not index_path.is_file():
            raise EvidenceError(
                f"reviewed OS replay session index is missing: {index_path}"
            )
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if (
            index.get("session_id") != case["session_id"]
            or index.get("generation_id")
            != case["session_index_generation_id"]
        ):
            raise EvidenceError(
                f"reviewed OS replay session identity drift: {case['case_id']}"
            )
        episode = next(
            (
                item
                for item in index.get("task_episodes", [])
                if item.get("episode_id") == case["episode_id"]
            ),
            None,
        )
        if (
            episode is None
            or episode.get("status") != "closed"
            or episode.get("stable_id") != case["stable_episode_id"]
        ):
            raise EvidenceError(
                f"reviewed OS replay episode drift: {case['case_id']}"
            )
        validate_session_index_anchor(
            case,
            index_path,
            episode,
            label="reviewed OS replay",
            mutable_anchor=mutable_anchors.get(case["case_id"]),
        )
        observed_counts = {
            "verification": len(episode.get("verification_refs", [])),
            "answer": len(episode.get("answer_refs", [])),
            "closeout": len(episode.get("closeout_refs", [])),
        }
        if observed_counts != case["episode_ref_counts"]:
            raise EvidenceError(
                f"reviewed OS replay ref-count drift: {case['case_id']}"
            )

        evidence = case["bounded_raw_evidence"]
        if [item.get("role") for item in evidence] != [
            "intent",
            "closeout",
            "terminal",
        ]:
            raise EvidenceError(
                f"reviewed OS replay evidence roles drift: {case['case_id']}"
            )
        event_range = episode["event_range"]
        for item in evidence:
            try:
                raw_line = int(item["raw_ref"].removeprefix("raw:line:"))
            except (AttributeError, ValueError) as error:
                raise EvidenceError(
                    f"reviewed OS replay raw ref invalid: {case['case_id']}"
                ) from error
            if not (
                event_range["from_line"]
                <= raw_line
                <= event_range["to_line"]
            ):
                raise EvidenceError(
                    f"reviewed OS replay raw ref escaped episode: "
                    f"{case['case_id']}"
                )
            block_path = (aoa_root / item["block_ref"]).resolve()
            if not block_path.is_relative_to(aoa_root.resolve()):
                raise EvidenceError(
                    f"reviewed OS replay block escaped archive: "
                    f"{case['case_id']}"
                )
            block = next(
                (
                    candidate
                    for candidate in index["raw_blocks"]["blocks"]
                    if Path(candidate["path"]).resolve() == block_path
                ),
                None,
            )
            if block is None or not block_path.is_file():
                raise EvidenceError(
                    f"reviewed OS replay block is missing: {case['case_id']}"
                )
            if (
                block.get("status") not in {"sealed", "open"}
                or block.get("sha256") != item["block_sha256"]
            ):
                raise EvidenceError(
                    f"reviewed OS replay block metadata drift: "
                    f"{case['case_id']}"
                )
            if sha256_file(block_path) != item["block_sha256"]:
                raise EvidenceError(
                    f"reviewed OS replay block digest drift: "
                    f"{case['case_id']}"
                )
            expected_block_line = (
                raw_line - block["source_range"]["from_line"] + 1
            )
            if item["block_line"] != expected_block_line:
                raise EvidenceError(
                    f"reviewed OS replay block coordinate drift: "
                    f"{case['case_id']}"
                )
            if not 1 <= item["block_line"] <= block["line_count"]:
                raise EvidenceError(
                    f"reviewed OS replay block line escaped block: "
                    f"{case['case_id']}"
                )
            raw_event = None
            with block_path.open(encoding="utf-8") as handle:
                for block_line, line in enumerate(handle, start=1):
                    if block_line == item["block_line"]:
                        raw_event = json.loads(line)
                        break
            if raw_event is None:
                raise EvidenceError(
                    f"reviewed OS replay event is missing: {case['case_id']}"
                )
            payload = raw_event.get("payload", {})
            observed_envelope = {
                "event_type": raw_event.get("type"),
                "item_type": payload.get("type"),
                "role": payload.get("role"),
                "phase": payload.get("phase"),
            }
            if observed_envelope != item["envelope"]:
                raise EvidenceError(
                    f"reviewed OS replay envelope drift: {case['case_id']}"
                )

        intent, closeout, terminal = evidence
        if (
            intent["envelope"]
            != {
                "event_type": "response_item",
                "item_type": "message",
                "role": "user",
                "phase": None,
            }
            or closeout["envelope"]
            != {
                "event_type": "response_item",
                "item_type": "message",
                "role": "assistant",
                "phase": "final_answer",
            }
            or terminal["envelope"]["event_type"] != "event_msg"
            or terminal["envelope"]["item_type"]
            not in {"task_complete", "thread_settings_applied"}
        ):
            raise EvidenceError(
                f"reviewed OS replay terminal envelope invalid: "
                f"{case['case_id']}"
            )
        review = case["review"]
        operator_correction_count = review.get("operator_correction_count")
        counterfactual = case["r1_counterfactual"]
        if (
            case.get("raw_bodies_embedded") is not False
            or not isinstance(case.get("task_abstraction"), str)
            or not case["task_abstraction"].strip()
            or not case["expected_invariants"]
            or not case["current_owner_refs"]
            or review.get("reviewer_role")
            != "bounded_source_evidence_review"
            or not isinstance(review.get("outcome_state"), str)
            or not review["outcome_state"].strip()
            or type(operator_correction_count) is not int
            or operator_correction_count < 0
            or not isinstance(review.get("operator_load_observation"), str)
            or not review["operator_load_observation"].strip()
            or not isinstance(review.get("projection_limitation"), str)
            or review.get("invariants_satisfied") is not True
            or review.get("benefit_attribution") != "not_established"
            or counterfactual.get("status") != "unexecuted"
            or type(counterfactual.get("eligible_owner_orientation")) is not bool
            or not isinstance(counterfactual.get("hypothesis"), str)
            or not counterfactual["hypothesis"].strip()
        ):
            raise EvidenceError(
                f"reviewed OS replay claim boundary drift: {case['case_id']}"
            )
        observed_operator_corrections += operator_correction_count

    if (
        observed_operator_corrections
        != scoring["observed_operator_correction_count"]
    ):
        raise EvidenceError("OS replay operator-correction count drift")
    if (
        scoring["scored_case_count"] != 0
        or scoring["model_runs_complete"] != 0
        or scoring["outcome_attribution_established"]
        or scoring["benefit_established"]
    ):
        raise EvidenceError("OS replay review widened its evidence ceiling")
    return fixture


def build_report(
    benchmark_root: Path,
    aoa_root: Path,
    *,
    model_report_paths: list[Path] | None = None,
    operator_replay_report_path: Path | None = None,
    accelerated_soak_report_path: Path | None = None,
    wall_clock_soak_report_path: Path | None = None,
    failed_model_attempts: int = 0,
) -> dict[str, Any]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    os_replay_fixture = validate_os_replay(aoa_root)
    checks, _ = artifact_checks(plan, benchmark_root)
    benchmarks = {
        item["benchmark_id"]: item for item in plan["public_benchmarks"]
    }
    lanes = [
        validate_lme_v1(benchmarks["longmemeval-v1-cleaned"], benchmark_root, checks),
        validate_lme_v2(benchmarks["longmemeval-v2"], benchmark_root, checks),
        validate_locomo_plus(benchmarks["locomo-plus"], benchmark_root, checks),
    ]
    selected_case_count = sum(item["selected_case_count"] for item in lanes)
    model_reports = []
    for path in model_report_paths or []:
        model_report, report_ref = load_validated_report(
            path,
            MODEL_REPORT_SCHEMA_PATH,
            label="model lane",
        )
        model_reports.append(
            {
                **report_ref,
                "model_label": model_report["model"]["label"],
                "complete_observations": model_report["execution"][
                    "complete_count"
                ],
                "invalid_observations": model_report["execution"][
                    "invalid_count"
                ],
            }
        )
    if len({item["model_label"] for item in model_reports}) != len(
        model_reports
    ):
        raise EvidenceError("duplicate model label in supplied reports")
    attempted_model_runs = failed_model_attempts + len(model_reports)
    if len(model_reports) >= 2:
        model_status = "complete"
        model_reason = (
            "Two or more pinned model reports are schema-valid; failed "
            "pre-report attempts remain counted separately."
        )
    elif model_reports:
        model_status = "partial"
        model_reason = (
            "One pinned local model report is complete; cross-model coverage "
            "remains incomplete."
        )
    elif failed_model_attempts:
        model_status = "aborted"
        model_reason = (
            "Model attempts terminated before a schema-valid report; no "
            "model score is admitted."
        )
    else:
        model_status = "not_started"
        model_reason = "No schema-valid pinned model report was supplied."

    operator_replay_ref = None
    operator_replay_result = None
    if operator_replay_report_path is not None:
        operator_replay, operator_replay_ref = load_validated_report(
            operator_replay_report_path,
            OPERATOR_REPLAY_SCHEMA_PATH,
            label="operator replay",
        )
        if (
            operator_replay["report_id"]
            != "aoa-memo-phase13-retrospective-operator-orientation-v3"
        ):
            raise EvidenceError(
                "only the final strict V3 operator replay is admissible"
            )
        zero_arm = operator_replay["by_arm"]["0"]
        active_arm = operator_replay["by_arm"]["A"]
        operator_replay_result = {
            "report_id": operator_replay["report_id"],
            "attempted_observations": operator_replay["execution"][
                "attempted_count"
            ],
            "complete_observations": operator_replay["execution"][
                "complete_count"
            ],
            "zero_decision_accuracy": zero_arm["decision_accuracy"],
            "active_decision_accuracy": active_arm["decision_accuracy"],
            "zero_correction_proxy": zero_arm[
                "correction_required_proxy_count"
            ],
            "active_correction_proxy": active_arm[
                "correction_required_proxy_count"
            ],
            "active_owner_route_hit_rate": active_arm[
                "eligible_owner_route_hit_rate"
            ],
            "silence_specificity": operator_replay["silence"][
                "specificity"
            ],
            "mean_prompt_token_delta_A_minus_0": (
                active_arm["mean_prompt_tokens"]
                - zero_arm["mean_prompt_tokens"]
            ),
            "p50_latency_delta_ms_A_minus_0": (
                active_arm["p50_latency_ms"]
                - zero_arm["p50_latency_ms"]
            ),
            "p95_latency_delta_ms_A_minus_0": (
                active_arm["p95_latency_ms"]
                - zero_arm["p95_latency_ms"]
            ),
            "paired_A_better": operator_replay[
                "paired_correction_proxy"
            ]["A_better"],
            "paired_same": operator_replay[
                "paired_correction_proxy"
            ]["same"],
            "paired_A_worse": operator_replay[
                "paired_correction_proxy"
            ]["A_worse"],
            "outcome_attribution_established": False,
            "operator_workload_reduction_established": False,
            "verdict": "negative_no_decision_or_correction_gain_higher_cost",
        }

    soak_report_ref = None
    accelerated_windows: list[int] = []
    fault_executed_count = 0
    fault_detected_count = 0
    fault_silent_failures = 0
    if accelerated_soak_report_path is not None:
        soak_report, soak_report_ref = load_validated_report(
            accelerated_soak_report_path,
            SOAK_REPORT_SCHEMA_PATH,
            label="accelerated soak",
        )
        fixture_sha = f"sha256:{sha256_file(BUNDLE_ROOT / 'fixtures' / 'phase13-soak-cases.json')}"
        if soak_report["fixture"]["sha256"] != fixture_sha:
            raise EvidenceError("accelerated soak fixture digest drift")
        if soak_report["summary"]["accelerated_7d_complete"]:
            accelerated_windows.append(7)
        if soak_report["summary"]["accelerated_30d_complete"]:
            accelerated_windows.append(30)
        fault_executed_count = len(soak_report["faults"])
        fault_detected_count = sum(
            item["detected"] for item in soak_report["faults"]
        )
        fault_silent_failures = soak_report["summary"]["silent_faults"]
    wall_clock_report_ref = None
    wall_clock_7d_complete = False
    wall_clock_30d_complete = False
    if wall_clock_soak_report_path is not None:
        wall_clock_report, wall_clock_report_ref = load_validated_report(
            wall_clock_soak_report_path,
            WALL_CLOCK_REPORT_SCHEMA_PATH,
            label="wall-clock soak",
        )
        wall_clock_7d_complete = wall_clock_report[
            "wall_clock_7d_complete"
        ]
        wall_clock_30d_complete = wall_clock_report[
            "wall_clock_30d_complete"
        ]
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )
    report = {
        "schema_version": 1,
        "report_id": "aoa-memo-phase13-evidence-data-readiness",
        "generated_at": generated_at,
        "plan": {
            "plan_id": plan["plan_id"],
            "path": str(PLAN_PATH),
            "sha256": canonical_sha256(plan),
            "benchmark_root": str(benchmark_root),
        },
        "artifact_checks": checks,
        "frontier_delta": plan["frontier_delta"],
        "benchmark_lanes": lanes,
        "os_replay": {
            "status": plan["os_replay"]["status"],
            "privacy_posture": plan["os_replay"]["privacy_posture"],
            "prepared_case_count": len(os_replay_fixture["cases"]),
            "reviewed_case_count": len(
                os_replay_fixture["reviewed_outcomes"]
            ),
            "observed_operator_correction_count": os_replay_fixture[
                "scoring_posture"
            ]["observed_operator_correction_count"],
            "outcome_attribution_established": False,
            "status_detail": (
                "Six structural refs-only cases remain prepared and unscored; "
                "six separate raw-block-digest-bound outcomes were reviewed, "
                "with four observed operator corrections. A/B/C replay and "
                "causal memory benefit remain incomplete."
            ),
            "raw_bodies_embedded": False,
        },
        "model_execution": {
            "status": model_status,
            "attempted_runs": attempted_model_runs,
            "complete_runs": len(model_reports),
            "failed_attempts": failed_model_attempts,
            "reports": model_reports,
            "resource_admission_bypassed": False,
            "reason": model_reason,
        },
        "operator_replay": {
            "status": (
                "complete"
                if operator_replay_result is not None
                else "not_started"
            ),
            "report_ref": operator_replay_ref,
            "result": operator_replay_result,
            "claim_limit": (
                "Retrospective local-model correction proxies are not "
                "natural operator time or causal benefit. The final V3 "
                "result rejects a Gemma foreground decision wrapper."
            ),
        },
        "soak": {
            "status": (
                "complete"
                if wall_clock_30d_complete
                else (
                    "partial"
                    if accelerated_soak_report_path
                    or wall_clock_soak_report_path
                    else "not_started"
                )
            ),
            "accelerated_report": soak_report_ref,
            "wall_clock_report": wall_clock_report_ref,
            "accelerated_windows_complete": accelerated_windows,
            "wall_clock_7d_complete": wall_clock_7d_complete,
            "wall_clock_30d_complete": wall_clock_30d_complete,
            "accelerated_replay_claimed_as_wall_clock": False,
            "required_metrics": plan["soak"]["required_metrics"],
        },
        "fault_matrix": {
            "declared_count": len(plan["fault_matrix"]),
            "executed_count": fault_executed_count,
            "detected_count": fault_detected_count,
            "silent_failures": fault_silent_failures,
            "report_ref": soak_report_ref,
        },
        "summary": {
            "overall_status": "partial",
            "all_present_artifacts_verified": all(
                item["status"] == "verified" for item in checks
            ),
            "selected_case_count": selected_case_count,
            "scored_model_run_count": len(model_reports),
            "benefit_established": False,
            "public_benchmark_is_sole_proof": False,
            "landing_performed": False,
        },
        "authority": plan["authority"],
    }
    schema = json.loads(REPORT_SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(report),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        detail = "\n".join(
            f"{'/'.join(map(str, error.absolute_path))}: {error.message}"
            for error in errors
        )
        raise EvidenceError(f"report schema validation failed:\n{detail}")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--benchmark-root",
        type=Path,
        required=True,
        help="Host-managed benchmark cache root containing data/ and sources/.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional host-temp output. Source trees must not be used.",
    )
    parser.add_argument(
        "--aoa-root",
        type=Path,
        default=Path("/srv/AbyssOS/.aoa"),
        help="Read-only logical session-memory root for refs-only OS cases.",
    )
    parser.add_argument(
        "--model-report",
        type=Path,
        action="append",
        default=[],
        help="Schema-valid pinned model-lane report; repeat for cross-model coverage.",
    )
    parser.add_argument(
        "--failed-model-attempts",
        type=int,
        default=0,
        help="Pre-report attempts retained as failures, never scores.",
    )
    parser.add_argument(
        "--operator-replay-report",
        type=Path,
        help=(
            "Schema-valid final strict V3 retrospective operator replay; "
            "never natural operator-benefit proof."
        ),
    )
    parser.add_argument(
        "--accelerated-soak-report",
        type=Path,
        help="Schema-valid accelerated lifecycle report; never wall-clock proof.",
    )
    parser.add_argument(
        "--wall-clock-soak-report",
        type=Path,
        help="Schema-valid passive natural-load wall-clock campaign status.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.failed_model_attempts < 0:
        print("failed model attempts must be non-negative", file=sys.stderr)
        return 2
    if args.output and args.output.resolve().is_relative_to(BUNDLE_ROOT):
        print("evidence output must remain outside the source tree", file=sys.stderr)
        return 2
    try:
        report = build_report(
            args.benchmark_root.resolve(),
            args.aoa_root.resolve(),
            model_report_paths=[path.resolve() for path in args.model_report],
            operator_replay_report_path=(
                args.operator_replay_report.resolve()
                if args.operator_replay_report
                else None
            ),
            accelerated_soak_report_path=(
                args.accelerated_soak_report.resolve()
                if args.accelerated_soak_report
                else None
            ),
            wall_clock_soak_report_path=(
                args.wall_clock_soak_report.resolve()
                if args.wall_clock_soak_report
                else None
            ),
            failed_model_attempts=args.failed_model_attempts,
        )
    except (EvidenceError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"phase13 evidence validation failed: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
