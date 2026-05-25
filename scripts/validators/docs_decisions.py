"""Decision index metadata and generated read-model contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml


DECISIONS_DIR = Path("docs/decisions")
INDEXES_DIR = DECISIONS_DIR / "indexes"
INDEX_CONTRACT_PATH = INDEXES_DIR / "index_contract.yaml"
GENERATED_INDEX_PATHS = (
    INDEXES_DIR / "README.md",
    INDEXES_DIR / "by-number.md",
    INDEXES_DIR / "by-surface.md",
    INDEXES_DIR / "by-mechanic.md",
    INDEXES_DIR / "by-validation-guard.md",
)
DECISION_NOTE_GLOB = "[0-9][0-9][0-9][0-9]-*.md"


SURFACE_CLASS_ORDER = (
    "root/topology",
    "proof topology",
    "mechanic package",
    "mechanic part",
    "validation guard",
    "legacy/provenance",
    "generated/readout",
    "report/release/receipt",
    "quest/lane",
    "boundary/runtime/sibling",
)
MECHANIC_PARENT_ORDER = (
    "proof-object",
    "proof-loop",
    "comparison-spine",
    "proof-infra",
    "publication-receipts",
    "release-support",
    "titan",
    "agon",
    "recurrence",
    "checkpoint",
    "experience",
    "antifragility",
    "method-growth",
    "rpg",
    "growth-cycle",
    "distillation",
    "questbook",
    "audit",
    "boundary-bridge",
    "cross-parent",
)
GUARD_FAMILY_ORDER = (
    "route residue",
    "parent and package",
    "part and payload",
    "legacy and provenance",
    "generated/report/receipt/runtime",
    "sibling and boundary",
    "decision index/read-model",
)


@dataclass(frozen=True)
class DecisionRecord:
    number: str
    title: str
    path: Path
    surface_classes: tuple[str, ...]
    mechanic_parents: tuple[str, ...]
    guard_families: tuple[str, ...]
    posture: str

    @property
    def repo_path(self) -> str:
        return self.path.as_posix()

    @property
    def index_link(self) -> str:
        return f"../{self.path.name}"


def split_metadata_value(value: str) -> tuple[str, ...]:
    value = value.strip()
    if not value or value == "none":
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def parse_title(text: str, *, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"{path.as_posix()} is missing a level-one title")


def parse_index_metadata(text: str, *, path: Path) -> dict[str, str]:
    marker = "\n## Index Metadata\n"
    if marker not in text:
        raise ValueError(f"{path.as_posix()} is missing ## Index Metadata")
    section = text.split(marker, 1)[1]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    metadata: dict[str, str] = {}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    required = {
        "surface classes",
        "mechanic parents",
        "guard families",
        "posture",
    }
    missing = sorted(required - set(metadata))
    if missing:
        raise ValueError(
            f"{path.as_posix()} index metadata is missing: {', '.join(missing)}"
        )
    return metadata


def load_decision_record(path: Path, *, repo_root: Path) -> DecisionRecord:
    text = path.read_text(encoding="utf-8")
    title = parse_title(text, path=path.relative_to(repo_root))
    metadata = parse_index_metadata(text, path=path.relative_to(repo_root))
    relative_path = path.relative_to(repo_root)
    return DecisionRecord(
        number=path.name[:4],
        title=title,
        path=relative_path,
        surface_classes=split_metadata_value(metadata["surface classes"]),
        mechanic_parents=split_metadata_value(metadata["mechanic parents"]),
        guard_families=split_metadata_value(metadata["guard families"]),
        posture=metadata["posture"].strip(),
    )


def collect_decision_records(repo_root: Path) -> tuple[list[DecisionRecord], list[tuple[str, str]]]:
    records: list[DecisionRecord] = []
    issues: list[tuple[str, str]] = []
    decisions_root = repo_root / DECISIONS_DIR
    if not decisions_root.is_dir():
        return records, [(DECISIONS_DIR.as_posix(), "decision directory is missing")]
    for path in sorted(decisions_root.glob(DECISION_NOTE_GLOB)):
        try:
            records.append(load_decision_record(path, repo_root=repo_root))
        except ValueError as exc:
            issues.append((path.relative_to(repo_root).as_posix(), str(exc)))
    numbers = [record.number for record in records]
    if len(numbers) != len(set(numbers)):
        issues.append((DECISIONS_DIR.as_posix(), "decision numbers must be unique"))
    if numbers != sorted(numbers):
        issues.append((DECISIONS_DIR.as_posix(), "decision records must sort by number"))
    return records, issues


def ordered_values(values: Iterable[str], preferred_order: Sequence[str]) -> list[str]:
    seen = set(values)
    ordered = [value for value in preferred_order if value in seen]
    ordered.extend(sorted(seen - set(ordered)))
    return ordered


def display_title(record: DecisionRecord) -> str:
    number_prefix = f"{record.number} "
    if record.title.startswith(number_prefix):
        return record.title
    return f"{record.number} {record.title}"


def bullet_line(record: DecisionRecord) -> str:
    return (
        f"- [{display_title(record)}]({record.index_link}) "
        f"(`{record.repo_path}`)"
    )


def render_generated_notice() -> str:
    return (
        "<!-- Generated by scripts/generate_decision_indexes.py; "
        "do not edit by hand. -->\n\n"
    )


def render_indexes_readme() -> str:
    return (
        "# Decision Lookup Indexes\n\n"
        + render_generated_notice()
        + "These files are generated read models from decision-note `Index Metadata`.\n"
        + "Decision notes own rationale; these indexes only make lookup cheaper for agents.\n\n"
        + "## Indexes\n\n"
        + "- [By number](by-number.md)\n"
        + "- [By surface class](by-surface.md)\n"
        + "- [By mechanic parent](by-mechanic.md)\n"
        + "- [By validation guard family](by-validation-guard.md)\n"
    )


def render_by_number(records: Sequence[DecisionRecord]) -> str:
    lines = [
        "# Decisions By Number",
        "",
        render_generated_notice().rstrip(),
        "",
        "| No. | Decision | Path | Surface classes | Mechanic parents | Guard families | Posture |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| {number} | [{title}]({link}) | `{path}` | {surfaces} | {parents} | {guards} | {posture} |".format(
                number=record.number,
                title=display_title(record),
                link=record.index_link,
                path=record.repo_path,
                surfaces=", ".join(record.surface_classes) or "none",
                parents=", ".join(record.mechanic_parents) or "none",
                guards=", ".join(record.guard_families) or "none",
                posture=record.posture,
            )
        )
    return "\n".join(lines) + "\n"


def render_grouped_index(
    *,
    title: str,
    records: Sequence[DecisionRecord],
    attribute: str,
    preferred_order: Sequence[str],
) -> str:
    values: list[str] = []
    for record in records:
        values.extend(getattr(record, attribute))
    lines = ["# " + title, "", render_generated_notice().rstrip(), ""]
    for value in ordered_values(values, preferred_order):
        lines.extend([f"## {value}", ""])
        for record in records:
            if value in getattr(record, attribute):
                lines.append(bullet_line(record))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_index_files(records: Sequence[DecisionRecord]) -> dict[Path, str]:
    return {
        INDEXES_DIR / "README.md": render_indexes_readme(),
        INDEXES_DIR / "by-number.md": render_by_number(records),
        INDEXES_DIR / "by-surface.md": render_grouped_index(
            title="Decisions By Surface Class",
            records=records,
            attribute="surface_classes",
            preferred_order=SURFACE_CLASS_ORDER,
        ),
        INDEXES_DIR / "by-mechanic.md": render_grouped_index(
            title="Decisions By Mechanic Parent",
            records=records,
            attribute="mechanic_parents",
            preferred_order=MECHANIC_PARENT_ORDER,
        ),
        INDEXES_DIR / "by-validation-guard.md": render_grouped_index(
            title="Decisions By Validation Guard Family",
            records=records,
            attribute="guard_families",
            preferred_order=GUARD_FAMILY_ORDER,
        ),
    }


def load_index_contract(repo_root: Path) -> tuple[dict[str, object] | None, list[tuple[str, str]]]:
    path = repo_root / INDEX_CONTRACT_PATH
    if not path.is_file():
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract is missing")]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract must be a mapping")]
    return payload, []


def validate_decision_index_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    records, issues = collect_decision_records(repo_root)
    contract, contract_issues = load_index_contract(repo_root)
    issues.extend(contract_issues)
    if contract is not None:
        expected = [path.as_posix() for path in GENERATED_INDEX_PATHS]
        if contract.get("generated_indexes") != expected:
            issues.append(
                (
                    INDEX_CONTRACT_PATH.as_posix(),
                    "generated_indexes must match the decision index read-model set",
                )
            )
    if issues:
        return issues

    rendered = render_index_files(records)
    for relative_path, expected_text in rendered.items():
        path = repo_root / relative_path
        if not path.is_file():
            issues.append((relative_path.as_posix(), "generated decision index is missing"))
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            issues.append(
                (
                    relative_path.as_posix(),
                    "generated decision index is stale; run python scripts/generate_decision_indexes.py",
                )
            )
    return issues
