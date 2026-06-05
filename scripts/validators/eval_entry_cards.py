"""Source eval public entry operating-card checks."""

from __future__ import annotations

from pathlib import Path

from validators.common import ValidationIssue
from validators.eval_bundle_common import (
    EVALS_README,
    EVAL_INDEX_NAME,
    EVAL_SELECTION_NAME,
    require_tokens,
)

EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    EVAL_SELECTION_NAME: (
        "## Operating Card",
        "root eval chooser for first bundle selection",
        "proof question, claim class, maturity need, comparison need, or diagnostic pressure",
        "selected source eval bundle, comparison surface, or defer-to-index route",
        "`EVAL_SELECTION.md` owns first-choice chooser wording",
        "[evals/AGENTS.md#validation](evals/AGENTS.md#validation)",
    ),
    EVAL_INDEX_NAME: (
        "## Operating Card",
        "repository-wide agent-facing index of public eval bundles",
        "public bundle inventory question, eval layer/status map question",
        "`EVAL_INDEX.md` owns public starter-table and layer-index wording",
        "generated catalog/readers, comparison spine reader, report index, and eval source validator",
        "[evals/AGENTS.md#validation](evals/AGENTS.md#validation)",
    ),
    EVALS_README.as_posix(): (
        "## Operating Card",
        "source eval package tree for bundle-local proof objects",
        "source proof question, bundle lookup, claim-family path",
        "bundle-local `EVAL.md` and `eval.yaml` own claim meaning",
        "`evals/AGENTS.md` owns source-tree edit law",
        "[evals/AGENTS.md#validation](AGENTS.md#validation)",
    ),
}


def validate_eval_source_entry_operating_cards(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for path_name, tokens in EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS.items():
        require_tokens(
            repo_root=repo_root,
            path_name=path_name,
            tokens=tokens,
            issues=issues,
        )

    return issues


__all__ = (
    "EVAL_SOURCE_ENTRY_OPERATING_CARD_REQUIRED_TOKENS",
    "validate_eval_source_entry_operating_cards",
)
