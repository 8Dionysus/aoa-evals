#!/usr/bin/env python3
"""Prepare bounded LongMemEval V1 A/B/C prompts from pinned public data."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
PLAN_PATH = BUNDLE_ROOT / "fixtures" / "phase13-evidence-plan.json"
EVIDENCE_RUNNER_PATH = Path(__file__).with_name("run_phase13_evidence_lab.py")
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "did",
    "do",
    "for",
    "from",
    "had",
    "has",
    "have",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


class PromptPreparationError(RuntimeError):
    """Raised when the pinned corpus cannot produce a valid prompt set."""


def load_evidence_runner():
    spec = importlib.util.spec_from_file_location(
        "phase13_evidence_runner", EVIDENCE_RUNNER_PATH
    )
    if spec is None or spec.loader is None:
        raise PromptPreparationError("cannot import Phase 13 evidence runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def tokenize(text: str) -> list[str]:
    return [
        token.casefold()
        for token in TOKEN_RE.findall(text)
        if token.casefold() not in STOPWORDS and len(token) > 1
    ]


def session_text(session: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{message.get('role', 'unknown')}: {message.get('content', '')}"
        for message in session
    )


def render_sessions(
    row: dict[str, Any],
    selected_indices: list[int],
    char_budget: int,
) -> tuple[str, list[str]]:
    chunks: list[str] = []
    selected_ids: list[str] = []
    consumed = 0
    sessions = row["haystack_sessions"]
    session_ids = row["haystack_session_ids"]
    dates = row["haystack_dates"]
    for index in selected_indices:
        body = session_text(sessions[index])
        header = f"[session id={session_ids[index]} date={dates[index]}]\n"
        remaining = char_budget - consumed
        if remaining <= len(header) + 64:
            break
        chunk = header + body[: remaining - len(header)]
        chunks.append(chunk)
        selected_ids.append(session_ids[index])
        consumed += len(chunk) + 2
    return "\n\n".join(chunks), selected_ids


def oracle_indices(row: dict[str, Any]) -> list[int]:
    answer_ids = set(row.get("answer_session_ids", []))
    preferred = [
        index
        for index, session_id in enumerate(row["haystack_session_ids"])
        if session_id in answer_ids
    ]
    remaining = [
        index
        for index in range(len(row["haystack_session_ids"]))
        if index not in preferred
    ]
    return preferred + remaining


def lexical_indices(row: dict[str, Any]) -> list[int]:
    question_terms = set(tokenize(row["question"]))
    session_term_sets = [
        set(tokenize(session_text(session)))
        for session in row["haystack_sessions"]
    ]
    document_frequency = Counter(
        term for terms in session_term_sets for term in terms & question_terms
    )
    session_count = max(len(session_term_sets), 1)

    def score(index: int) -> tuple[float, str]:
        terms = session_term_sets[index]
        weighted_overlap = sum(
            math.log((session_count + 1) / (document_frequency[term] + 1)) + 1
            for term in question_terms & terms
        )
        length_penalty = math.sqrt(max(len(terms), 1))
        return (
            weighted_overlap / length_penalty,
            row["haystack_session_ids"][index],
        )

    return sorted(
        range(len(session_term_sets)),
        key=lambda index: (-score(index)[0], score(index)[1]),
    )


def prompt_text(question: str, context: str) -> str:
    if context:
        return (
            "Use only the conversation evidence below. Answer the question "
            "with one short phrase. If the evidence does not support an "
            "answer, respond UNKNOWN.\n\n"
            f"EVIDENCE\n{context}\n\nQUESTION\n{question}\n\nANSWER"
        )
    return (
        "No memory evidence is available. Answer the question with one short "
        "phrase. If it cannot be answered without memory, respond UNKNOWN."
        f"\n\nQUESTION\n{question}\n\nANSWER"
    )


def prepare(
    benchmark_root: Path, output_dir: Path, char_budget: int
) -> dict[str, Any]:
    evidence_runner = load_evidence_runner()
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    benchmark = next(
        item
        for item in plan["public_benchmarks"]
        if item["benchmark_id"] == "longmemeval-v1-cleaned"
    )
    checks, _ = evidence_runner.artifact_checks(plan, benchmark_root)
    evidence_runner.require_verified(benchmark, checks)
    selected_ids = {
        question_id
        for ids in benchmark["selected_cases"].values()
        for question_id in ids
    }

    artifact_by_role = {
        item["required_for"]: benchmark_root / item["relative_path"]
        for item in benchmark["artifacts"]
    }
    oracle_rows = {
        row["question_id"]: row
        for row in evidence_runner.iter_json_array(
            artifact_by_role["reviewed_pull_upper_bound"]
        )
        if row["question_id"] in selected_ids
    }
    noisy_rows = {
        row["question_id"]: row
        for row in evidence_runner.iter_json_array(
            artifact_by_role["noisy_history_retrieval"]
        )
        if row["question_id"] in selected_ids
    }
    if set(oracle_rows) != selected_ids or set(noisy_rows) != selected_ids:
        raise PromptPreparationError("selected LongMemEval rows are incomplete")

    prompts: list[dict[str, Any]] = []
    for stratum, question_ids in benchmark["selected_cases"].items():
        for question_id in question_ids:
            oracle_row = oracle_rows[question_id]
            noisy_row = noisy_rows[question_id]
            arms = {
                "A": ("question_only_memory_disabled", "", []),
                "B": (
                    "oracle_sessions_reviewed_pull_upper_bound",
                    *render_sessions(
                        oracle_row, oracle_indices(oracle_row), char_budget
                    ),
                ),
                "C": (
                    "bounded_lexical_retrieval_from_noisy_history",
                    *render_sessions(
                        noisy_row, lexical_indices(noisy_row), char_budget
                    ),
                ),
            }
            for arm_id, (arm_label, context, session_ids) in arms.items():
                prompt = prompt_text(oracle_row["question"], context)
                prompts.append(
                    {
                        "prompt_id": f"{question_id}:{arm_id}",
                        "question_id": question_id,
                        "question_type": stratum,
                        "arm_id": arm_id,
                        "arm_label": arm_label,
                        "question": oracle_row["question"],
                        "expected_answer": oracle_row["answer"],
                        "selected_session_ids": session_ids,
                        "context_chars": len(context),
                        "prompt_sha256": (
                            "sha256:"
                            + hashlib.sha256(prompt.encode()).hexdigest()
                        ),
                        "prompt": prompt,
                    }
                )

    output_dir.mkdir(parents=True, exist_ok=True)
    prompts_path = output_dir / "lme-v1-prompts.jsonl"
    prompts_rendered = "".join(
        json.dumps(item, sort_keys=True) + "\n" for item in prompts
    )
    prompts_path.write_text(prompts_rendered, encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "manifest_id": "aoa-memo-phase13-lme-v1-prompts-v1",
        "plan_sha256": evidence_runner.canonical_sha256(plan),
        "benchmark_id": benchmark["benchmark_id"],
        "selection_policy": plan["selection_policy"]["algorithm"],
        "context_char_budget": char_budget,
        "prompt_count": len(prompts),
        "case_count": len(selected_ids),
        "arms": benchmark["arms"],
        "prompts_path": str(prompts_path),
        "prompts_sha256": (
            "sha256:" + hashlib.sha256(prompts_rendered.encode()).hexdigest()
        ),
        "answer_used_for_retrieval": False,
        "has_answer_marker_used_for_retrieval": False,
        "official_leaderboard_claim": False,
        "landing_performed": False,
    }
    (output_dir / "lme-v1-prompt-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--context-char-budget", type=int, default=10000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.context_char_budget < 1000:
        print("context char budget must be at least 1000", file=sys.stderr)
        return 2
    try:
        manifest = prepare(
            args.benchmark_root.resolve(),
            args.output_dir.resolve(),
            args.context_char_budget,
        )
    except (PromptPreparationError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"LongMemEval prompt preparation failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
