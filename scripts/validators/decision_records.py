"""Decision note metadata parsing and record collection."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from validators.decision_index_paths import (
    DECISION_ROOT_FILENAMES,
    DECISIONS_DIR,
    FULL_ID_FILENAME_RE,
)


DECISION_ID_RE = re.compile(r"^- Decision ID: (AOA-EV-D-(\d{4}))$", re.MULTILINE)
DATE_VALUE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    number: int
    title: str
    path: Path
    date: str
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


def parse_decision_id(text: str, *, path: Path) -> tuple[str, int]:
    match = DECISION_ID_RE.search(text)
    if not match:
        raise ValueError(f"{path.as_posix()} is missing '- Decision ID: AOA-EV-D-####'")
    return match.group(1), int(match.group(2))


def parse_original_date(metadata: dict[str, str], *, path: Path) -> str:
    value = metadata["original date"].strip()
    if not DATE_VALUE_RE.match(value):
        raise ValueError(f"{path.as_posix()} original date must use YYYY-MM-DD")
    return value


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
        "original date",
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
    relative_path = path.relative_to(repo_root)
    decision_id, number = parse_decision_id(text, path=relative_path)
    title = parse_title(text, path=relative_path)
    metadata = parse_index_metadata(text, path=relative_path)
    date = parse_original_date(metadata, path=relative_path)
    return DecisionRecord(
        decision_id=decision_id,
        number=number,
        title=title,
        path=relative_path,
        date=date,
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
    for path in sorted(
        item
        for item in decisions_root.glob("*.md")
        if item.name not in DECISION_ROOT_FILENAMES
    ):
        try:
            record = load_decision_record(path, repo_root=repo_root)
        except ValueError as exc:
            issues.append((path.relative_to(repo_root).as_posix(), str(exc)))
            continue
        filename_match = FULL_ID_FILENAME_RE.match(record.path.name)
        if not filename_match:
            issues.append(
                (
                    record.repo_path,
                    "decision path must use the full canonical ID filename format",
                )
            )
        elif filename_match.group(1) != record.decision_id:
            issues.append(
                (
                    record.repo_path,
                    "decision path canonical ID must match the note Decision ID",
                )
            )
        elif int(filename_match.group(2)) != record.number:
            issues.append(
                (
                    record.repo_path,
                    "decision path number must match the note Decision ID number",
                )
            )
        records.append(record)

    numbers = [record.number for record in records]
    if len(numbers) != len(set(numbers)):
        issues.append((DECISIONS_DIR.as_posix(), "decision numbers must be unique"))
    if numbers != sorted(numbers):
        issues.append((DECISIONS_DIR.as_posix(), "decision records must sort by number"))
    ids = [record.decision_id for record in records]
    if len(ids) != len(set(ids)):
        issues.append((DECISIONS_DIR.as_posix(), "decision IDs must be unique"))
    return records, issues


__all__ = (
    "DecisionRecord",
    "collect_decision_records",
    "load_decision_record",
    "parse_decision_id",
    "parse_index_metadata",
    "parse_original_date",
    "parse_title",
    "split_metadata_value",
)
