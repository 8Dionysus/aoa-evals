"""Questbook obligation index and alignment note checks."""

from __future__ import annotations

from pathlib import Path

from validators import questbook_io as questbook_io_validator
from validators import questbook_orchestrator_constants as questbook_orchestrator_constants_validator
from validators import questbook_route_paths as questbook_route_paths_validator
from validators import questbook_route_tokens as questbook_route_tokens_validator
from validators.common import ValidationIssue


def validate_questbook_obligation_index(
    repo_root: Path,
    *,
    active_quest_ids: list[str],
    closed_quest_ids: list[str],
    needs_orchestrator_alignment_doc: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    questbook_path = repo_root / questbook_route_paths_validator.QUESTBOOK_NAME
    integration_path = repo_root / questbook_route_paths_validator.QUESTBOOK_INTEGRATION_NAME
    orchestrator_alignment_path = (
        repo_root / questbook_orchestrator_constants_validator.ORCHESTRATOR_PROOF_ALIGNMENT_NAME
    )

    questbook_text = questbook_io_validator.read_text_or_issue(
        questbook_path,
        issues,
        root=repo_root,
    )
    integration_text = questbook_io_validator.read_text_or_issue(
        integration_path,
        issues,
        root=repo_root,
    )

    if questbook_text:
        for token in questbook_route_tokens_validator.QUESTBOOK_NOTE_REQUIRED_TOKENS:
            if token not in questbook_text:
                issues.append(
                    ValidationIssue(
                        questbook_io_validator.relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must mention '{token}'",
                    )
                )
        for quest_name in active_quest_ids:
            if quest_name not in questbook_text:
                issues.append(
                    ValidationIssue(
                        questbook_io_validator.relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must reference active quest id '{quest_name}'",
                    )
                )
        for quest_name in closed_quest_ids:
            if quest_name in questbook_text:
                issues.append(
                    ValidationIssue(
                        questbook_io_validator.relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must not list closed quest id '{quest_name}'",
                    )
                )

    if integration_text:
        for token in questbook_route_tokens_validator.QUESTBOOK_INTEGRATION_REQUIRED_TOKENS:
            if token not in integration_text:
                issues.append(
                    ValidationIssue(
                        questbook_io_validator.relative_location(integration_path, repo_root),
                        f"integration note must mention '{token}'",
                    )
                )

    if needs_orchestrator_alignment_doc or orchestrator_alignment_path.exists():
        orchestrator_doc_text = questbook_io_validator.read_text_or_issue(
            orchestrator_alignment_path,
            issues,
            root=repo_root,
        )
        if orchestrator_doc_text:
            for token in questbook_orchestrator_constants_validator.ORCHESTRATOR_PROOF_REQUIRED_TOKENS:
                if token not in orchestrator_doc_text:
                    issues.append(
                        ValidationIssue(
                            questbook_io_validator.relative_location(
                                orchestrator_alignment_path,
                                repo_root,
                            ),
                            "orchestrator proof alignment note must mention "
                            f"'{token}'",
                        )
                    )

    return issues


__all__ = ("validate_questbook_obligation_index",)
