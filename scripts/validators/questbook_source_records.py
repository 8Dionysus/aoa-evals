"""Questbook authored source record checks."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from validators import questbook_io as questbook_io_validator
from validators import questbook_orchestrator_constants as questbook_orchestrator_constants_validator
from validators import questbook_orchestrator_refs as questbook_orchestrator_refs_validator
from validators import questbook_projection_records as questbook_projection_records_validator
from validators import questbook_progression as questbook_progression_validator
from validators import questbook_source_constants as questbook_source_constants_validator
from validators.common import ValidationIssue


@dataclass
class QuestSourceRecordValidation:
    issues: list[ValidationIssue] = field(default_factory=list)
    valid_quest_ids: list[str] = field(default_factory=list)
    active_quest_ids: list[str] = field(default_factory=list)
    closed_quest_ids: list[str] = field(default_factory=list)
    expected_catalog_entries: list[dict[str, Any]] = field(default_factory=list)
    expected_dispatch_entries: list[dict[str, Any]] = field(default_factory=list)
    needs_orchestrator_alignment_doc: bool = False
    unlock_proof_bridge_quest_present: bool = False


def validate_quest_source_records(repo_root: Path) -> QuestSourceRecordValidation:
    result = QuestSourceRecordValidation()
    quest_paths = questbook_projection_records_validator.discover_quest_paths(repo_root)
    if quest_paths:
        quest_names = [path.stem for path in quest_paths]
    else:
        quest_names = list(questbook_source_constants_validator.FOUNDATION_QUEST_NAMES)
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in quest_names
        ]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    for quest_name in duplicate_names:
        result.issues.append(
            ValidationIssue(
                "quests",
                f"duplicate quest source id '{quest_name}'",
            )
        )
    for quest_name in questbook_projection_records_validator.missing_foundation_quest_names(
        quest_names
    ):
        result.issues.append(
            ValidationIssue(
                "quests",
                f"missing required foundation quest file '{quest_name}.yaml'",
            )
        )

    live_orchestrator_class_ids: set[str] | None = None
    for quest_name, quest_path in zip(quest_names, quest_paths, strict=True):
        quest_data = questbook_io_validator.load_yaml_file(quest_path, result.issues)
        if not isinstance(quest_data, dict):
            continue
        location = questbook_io_validator.relative_location(quest_path, repo_root)
        if not questbook_io_validator.validate_against_schema(
            quest_data,
            questbook_source_constants_validator.QUEST_SCHEMA_NAME,
            location,
            result.issues,
        ):
            continue
        shape_issue = questbook_projection_records_validator.quest_source_path_shape_issue(
            repo_root,
            quest_path,
            quest_data,
        )
        if shape_issue is not None:
            result.issues.append(ValidationIssue(location, shape_issue))
        if quest_data.get("schema_version") != questbook_source_constants_validator.QUEST_SCHEMA_VERSION:
            result.issues.append(
                ValidationIssue(
                    location,
                    f"schema_version must be '{questbook_source_constants_validator.QUEST_SCHEMA_VERSION}'",
                )
            )
        if quest_data.get("repo") != "aoa-evals":
            result.issues.append(
                ValidationIssue(location, "quest repo must be 'aoa-evals'")
            )
        if quest_data.get("id") != quest_name:
            result.issues.append(
                ValidationIssue(location, f"quest id must match filename '{quest_name}'")
            )
        if quest_data.get("public_safe") is not True:
            result.issues.append(
                ValidationIssue(location, "quest must set public_safe to true")
            )
        orchestrator_class_ref = quest_data.get("orchestrator_class_ref")
        capability_target = quest_data.get("capability_target")
        if orchestrator_class_ref is None and capability_target is not None:
            result.issues.append(
                ValidationIssue(
                    location,
                    "quest must not declare capability_target without orchestrator_class_ref",
                )
            )
        if orchestrator_class_ref is not None:
            result.needs_orchestrator_alignment_doc = True
            if live_orchestrator_class_ids is None:
                live_orchestrator_class_ids = (
                    questbook_orchestrator_refs_validator.load_live_orchestrator_class_ids(
                        result.issues
                    )
                )
            questbook_orchestrator_refs_validator.validate_orchestrator_class_ref(
                orchestrator_class_ref,
                location=location,
                issues=result.issues,
                live_class_ids=live_orchestrator_class_ids,
            )
            if (
                capability_target
                not in questbook_orchestrator_constants_validator.ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS
            ):
                result.issues.append(
                    ValidationIssue(
                        location,
                        "quest capability_target must resolve to a supported orchestrator capability",
                    )
                )
        expected_orchestrator_pair = questbook_orchestrator_constants_validator.ORCHESTRATOR_PROOF_QUESTS.get(
            quest_name
        )
        if expected_orchestrator_pair is not None:
            expected_ref, expected_target = expected_orchestrator_pair
            if quest_data.get("kind") != "proof":
                result.issues.append(
                    ValidationIssue(
                        location,
                        "orchestrator proof quests must keep kind 'proof'",
                    )
                )
            if (
                quest_data.get("owner_surface")
                != questbook_orchestrator_constants_validator.ORCHESTRATOR_PROOF_ALIGNMENT_NAME
            ):
                result.issues.append(
                    ValidationIssue(
                        location,
                        "orchestrator proof quests must keep owner_surface "
                        f"{questbook_orchestrator_constants_validator.ORCHESTRATOR_PROOF_ALIGNMENT_NAME}",
                    )
                )
            if orchestrator_class_ref != expected_ref:
                result.issues.append(
                    ValidationIssue(
                        location,
                        "orchestrator proof quest must keep orchestrator_class_ref "
                        f"'{expected_ref}'",
                    )
                )
            if capability_target != expected_target:
                result.issues.append(
                    ValidationIssue(
                        location,
                        "orchestrator proof quest must keep capability_target "
                        f"'{expected_target}'",
                    )
                )
        if quest_name == "AOA-EV-Q-0005":
            if quest_data.get("kind") != "proof":
                result.issues.append(
                    ValidationIssue(
                        location,
                        "progression evidence quest must keep kind 'proof'",
                    )
                )
            if (
                quest_data.get("owner_surface")
                != questbook_progression_validator.PROGRESSION_EVIDENCE_MODEL_NAME
            ):
                result.issues.append(
                    ValidationIssue(
                        location,
                        "progression evidence quest must keep owner_surface "
                        f"{questbook_progression_validator.PROGRESSION_EVIDENCE_MODEL_NAME}",
                    )
                )
        if quest_name == "AOA-EV-Q-0009":
            if quest_data.get("kind") != "proof":
                result.issues.append(
                    ValidationIssue(
                        location,
                        "unlock proof bridge quest must keep kind 'proof'",
                    )
                )
            if (
                quest_data.get("owner_surface")
                != questbook_progression_validator.UNLOCK_PROOF_BRIDGE_NAME
            ):
                result.issues.append(
                    ValidationIssue(
                        location,
                        "unlock proof bridge quest must keep owner_surface "
                        f"{questbook_progression_validator.UNLOCK_PROOF_BRIDGE_NAME}",
                    )
                )
        if quest_data.get("state") in questbook_source_constants_validator.CLOSED_QUEST_STATES:
            result.closed_quest_ids.append(quest_name)
        else:
            result.active_quest_ids.append(quest_name)

        if quest_data.get("id") != quest_name:
            continue
        source_path = quest_path.relative_to(repo_root).as_posix()
        result.valid_quest_ids.append(quest_name)
        result.expected_catalog_entries.append(
            questbook_projection_records_validator.build_expected_quest_catalog_entry(
                quest_data,
                source_path=source_path,
            )
        )
        result.expected_dispatch_entries.append(
            questbook_projection_records_validator.build_expected_quest_dispatch_entry(
                quest_data,
                quest_name=quest_name,
                source_path=source_path,
            )
        )

    result.unlock_proof_bridge_quest_present = "AOA-EV-Q-0009" in result.valid_quest_ids
    return result


__all__ = (
    "QuestSourceRecordValidation",
    "validate_quest_source_records",
)
