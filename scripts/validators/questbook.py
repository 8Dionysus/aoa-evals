"""Questbook source/projection boundary contracts."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import yaml
from jsonschema import Draft202012Validator, SchemaError

REPO_ROOT = Path(__file__).resolve().parents[2]
STRICT_SIBLING_COMPAT_ENV = "AOA_EVALS_STRICT_SIBLING_COMPAT"


def repo_root_from_env(env_name: str, default: Path) -> Path:
    override = os.environ.get(env_name)
    if not override:
        return default
    return Path(override).expanduser().resolve()


AOA_AGENTS_ROOT = repo_root_from_env("AOA_AGENTS_ROOT", REPO_ROOT.parent / "aoa-agents")

QUESTBOOK_NAME = "QUESTBOOK.md"
QUESTS_README_NAME = "quests/README.md"
QUESTS_AGENTS_NAME = "quests/AGENTS.md"
QUEST_LIFECYCLE_NAME = "quests/LIFECYCLE.md"
QUESTBOOK_INTEGRATION_NAME = "docs/operations/QUESTBOOK_EVAL_INTEGRATION.md"
QUEST_SCHEMA_NAME = "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json"
QUEST_DISPATCH_SCHEMA_NAME = "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json"
QUEST_CATALOG_NAME = "generated/quest_catalog.min.json"
QUEST_DISPATCH_NAME = "generated/quest_dispatch.min.json"
QUEST_CATALOG_EXAMPLE_NAME = "generated/quest_catalog.min.example.json"
QUEST_DISPATCH_EXAMPLE_NAME = "generated/quest_dispatch.min.example.json"
QUEST_SOURCE_LANES = (
    "proof",
    "trace",
    "orchestrator",
    "unlock",
    "runtime",
    "closeout",
    "agon",
    "harvest",
    "questbook",
)
QUEST_SOURCE_STATES = (
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
)
FOUNDATION_QUEST_NAMES = (
    "AOA-EV-Q-0001",
    "AOA-EV-Q-0002",
    "AOA-EV-Q-0003",
    "AOA-EV-Q-0004",
)
CLOSED_QUEST_STATES = {"done", "dropped"}
QUESTBOOK_INTEGRATION_REQUIRED_TOKENS = (
    "proof",
    "regression",
    "verdict-bridge",
    "example-only",
    "repo-local review projection",
)
QUESTBOOK_NOTE_REQUIRED_TOKENS = (
    "# Questbook Obligation Index",
    "public human obligation index",
    "proof",
    "regression",
    "verdict-bridge",
    "Closed source records stay in `quests/` and generated projections as",
    "Promotion happens through reviewed owner acceptance",
    "Quest-harvest route:",
    "route output into quest source records, owner handoff, or reviewed",
    "Eval bundle meaning stays in source bundles",
)
QUESTS_README_REQUIRED_TOKENS = (
    "# Quest Source Records",
    "source quest record district",
    "human questbook index",
    "mechanics/questbook/",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "source eval packages under `evals/`",
)
QUESTS_AGENTS_REQUIRED_TOKENS = (
    "source quest record district",
    "mechanics/questbook/",
    "generated quest files as dispatch readers",
    "source quest records",
    "schema-backed YAML",
    "QUESTBOOK.md",
    "quests/LIFECYCLE.md",
    "generated/quest_catalog.min.json",
    "quests/<lane>/<state>/",
    "legacy path vocabulary",
    "validate_repo.py",
)
QUEST_LIFECYCLE_REQUIRED_TOKENS = (
    "# Quest Lifecycle Contract",
    "State Matrix",
    "Open-index posture",
    "Return posture",
    "Promotion posture",
    "Proof-Loop Return Use",
    "mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md",
    "below eval result receipt",
    "Open states",
    "Closed states",
    "`QUESTBOOK.md` must list open quest IDs and leave closed quest IDs out",
)
QUEST_SCHEMA_TITLE = "work_quest_v1"
QUEST_SCHEMA_VERSION = "work_quest_v1"
QUEST_DISPATCH_SCHEMA_TITLE = "quest_dispatch_v1"
QUEST_DISPATCH_SCHEMA_VERSION = "quest_dispatch_v1"
QUEST_DISPATCH_ARTIFACT_OVERRIDES = {
    "AOA-EV-Q-0001": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0002": [
        "bounded_plan",
        "evaluation_result",
        "verification_result",
    ],
    "AOA-EV-Q-0003": [
        "bounded_plan",
        "work_result",
        "verification_result",
    ],
    "AOA-EV-Q-0004": [
        "recurrence_evidence",
        "promotion_decision",
    ],
}
QUESTBOOK_MECHANIC_README_NAME = "mechanics/questbook/README.md"
QUESTBOOK_MECHANIC_AGENTS_NAME = "mechanics/questbook/AGENTS.md"
QUESTBOOK_MECHANIC_PARTS_NAME = "mechanics/questbook/PARTS.md"
QUESTBOOK_MECHANIC_PROVENANCE_NAME = "mechanics/questbook/PROVENANCE.md"
QUESTBOOK_SOURCE_RECORD_PART_README_NAME = (
    "mechanics/questbook/parts/source-record-contract/README.md"
)
QUESTBOOK_DISPATCH_READER_PART_README_NAME = (
    "mechanics/questbook/parts/dispatch-reader/README.md"
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0070-questbook-part-owner-split-contract.md"
)
QUESTBOOK_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "quests/",
    "quests/LIFECYCLE.md",
    "source-record-contract",
    "dispatch-reader",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "lane/state",
    "Quests route eval-bundle",
    "python scripts/build_catalog.py --check",
    "python scripts/validate_repo.py",
)
QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source quest record",
    "QUESTBOOK.md",
    "mechanics/questbook/PARTS.md",
    "mechanics/questbook/PROVENANCE.md",
    "quests/LIFECYCLE.md",
    "generated quest reader",
    "lane/state",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "source-record-contract",
    "dispatch-reader",
    "generated quest reader",
    "source quest record",
    "old top-level quest source path revived as alias",
    "AGENTS.md#validation",
)
QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS = (
    "Quest Source Record Contract",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/source-record-contract/schemas/quest.schema.json",
    "quests/<lane>/<state>/AOA-EV-Q-*.yaml",
    "quests/LIFECYCLE.md",
    "QUESTBOOK.md",
    "generated projection input",
    "source quest record identity",
    "aoa-quest-harvest",
    "roadmap direction",
    "owner acceptance",
    "python scripts/build_catalog.py --check",
)
QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS = (
    "Quest Dispatch Reader",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/questbook/parts/dispatch-reader/schemas/quest_dispatch.schema.json",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.json",
    "scripts/build_catalog.py",
    "generated projection contract",
    "source quest truth",
    "live task assignment",
    "proof-surface promotion",
    "python scripts/build_catalog.py --check",
)
QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS = (
    "quests/LIFECYCLE.md",
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
    "proof-loop",
    "route-smoke",
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0098-agon-quest-note-provenance-route.md"
)
AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS = (
    "mechanics/agon/PROVENANCE.md",
    "Agon legacy archive",
    "archive-local accounting",
    "schema-backed source quest records",
    "markdown quest notes",
    "quests/",
    "python -m pytest -q tests/test_quest_and_reader_surfaces.py -k quest_route",
)
QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/questbook/",
    "source quest records",
    "generated quest",
    "lane/state",
    "no empty taxonomy",
)
QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Questbook Part Owner-split Contract",
    "mechanics/questbook/parts/source-record-contract/README.md",
    "mechanics/questbook/parts/dispatch-reader/README.md",
    "`## Stronger Owner Split`",
    "Source quest records stay under `quests/<lane>/<state>/`",
    "Human visibility stays",
    "Generated quest readers stay under root `generated/`",
    "aoa-quest-harvest",
    "live task assignment",
    "python -m pytest -q tests/test_mechanic_surface_contracts.py -k questbook_part_owner_split",
)
ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS = {
    "repo_layer_selection",
    "evidence_closure",
    "bounded_next_step",
}
ORCHESTRATOR_PROOF_QUESTS = {
    "AOA-EV-Q-0006": ("aoa-agents:router", "repo_layer_selection"),
    "AOA-EV-Q-0007": ("aoa-agents:review", "evidence_closure"),
    "AOA-EV-Q-0008": ("aoa-agents:bounded_execution", "bounded_next_step"),
}
ORCHESTRATOR_CLASS_CATALOG_NAME = "generated/orchestrator_class_catalog.min.json"
ORCHESTRATOR_PROOF_ALIGNMENT_NAME = (
    "mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/"
    "ORCHESTRATOR_PROOF_ALIGNMENT.md"
)
ORCHESTRATOR_PROOF_REQUIRED_TOKENS = (
    "## Router",
    "## Review",
    "## Bounded execution",
    "## Boundary rule",
    "Proof surfaces judge work.",
)
PROGRESSION_EVIDENCE_MODEL_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md"
)
PROGRESSION_EVIDENCE_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json"
)
PROGRESSION_EVIDENCE_EXAMPLE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/examples/progression_evidence.example.json"
)
UNLOCK_PROOF_BRIDGE_NAME = (
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md"
)
UNLOCK_PROOF_SCHEMA_NAME = (
    "mechanics/rpg/parts/progression-unlocks/schemas/unlock_proof_catalog.schema.json"
)
UNLOCK_PROOF_EXAMPLE_NAME = "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json"
PROGRESSION_EVIDENCE_REQUIRED_TOKENS = (
    "## Core route",
    "Progression evidence is quest-scoped or route-scoped proof.",
    "| one universal score or broad capability growth | keep multi-axis deltas here; route broad comparison through comparison/growth owner review |",
    "| quest acceptance or state-transition pressure | quest owner route plus cited evidence |",
    "cautions are first-class proof",
)
UNLOCK_PROOF_REQUIRED_TOKENS = (
    "## Core route",
    "`gated_grant`",
    "It interprets reviewed evidence",
    "| runtime equip or activation pressure | `abyss-stack` runtime route plus owner gates |",
    "| one proof object as a universal agent ranking | multi-axis progression evidence plus owner review |",
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


@dataclass(frozen=True)
class QuestbookRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    schema_path = REPO_ROOT / schema_name
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=None)
def get_schema_validator(schema_name: str) -> Draft202012Validator:
    return Draft202012Validator(load_schema(schema_name))


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


def relative_location(path: Path, root: Path | None = None) -> str:
    target_root = root or REPO_ROOT
    try:
        return path.relative_to(target_root).as_posix()
    except ValueError:
        return path.as_posix()


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def load_yaml_file(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid YAML: {exc}"))
        return None
    return data


def load_json_payload(path: Path, issues: list[ValidationIssue]) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path), f"invalid JSON: {exc}"))
        return None


def validate_inline_schema(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    if not isinstance(schema, dict):
        issues.append(ValidationIssue(location, "schema must parse to an object"))
        return False
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        issues.append(ValidationIssue(location, f"invalid JSON schema: {exc.message}"))
        return False
    return True


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
) -> bool:
    active_validator = validator or get_schema_validator(schema_name)
    schema_errors = sorted(
        active_validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
    if not text:
        return text
    for token in tokens:
        if token not in text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def _require(
    context: QuestbookRouteContext,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    return context.require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=tokens,
        issues=issues,
    )


def validate_quest_route_surfaces(
    repo_root: Path,
    *,
    context: QuestbookRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, QUESTS_README_NAME, QUESTS_README_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTS_AGENTS_NAME, QUESTS_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUEST_LIFECYCLE_NAME, QUEST_LIFECYCLE_REQUIRED_TOKENS, issues)
    for path_name, stale_token in (
        (QUESTS_README_NAME, "It is not `QUESTBOOK.md`"),
        (QUESTS_README_NAME, "Quests are not eval bundles."),
        (QUEST_LIFECYCLE_NAME, "It is not `QUESTBOOK.md`"),
        (QUEST_LIFECYCLE_NAME, "does not create an eval result receipt"),
    ):
        text = read_text_or_issue(repo_root / path_name, issues, root=repo_root)
        if stale_token in text:
            issues.append(
                ValidationIssue(
                    path_name,
                    "quest route surfaces should use positive role routing instead of stale negative scaffold "
                    f"'{stale_token}'",
                )
            )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0004-questbook-topology.md",
        ("QUESTBOOK.md", "generated quest", "lane/state", "eval bundles"),
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0018-quest-lane-state-source-layout.md",
        (
            "quests/<lane>/<state>/",
            "generated quest readers",
            "legacy path vocabulary",
            "stale top-level quest source files",
        ),
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0021-quest-lifecycle-contract.md",
        QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME,
        AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    for stale_path in sorted((repo_root / "quests").glob("AOA-EV-Q-*.yaml")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level quest source files must stay moved to quests/<lane>/<state>/",
            )
        )
    for stale_path in sorted((repo_root / "quests").glob("AOE-Q-AGON-*.md")):
        issues.append(
            ValidationIssue(
                relative_location(stale_path, repo_root),
                "top-level Agon quest notes must stay behind mechanics/agon/PROVENANCE.md",
            )
        )
    for markdown_path in sorted((repo_root / "quests").rglob("*.md")):
        relative_parts = markdown_path.relative_to(repo_root).parts
        if relative_parts in {
            ("quests", "README.md"),
            ("quests", "AGENTS.md"),
            ("quests", "LIFECYCLE.md"),
        }:
            continue
        issues.append(
            ValidationIssue(
                relative_location(markdown_path, repo_root),
                "markdown quest notes must not live under active quest lifecycle paths; "
                "route lineage through the owning mechanic PROVENANCE.md",
            )
        )
    return issues


def validate_questbook_route_surfaces(
    repo_root: Path,
    *,
    context: QuestbookRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, QUESTBOOK_MECHANIC_README_NAME, QUESTBOOK_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_AGENTS_NAME, QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_PARTS_NAME, QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_SOURCE_RECORD_PART_README_NAME, QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_DISPATCH_READER_PART_README_NAME, QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, QUESTBOOK_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0006-questbook-mechanic-package.md",
        QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/AOA-EV-D-0021-quest-lifecycle-contract.md",
        QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
        QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME,
            "Questbook Part Owner-split Contract",
        ),
        issues,
    )
    return issues


def strict_sibling_compat_checks_enabled() -> bool:
    return os.environ.get(STRICT_SIBLING_COMPAT_ENV, "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

def load_live_orchestrator_class_ids(issues: list[ValidationIssue]) -> set[str] | None:
    catalog_path = AOA_AGENTS_ROOT / ORCHESTRATOR_CLASS_CATALOG_NAME
    if not strict_sibling_compat_checks_enabled() or not AOA_AGENTS_ROOT.exists():
        return None
    payload = load_json_payload(catalog_path, issues)
    if not isinstance(payload, dict):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, AOA_AGENTS_ROOT),
                "orchestrator class catalog must be an object",
            )
        )
        return set()
    entries = payload.get("orchestrator_classes")
    if not isinstance(entries, list):
        issues.append(
            ValidationIssue(
                relative_location(catalog_path, AOA_AGENTS_ROOT),
                "orchestrator class catalog must expose an orchestrator_classes list",
            )
        )
        return set()
    class_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, AOA_AGENTS_ROOT)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must be an object",
                )
            )
            continue
        class_id = entry.get("id")
        if not isinstance(class_id, str) or not class_id:
            issues.append(
                ValidationIssue(
                    f"{relative_location(catalog_path, AOA_AGENTS_ROOT)}.orchestrator_classes[{index}]",
                    "orchestrator class entry must expose a string id",
                )
            )
            continue
        class_ids.add(class_id)
    return class_ids


def validate_orchestrator_class_ref(
    orchestrator_class_ref: object,
    *,
    location: str,
    issues: list[ValidationIssue],
    live_class_ids: set[str] | None,
) -> str | None:
    if not isinstance(orchestrator_class_ref, str):
        issues.append(ValidationIssue(location, "quest orchestrator_class_ref must be a string"))
        return None
    repo_name, separator, class_id = orchestrator_class_ref.partition(":")
    if separator != ":" or repo_name != "aoa-agents" or not class_id:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must use the form 'aoa-agents:<class_id>'",
            )
        )
        return None
    if live_class_ids is not None and class_id not in live_class_ids:
        issues.append(
            ValidationIssue(
                location,
                "quest orchestrator_class_ref must resolve in aoa-agents/generated/orchestrator_class_catalog.min.json",
            )
        )
        return None
    return class_id


def validate_quest_projection_record(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> None:
    schema_path = repo_root / QUEST_SCHEMA_NAME
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise ValueError(
            f"{schema_path.relative_to(repo_root).as_posix()} could not be loaded for quest projection: {exc}"
        ) from exc
    errors = sorted(
        Draft202012Validator(schema).iter_errors(quest_data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if errors:
        error = errors[0]
        error_path = format_schema_path(error.absolute_path)
        detail = f" at '{error_path}'" if error_path else ""
        raise ValueError(
            f"{quest_path.relative_to(repo_root).as_posix()} violates {QUEST_SCHEMA_NAME}{detail}: {error.message}"
        )

def quest_sort_key(quest_name: str) -> tuple[int, str]:
    suffix = quest_name.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_name)
    except ValueError:
        return (sys.maxsize, quest_name)


def discover_quest_paths(repo_root: Path) -> list[Path]:
    quests_dir = repo_root / "quests"
    if not quests_dir.is_dir():
        return []
    return sorted(
        {
            path
            for path in quests_dir.rglob("AOA-EV-Q-*.yaml")
            if path.is_file()
        },
        key=lambda path: quest_sort_key(path.stem),
    )


def discover_quest_names(repo_root: Path) -> list[str]:
    quest_names = sorted(
        {path.stem for path in discover_quest_paths(repo_root)},
        key=quest_sort_key,
    )
    if not quest_names:
        return list(FOUNDATION_QUEST_NAMES)
    return quest_names


def missing_foundation_quest_names(quest_names: Iterable[str]) -> list[str]:
    quest_name_set = set(quest_names)
    return [quest_name for quest_name in FOUNDATION_QUEST_NAMES if quest_name not in quest_name_set]


def should_validate_questbook_surface(repo_root: Path) -> bool:
    questbook_paths = (
        repo_root / QUESTBOOK_NAME,
        repo_root / QUESTBOOK_INTEGRATION_NAME,
        repo_root / QUEST_SCHEMA_NAME,
        repo_root / QUEST_DISPATCH_SCHEMA_NAME,
        repo_root / QUEST_CATALOG_EXAMPLE_NAME,
        repo_root / QUEST_DISPATCH_EXAMPLE_NAME,
    )
    if any(path.exists() for path in questbook_paths):
        return True
    return bool(discover_quest_paths(repo_root))


def quest_source_path_shape_issue(
    repo_root: Path,
    quest_path: Path,
    quest_data: dict[str, Any],
) -> str | None:
    relative_path = quest_path.relative_to(repo_root).as_posix()
    parts = quest_path.relative_to(repo_root).parts
    if len(parts) != 4 or parts[0] != "quests" or not parts[3].endswith(".yaml"):
        return "quest source path must use quests/<lane>/<state>/<quest-id>.yaml"
    lane = parts[1]
    state = parts[2]
    if lane not in QUEST_SOURCE_LANES:
        allowed = ", ".join(QUEST_SOURCE_LANES)
        return f"quest lane '{lane}' is not allowed; expected one of: {allowed}"
    if state not in QUEST_SOURCE_STATES:
        allowed = ", ".join(QUEST_SOURCE_STATES)
        return f"quest state directory '{state}' is not allowed; expected one of: {allowed}"
    quest_state = quest_data.get("state")
    if isinstance(quest_state, str) and state != quest_state:
        return f"quest state directory '{state}' must match state '{quest_state}'"
    if quest_path.stem != quest_data.get("id"):
        return f"quest source filename in {relative_path} must match quest id"
    return None


def validate_quest_schema_envelope(
    schema: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    expected_title: str,
    expected_schema_version: str,
) -> bool:
    if not validate_inline_schema(schema, location=location, issues=issues):
        return False
    if not isinstance(schema, dict):
        return False

    ok = True
    if schema.get("title") != expected_title:
        issues.append(
            ValidationIssue(location, f"schema title must be '{expected_title}'")
        )
        ok = False
    if schema.get("type") != "object":
        issues.append(ValidationIssue(location, "schema must describe an object"))
        ok = False
    if schema.get("additionalProperties") is not False:
        issues.append(
            ValidationIssue(location, "schema must forbid additional properties")
        )
        ok = False
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        issues.append(ValidationIssue(location, "schema properties must be an object"))
        return False
    schema_version = properties.get("schema_version")
    if not isinstance(schema_version, dict) or schema_version.get("const") != expected_schema_version:
        issues.append(
            ValidationIssue(
                location,
                f"schema_version must be a const of '{expected_schema_version}'",
            )
        )
        ok = False
    required = schema.get("required")
    if not isinstance(required, list):
        issues.append(ValidationIssue(location, "schema required list is missing"))
        ok = False
    else:
        for field in ("schema_version", "id", "public_safe"):
            if field not in required:
                issues.append(
                    ValidationIssue(location, f"schema must require '{field}'")
                )
                ok = False
    return ok


def validate_quest_lifecycle_surface(
    repo_root: Path,
    quest_schema: dict[str, Any] | None = None,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    lifecycle_text = require_tokens(
        repo_root=repo_root,
        path_name=QUEST_LIFECYCLE_NAME,
        tokens=QUEST_LIFECYCLE_REQUIRED_TOKENS,
        issues=issues,
    )
    if not lifecycle_text:
        return issues

    schema_states: list[str] = []
    if isinstance(quest_schema, dict):
        properties = quest_schema.get("properties")
        if isinstance(properties, dict):
            state_schema = properties.get("state")
            if isinstance(state_schema, dict):
                raw_enum = state_schema.get("enum")
                if isinstance(raw_enum, list):
                    schema_states = [item for item in raw_enum if isinstance(item, str)]
    if not schema_states:
        schema_states = list(QUEST_SOURCE_STATES)

    if tuple(schema_states) != QUEST_SOURCE_STATES:
        issues.append(
            ValidationIssue(
                QUEST_SCHEMA_NAME,
                "quest state enum must match the lifecycle state order",
            )
        )

    for state in schema_states:
        table_token = f"| `{state}` |"
        if table_token not in lifecycle_text:
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"quest lifecycle matrix must include state '{state}'",
                )
            )

    for state in sorted(CLOSED_QUEST_STATES):
        if f"`{state}` | closed; not listed as open" not in lifecycle_text:
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"closed state '{state}' must be marked closed in the lifecycle matrix",
                )
            )
    for state in QUEST_SOURCE_STATES:
        if (
            state not in CLOSED_QUEST_STATES
            and f"| `{state}` | listed in `QUESTBOOK.md`" not in lifecycle_text
        ):
            issues.append(
                ValidationIssue(
                    QUEST_LIFECYCLE_NAME,
                    f"open state '{state}' must be marked listed in QUESTBOOK.md",
                )
            )
    return issues


def build_expected_quest_catalog_entry(
    quest: dict[str, Any],
    *,
    source_path: str,
) -> dict[str, Any]:
    entry = {
        "id": quest["id"],
        "title": quest["title"],
        "repo": quest["repo"],
        "theme_ref": quest.get("theme_ref", ""),
        "milestone_ref": quest.get("milestone_ref", ""),
        "state": quest["state"],
        "band": quest["band"],
        "kind": quest["kind"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "owner_surface": quest["owner_surface"],
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    for optional_key in (
        "orchestrator_class_ref",
        "capability_target",
        "playbook_family_refs",
        "proof_surface_refs",
        "memory_surface_refs",
    ):
        if optional_key in quest:
            entry[optional_key] = quest[optional_key]
    return entry


def build_expected_quest_dispatch_entry(
    quest: dict[str, Any],
    *,
    quest_name: str,
    source_path: str,
) -> dict[str, Any]:
    activation = quest.get("activation")
    if not isinstance(activation, dict):
        activation = {}
    requires_artifacts = QUEST_DISPATCH_ARTIFACT_OVERRIDES.get(quest_name)
    if requires_artifacts is None:
        kind = quest.get("kind")
        if kind == "harvest":
            requires_artifacts = ["recurrence_evidence", "promotion_decision"]
        else:
            requires_artifacts = ["bounded_plan", "work_result", "verification_result"]
    entry = {
        "schema_version": QUEST_DISPATCH_SCHEMA_VERSION,
        "id": quest["id"],
        "repo": quest["repo"],
        "state": quest["state"],
        "band": quest["band"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "control_mode": quest["control_mode"],
        "delegate_tier": quest["delegate_tier"],
        "split_required": quest["split_required"],
        "write_scope": quest["write_scope"],
        "requires_artifacts": requires_artifacts,
        "activation_mode": activation.get("mode"),
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    if "fallback_tier" in quest:
        entry["fallback_tier"] = quest.get("fallback_tier")
    if "wrapper_class" in quest:
        entry["wrapper_class"] = quest.get("wrapper_class")
    for optional_key in ("orchestrator_class_ref", "capability_target"):
        if optional_key in quest:
            entry[optional_key] = quest.get(optional_key)
    return entry


def load_quest_projection_records(repo_root: Path) -> list[tuple[str, dict[str, Any], str]]:
    records: list[tuple[str, dict[str, Any], str]] = []
    quest_paths = discover_quest_paths(repo_root)
    if not quest_paths:
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in FOUNDATION_QUEST_NAMES
        ]
    quest_names = [path.stem for path in quest_paths]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    if duplicate_names:
        raise ValueError(f"duplicate quest source id(s): {', '.join(duplicate_names)}")
    missing_foundation = missing_foundation_quest_names(quest_names)
    if missing_foundation:
        missing_display = ", ".join(missing_foundation)
        raise ValueError(f"missing required foundation quest files: {missing_display}")
    for quest_path in quest_paths:
        quest_name = quest_path.stem
        try:
            quest_data = yaml.safe_load(quest_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is missing") from exc
        except yaml.YAMLError as exc:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} is invalid YAML: {exc}") from exc
        if not isinstance(quest_data, dict):
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must be a YAML mapping")
        validate_quest_projection_record(repo_root, quest_path, quest_data)
        shape_issue = quest_source_path_shape_issue(repo_root, quest_path, quest_data)
        if shape_issue is not None:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()}: {shape_issue}")
        if quest_data.get("schema_version") != QUEST_SCHEMA_VERSION:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep schema_version '{QUEST_SCHEMA_VERSION}'")
        if quest_data.get("repo") != "aoa-evals":
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep repo 'aoa-evals'")
        if quest_data.get("id") != quest_name:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep id '{quest_name}'")
        if quest_data.get("public_safe") is not True:
            raise ValueError(f"{quest_path.relative_to(repo_root).as_posix()} must keep public_safe true")
        records.append((quest_name, quest_data, quest_path.relative_to(repo_root).as_posix()))
    return records


def build_quest_catalog_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_catalog_entry(quest_data, source_path=source_path)
        for _, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


def build_quest_dispatch_projection(repo_root: Path) -> list[dict[str, Any]]:
    return [
        build_expected_quest_dispatch_entry(
            quest_data,
            quest_name=quest_name,
            source_path=source_path,
        )
        for quest_name, quest_data, source_path in load_quest_projection_records(repo_root)
    ]


def validate_questbook_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    questbook_path = repo_root / QUESTBOOK_NAME
    integration_path = repo_root / QUESTBOOK_INTEGRATION_NAME
    orchestrator_alignment_path = repo_root / ORCHESTRATOR_PROOF_ALIGNMENT_NAME
    quest_schema_path = repo_root / QUEST_SCHEMA_NAME
    quest_dispatch_schema_path = repo_root / QUEST_DISPATCH_SCHEMA_NAME
    quest_catalog_path = repo_root / QUEST_CATALOG_NAME
    quest_dispatch_path = repo_root / QUEST_DISPATCH_NAME
    quest_catalog_example_path = repo_root / QUEST_CATALOG_EXAMPLE_NAME
    quest_dispatch_example_path = repo_root / QUEST_DISPATCH_EXAMPLE_NAME
    quest_paths = discover_quest_paths(repo_root)
    if quest_paths:
        quest_names = [path.stem for path in quest_paths]
    else:
        quest_names = list(FOUNDATION_QUEST_NAMES)
        quest_paths = [
            repo_root / "quests" / f"{quest_name}.yaml"
            for quest_name in quest_names
        ]
    duplicate_names = sorted(
        name for name, count in Counter(quest_names).items() if count > 1
    )
    for quest_name in duplicate_names:
        issues.append(
            ValidationIssue(
                "quests",
                f"duplicate quest source id '{quest_name}'",
            )
        )
    for quest_name in missing_foundation_quest_names(quest_names):
        issues.append(
            ValidationIssue(
                "quests",
                f"missing required foundation quest file '{quest_name}.yaml'",
            )
        )

    questbook_text = read_text_or_issue(questbook_path, issues, root=repo_root)
    integration_text = read_text_or_issue(integration_path, issues, root=repo_root)

    quest_schema = load_json_payload(quest_schema_path, issues)
    if quest_schema is not None:
        validate_quest_schema_envelope(
            quest_schema,
            location=relative_location(quest_schema_path, repo_root),
            issues=issues,
            expected_title=QUEST_SCHEMA_TITLE,
            expected_schema_version=QUEST_SCHEMA_VERSION,
        )
    issues.extend(validate_quest_lifecycle_surface(repo_root, quest_schema))
    quest_dispatch_schema = load_json_payload(quest_dispatch_schema_path, issues)
    if quest_dispatch_schema is not None:
        validate_quest_schema_envelope(
            quest_dispatch_schema,
            location=relative_location(quest_dispatch_schema_path, repo_root),
            issues=issues,
            expected_title=QUEST_DISPATCH_SCHEMA_TITLE,
            expected_schema_version=QUEST_DISPATCH_SCHEMA_VERSION,
        )

    if questbook_text:
        for token in QUESTBOOK_NOTE_REQUIRED_TOKENS:
            if token not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must mention '{token}'",
                    )
                )

    if integration_text:
        for token in QUESTBOOK_INTEGRATION_REQUIRED_TOKENS:
            if token not in integration_text:
                issues.append(
                    ValidationIssue(
                        relative_location(integration_path, repo_root),
                        f"integration note must mention '{token}'",
                    )
                )

    expected_catalog_entries: list[dict[str, Any]] = []
    expected_dispatch_entries: list[dict[str, Any]] = []
    valid_quest_ids: list[str] = []
    active_quest_ids: list[str] = []
    closed_quest_ids: list[str] = []
    live_orchestrator_class_ids: set[str] | None = None
    needs_orchestrator_alignment_doc = False
    for quest_name, quest_path in zip(quest_names, quest_paths, strict=True):
        quest_data = load_yaml_file(quest_path, issues)
        if not isinstance(quest_data, dict):
            continue
        location = relative_location(quest_path, repo_root)
        if not validate_against_schema(quest_data, QUEST_SCHEMA_NAME, location, issues):
            continue
        shape_issue = quest_source_path_shape_issue(repo_root, quest_path, quest_data)
        if shape_issue is not None:
            issues.append(ValidationIssue(location, shape_issue))
        if quest_data.get("schema_version") != QUEST_SCHEMA_VERSION:
            issues.append(
                ValidationIssue(location, f"schema_version must be '{QUEST_SCHEMA_VERSION}'")
            )
        if quest_data.get("repo") != "aoa-evals":
            issues.append(ValidationIssue(location, "quest repo must be 'aoa-evals'"))
        if quest_data.get("id") != quest_name:
            issues.append(
                ValidationIssue(location, f"quest id must match filename '{quest_name}'")
            )
        if quest_data.get("public_safe") is not True:
            issues.append(ValidationIssue(location, "quest must set public_safe to true"))
        orchestrator_class_ref = quest_data.get("orchestrator_class_ref")
        capability_target = quest_data.get("capability_target")
        if orchestrator_class_ref is None and capability_target is not None:
            issues.append(
                ValidationIssue(
                    location,
                    "quest must not declare capability_target without orchestrator_class_ref",
                )
            )
        if orchestrator_class_ref is not None:
            needs_orchestrator_alignment_doc = True
            if live_orchestrator_class_ids is None:
                live_orchestrator_class_ids = load_live_orchestrator_class_ids(issues)
            validate_orchestrator_class_ref(
                orchestrator_class_ref,
                location=location,
                issues=issues,
                live_class_ids=live_orchestrator_class_ids,
            )
            if capability_target not in ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS:
                issues.append(
                    ValidationIssue(
                        location,
                        "quest capability_target must resolve to a supported orchestrator capability",
                    )
                )
        expected_orchestrator_pair = ORCHESTRATOR_PROOF_QUESTS.get(quest_name)
        if expected_orchestrator_pair is not None:
            expected_ref, expected_target = expected_orchestrator_pair
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "orchestrator proof quests must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != ORCHESTRATOR_PROOF_ALIGNMENT_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quests must keep owner_surface {ORCHESTRATOR_PROOF_ALIGNMENT_NAME}",
                    )
                )
            if orchestrator_class_ref != expected_ref:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quest must keep orchestrator_class_ref '{expected_ref}'",
                    )
                )
            if capability_target != expected_target:
                issues.append(
                    ValidationIssue(
                        location,
                        f"orchestrator proof quest must keep capability_target '{expected_target}'",
                    )
                )
        if quest_name == "AOA-EV-Q-0005":
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "progression evidence quest must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != PROGRESSION_EVIDENCE_MODEL_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"progression evidence quest must keep owner_surface {PROGRESSION_EVIDENCE_MODEL_NAME}",
                    )
                )
        if quest_name == "AOA-EV-Q-0009":
            if quest_data.get("kind") != "proof":
                issues.append(
                    ValidationIssue(location, "unlock proof bridge quest must keep kind 'proof'")
                )
            if quest_data.get("owner_surface") != UNLOCK_PROOF_BRIDGE_NAME:
                issues.append(
                    ValidationIssue(
                        location,
                        f"unlock proof bridge quest must keep owner_surface {UNLOCK_PROOF_BRIDGE_NAME}",
                    )
                )
        if quest_data.get("state") in CLOSED_QUEST_STATES:
            closed_quest_ids.append(quest_name)
        else:
            active_quest_ids.append(quest_name)

        if quest_data.get("id") != quest_name:
            continue
        source_path = quest_path.relative_to(repo_root).as_posix()
        valid_quest_ids.append(quest_name)
        expected_catalog_entries.append(
            build_expected_quest_catalog_entry(quest_data, source_path=source_path)
        )
        expected_dispatch_entries.append(
            build_expected_quest_dispatch_entry(
                quest_data,
                quest_name=quest_name,
                source_path=source_path,
            )
        )

    if orchestrator_alignment_path.exists():
        needs_orchestrator_alignment_doc = True
    if needs_orchestrator_alignment_doc:
        orchestrator_doc_text = read_text_or_issue(
            orchestrator_alignment_path,
            issues,
            root=repo_root,
        )
        if orchestrator_doc_text:
            for token in ORCHESTRATOR_PROOF_REQUIRED_TOKENS:
                if token not in orchestrator_doc_text:
                    issues.append(
                        ValidationIssue(
                            relative_location(orchestrator_alignment_path, repo_root),
                            f"orchestrator proof alignment note must mention '{token}'",
                        )
                    )

    if "AOA-EV-Q-0009" in valid_quest_ids:
        issues.extend(validate_unlock_proof_bridge_surface(repo_root))

    if questbook_text:
        for quest_name in active_quest_ids:
            if quest_name not in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must reference active quest id '{quest_name}'",
                    )
                )
        for quest_name in closed_quest_ids:
            if quest_name in questbook_text:
                issues.append(
                    ValidationIssue(
                        relative_location(questbook_path, repo_root),
                        f"QUESTBOOK.md must not list closed quest id '{quest_name}'",
                    )
                )

    expected_catalog_by_id = {
        entry["id"]: entry for entry in expected_catalog_entries
    }
    actual_live_catalog = load_json_payload(quest_catalog_path, issues)
    actual_live_catalog_by_id: dict[str, dict[str, Any]] = {}
    if isinstance(actual_live_catalog, list):
        unexpected_ids: list[str] = []
        for item in actual_live_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_live_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    f"generated quest catalog has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_live_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_path, repo_root),
                    "generated quest catalog is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_path, repo_root),
                "generated quest catalog must be an array",
            )
        )
    actual_catalog = load_json_payload(quest_catalog_example_path, issues)
    if isinstance(actual_catalog, list):
        actual_catalog_by_id: dict[str, dict[str, Any]] = {}
        unexpected_ids: list[str] = []
        for item in actual_catalog:
            if isinstance(item, dict):
                item_id = item.get("id")
                if isinstance(item_id, str) and item_id in expected_catalog_by_id:
                    actual_catalog_by_id[item_id] = item
                elif isinstance(item_id, str):
                    unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    f"generated quest catalog example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        if any(
            actual_catalog_by_id.get(quest_id) != expected_catalog_by_id[quest_id]
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example is out of date or mismatched",
                )
            )
        elif any(
            actual_catalog_by_id.get(quest_id) != actual_live_catalog_by_id.get(quest_id)
            for quest_id in valid_quest_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_catalog_example_path, repo_root),
                    "generated quest catalog example must match generated quest catalog",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_catalog_example_path, repo_root),
                "generated quest catalog example must be an array",
            )
        )
    expected_dispatch_by_id = {
        entry["id"]: entry for entry in expected_dispatch_entries
    }
    actual_live_dispatch = load_json_payload(quest_dispatch_path, issues)
    actual_live_dispatch_by_id: dict[str, dict[str, Any]] = {}
    invalid_live_dispatch_ids: set[str] = set()
    if isinstance(actual_live_dispatch, list):
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_live_dispatch):
            location = f"{relative_location(quest_dispatch_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_live_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_live_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    f"generated quest dispatch has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_live_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_live_dispatch_ids
        ]
        if any(
            actual_live_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_live_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_path, repo_root),
                    "generated quest dispatch is out of date or mismatched",
                )
            )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_path, repo_root),
                "generated quest dispatch must be an array",
            )
        )
    actual_dispatch = load_json_payload(quest_dispatch_example_path, issues)
    if isinstance(actual_dispatch, list):
        actual_dispatch_by_id: dict[str, dict[str, Any]] = {}
        invalid_example_dispatch_ids: set[str] = set()
        unexpected_ids: list[str] = []
        for index, item in enumerate(actual_dispatch):
            location = f"{relative_location(quest_dispatch_example_path, repo_root)}[{index}]"
            if not isinstance(item, dict):
                continue
            item_valid = validate_against_schema(
                item,
                QUEST_DISPATCH_SCHEMA_NAME,
                location,
                issues,
            )
            item_id = item.get("id")
            if not item_valid and isinstance(item_id, str):
                invalid_example_dispatch_ids.add(item_id)
            if item_valid and isinstance(item_id, str) and item_id in expected_dispatch_by_id:
                actual_dispatch_by_id[item_id] = item
            elif item_valid and isinstance(item_id, str):
                unexpected_ids.append(item_id)
        if unexpected_ids:
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    f"generated quest dispatch example has unexpected quest id(s): {', '.join(sorted(unexpected_ids))}",
                )
            )
        comparable_example_dispatch_ids = [
            quest_id
            for quest_id in valid_quest_ids
            if quest_id not in invalid_example_dispatch_ids
        ]
        if any(
            actual_dispatch_by_id.get(quest_id) != expected_dispatch_by_id[quest_id]
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example is out of date or mismatched",
                )
            )
        elif any(
            actual_dispatch_by_id.get(quest_id) != actual_live_dispatch_by_id.get(quest_id)
            for quest_id in comparable_example_dispatch_ids
        ):
            issues.append(
                ValidationIssue(
                    relative_location(quest_dispatch_example_path, repo_root),
                    "generated quest dispatch example must match generated quest dispatch",
                )
            )
        else:
            for quest_id in comparable_example_dispatch_ids:
                item = actual_dispatch_by_id.get(quest_id)
                if item is None:
                    continue
                requires_artifacts = item.get("requires_artifacts")
                if not isinstance(requires_artifacts, list) or not requires_artifacts:
                    issues.append(
                        ValidationIssue(
                            relative_location(quest_dispatch_example_path, repo_root),
                            "dispatch example must keep requires_artifacts as a non-empty example-only list",
                        )
                    )
    else:
        issues.append(
            ValidationIssue(
                relative_location(quest_dispatch_example_path, repo_root),
                "generated quest dispatch example must be an array",
            )
        )

    return issues


def validate_unlock_proof_bridge_surface(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    progression_doc_path = repo_root / PROGRESSION_EVIDENCE_MODEL_NAME
    progression_schema_path = repo_root / PROGRESSION_EVIDENCE_SCHEMA_NAME
    progression_example_path = repo_root / PROGRESSION_EVIDENCE_EXAMPLE_NAME
    doc_path = repo_root / UNLOCK_PROOF_BRIDGE_NAME
    schema_path = repo_root / UNLOCK_PROOF_SCHEMA_NAME
    example_path = repo_root / UNLOCK_PROOF_EXAMPLE_NAME

    progression_doc_text = read_text_or_issue(
        progression_doc_path,
        issues,
        root=repo_root,
    )
    if progression_doc_text:
        for token in PROGRESSION_EVIDENCE_REQUIRED_TOKENS:
            if token not in progression_doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(progression_doc_path, repo_root),
                        f"progression evidence note must mention '{token}'",
                    )
                )

    progression_schema_payload = load_json_payload(progression_schema_path, issues)
    if isinstance(progression_schema_payload, dict):
        if progression_schema_payload.get("title") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    "progression evidence schema title must be 'progression_evidence_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(progression_schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(progression_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif progression_schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_schema_path, repo_root),
                "progression evidence schema must be a JSON object",
            )
        )

    progression_example_payload = load_json_payload(progression_example_path, issues)
    if isinstance(progression_example_payload, dict):
        validate_against_schema(
            progression_example_payload,
            PROGRESSION_EVIDENCE_SCHEMA_NAME,
            relative_location(progression_example_path, repo_root),
            issues,
        )
        if progression_example_payload.get("schema_version") != "progression_evidence_v1":
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example schema_version must be 'progression_evidence_v1'",
                )
            )
        if progression_example_payload.get("public_safe") is not True:
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep public_safe true",
                )
            )
        if not progression_example_payload.get("cautions"):
            issues.append(
                ValidationIssue(
                    relative_location(progression_example_path, repo_root),
                    "progression evidence example must keep cautions explicit",
                )
            )
    elif progression_example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(progression_example_path, repo_root),
                "progression evidence example must be a JSON object",
            )
        )

    doc_text = read_text_or_issue(doc_path, issues, root=repo_root)
    if doc_text:
        for token in UNLOCK_PROOF_REQUIRED_TOKENS:
            if token not in doc_text:
                issues.append(
                    ValidationIssue(
                        relative_location(doc_path, repo_root),
                        f"unlock proof bridge note must mention '{token}'",
                    )
                )

    schema_payload = load_json_payload(schema_path, issues)
    if isinstance(schema_payload, dict):
        if schema_payload.get("title") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    "unlock proof schema title must be 'unlock_proof_catalog_v1'",
                )
            )
        try:
            Draft202012Validator.check_schema(schema_payload)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
    elif schema_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(schema_path, repo_root),
                "unlock proof schema must be a JSON object",
            )
        )

    example_text = read_text_or_issue(example_path, issues, root=repo_root)
    example_payload = load_json_payload(example_path, issues)
    if isinstance(example_payload, dict):
        validate_against_schema(
            example_payload,
            UNLOCK_PROOF_SCHEMA_NAME,
            relative_location(example_path, repo_root),
            issues,
        )
        if example_payload.get("schema_version") != "unlock_proof_catalog_v1":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example schema_version must be 'unlock_proof_catalog_v1'",
                )
            )
        proofs = example_payload.get("proofs")
        if not isinstance(proofs, list) or not proofs:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must expose a non-empty proofs list",
                )
            )
        else:
            for index, proof in enumerate(proofs):
                if not isinstance(proof, dict):
                    continue
                if proof.get("public_safe") is not True:
                    issues.append(
                        ValidationIssue(
                            f"{relative_location(example_path, repo_root)}.proofs[{index}]",
                            "unlock proof example entries must keep public_safe true",
                        )
                    )
        if example_payload.get("notes") and "Example only." not in str(example_payload.get("notes")):
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example notes must keep example-only posture explicit",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "unlock proof example must be a JSON object",
            )
        )

    if example_text:
        if "AOA-PB-Q-0004" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not keep legacy playbook quest id 'AOA-PB-Q-0004'",
                )
            )
        if "AOA-EV-PROG-0002" in example_text:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "unlock proof example must not reference missing progression evidence id 'AOA-EV-PROG-0002'",
                )
            )

    return issues


__all__ = (
    "QUESTBOOK_NAME",
    "QUESTS_README_NAME",
    "QUESTS_AGENTS_NAME",
    "QUEST_LIFECYCLE_NAME",
    "QUESTBOOK_INTEGRATION_NAME",
    "QUEST_SCHEMA_NAME",
    "QUEST_DISPATCH_SCHEMA_NAME",
    "QUEST_CATALOG_NAME",
    "QUEST_DISPATCH_NAME",
    "QUEST_CATALOG_EXAMPLE_NAME",
    "QUEST_DISPATCH_EXAMPLE_NAME",
    "QUEST_SOURCE_LANES",
    "QUEST_SOURCE_STATES",
    "FOUNDATION_QUEST_NAMES",
    "CLOSED_QUEST_STATES",
    "QUESTBOOK_INTEGRATION_REQUIRED_TOKENS",
    "QUESTBOOK_NOTE_REQUIRED_TOKENS",
    "QUESTS_README_REQUIRED_TOKENS",
    "QUESTS_AGENTS_REQUIRED_TOKENS",
    "QUEST_LIFECYCLE_REQUIRED_TOKENS",
    "QUESTBOOK_MECHANIC_README_NAME",
    "QUESTBOOK_MECHANIC_AGENTS_NAME",
    "QUESTBOOK_MECHANIC_PARTS_NAME",
    "QUESTBOOK_MECHANIC_PROVENANCE_NAME",
    "QUESTBOOK_SOURCE_RECORD_PART_README_NAME",
    "QUESTBOOK_DISPATCH_READER_PART_README_NAME",
    "QUESTBOOK_PART_OWNER_SPLIT_DECISION_NAME",
    "QUESTBOOK_MECHANIC_REQUIRED_TOKENS",
    "QUESTBOOK_MECHANIC_AGENTS_REQUIRED_TOKENS",
    "QUESTBOOK_MECHANIC_PARTS_REQUIRED_TOKENS",
    "QUESTBOOK_SOURCE_RECORD_PART_REQUIRED_TOKENS",
    "QUESTBOOK_DISPATCH_READER_PART_REQUIRED_TOKENS",
    "QUEST_LIFECYCLE_DECISION_REQUIRED_TOKENS",
    "AGON_QUEST_NOTE_PROVENANCE_DECISION_NAME",
    "AGON_QUEST_NOTE_PROVENANCE_DECISION_REQUIRED_TOKENS",
    "QUESTBOOK_MECHANIC_DECISION_REQUIRED_TOKENS",
    "QUESTBOOK_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS",
    "QUEST_SCHEMA_TITLE",
    "QUEST_SCHEMA_VERSION",
    "QUEST_DISPATCH_SCHEMA_TITLE",
    "QUEST_DISPATCH_SCHEMA_VERSION",
    "QUEST_DISPATCH_ARTIFACT_OVERRIDES",
    "ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS",
    "ORCHESTRATOR_PROOF_QUESTS",
    "ORCHESTRATOR_CLASS_CATALOG_NAME",
    "ORCHESTRATOR_PROOF_ALIGNMENT_NAME",
    "ORCHESTRATOR_PROOF_REQUIRED_TOKENS",
    "PROGRESSION_EVIDENCE_MODEL_NAME",
    "PROGRESSION_EVIDENCE_SCHEMA_NAME",
    "PROGRESSION_EVIDENCE_EXAMPLE_NAME",
    "UNLOCK_PROOF_BRIDGE_NAME",
    "UNLOCK_PROOF_SCHEMA_NAME",
    "UNLOCK_PROOF_EXAMPLE_NAME",
    "PROGRESSION_EVIDENCE_REQUIRED_TOKENS",
    "UNLOCK_PROOF_REQUIRED_TOKENS",
    "QuestbookRouteContext",
    "validate_quest_route_surfaces",
    "validate_questbook_route_surfaces",
    "load_live_orchestrator_class_ids",
    "validate_orchestrator_class_ref",
    "validate_quest_projection_record",
    "quest_sort_key",
    "discover_quest_paths",
    "discover_quest_names",
    "missing_foundation_quest_names",
    "should_validate_questbook_surface",
    "quest_source_path_shape_issue",
    "validate_quest_schema_envelope",
    "validate_quest_lifecycle_surface",
    "build_expected_quest_catalog_entry",
    "build_expected_quest_dispatch_entry",
    "load_quest_projection_records",
    "build_quest_catalog_projection",
    "build_quest_dispatch_projection",
    "validate_questbook_surface",
    "validate_unlock_proof_bridge_surface",
)
